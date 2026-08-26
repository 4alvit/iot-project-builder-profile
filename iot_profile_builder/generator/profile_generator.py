"""LLM-based engineering profile generator."""

from __future__ import annotations

import json
import logging
import re
from typing import TYPE_CHECKING, Any

import anthropic

from ..models import (
    ComplexityLevel,
    EngineeringProfile,
    FocusArea,
    RepositoryMetrics,
    ScanConfig,
)

if TYPE_CHECKING:
    from iot_profile_builder.analyzers.dbus_analyzer import DBusAnalysis
    from iot_profile_builder.analyzers.esphome_analyzer import ESPHomeAnalysis

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are an expert IoT engineer analyzing a developer's GitHub activity "
    "to create a comprehensive engineering profile.\n\n"
    "Analyze the provided data and generate:\n"
    "1. Skill assessments with proficiency levels (1-10) and evidence\n"
    "2. Focus area scores (0-1) with reasoning\n"
    "3. Narrative summary of the developer's IoT expertise\n"
    "4. Key strengths and growth areas\n\n"
    "Be specific and evidence-based. Reference actual repositories, "
    "components, and technologies found.\n"
    "Focus on IoT-relevant skills: embedded systems, protocols "
    "(MQTT, Modbus, BLE, etc.), Home Assistant/ESPHome, energy systems, "
    "battery management, firmware, edge computing, data pipelines."
)

SKILL_CATEGORIES = {
    "embedded_firmware": [
        "C",
        "C++",
        "Rust",
        "Zephyr",
        "FreeRTOS",
        "ESP-IDF",
        "Arduino",
        "STM32",
        "NRF52",
        "RP2040",
        "GPIO",
        "I2C",
        "SPI",
        "UART",
        "ADC",
        "DAC",
        "PWM",
        "interrupts",
        "DMA",
        "bootloader",
        "OTA",
    ],
    "home_automation": [
        "Home Assistant",
        "ESPHome",
        "ESP32",
        "ESP8266",
        "YAML",
        "Jinja2",
        "automation",
        "script",
        "sensor",
        "switch",
        "light",
        "climate",
        "Matter",
        "Thread",
        "Zigbee",
        "Z-Wave",
        "Bluetooth",
        "BLE",
    ],
    "energy_systems": [
        "solar",
        "photovoltaic",
        "inverter",
        "MPPT",
        "battery",
        "BMS",
        "Victron",
        "energy meter",
        "power monitoring",
        "grid",
        "off-grid",
        "LiFePO4",
        "cell balancing",
        "SOC",
        "SOH",
        "Modbus",
        "DBus",
    ],
    "protocols_networking": [
        "MQTT",
        "Modbus",
        "CANbus",
        "HTTP",
        "WebSocket",
        "CoAP",
        "gRPC",
        "TCP",
        "UDP",
        "LoRaWAN",
        "WiFi",
        "Ethernet",
        "BLE",
        "Zigbee",
        "Thread",
        "Matter",
        "DBus",
        "D-Bus",
        "systemd",
        "NetworkManager",
    ],
    "data_pipeline": [
        "InfluxDB",
        "TimescaleDB",
        "Prometheus",
        "Grafana",
        "Telegraf",
        "Kafka",
        "MQTT",
        "Flux",
        "SQL",
        "PostgreSQL",
        "Redis",
        "data pipeline",
        "ETL",
        "analytics",
        "visualization",
    ],
    "edge_computing": [
        "Docker",
        "Podman",
        "Kubernetes",
        "K3s",
        "KubeEdge",
        "OpenYurt",
        "container",
        "WASM",
        "WebAssembly",
        "edge",
        "IoT Edge",
        "Azure IoT Edge",
        "AWS Greengrass",
    ],
    "python_iot": [
        "Python",
        "asyncio",
        "aiohttp",
        "paho-mqtt",
        "bleak",
        "pyModbus",
        "dbus-python",
        "pydbus",
        "gi.repository",
        "Home Assistant",
        "ESPHome",
        "custom components",
        "integration",
    ],
    "voice_ai": [
        "voice assistant",
        "wake word",
        "STT",
        "TTS",
        "Piper",
        "Whisper",
        "Wyoming",
        "Rhasspy",
        "ESP32-S3",
        "I2S",
        "ES8311",
        "ES7210",
        "microphone",
        "speaker",
        "audio pipeline",
    ],
}


