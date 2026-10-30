"""Exercise the installed Anthropic SDK with offline HTTP/SSE responses."""

import json
from collections.abc import Callable
from unittest import TestCase
from unittest.mock import patch

import anthropic
import httpx2

from iot_profile_builder.generator.profile_generator import GenerationError, ProfileGenerator
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

    def generate(self, response: bytes, *, strict: bool = False) -> EngineeringProfile:
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
        with patch("anthropic.Anthropic", return_value=client) as constructor:
            generator = ProfileGenerator(
                ScanConfig(username="offline", llm_model="offline-model", strict_scan=strict)
            )
            constructor.assert_called_once_with(timeout=120.0, max_retries=0)
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

    @staticmethod
    def complete_analysis() -> dict[str, object]:
        """A complete model response with one source-backed skill."""
        return {
            "skills": [
                {
                    "name": "MQTT",
                    "category": "protocols",
                    "proficiency": 6,
                    "evidence": ["mqtt-battery"],
                    "confidence": 0.8,
                }
            ],
            "focus_areas": {"networking_protocols": 0.8},
            "narrative_summary": "Maintains MQTT integrations.",
            "key_strengths": ["Protocol integration"],
            "growth_areas": [],
        }

    def analysis_stream(self, content: str, *, reason: str = "end_turn") -> bytes:
        """Encode the model's JSON as a real Messages text stream."""
        return (
            message_start()
            + block(0, {"type": "text", "text": ""}, {"type": "text_delta", "text": content})
            + message_stop(reason)
        )

    def test_strict_stream_retains_valid_assessments(self) -> None:
        """A completed structured response still produces a publishable profile."""
        profile = self.generate(
            self.analysis_stream(json.dumps(self.complete_analysis())), strict=True
        )
        self.assertEqual(profile.skills[0].name, "MQTT")
        self.assertEqual(profile.skills[0].evidence, ["mqtt-battery"])
        self.assertEqual(profile.narrative_summary, "Maintains MQTT integrations.")
        self.assertEqual(
            profile.github_stats["generation"],
            {
                "mode": "llm",
                "requested_model": "offline-model",
                "provider_reported_model": "offline-model",
            },
        )

    def test_strict_stream_rejects_errors_without_disclosing_provider_body(self) -> None:
        """Publication fails rather than reporting model success from a fallback."""
        response = message_start() + event(
            "error", error={"type": "overloaded_error", "message": "private-provider-detail"}
        )
        with self.assertRaises(GenerationError) as raised:
            self.generate(response, strict=True)
        self.assertNotIn("private-provider-detail", str(raised.exception))
        self.assertIsNone(raised.exception.__cause__)

    def test_strict_stream_rejects_truncated_or_invalid_assessments(self) -> None:
        """Incomplete JSON or invalid scores must not be repaired or silently dropped."""
        valid = self.complete_analysis()
        cases = [
            (json.dumps(valid), "max_tokens"),
            (json.dumps(valid)[:-1] + ",}", "end_turn"),
            (json.dumps({"skills": []}), "end_turn"),
            (json.dumps({**valid, "skills": []}), "end_turn"),
            (json.dumps({**valid, "focus_areas": {}}), "end_turn"),
            (json.dumps({**valid, "key_strengths": []}), "end_turn"),
            (json.dumps({**valid, "skills": ["invalid"]}), "end_turn"),
            (json.dumps({**valid, "focus_areas": {"unknown-area": 0.5}}), "end_turn"),
            (
                json.dumps({**valid, "focus_areas": {"networking_protocols": float("nan")}}),
                "end_turn",
            ),
            (json.dumps({**valid, "key_strengths": "not a list"}), "end_turn"),
            (json.dumps({**valid, "narrative_summary": ""}), "end_turn"),
        ]
        for text, reason in cases:
            with self.subTest(content=text, reason=reason), self.assertRaises(GenerationError):
                self.generate(self.analysis_stream(text, reason=reason), strict=True)

    def test_model_environment_default_and_explicit_override(self) -> None:
        """Deployments can change their configured model without modifying source."""
        with patch.dict("os.environ", {"PROFILE_LLM_MODEL": "configured/model"}):
            self.assertEqual(ScanConfig(username="offline").llm_model, "configured/model")
            self.assertEqual(
                ScanConfig(username="offline", llm_model="explicit/model").llm_model,
                "explicit/model",
            )

    def test_initialization_error_does_not_expose_configuration(self) -> None:
        with (
            patch("anthropic.Anthropic", side_effect=RuntimeError("private-config-detail")),
            self.assertRaises(GenerationError) as raised,
        ):
            ProfileGenerator(ScanConfig(username="offline", strict_scan=True))
        self.assertNotIn("private-config-detail", str(raised.exception))

    def access_generator(
        self, handler: Callable[[httpx2.Request], httpx2.Response], **env: str
    ) -> ProfileGenerator:
        """Use the real SDK without allowing its credential discovery onto the wire."""
        settings = {
            "ANTHROPIC_BASE_URL": "https://sdk.invalid",
            "PROFILE_ACCESS_CLIENT_ID": "offline-client-id",
            "PROFILE_ACCESS_CLIENT_SECRET": "offline-client-secret",
            "PROFILE_LLM_API_KEY": "",
            "ANTHROPIC_API_KEY": "ambient-key-must-not-leave",
            "ANTHROPIC_AUTH_TOKEN": "ambient-token-must-not-leave",
            "ANTHROPIC_PROFILE": "profile-must-not-be-read",
            "ANTHROPIC_CUSTOM_HEADERS": (
                "Authorization: ambient-header\nX-Other-Secret: ambient-secret"
            ),
            **env,
        }
        client = httpx2.Client(
            transport=httpx2.MockTransport(handler), follow_redirects=False, trust_env=False
        )
        self.addCleanup(client.close)
        with (
            patch.dict("os.environ", settings),
            patch("anthropic.DefaultHttpxClient", return_value=client) as constructor,
        ):
            generator = ProfileGenerator(
                ScanConfig(username="offline", llm_model="offline-model", strict_scan=True)
            )
        constructor.assert_called_once_with(follow_redirects=False)
        self.addCleanup(generator.client.close)
        return generator

    def test_access_auth_suppresses_ambient_credentials_and_applies_timeout(self) -> None:
        """Only the dedicated Access identity should be sent to a protected gateway."""
        requests = []

        def handler(request: httpx2.Request) -> httpx2.Response:
            requests.append(request)
            self.assertEqual(request.headers["CF-Access-Client-Id"], "offline-client-id")
            self.assertEqual(request.headers["CF-Access-Client-Secret"], "offline-client-secret")
            for name in ("Authorization", "X-Api-Key", "X-Other-Secret"):
                self.assertNotIn(name, request.headers)
            self.assertEqual(request.extensions["timeout"]["read"], 120.0)
            return httpx2.Response(
                200,
                headers={"content-type": "text/event-stream"},
                content=self.analysis_stream(json.dumps(self.complete_analysis())),
            )

        profile = self.access_generator(handler).generate([], [], [], {})
        self.assertEqual(len(requests), 1)
        self.assertEqual(profile.github_stats["generation"]["mode"], "llm")

    def test_access_redirect_is_not_followed_with_service_credentials(self) -> None:
        """A redirect must not carry the Access secret to another origin."""
        requests = []

        def handler(request: httpx2.Request) -> httpx2.Response:
            requests.append(request)
            return httpx2.Response(307, headers={"location": "https://other.invalid/v1/messages"})

        generator = self.access_generator(handler)
        with self.assertRaises(GenerationError):
            generator.generate([], [], [], {})
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0].url.host, "sdk.invalid")

    def test_access_backend_key_must_be_explicit(self) -> None:
        """An optional origin key is distinct from local Anthropic credentials."""

        def handler(request: httpx2.Request) -> httpx2.Response:
            self.assertEqual(request.headers["X-Api-Key"], "explicit-origin-key")
            self.assertNotIn("Authorization", request.headers)
            return httpx2.Response(
                200,
                headers={"content-type": "text/event-stream"},
                content=self.analysis_stream(json.dumps(self.complete_analysis())),
            )

        self.access_generator(handler, PROFILE_LLM_API_KEY="explicit-origin-key").generate(
            [], [], [], {}
        )

    def test_access_configuration_requires_pair_and_https_endpoint(self) -> None:
        """Reject incomplete identity or unsafe destinations before opening a client."""
        cases = [
            {"PROFILE_ACCESS_CLIENT_ID": "id"},
            {"PROFILE_ACCESS_CLIENT_SECRET": "secret"},
            {"PROFILE_ACCESS_CLIENT_ID": "id", "PROFILE_ACCESS_CLIENT_SECRET": "secret"},
            {"ANTHROPIC_BASE_URL": "http://sdk.invalid"},
            {"ANTHROPIC_BASE_URL": "https://user:password@sdk.invalid"},
        ]
        for settings in cases:
            with (
                self.subTest(settings=settings),
                patch.dict("os.environ", settings, clear=True),
                patch("anthropic.Anthropic") as constructor,
                self.assertRaises(GenerationError),
            ):
                ProfileGenerator(ScanConfig(username="offline", strict_scan=True))
            constructor.assert_not_called()
