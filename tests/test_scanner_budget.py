"""Offline tests for bounded GitHub waits and avoiding unnecessary API reads."""

import io
import json
from datetime import UTC, datetime
from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch

from github.GithubException import RateLimitExceededExceedsMaxWait
from github.GithubRetry import GithubRetry
from urllib3.response import HTTPResponse

from iot_profile_builder.models import ComplexityLevel, ScanConfig
from iot_profile_builder.scanner.github_scanner import GitHubScanner


def repository(name: str, *, relevant: bool) -> MagicMock:
    """Supply public repository metadata without making any network request."""
    repo = MagicMock()
    repo.full_name = f"owner/{name}"
    repo.name = name
    repo.private = False
    repo.fork = False
    repo.description = (
        "ESPHome MQTT battery solar energy monitoring for Home Assistant"
        if relevant
        else "Poem collection"
    )
    repo.language = "Python" if relevant else "Text"
    repo.raw_data = {"topics": ["esphome", "mqtt", "battery", "solar"] if relevant else []}
    repo.stargazers_count = 0
    repo.forks_count = 0
    repo.size = 1500
    repo.created_at = datetime(2020, 1, 1, tzinfo=UTC)
    repo.updated_at = datetime(2020, 1, 1, tzinfo=UTC)
    repo.get_languages.return_value = {"Python": 100, "C": 50, "C++": 25, "Shell": 10}
    return repo


def exhausted_quota(reset_at: int) -> HTTPResponse:
    """A real urllib3 response shaped like GitHub's primary quota exhaustion."""
    return HTTPResponse(
        status=403,
        reason="Forbidden",
        headers={"X-RateLimit-Reset": str(reset_at), "Content-Type": "application/json"},
        body=io.BytesIO(json.dumps({"message": "API rate limit exceeded for fixture"}).encode()),
        preload_content=False,
    )


class ScannerBudgetTests(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.client = MagicMock()
        self.factory = self.enterContext(
            patch("iot_profile_builder.scanner.github_scanner.Github", return_value=self.client)
        )
        self.enterContext(
            patch("iot_profile_builder.scanner.github_scanner.enforce_github_tls", lambda x: x)
        )
        self.scanner = GitHubScanner(
            ScanConfig(username="owner", include_orgs=[], strict_scan=True)
        )

    def configured_retry(self) -> GithubRetry:
        """Exercise the actual retry policy installed by the scanner constructor."""
        retry = self.factory.call_args.kwargs["retry"]
        assert isinstance(retry, GithubRetry)
        return retry

    def test_hour_long_quota_reset_is_rejected_without_waiting(self) -> None:
        now = datetime(2030, 1, 1, tzinfo=UTC)
        response = exhausted_quota(int(now.timestamp()) + 3600)
        with (
            patch.object(GithubRetry, "_GithubRetry__datetime", wraps=datetime) as clock,
            patch("time.sleep") as sleep,
            self.assertRaises(RateLimitExceededExceedsMaxWait) as raised,
        ):
            clock.now.return_value = now
            self.configured_retry().increment("GET", "https://api.github.com/example", response)
        self.assertEqual(raised.exception.wait, 3601)
        sleep.assert_not_called()

    def test_short_quota_reset_retains_the_bound_on_the_next_retry(self) -> None:
        now = datetime(2030, 1, 1, tzinfo=UTC)
        response = exhausted_quota(int(now.timestamp()) + 20)
        with patch.object(GithubRetry, "_GithubRetry__datetime", wraps=datetime) as clock:
            clock.now.return_value = now
            following = self.configured_retry().increment(
                "GET", "https://api.github.com/example", response
            )
        self.assertEqual(following.get_backoff_time(), 21)
        assert isinstance(following, GithubRetry)
        self.assertEqual(following.max_rate_limit_wait, 60)

    def test_retry_after_header_cannot_bypass_the_bound_after_cloning(self) -> None:
        response = HTTPResponse(status=403, headers={"Retry-After": "3600"})
        policy = self.configured_retry()
        following = policy.increment("GET", "https://api.github.com/example", response)
        self.assertIs(type(following), type(policy))
        with (
            patch("time.sleep") as sleep,
            self.assertRaises(RateLimitExceededExceedsMaxWait) as raised,
        ):
            following.sleep(response)
        self.assertEqual(raised.exception.wait, 3600)
        sleep.assert_not_called()

    def test_short_retry_after_is_respected_without_retrying_early(self) -> None:
        response = HTTPResponse(status=403, headers={"Retry-After": "60"})
        following = self.configured_retry().increment(
            "GET", "https://api.github.com/example", response
        )
        with patch("time.sleep") as sleep:
            following.sleep(response)
        sleep.assert_called_once_with(60)

    def test_short_retry_after_cannot_override_hour_long_primary_reset(self) -> None:
        now = datetime(2030, 1, 1, tzinfo=UTC)
        response = HTTPResponse(
            status=403,
            headers={
                "Retry-After": "30",
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": str(int(now.timestamp()) + 3600),
            },
        )
        following = self.configured_retry().increment(
            "GET", "https://api.github.com/example", response
        )
        with (
            patch("iot_profile_builder.scanner.github_scanner.datetime", wraps=datetime) as clock,
            patch("time.sleep") as sleep,
            self.assertRaises(RateLimitExceededExceedsMaxWait) as raised,
        ):
            clock.now.return_value = now
            following.sleep(response)
        self.assertEqual(raised.exception.wait, 3601)
        sleep.assert_not_called()

    def test_combined_rate_limit_headers_respect_the_later_allowed_time(self) -> None:
        now = datetime(2030, 1, 1, tzinfo=UTC)
        for retry_after, reset_seconds, expected in [(30, 45, 46), (50, 10, 50)]:
            with self.subTest(retry_after=retry_after, reset_seconds=reset_seconds):
                response = HTTPResponse(
                    status=403,
                    headers={
                        "Retry-After": str(retry_after),
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": str(int(now.timestamp()) + reset_seconds),
                    },
                )
                following = self.configured_retry().increment(
                    "GET", "https://api.github.com/example", response
                )
                with (
                    patch(
                        "iot_profile_builder.scanner.github_scanner.datetime", wraps=datetime
                    ) as clock,
                    patch("time.sleep") as sleep,
                ):
                    clock.now.return_value = now
                    following.sleep(response)
                sleep.assert_called_once_with(expected)

    async def test_irrelevant_repositories_do_not_spend_language_requests(self) -> None:
        relevant = repository("mqtt-battery", relevant=True)
        irrelevant = repository("poems", relevant=False)
        irrelevant.get_languages.side_effect = AssertionError("unnecessary API request")
        self.client.get_user.return_value.get_repos.return_value = [irrelevant, relevant]
        result = await self.scanner.scan()

        self.assertEqual(self.factory.call_args.kwargs["per_page"], 100)
        irrelevant.get_languages.assert_not_called()
        relevant.get_languages.assert_called_once_with()
        relevant.get_topics.assert_not_called()
        self.assertEqual(result.total_scanned, 2)
        self.assertEqual(result.iot_repos, 1)
        self.assertEqual(result.errors, [])
        metrics = result.repositories[0]
        self.assertEqual(metrics.full_name, "owner/mqtt-battery")
        self.assertEqual(metrics.language, "Python")
        self.assertEqual(metrics.topics, relevant.raw_data["topics"])
        self.assertEqual(metrics.complexity, ComplexityLevel.HIGH)
        self.assertAlmostEqual(metrics.iot_score, 0.83)
