"""GitHub API scanner for IoT-related repositories."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Any

from github import Auth, Github
from github.ContentFile import ContentFile
from github.GithubException import RateLimitExceededExceedsMaxWait
from github.GithubRetry import GithubRetry
from github.Repository import Repository

from ..github_tls import enforce_github_tls
from ..models import (
    ComplexityLevel,
    FocusArea,
    RepositoryMetrics,
    ScanConfig,
)

if TYPE_CHECKING:
    from github.PaginatedList import PaginatedList
    from urllib3.response import BaseHTTPResponse

logger = logging.getLogger(__name__)


class ScanError(RuntimeError):
    """A strict scan cannot publish incomplete repository evidence."""


class _BoundedGithubRetry(GithubRetry):
    """Also bound Retry-After headers, which bypass PyGithub's reset-time guard."""

    def get_retry_after(self, response: BaseHTTPResponse) -> float | None:
        delay = super().get_retry_after(response)
        if (
            delay is not None
            and self.max_rate_limit_wait is not None
            and delay > self.max_rate_limit_wait
        ):
            # Refuse this attempt instead of retrying earlier than GitHub allows.
            raise RateLimitExceededExceedsMaxWait(
                response.status,
                {"message": "GitHub Retry-After exceeds the configured wait limit"},
                wait=delay,
            )
        return delay


IOT_KEYWORDS = {
    "esphome",
    "homeassistant",
    "home-assistant",
    "mqtt",
    "zigbee",
    "zwave",
    "ble",
    "bluetooth",
    "modbus",
    "canbus",
    "can-bus",
    "d-bus",
    "dbus",
    "bms",
    "battery",
    "inverter",
    "solar",
    "energy",
    "power",
    "meter",
    "sensor",
    "actuator",
    "gpio",
    "i2c",
    "spi",
    "uart",
    "rs485",
    "esp32",
    "esp8266",
    "rp2040",
    "stm32",
    "nrf52",
    "arduino",
    "firmware",
    "embedded",
    "micropython",
    "circuitpython",
    "zephyr",
    "freertos",
    "lora",
    "lorawan",
    "wifi",
    "ethernet",
    "thread",
    "matter",
    "homekit",
    "alexa",
    "google-home",
    "voice",
    "automation",
    "smart-home",
    "iot",
    "industrial",
    "scada",
    "telemetry",
    "monitoring",
    "datalogger",
    "data-logger",
}

IOT_LANGUAGES = {
    "Python",
    "C",
    "C++",
    "Rust",
    "Go",
    "C#",
    "TypeScript",
    "JavaScript",
    "YAML",
    "CMake",
    "Makefile",
}

FOCUS_KEYWORDS: dict[FocusArea, set[str]] = {
    FocusArea.HOME_AUTOMATION: {
        "homeassistant",
        "home-assistant",
        "hass",
        "automation",
        "smart-home",
        "light",
        "switch",
        "climate",
        "cover",
        "lock",
        "camera",
        "doorbell",
    },
    FocusArea.INDUSTRIAL_IOT: {
        "modbus",
        "canbus",
        "can-bus",
        "opcua",
        "opc-ua",
        "scada",
        "plc",
        "industrial",
        "factory",
        "manufacturing",
        "process-control",
    },
    FocusArea.ENERGY_MANAGEMENT: {
        "solar",
        "pv",
        "inverter",
        "energy",
        "power",
        "meter",
        "grid",
        "battery",
        "bms",
        "charge",
        "discharge",
        "mppt",
        "photovoltaic",
    },
    FocusArea.BMS: {
        "bms",
        "battery-management",
        "cell",
        "balancing",
        "so",
        "soc",
        "soh",
        "lifepo4",
        "li-ion",
        "battery-pack",
        "jbd",
        "daly",
    },
    FocusArea.ENVIRONMENTAL: {
        "temperature",
        "humidity",
        "pressure",
        "air-quality",
        "co2",
        "pm25",
        "pm10",
        "voc",
        "weather",
        "environment",
        "climate-sensor",
    },
    FocusArea.VOICE_ASSISTANT: {
        "voice",
        "assistant",
        "wake-word",
        "stt",
        "tts",
        "piper",
        "whisper",
        "wyoming",
        "rhasspy",
        "snips",
        "alexa",
        "google-assistant",
    },
    FocusArea.NETWORKING: {
        "mqtt",
        "zigbee",
        "zwave",
        "z-wave",
        "thread",
        "matter",
        "ble",
        "bluetooth",
        "lorawan",
        "wifi",
        "ethernet",
        "tcp",
        "udp",
        "coap",
        "http",
        "websocket",
        "d-bus",
        "dbus",
        "grpc",
    },
    FocusArea.EDGE_COMPUTING: {
        "edge",
        "k3s",
        "kubeedge",
        "openyurt",
        "kubelet",
        "container",
        "docker",
        "podman",
        "wasm",
        "webassembly",
        "edge-computing",
    },
    FocusArea.FIRMWARE: {
        "firmware",
        "bootloader",
        "ota",
        "dfu",
        "flash",
        "gpio",
        "i2c",
        "spi",
        "uart",
        "pwm",
        "adc",
        "dac",
        "rtos",
        "interrupt",
    },
    FocusArea.DATA_PIPELINE: {
        "influxdb",
        "timeseries",
        "time-series",
        "prometheus",
        "grafana",
        "kafka",
        "mqtt",
        "telegraf",
        "flux",
        "sql",
        "postgresql",
        "redis",
        "data-pipeline",
        "etl",
        "analytics",
        "visualization",
    },
}


