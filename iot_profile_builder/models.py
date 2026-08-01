"""Core data models for IoT developer profile."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Any


class ComplexityLevel(StrEnum):
    """Project complexity classification."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXPERT = "expert"


class FocusArea(StrEnum):
    """IoT focus area categories."""

    HOME_AUTOMATION = "home_automation"
    INDUSTRIAL_IOT = "industrial_iot"
    ENERGY_MANAGEMENT = "energy_management"
    BMS = "battery_management"
    ENVIRONMENTAL = "environmental_monitoring"
    VOICE_ASSISTANT = "voice_assistant"
    NETWORKING = "networking_protocols"
    EDGE_COMPUTING = "edge_computing"
    FIRMWARE = "firmware_development"
    DATA_PIPELINE = "data_pipeline"
    UNKNOWN = "unknown"


@dataclass
class RepositoryMetrics:
    """Metrics for a single repository."""

    name: str
    description: str | None
    stars: int
    forks: int
    language: str | None
    topics: list[str]
    is_fork: bool
    created_at: datetime
    updated_at: datetime
    size_kb: int
    complexity: ComplexityLevel
    focus_areas: list[FocusArea]
    iot_score: float  # 0-1 confidence this is IoT-related


@dataclass
class ESPHomeComponent:
    """Parsed ESPHome component."""

    type: str  # sensor, binary_sensor, switch, light, climate, etc.
    platform: str | None
    name: str
    config: dict[str, Any]
    integrations: list[str]  # homeassistant, mqtt, ble, etc.


@dataclass
class ESPHomeAnalysis:
    """ESPHome configuration analysis result."""

    file_path: str
    devices: list[str]  # ESP32, ESP8266, RP2040
    components: list[ESPHomeComponent]
    custom_components: list[str]
    external_libs: list[str]
    complexity: ComplexityLevel
    focus_areas: list[FocusArea]


@dataclass
class DBusInterface:
    """D-Bus interface definition."""

    name: str
    path: str
    methods: list[dict[str, Any]]
    signals: list[dict[str, Any]]
    properties: list[dict[str, Any]]


@dataclass
class DBusAnalysis:
    """D-Bus service analysis result."""

    service_name: str
    interfaces: list[DBusInterface]
    object_paths: list[str]
    complexity: ComplexityLevel
    focus_areas: list[FocusArea]


@dataclass
class SkillAssessment:
    """Individual skill with proficiency level."""

    name: str
    category: str
    proficiency: int  # 1-10
    evidence: list[str]
    confidence: float  # 0-1


@dataclass
class EngineeringProfile:
    """Complete IoT developer engineering profile."""

    username: str
    generated_at: datetime
    total_repos_analyzed: int
    iot_repos_count: int

    # Skills
    skills: list[SkillAssessment] = field(default_factory=list)

    # Focus areas with scores
    focus_areas: dict[FocusArea, float] = field(default_factory=dict)

    # Complexity distribution
    complexity_distribution: dict[ComplexityLevel, int] = field(default_factory=dict)

    # Top repositories
    top_repositories: list[RepositoryMetrics] = field(default_factory=list)

    # ESPHome analysis
    esphome_analyses: list[ESPHomeAnalysis] = field(default_factory=list)

    # D-Bus analysis
    dbus_analyses: list[DBusAnalysis] = field(default_factory=list)

    # Summary
    narrative_summary: str = ""
    key_strengths: list[str] = field(default_factory=list)
    growth_areas: list[str] = field(default_factory=list)

    # Metadata
    github_stats: dict[str, Any] = field(default_factory=dict)


@dataclass
class ScanConfig:
    """Configuration for GitHub scanning."""

    username: str
    token: str | None = None
    max_repos: int = 100
    include_forks: bool = False
    min_iot_score: float = 0.3
    analyze_esphome: bool = True
    analyze_dbus: bool = True
    llm_model: str = "claude-3-5-sonnet-20241022"