class ProfileGenerator:
    """Generates engineering profile from scan data using LLM."""

    def __init__(self, config: ScanConfig):
        self.config = config
        self.client = anthropic.Anthropic()
        self.model = config.llm_model

    def generate(
        self,
        repos: list[RepositoryMetrics],
        esphome_analyses: list[ESPHomeAnalysis],
        dbus_analyses: list[DBusAnalysis],
        github_stats: dict[str, Any],
    ) -> EngineeringProfile:
        """Generate complete engineering profile."""

        # Build context for LLM
        context = self._build_context(repos, esphome_analyses, dbus_analyses, github_stats)

        # Get LLM analysis
        llm_result = self._call_llm(context)

        # Parse and construct profile
        profile = self._parse_llm_result(
            llm_result, repos, esphome_analyses, dbus_analyses, github_stats
        )

        return profile

    def _build_context(
        self,
        repos: list[RepositoryMetrics],
        esphome_analyses: list[ESPHomeAnalysis],
        dbus_analyses: list[DBusAnalysis],
        github_stats: dict[str, Any],
    ) -> str:
        """Build context string for LLM."""

        repo_summaries = []
        for r in repos[:20]:
            repo_summaries.append(
                f"- {r.name}: {r.description or 'No description'} "
                f"({r.language}, {r.stars}⭐, iot_score: {r.iot_score:.2f}, "
                f"complexity: {r.complexity.value}, areas: "
                f"{[a.value for a in r.focus_areas]})"
            )

        esphome_summary = []
        for e in esphome_analyses[:10]:
            comps = [f"{c.type}:{c.platform or 'default'}" for c in e.components]
            esphome_summary.append(
                f"- {e.file_path}: devices={e.devices}, "
                f"components=[{', '.join(comps[:10])}], "
                f"complexity={e.complexity.value}, "
                f"areas={[a.value for a in e.focus_areas]}"
            )

        dbus_summary = []
        for d in dbus_analyses[:10]:
            total_methods = sum(len(i.methods) for i in d.interfaces)
            total_signals = sum(len(i.signals) for i in d.interfaces)
            dbus_summary.append(
                f"- {d.service_name}: {len(d.interfaces)} interfaces, "
                f"{total_methods} methods, {total_signals} signals, "
                f"complexity={d.complexity.value}, "
                f"areas={[a.value for a in d.focus_areas]}"
            )

        context = (
            f"GitHub Stats: {json.dumps(github_stats, default=str)}\n\n"
            f"Repositories ({len(repos)} IoT-related):\n"
            f"{chr(10).join(repo_summaries)}\n\n"
            f"ESPHome Analyses ({len(esphome_analyses)} files):\n"
            f"{chr(10).join(esphome_summary) or 'None'}\n\n"
            f"D-Bus Analyses ({len(dbus_analyses)} services):\n"
            f"{chr(10).join(dbus_summary) or 'None'}\n\n"
            f"Skill Categories Reference:\n"
            f"{json.dumps(SKILL_CATEGORIES, indent=2)}"
        )
        return context

    def _call_llm(self, context: str) -> dict[str, Any]:
        """Call Anthropic API for profile generation."""

        focus_area_values = [a.value for a in FocusArea]
        user_prompt = (
            "Analyze this IoT developer's GitHub activity and create a "
            f"comprehensive engineering profile.\n\n{context}\n\n"
            "Return JSON with these fields:\n"
            "{\n"
            '    "skills": [\n'
            '        {"name": "skill name", "category": "category", '
            '"proficiency": 1-10, "evidence": ["repo1", "repo2"], '
            '"confidence": 0.0-1.0}\n'
            "    ],\n"
            '    "focus_areas": {"focus_area_name": 0.0-1.0},\n'
            '    "narrative_summary": "2-3 paragraph summary",\n'
            '    "key_strengths": ["strength1", "strength2"],\n'
            '    "growth_areas": ["area1", "area2"]\n'
            "}\n\n"
            f"Focus areas must be from: {focus_area_values}\n"
            "Categories from skill categories reference above.\n"
            "Output ONLY the JSON object — no markdown fences, no comments, "
            "no trailing commas. It must parse with a strict JSON parser."
        )

        try:
            # Stream + concatenate text blocks: gateways that always stream
            # (ignoring stream:false) break plain messages.create, and reasoning
            # models may prepend a thinking block before the answer text.
            with self.client.messages.stream(
                model=self.model,
                max_tokens=8192,
                temperature=0.3,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_prompt}],
            ) as stream:
                response = stream.get_final_message()
            content = "".join(b.text for b in response.content if b.type == "text")

            # Extract JSON from response
            json_start = content.find("{")
            json_end = content.rfind("}") + 1
            if json_start < 0 or json_end <= json_start:
                raise ValueError("no JSON object found in LLM output")
            candidate = content[json_start:json_end]

            parsed = None
            try:
                parsed = json.loads(candidate)
            except json.JSONDecodeError:
                # Best-effort repair for sloppy LLM JSON (trailing commas etc.)
                repaired = re.sub(r",\s*(?=[}\]])", "", candidate)
                parsed = json.loads(repaired)  # may raise -> logged below
            if not isinstance(parsed, dict):
                raise ValueError("LLM returned non-object JSON")

            # Unwrap nested wrappers like {"profile_analysis": {"skills": ...}}
            while "skills" not in parsed and any(isinstance(v, dict) for v in parsed.values()):
                inner = next(v for v in parsed.values() if isinstance(v, dict))
                parsed = inner
            if "skills" not in parsed:
                raise ValueError("LLM JSON missing 'skills' key")

            return parsed

        except Exception as e:
            logger.error(f"LLM call failed: {e}")

        return self._fallback_analysis()

    def _parse_llm_result(
        self,
        llm_result: dict[str, Any],
        repos: list[RepositoryMetrics],
        esphome_analyses: list[ESPHomeAnalysis],
        dbus_analyses: list[DBusAnalysis],
        github_stats: dict[str, Any],
    ) -> EngineeringProfile:
        """Parse LLM result into EngineeringProfile."""

        from ..models import SkillAssessment

        # Parse skills
        skills = []
        for s in llm_result.get("skills", []):
            skills.append(
                SkillAssessment(
                    name=s["name"],
                    category=s["category"],
                    proficiency=s["proficiency"],
                    evidence=s["evidence"],
                    confidence=s["confidence"],
                )
            )

        # Parse focus areas
        focus_areas = {}
        for area_str, score in llm_result.get("focus_areas", {}).items():
            try:
                area = FocusArea(area_str)
                focus_areas[area] = float(score)
            except ValueError:
                pass

        # Build complexity distribution
        complexity_dist: dict[ComplexityLevel, int] = {}
        for repo in repos:
            complexity_dist[repo.complexity] = complexity_dist.get(repo.complexity, 0) + 1
        for e in esphome_analyses:
            complexity_dist[e.complexity] = complexity_dist.get(e.complexity, 0) + 1
        for d in dbus_analyses:
            complexity_dist[d.complexity] = complexity_dist.get(d.complexity, 0) + 1

        # Top repositories by IoT score
        top_repos = sorted(repos, key=lambda r: r.iot_score, reverse=True)[:10]

        return EngineeringProfile(
            username=self.config.username,
            generated_at=__import__("datetime").datetime.now(),
            total_repos_analyzed=len(repos) + len(esphome_analyses) + len(dbus_analyses),
            iot_repos_count=len(repos),
            skills=skills,
            focus_areas=focus_areas,
            complexity_distribution=complexity_dist,
            top_repositories=top_repos,
            esphome_analyses=esphome_analyses,
            dbus_analyses=dbus_analyses,
            narrative_summary=llm_result.get("narrative_summary", ""),
            key_strengths=llm_result.get("key_strengths", []),
            growth_areas=llm_result.get("growth_areas", []),
            github_stats=github_stats,
        )

    def _fallback_analysis(self) -> dict[str, Any]:
        """Fallback analysis if LLM fails."""
        return {
            "skills": [],
            "focus_areas": {},
            "narrative_summary": (
                "LLM analysis unavailable. Profile based on heuristic analysis only."
            ),
            "key_strengths": [],
            "growth_areas": ["Enable LLM analysis for deeper insights"],
        }


