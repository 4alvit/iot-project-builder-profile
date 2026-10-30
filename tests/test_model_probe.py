"""Model preflight uses the real SDK with local, synthetic HTTP responses."""

import io
import json
from contextlib import redirect_stdout
from unittest import TestCase
from unittest.mock import MagicMock, patch

import anthropic
import httpx2

from iot_profile_builder.generator.profile_generator import ProfileGenerator
from iot_profile_builder.models import ScanConfig
from scripts import probe_profile_model
from tests.test_anthropic_streaming import block, message_start, message_stop


def probe_stream(text: str = "READY", reason: str = "end_turn") -> bytes:
    """Build an actual Messages SSE response without any provider service."""
    return (
        message_start()
        + block(0, {"type": "text", "text": ""}, {"type": "text_delta", "text": text})
        + message_stop(reason)
    )


class ModelProbeTests(TestCase):
    def generator(
        self, body: bytes, status: int = 200, headers: dict[str, str] | None = None
    ) -> ProfileGenerator:
        self.requests: list[httpx2.Request] = []

        def handler(request: httpx2.Request) -> httpx2.Response:
            self.requests.append(request)
            payload = json.loads(request.content)
            self.assertEqual(request.url.path, "/v1/messages")
            self.assertEqual(payload["max_tokens"], 128)
            self.assertEqual(payload["model"], "offline-model")
            self.assertTrue(payload["stream"])
            self.assertEqual(
                payload["messages"],
                [{"role": "user", "content": "Reply with exactly READY and no other text."}],
            )
            return httpx2.Response(
                status,
                content=body,
                headers=headers or {"content-type": "text/event-stream"},
            )

        client = anthropic.Anthropic(
            api_key="private-test-credential",
            base_url="https://private-endpoint.invalid",
            timeout=120.0,
            max_retries=0,
            http_client=httpx2.Client(transport=httpx2.MockTransport(handler), trust_env=False),
        )
        self.addCleanup(client.close)
        with patch("anthropic.Anthropic", return_value=client) as constructor:
            generator = ProfileGenerator(
                ScanConfig(username="offline", llm_model="offline-model", strict_scan=True)
            )
        constructor.assert_called_once_with(timeout=120.0, max_retries=0)
        return generator

    def test_success_has_no_narrative_and_uses_one_small_request(self) -> None:
        result = self.generator(probe_stream()).probe()
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["model"], "offline-model")
        self.assertEqual(result["mode"], "model_preflight")
        self.assertGreaterEqual(result["duration_seconds"], 0)
        self.assertEqual(len(self.requests), 1)
        self.assertNotIn("READY", json.dumps(result))
        self.assertNotIn("narrative", result)

    def test_truncated_and_incorrect_replies_cannot_pass(self) -> None:
        for text, reason in [
            ("READY", "max_tokens"),
            ("Wrong answer", "end_turn"),
            ("", "end_turn"),
        ]:
            with self.subTest(text=text, reason=reason):
                result = self.generator(probe_stream(text, reason)).probe()
                self.assertEqual(result["status"], "failed")
                self.assertEqual(result["error"], "invalid_response")
                self.assertEqual(len(self.requests), 1)
                self.assertNotIn("Wrong answer", json.dumps(result))

    def test_cloudflare_failure_reports_only_allowlisted_metadata(self) -> None:
        result = self.generator(
            b"error code: 1010\nprivate-test-credential\nhttps://private-endpoint.invalid",
            status=403,
            headers={
                "content-type": "text/plain; charset=UTF-8",
                "cf-ray": "1234567890abcdef-SJC",
                "server": "cloudflare",
                "set-cookie": "private-cookie",
            },
        ).probe()
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["http_status"], 403)
        self.assertEqual(result["cloudflare_ray_id"], "1234567890abcdef-SJC")
        self.assertEqual(result["edge_error_code"], 1010)
        self.assertEqual(len(self.requests), 1)
        serialized = json.dumps(result)
        for private in ("private-test-credential", "private-endpoint", "private-cookie"):
            self.assertNotIn(private, serialized)

    def test_auth_error_does_not_echo_json_body_or_invalid_ray(self) -> None:
        result = self.generator(
            b'{"error":{"type":"authentication_error","message":"private-token 1010"}}',
            status=401,
            headers={"content-type": "application/json", "cf-ray": "private-token"},
        ).probe()
        self.assertEqual(result["http_status"], 401)
        self.assertNotIn("edge_error_code", result)
        self.assertNotIn("cloudflare_ray_id", result)
        self.assertNotIn("private-token", json.dumps(result))

    def test_cli_rejects_missing_configuration_without_model_request(self) -> None:
        output = io.StringIO()
        with (
            patch.dict("os.environ", {}, clear=True),
            patch.object(probe_profile_model, "ProfileGenerator") as constructor,
            redirect_stdout(output),
            patch("logging.disable"),
        ):
            status = probe_profile_model.main()
        self.assertEqual(status, 1)
        constructor.assert_not_called()
        self.assertEqual(json.loads(output.getvalue())["error"], "configuration_error")

    def test_cli_failure_emits_one_json_record_and_nonzero_status(self) -> None:
        generator = MagicMock()
        generator.probe.return_value = {
            "mode": "model_preflight",
            "status": "failed",
            "http_status": 403,
        }
        generator.client.close.side_effect = RuntimeError("private-cleanup-detail")
        output = io.StringIO()
        with (
            patch.dict(
                "os.environ",
                {
                    "PROFILE_LLM_MODEL": "offline-model",
                    "ANTHROPIC_BASE_URL": "https://private.invalid",
                },
            ),
            patch.object(probe_profile_model, "ProfileGenerator", return_value=generator),
            redirect_stdout(output),
            patch("logging.disable"),
        ):
            status = probe_profile_model.main()
        self.assertEqual(status, 1)
        self.assertEqual(json.loads(output.getvalue())["http_status"], 403)
        self.assertEqual(len(output.getvalue().splitlines()), 1)
        self.assertNotIn("private", output.getvalue())
