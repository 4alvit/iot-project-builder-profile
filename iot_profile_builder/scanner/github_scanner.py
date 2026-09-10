"""GitHub API scanner for IoT-related repositories."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Any

from github import Github
from github.ContentFile import ContentFile
from github.Repository import Repository

from ..models import (
    ComplexityLevel,
    FocusArea,
    RepositoryMetrics,
    ScanConfig,
)

if TYPE_CHECKING:
    from github.PaginatedList import PaginatedList

logger = logging.getLogger(__name__)

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
        self.client = Github(config.token) if config.token else Github()
        self.user = self.client.get_user(config.username)

    def _calculate_iot_score(self, repo: Repository) -> float:
        """Calculate IoT relevance score (0-1)."""
        score = 0.0
        text = " ".join(
            [
                (repo.description or "").lower(),
                " ".join(repo.get_topics()).lower(),
                (repo.language or "").lower(),
            ]
        )

        # Language match
        if repo.language in IOT_LANGUAGES:
            score += 0.15

        # Topic/keyword matches
        matches = sum(1 for kw in IOT_KEYWORDS if kw in text)
        score += min(matches * 0.08, 0.5)

        # Description quality
        if repo.description and len(repo.description) > 50:
            score += 0.1

        # Stars/forks indicate activity
        if repo.stargazers_count > 10:
            score += 0.1
        if repo.forks_count > 5:
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
        except Exception:
            pass

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
                " ".join(repo.get_topics()).lower(),
            ]
        ).split()

        areas = []
        for area, keywords in FOCUS_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                areas.append(area)

        return areas if areas else [FocusArea.UNKNOWN]

    def _repo_to_metrics(self, repo: Repository) -> RepositoryMetrics:
        """Convert GitHub repo to metrics object."""
        iot_score = self._calculate_iot_score(repo)
        complexity = self._determine_complexity(repo, iot_score)
        focus_areas = self._detect_focus_areas(repo)

        return RepositoryMetrics(
            name=repo.name,
            full_name=repo.full_name,
            description=repo.description,
            stars=repo.stargazers_count,
            forks=repo.forks_count,
            language=repo.language,
            topics=repo.get_topics(),
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
                break
            org_repos.append(org_repo)
        return org_repos

    async def scan(self) -> ScanResult:
        """Scan user's repositories for IoT projects."""
        repos: list[RepositoryMetrics] = []
        errors: list[str] = []
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
                    break
                gh_repos.append(user_repo)

            # Explicit orgs — public repos only (GITHUB_TOKEN is sufficient)
            for org_name in self.config.include_orgs:
                try:
                    org_repos = self._iter_org_repos(org_name, self.config.max_repos)
                    gh_repos.extend(org_repos)
                    logger.info(f"Included {len(org_repos)} repos from org {org_name}")
                except Exception as e:
                    errors.append(f"org:{org_name}: {e!s}")
                    logger.warning(f"Failed to list org {org_name}: {e}")

            for repo in gh_repos:
                if repo.full_name in seen:
                    continue
                seen.add(repo.full_name)
                if len(seen) > self.config.max_repos * 2:
                    break
                total += 1
                try:
                    if getattr(repo, "private", False):
                        continue  # public repos only
                    if repo.fork and not self.config.include_forks:
                        continue
                    metrics = self._repo_to_metrics(repo)
                    if metrics.iot_score >= self.config.min_iot_score:
                        repos.append(metrics)
                        iot_count += 1
                        logger.info(
                            f"Found IoT repo: {repo.full_name} (score: {metrics.iot_score:.2f})"
                        )
                except Exception as e:
                    errors.append(f"{repo.full_name}: {e!s}")
                    logger.warning(f"Error processing {repo.full_name}: {e}")

        except Exception as e:
            errors.append(f"Scan failed: {e!s}")
            logger.error(f"Scan failed: {e}")

        return ScanResult(
            repositories=repos,
            total_scanned=total,
            iot_repos=iot_count,
            errors=errors,
        )

    def _resolve_repo(self, repo_ref: str):
        """Resolve owner/name or bare name under configured username."""
        full = repo_ref if "/" in repo_ref else f"{self.config.username}/{repo_ref}"
        return self.client.get_repo(full)

    async def get_repo_contents(self, repo_name: str, path: str = "") -> list[dict[str, Any]]:
        """Get repository contents for deeper analysis (single directory)."""
        try:
            repo = self._resolve_repo(repo_name)
            contents = repo.get_contents(path)
            # get_contents returns a single ContentFile for files, list for dirs
            if isinstance(contents, ContentFile):
                contents = [contents]
            return [
                {"name": c.name, "path": c.path, "type": c.type, "size": c.size} for c in contents
            ]
        except Exception as e:
            logger.error(f"Failed to get contents for {repo_name}: {e}")
            return []

    async def list_repo_files(
        self,
        repo_name: str,
        suffixes: tuple[str, ...] = (".yaml", ".yml", ".py"),
        max_files: int = 200,
    ) -> list[dict[str, Any]]:
        """List matching files recursively via Git Trees API (falls back to root listing)."""
        try:
            repo = self._resolve_repo(repo_name)
            sha = repo.get_branch(repo.default_branch).commit.sha
            tree = repo.get_git_tree(sha, recursive=True)
            files: list[dict[str, Any]] = []
            skip_parts = (
                ".git/",
                "node_modules/",
                "vendor/",
                ".venv/",
                "dist/",
                "build/",
                "__pycache__/",
            )
            for entry in tree.tree:
                if entry.type != "blob":
                    continue
                path = entry.path
                if any(p in path for p in skip_parts):
                    continue
                lower = path.lower()
                if not any(lower.endswith(sfx) or lower.endswith(sfx + ".j2") for sfx in suffixes):
                    continue
                # Skip secrets examples / lock-ish yaml noise at root of CI configs optionally
                name = path.rsplit("/", 1)[-1]
                files.append(
                    {
                        "name": name,
                        "path": path,
                        "type": "file",
                        "size": entry.size or 0,
                    }
                )
                if len(files) >= max_files:
                    break
            return files
        except Exception as e:
            logger.warning(f"Tree listing failed for {repo_name} ({e}); falling back to root")
            contents = await self.get_repo_contents(repo_name)
            return [
                c
                for c in contents
                if c.get("type") == "file"
                and any(
                    c["path"].lower().endswith(sfx) or c["path"].lower().endswith(sfx + ".j2")
                    for sfx in suffixes
                )
            ]

    async def get_file_content(self, repo_name: str, path: str) -> str | None:
        """Get file content from repository."""
        try:
            repo = self._resolve_repo(repo_name)
            file = repo.get_contents(path)
            if isinstance(file, list):
                raise ValueError(f"{path} is a directory, not a file")
            return (file.decoded_content or b"").decode("utf-8")
        except Exception as e:
            logger.error(f"Failed to get file {path} from {repo_name}: {e}")
            return None