def generate_heuristic_profile(
    repos: list[RepositoryMetrics],
    esphome_analyses: list[ESPHomeAnalysis],
    dbus_analyses: list[DBusAnalysis],
    github_stats: dict[str, Any],
    username: str,
) -> EngineeringProfile:
    """Generate profile without LLM (heuristic only)."""
    # This provides a baseline when LLM is not available
    from ..models import SkillAssessment

    skills = []
    focus_areas = {area: 0.0 for area in FocusArea}
    complexity_dist: dict[ComplexityLevel, int] = {}

    # Aggregate from repos
    for repo in repos:
        for area in repo.focus_areas:
            focus_areas[area] = focus_areas.get(area, 0.0) + repo.iot_score
        complexity_dist[repo.complexity] = complexity_dist.get(repo.complexity, 0) + 1

    # Aggregate from ESPHome
    for e in esphome_analyses:
        for area in e.focus_areas:
            focus_areas[area] = focus_areas.get(area, 0.0) + 0.5
        complexity_dist[e.complexity] = complexity_dist.get(e.complexity, 0) + 1

    # Aggregate from D-Bus
    for d in dbus_analyses:
        for area in d.focus_areas:
            focus_areas[area] = focus_areas.get(area, 0.0) + 0.5
        complexity_dist[d.complexity] = complexity_dist.get(d.complexity, 0) + 1

    # Normalize focus areas
    max_score = max(focus_areas.values()) if focus_areas else 1.0
    if max_score > 0:
        focus_areas = {k: v / max_score for k, v in focus_areas.items()}

    # Detect skills from technologies
    tech_keywords = {
        "ESPHome": "home_automation",
        "Home Assistant": "home_automation",
        "MQTT": "protocols_networking",
        "Modbus": "protocols_networking",
        "Victron": "energy_systems",
        "DBus": "protocols_networking",
        "ESP32": "embedded_firmware",
        "ESP8266": "embedded_firmware",
        "BLE": "protocols_networking",
        "Docker": "edge_computing",
        "Kubernetes": "edge_computing",
        "InfluxDB": "data_pipeline",
        "Grafana": "data_pipeline",
        "Prometheus": "data_pipeline",
        "Python": "python_iot",
        "YAML": "home_automation",
    }

    all_text = " ".join(
        [r.name + " " + (r.description or "") + " " + " ".join(r.topics) for r in repos]
    ).lower()

    for tech, category in tech_keywords.items():
        if tech.lower() in all_text:
            skills.append(
                SkillAssessment(
                    name=tech,
                    category=category,
                    proficiency=min(5 + all_text.count(tech.lower()), 10),
                    evidence=[r.name for r in repos if tech.lower() in r.name.lower()][:3],
                    confidence=0.7,
                )
            )

    top_repos = sorted(repos, key=lambda r: r.iot_score, reverse=True)[:10]

    return EngineeringProfile(
        username=username,
        generated_at=__import__("datetime").datetime.now(),
        total_repos_analyzed=len(repos) + len(esphome_analyses) + len(dbus_analyses),
        iot_repos_count=len(repos),
        skills=skills,
        focus_areas=focus_areas,
        complexity_distribution=complexity_dist,
        top_repositories=top_repos,
        esphome_analyses=esphome_analyses,
        dbus_analyses=dbus_analyses,
        narrative_summary=(
            "Heuristic analysis based on repository metadata, "
            "ESPHome configs, and D-Bus services found."
        ),
        key_strengths=[area.value for area, score in focus_areas.items() if score > 0.5][:3],
        growth_areas=[area.value for area, score in focus_areas.items() if score < 0.3][:3],
        github_stats=github_stats,
    )
