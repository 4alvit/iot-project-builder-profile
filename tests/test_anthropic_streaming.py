"""Exercise the installed Anthropic SDK with offline HTTP/SSE responses."""

import json
from unittest import TestCase
from unittest.mock import patch

import anthropic
import httpx2

from iot_profile_builder.generator.profile_generator import ProfileGenerator
from iot_profile_builder.models import EngineeringProfile, ScanConfig


def event(kind: str, **fields: object) -> bytes:
    """Encode an actual server-sent event, leaving decoding to the SDK."""
    return f"event: {kind}\ndata: {json.dumps({'type': kind, **fields})}\n\n".encode()


def message_start() -> bytes:
    """Start an ordinary Messages streaming response."""
    return event(
        "message_start",
        message={
            "id": "msg_offline",
            "type": "message",
            "role": "assistant",
            "model": "offline-model",
            "content": [],
            "stop_reason": None,
            "stop_sequence": None,
            "usage": {"input_tokens": 1, "output_tokens": 0},
        },
    )


def block(index: int, content: dict[str, object], delta: dict[str, object]) -> bytes:
    """Send a block whose payload arrives through the delta event."""
    return (
        event("content_block_start", index=index, content_block=content)
        + event("content_block_delta", index=index, delta=delta)
        + event("content_block_stop", index=index)
    )


def message_stop(reason: str = "end_turn") -> bytes:
    """Finish a response using the SDK's normal message finalization path."""
    return event(
        "message_delta",
        delta={"stop_reason": reason, "stop_sequence": None},
        usage={"output_tokens": 1},
    ) + event("message_stop")


class AnthropicStreamingTests(TestCase):
    """The client, streaming parser and final Message are real SDK objects."""

    def generate(self, response: bytes) -> EngineeringProfile:
        """Replace only HTTP transport; no endpoint or credential is contacted."""
        requests = []

        def handler(request: httpx2.Request) -> httpx2.Response:
            requests.append(request)
            self.assertEqual(request.url.host, "sdk.invalid")
            self.assertEqual(request.url.path, "/v1/messages")
            payload = json.loads(request.content)
            self.assertTrue(payload["stream"])
            self.assertEqual(payload["model"], "offline-model")
            self.assertEqual(payload["messages"][0]["role"], "user")
            return httpx2.Response(
                200, headers={"content-type": "text/event-stream"}, content=response
            )

        client = anthropic.Anthropic(
            api_key="offline-fixture",
            base_url="https://sdk.invalid",
            max_retries=0,
            http_client=httpx2.Client(transport=httpx2.MockTransport(handler), trust_env=False),
        )
        self.addCleanup(client.close)
        with patch("anthropic.Anthropic", return_value=client):
            generator = ProfileGenerator(ScanConfig(username="offline", llm_model="offline-model"))
        profile = generator.generate([], [], [], {})
        self.assertEqual(len(requests), 1)
        return profile

    def test_mixed_blocks_accumulate_only_text_into_profile(self) -> None:
        """Thinking and tool JSON cannot overwrite the actual text answer."""
        response = message_start()
        response += block(
            0,
            {"type": "thinking", "thinking": "", "signature": ""},
            {"type": "thinking_delta", "thinking": '{"skills": [], "narrative_summary": "wrong"}'},
        )
        response += block(
            1,
            {"type": "tool_use", "id": "tool_offline", "name": "unused", "input": {}},
            {"type": "input_json_delta", "partial_json": '{"narrative_summary": "wrong"}'},
        )
        for index, text in enumerate(
            ['{"skills": [], "narrative_', 'summary": "SDK transport verified"}'], start=2
        ):
            response += block(
                index, {"type": "text", "text": ""}, {"type": "text_delta", "text": text}
            )
        profile = self.generate(response + message_stop())
        self.assertEqual(profile.narrative_summary, "SDK transport verified")
        self.assertEqual(profile.skills, [])

    def test_stream_error_degrades_to_existing_fallback(self) -> None:
        """A server error event is decoded by the SDK and handled by the app."""
        response = message_start() + event(
            "error", error={"type": "overloaded_error", "message": "offline overload"}
        )
        self.assertIn("unavailable", self.generate(response).narrative_summary)

    def test_tool_only_response_does_not_become_profile_json(self) -> None:
        """The application does not execute tools or treat tool input as a profile."""
        response = message_start() + block(
            0,
            {"type": "tool_use", "id": "tool_offline", "name": "unused", "input": {}},
            {
                "type": "input_json_delta",
                "partial_json": '{"skills": [], "narrative_summary": "wrong"}',
            },
        )
        self.assertIn(
            "unavailable", self.generate(response + message_stop("tool_use")).narrative_summary
        )