@dataclass
class ScanResult:
    """Result of GitHub scanning."""

    repositories: list[RepositoryMetrics]
    total_scanned: int
    iot_repos: int
    errors: list[str]


class GitHubScanner:
    """Scans GitHub repositories for IoT-related projects."""

    def __init__(self, config: ScanConfig):
        self.config = config
        self.client = enforce_github_tls(
            Github(
                auth=Auth.Token(config.token) if config.token else None,
                per_page=100,
                retry=_BoundedGithubRetry(max_rate_limit_wait=60),
            )
        )
        self.user = self.client.get_user(config.username)
        self.errors: list[str] = []
        self._repositories: dict[str, Repository] = {}
        self._topics: dict[str, list[str]] = {}
        self._heads: dict[str, str] = {}
        self._trees: dict[str, list[dict[str, Any]]] = {}
        self._contents: dict[tuple[str, str], list[dict[str, Any]]] = {}
        self._files: dict[tuple[str, str], str] = {}

    def record_error(self, message: str) -> None:
        """Record incomplete evidence; publication scans stop at the first error."""
        self.errors.append(message)
        if self.config.strict_scan:
            raise ScanError(message)
        logger.warning(message)

    def _repo_topics(self, repo: Repository) -> list[str]:
        key = repo.full_name.lower()
        if key not in self._topics:
            # Enumeration includes topics on current GitHub APIs.
            topics = repo.raw_data.get("topics")
            if not isinstance(topics, list) or not all(isinstance(t, str) for t in topics):
                topics = repo.get_topics()
            self._topics[key] = topics
        return self._topics[key]

    def _calculate_iot_score(self, repo: Repository) -> float:
        """Calculate IoT relevance score (0-1)."""
        score = 0.0
        text = " ".join(
            [
                (repo.description or "").lower(),
                " ".join(self._repo_topics(repo)).lower(),
                (repo.language or "").lower(),
            ]
        )

        # Language match (ESPHome/YAML repos are often language-null in GitHub)
        if repo.language in IOT_LANGUAGES or "esphome" in text or "yaml" in text:
            score += 0.15

        # Topic/keyword matches
        matches = sum(1 for kw in IOT_KEYWORDS if kw in text)
        score += min(matches * 0.08, 0.5)

        # Description quality
        if repo.description and len(repo.description) > 50:
            score += 0.1

        # Popularity OR rich IoT metadata (public niche repos often have 0 stars)
        if repo.stargazers_count > 10 or matches >= 6:
            score += 0.1
        if repo.forks_count > 5 or matches >= 8:
            score += 0.05

        # Recent activity
        days_since_update = (datetime.now() - repo.updated_at.replace(tzinfo=None)).days
        if days_since_update < 30:
            score += 0.1
        elif days_since_update < 90:
            score += 0.05

        return min(score, 1.0)

    def _determine_complexity(self, repo: Repository, iot_score: float) -> ComplexityLevel:
        """Determine project complexity level."""
        factors = 0

        if repo.size > 10000:  # >10MB
            factors += 2
        elif repo.size > 1000:
            factors += 1

        if repo.stargazers_count > 100:
            factors += 2
        elif repo.stargazers_count > 20:
            factors += 1

        if iot_score > 0.7:
            factors += 1

        # Check for multiple languages (polyglot)
        try:
            languages = repo.get_languages()
            if len(languages) > 3:
                factors += 1
        except Exception as error:
            self.record_error(f"Failed to get languages for {repo.full_name}: {error}")

        if factors >= 5:
            return ComplexityLevel.EXPERT
        elif factors >= 3:
            return ComplexityLevel.HIGH
        elif factors >= 1:
            return ComplexityLevel.MEDIUM
        return ComplexityLevel.LOW

    def _detect_focus_areas(self, repo: Repository) -> list[FocusArea]:
        """Detect IoT focus areas from repository metadata."""
        text = " ".join(
            [
                (repo.description or "").lower(),
                " ".join(self._repo_topics(repo)).lower(),
            ]
        ).split()

        areas = []
        for area, keywords in FOCUS_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                areas.append(area)

        return areas if areas else [FocusArea.UNKNOWN]

    def _repo_to_metrics(self, repo: Repository, iot_score: float) -> RepositoryMetrics:
        """Convert GitHub repo to metrics object."""
        complexity = self._determine_complexity(repo, iot_score)
        focus_areas = self._detect_focus_areas(repo)

        return RepositoryMetrics(
            name=repo.name,
            full_name=repo.full_name,
            description=repo.description,
            stars=repo.stargazers_count,
            forks=repo.forks_count,
            language=repo.language,
            topics=self._repo_topics(repo),
            is_fork=repo.fork,
            created_at=repo.created_at,
            updated_at=repo.updated_at,
            size_kb=repo.size,
            complexity=complexity,
            focus_areas=focus_areas,
            iot_score=iot_score,
        )

    def _iter_org_repos(self, org_name: str, limit: int) -> list[Repository]:
        """List up to `limit` repos for an org without PaginatedList IndexError."""
        org = self.client.get_organization(org_name)
        org_repos: list[Repository] = []
        for i, org_repo in enumerate(org.get_repos(type="public")):
            if i >= limit:
                self.record_error(f"org:{org_name}: repository list exceeds max_repos={limit}")
                break
            org_repos.append(org_repo)
        return org_repos

    async def scan(self) -> ScanResult:
        """Scan user's repositories for IoT projects."""
        repos: list[RepositoryMetrics] = []
        # Never reuse old evidence when a builder starts a second scan.
        self.errors = []
        self._repositories.clear()
        self._topics.clear()
        self._heads.clear()
        self._trees.clear()
        self._contents.clear()
        self._files.clear()
        total = 0
        iot_count = 0

        try:
            seen: set[str] = set()
            gh_repos: list[Repository] = []

            user_repos: PaginatedList[Repository] = self.user.get_repos(
                type="owner" if not self.config.include_forks else "all",
                sort="updated",
                direction="desc",
            )
            for i, user_repo in enumerate(user_repos):
                if i >= self.config.max_repos:
                    self.record_error(
                        f"user:{self.config.username}: repository list exceeds "
                        f"max_repos={self.config.max_repos}"
                    )
                    break
                gh_repos.append(user_repo)

            # Explicit orgs — public repos only (GITHUB_TOKEN is sufficient)
            for org_name in self.config.include_orgs:
                try:
                    org_repos = self._iter_org_repos(org_name, self.config.max_repos)
                    gh_repos.extend(org_repos)
                    logger.info(f"Included {len(org_repos)} repos from org {org_name}")
                except ScanError:
                    raise
                except Exception as e:
                    self.record_error(f"org:{org_name}: {e!s}")

            for repo in gh_repos:
                if repo.full_name in seen:
                    continue
                seen.add(repo.full_name)
                total += 1
                try:
                    if getattr(repo, "private", False):
                        continue  # public repos only
                    if repo.fork and not self.config.include_forks:
                        continue
                    self._repositories[repo.full_name.lower()] = repo
                    iot_score = self._calculate_iot_score(repo)
                    if iot_score >= self.config.min_iot_score:
                        metrics = self._repo_to_metrics(repo, iot_score)
                        repos.append(metrics)
                        iot_count += 1
                        logger.info(
                            f"Found IoT repo: {repo.full_name} (score: {metrics.iot_score:.2f})"
                        )
                except ScanError:
                    raise
                except Exception as e:
                    self.record_error(f"{repo.full_name}: {e!s}")

        except ScanError:
            raise
        except Exception as e:
            self.record_error(f"Scan failed: {e!s}")

        return ScanResult(
            repositories=repos,
            total_scanned=total,
            iot_repos=iot_count,
            errors=self.errors,
        )

    def _resolve_repo(self, repo_ref: str) -> Repository:
        """Reuse public enumeration objects instead of refetching every file's repo."""
        full = repo_ref if "/" in repo_ref else f"{self.config.username}/{repo_ref}"
        key = full.lower()
        if key not in self._repositories:
            repo = self.client.get_repo(full)
            if repo.private is True:
                raise ValueError("Private repositories cannot be public profile evidence")
            self._repositories[key] = repo
        return self._repositories[key]

    def _head(self, repo: Repository) -> str:
        key = repo.full_name.lower()
        if key not in self._heads:
            self._heads[key] = repo.get_branch(repo.default_branch).commit.sha
        return self._heads[key]

    async def get_repo_contents(self, repo_name: str, path: str = "") -> list[dict[str, Any]]:
        """Get repository contents for deeper analysis (single directory)."""
        try:
            repo = self._resolve_repo(repo_name)
            key = (repo.full_name.lower(), path)
            if key in self._contents:
                return self._contents[key]
            contents = repo.get_contents(path, ref=self._head(repo))
            # get_contents returns a single ContentFile for files, list for dirs
            if isinstance(contents, ContentFile):
                contents = [contents]
            result = [
                {"name": c.name, "path": c.path, "type": c.type, "size": c.size} for c in contents
            ]
            self._contents[key] = result
            return result
        except ScanError:
            raise
        except Exception as e:
            self.record_error(f"Failed to get contents for {repo_name}: {e}")
            return []

    async def list_repo_files(
        self,
        repo_name: str,
        suffixes: tuple[str, ...] = (".yaml", ".yml", ".py"),
        max_files: int = 200,
    ) -> list[dict[str, Any]]:
        """Reuse one pinned recursive tree for ESPHome and D-Bus analysis."""
        try:
            repo = self._resolve_repo(repo_name)
            key = repo.full_name.lower()
            if key not in self._trees:
                tree = repo.get_git_tree(self._head(repo), recursive=True)
                if tree.truncated is True:
                    self.record_error(f"Truncated Git tree for {repo_name}")
                self._trees[key] = [
                    {
                        "name": entry.path.rsplit("/", 1)[-1],
                        "path": entry.path,
                        "type": "file",
                        "size": entry.size or 0,
                    }
                    for entry in tree.tree
                    if entry.type == "blob"
                ]
            files: list[dict[str, Any]] = []
            skip_parts = (
                ".git",
                "node_modules",
                "vendor",
                ".venv",
                "dist",
                "build",
                "__pycache__",
                ".github",
                "tests",
                "test",
            )
            for entry in self._trees[key]:
                path = entry["path"]
                if any(part in skip_parts for part in path.split("/")[:-1]):
                    continue
                lower = path.lower()
                if not any(lower.endswith(sfx) or lower.endswith(sfx + ".j2") for sfx in suffixes):
                    continue
                files.append(entry)
                if len(files) >= max_files:
                    break
            return files
        except ScanError:
            raise
        except Exception as e:
            self.record_error(f"Tree listing failed for {repo_name} ({e}); falling back to root")
            contents = await self.get_repo_contents(repo_name)
            return [
                c
                for c in contents
                if c.get("type") == "file"
                and any(
                    c["path"].lower().endswith(sfx) or c["path"].lower().endswith(sfx + ".j2")
                    for sfx in suffixes
                )
            ][:max_files]

    async def get_file_content(self, repo_name: str, path: str) -> str | None:
        """Get file content from repository."""
        try:
            repo = self._resolve_repo(repo_name)
            key = (repo.full_name.lower(), path)
            if key in self._files:
                return self._files[key]
            file = repo.get_contents(path, ref=self._head(repo))
            if isinstance(file, list):
                raise ValueError(f"{path} is a directory, not a file")
            content = (file.decoded_content or b"").decode("utf-8")
            self._files[key] = content
            return content
        except ScanError:
            raise
        except Exception as e:
            self.record_error(f"Failed to get file {path} from {repo_name}: {e}")
            return None
