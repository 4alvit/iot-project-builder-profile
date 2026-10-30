"""Output generation for engineering profiles (Markdown, HTML, charts)."""

from __future__ import annotations

import json
import logging
from base64 import b64encode
from copy import deepcopy
from datetime import datetime
from hashlib import sha256
from math import isfinite
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

import plotly.graph_objects as go  # type: ignore[import-untyped]
from jinja2 import ChoiceLoader, DictLoader, Environment, FileSystemLoader
from plotly.offline import get_plotlyjs  # type: ignore[import-untyped]

from ..models import (
    ComplexityLevel,
    DBusAnalysis,
    DBusInterface,
    EngineeringProfile,
    ESPHomeAnalysis,
    ESPHomeComponent,
    FocusArea,
    RepositoryMetrics,
    SkillAssessment,
)
from .profile_behavior import PROFILE_SCRIPT
from .profile_page import PROFILE_HTML

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    pass


class ProfileRenderer:
    """Renders engineering profiles to Markdown and HTML."""

    def __init__(self, template_dir: Path | None = None):
        if template_dir is None:
            template_dir = Path(__file__).parent / "templates"
        # Installed packages may be read-only. User templates take precedence,
        # while built-in defaults are loaded without creating package files.
        self.env = Environment(
            loader=ChoiceLoader(
                [
                    FileSystemLoader(template_dir),
                    DictLoader(
                        {
                            "profile.md.j2": self._default_markdown_template(),
                            "profile.html.j2": self._default_html_template(),
                        }
                    ),
                ]
            ),
            autoescape=True,
        )

    def _default_markdown_template(self) -> str:
        return (
            "# IoT Engineering Profile: {{ profile.username }}\n\n"
            "*Generated: {{ profile.generated_at.strftime('%Y-%m-%d %H:%M') }}*\n\n"
            "## Summary\n\n"
            "{{ profile.narrative_summary }}\n\n"
            "---\n\n"
            "## 📊 Repository Overview\n\n"
            "- **Public repositories scanned**: {{ profile.total_repos_analyzed }}\n"
            "- **IoT-Related Repositories**: {{ profile.iot_repos_count }}\n"
            "- **ESPHome Configurations**: {{ profile.esphome_analyses|length }}\n"
            "- **D-Bus analysis records**: {{ profile.dbus_analyses|length }}\n\n"
            "### Complexity Distribution\n\n"
            "Analysis records from IoT repositories, ESPHome configurations and D-Bus analyses.\n\n"
            "{% for level, count in profile.complexity_distribution.items() %}\n"
            "- **{{ level.value.capitalize() }}**: {{ count }}\n"
            "{% endfor %}\n\n"
            "---\n\n"
            "## 🎯 Focus Areas\n\n"
            "{% for area, score in profile.focus_areas.items() %}\n"
            "### {{ area.value.replace('_', ' ').title() }}: {{ \"%.1f\"|format(score * 100) }}%\n\n"
            "{% endfor %}\n\n"
            "---\n\n"
            "## 🛠️ Skills Assessment\n\n"
            "| Skill | Category | Proficiency | Confidence | Evidence |\n"
            "|-------|----------|-------------|------------|----------|\n"
            "{% for skill in profile.skills|sort(attribute='proficiency', reverse=True) %}\n"
            "| {{ skill.name }} | {{ skill.category }} | {{ skill.proficiency }}/10 | "
            "{{ \"%.1f\"|format(skill.confidence * 100) }}% | {{ skill.evidence|join(', ') }} |\n"
            "{% endfor %}\n\n"
            "---\n\n"
            "## 💪 Key Strengths\n\n"
            "{% for strength in profile.key_strengths %}\n"
            "- {{ strength }}\n"
            "{% endfor %}\n\n"
            "---\n\n"
            "## 📈 Growth Areas\n\n"
            "{% for area in profile.growth_areas %}\n"
            "- {{ area }}\n"
            "{% endfor %}\n\n"
            "---\n\n"
            "## 🏆 Top Repositories\n\n"
            "{% for repo in profile.top_repositories %}\n"
            "### {{ repo.name }}\n\n"
            "- **Description**: {{ repo.description or 'No description' }}\n"
            "- **Language**: {{ repo.language or 'N/A' }}\n"
            "- **Stars**: {{ repo.stars }} ⭐ | **Forks**: {{ repo.forks }}\n"
            '- **IoT Score**: {{ "%.2f"|format(repo.iot_score) }}\n'
            "- **Complexity**: {{ repo.complexity.value }}\n"
            "- **Focus Areas**: {{ repo.focus_areas|join(', ') }}\n"
            "- **Topics**: {{ repo.topics|join(', ') }}\n"
            "{% endfor %}\n\n"
            "---\n\n"
            "## 🔧 ESPHome Configurations\n\n"
            "{% for esphome in profile.esphome_analyses %}\n"
            "### {{ esphome.file_path }}\n\n"
            "- **Devices**: {{ esphome.devices|join(', ') }}\n"
            "- **Components**: {{ esphome.components|length }}\n"
            "- **Custom Components**: {{ esphome.custom_components|join(', ') or 'None' }}\n"
            "- **External Libraries**: {{ esphome.external_libs|join(', ') or 'None' }}\n"
            "- **Complexity**: {{ esphome.complexity.value }}\n"
            "- **Focus Areas**: {{ esphome.focus_areas|map(attribute='value')|join(', ') }}\n\n"
            "**Component Breakdown**:\n"
            "{% for comp in esphome.components %}\n"
            "- {{ comp.type }}{% if comp.platform %} ({{ comp.platform }}){% endif %}: "
            "{{ comp.name or 'unnamed' }}\n"
            "{% endfor %}\n"
            "{% endfor %}\n\n"
            "---\n\n"
            "## 📡 D-Bus Services\n\n"
            "{% for dbus in profile.dbus_analyses %}\n"
            "### {{ dbus.service_name }}\n\n"
            "- **Interfaces**: {{ dbus.interfaces|length }}\n"
            "- **Object Paths**: {{ dbus.object_paths|join(', ') }}\n"
            "- **Total Methods**: {{ dbus.interfaces|map(attribute='methods')|map('length')|sum }}\n"
            "- **Total Signals**: {{ dbus.interfaces|map(attribute='signals')|map('length')|sum }}\n"
            "- **Total Properties**: {{ dbus.interfaces|map(attribute='properties')|map('length')|sum }}\n"
            "- **Complexity**: {{ dbus.complexity.value }}\n"
            "- **Focus Areas**: {{ dbus.focus_areas|map(attribute='value')|join(', ') }}\n\n"
            "**Interfaces**:\n"
            "{% for iface in dbus.interfaces %}\n"
            "#### {{ iface.name }} ({{ iface.path }})\n"
            "- Methods: {{ iface.methods|map(attribute='name')|join(', ') or 'None' }}\n"
            "- Signals: {{ iface.signals|map(attribute='name')|join(', ') or 'None' }}\n"
            "- Properties: {{ iface.properties|map(attribute='name')|join(', ') or 'None' }}\n"
            "{% endfor %}\n"
            "{% endfor %}\n\n"
            "---\n\n"
            "## 📈 GitHub Statistics\n\n"
            "```json\n"
            "{{ profile.github_stats|tojson(indent=2) }}\n"
            "```\n"
        )

    def _default_html_template(self) -> str:
        return PROFILE_HTML

    def render_markdown(self, profile: EngineeringProfile, output_path: Path) -> None:
        """Render profile to Markdown."""
        template = self.env.get_template("profile.md.j2")
        content = template.render(profile=profile)
        output_path.write_text(content, encoding="utf-8")

    def render_html(
        self,
        profile: EngineeringProfile,
        output_path: Path,
        *,
        page_kind: str = "overview",
    ) -> None:
        """Render portable HTML with inline charts and source evidence."""
        if page_kind not in ("overview", "repositories", "evidence"):
            raise ValueError("Unknown profile page kind")
        template = self.env.get_template("profile.html.j2")
        # The built-in script is static. Repository and model data retain Jinja
        # escaping; CSP permits only the exact bundled enhancement script.
        script_digest = b64encode(sha256(PROFILE_SCRIPT.encode("utf-8")).digest()).decode("ascii")
        policy = (
            "default-src 'none'; "
            f"script-src 'sha256-{script_digest}'; "
            "style-src 'unsafe-inline'; img-src 'self'; "
            "connect-src 'self' https://api.github.com; "
            "base-uri 'none'; object-src 'none'; form-action 'none'"
        )
        content = template.render(
            profile=profile,
            plotly_js=get_plotlyjs(),
            page_kind=page_kind,
            content_security_policy=policy,
        )
        output_path.write_text(content, encoding="utf-8")

    def generate_charts(self, profile: EngineeringProfile, output_dir: Path) -> dict[str, Path]:
        """Generate chart images and return paths."""
        output_dir.mkdir(parents=True, exist_ok=True)
        chart_paths = {}

        # Focus areas radar chart
        if profile.focus_areas:
            fig = go.Figure()
            fig.add_trace(
                go.Scatterpolar(
                    r=[score * 100 for score in profile.focus_areas.values()],
                    theta=[area.value.replace("_", " ").title() for area in profile.focus_areas],
                    fill="toself",
                    name="Focus Areas",
                    line_color="#667eea",
                )
            )
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=False,
                margin=dict(t=20, b=20, l=20, r=20),
            )
            path = output_dir / "focus_areas_radar.png"
            fig.write_image(str(path))
            chart_paths["focus_areas"] = path

        # Complexity distribution pie chart
        if profile.complexity_distribution:
            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=[
                            level.value.capitalize() for level in profile.complexity_distribution
                        ],
                        values=list(profile.complexity_distribution.values()),
                        hole=0.4,
                        marker_colors=["#28a745", "#ffc107", "#fd7e14", "#dc3545"],
                    )
                ]
            )
            fig.update_layout(
                showlegend=True,
                margin=dict(t=20, b=20, l=20, r=20),
            )
            path = output_dir / "complexity_pie.png"
            fig.write_image(str(path))
            chart_paths["complexity"] = path

        # Skills bar chart
        if profile.skills:
            top_skills = sorted(profile.skills, key=lambda s: s.proficiency, reverse=True)[:15]
            fig = go.Figure(
                data=[
                    go.Bar(
                        x=[s.proficiency for s in top_skills],
                        y=[s.name for s in top_skills],
                        orientation="h",
                        marker_color="#667eea",
                        text=[f"{s.proficiency}/10" for s in top_skills],
                        textposition="auto",
                    )
                ]
            )
            fig.update_layout(
                title="Top Skills by Proficiency",
                xaxis_title="Proficiency (1-10)",
                yaxis=dict(autorange="reversed"),
                margin=dict(t=50, b=20, l=150, r=20),
                height=500,
            )
            path = output_dir / "skills_bar.png"
            fig.write_image(str(path))
            chart_paths["skills"] = path

        return chart_paths


def generate_profile_outputs(
    profile: EngineeringProfile,
    output_dir: Path,
    formats: list[str] | None = None,
) -> dict[str, Path]:
    """Generate all profile outputs."""
    if formats is None:
        formats = ["markdown", "html", "json"]

    output_dir.mkdir(parents=True, exist_ok=True)
    renderer = ProfileRenderer()
    results = {}

    if "markdown" in formats:
        md_path = output_dir / f"{profile.username}_profile.md"
        renderer.render_markdown(profile, md_path)
        results["markdown"] = md_path

    if "html" in formats:
        html_path = output_dir / f"{profile.username}_profile.html"
        renderer.render_html(profile, html_path)
        results["html"] = html_path
        for page_kind in ("repositories", "evidence"):
            page_path = output_dir / f"{page_kind}.html"
            renderer.render_html(profile, page_path, page_kind=page_kind)
            results[page_kind] = page_path

    if "json" in formats:
        json_path = output_dir / f"{profile.username}_profile.json"
        # Convert profile to dict for JSON serialization
        profile_dict = _profile_to_dict(profile)
        json_path.write_text(json.dumps(profile_dict, indent=2, default=str))
        results["json"] = json_path

    if "charts" in formats:
        try:
            chart_paths = renderer.generate_charts(profile, output_dir / "charts")
            results.update(chart_paths)
        except Exception as e:  # charts are optional; needs kaleido for PNG export
            logger.warning("Chart generation skipped: %s", e)

    return results


def _esphome_to_dict(e: ESPHomeAnalysis) -> dict[str, Any]:
    return {
        "file_path": e.file_path,
        "devices": e.devices,
        "components": [
            {
                "type": c.type,
                "platform": c.platform,
                "name": c.name,
                "integrations": c.integrations,
            }
            for c in e.components
        ],
        "custom_components": e.custom_components,
        "external_libs": e.external_libs,
        "complexity": e.complexity.value,
        "focus_areas": [a.value for a in e.focus_areas],
    }


def _dbus_to_dict(d: DBusAnalysis) -> dict[str, Any]:
    return {
        "service_name": d.service_name,
        "interfaces": [
            {
                "name": i.name,
                "path": i.path,
                "methods": i.methods,
                "signals": i.signals,
                "properties": i.properties,
            }
            for i in d.interfaces
        ],
        "object_paths": d.object_paths,
        "complexity": d.complexity.value,
        "focus_areas": [a.value for a in d.focus_areas],
    }


def _profile_to_dict(profile: EngineeringProfile) -> dict[str, Any]:
    """Convert EngineeringProfile to dictionary for JSON serialization."""

    def skill_to_dict(s: SkillAssessment) -> dict[str, Any]:
        return {
            "name": s.name,
            "category": s.category,
            "proficiency": s.proficiency,
            "evidence": s.evidence,
            "confidence": s.confidence,
        }

    def repo_to_dict(r: RepositoryMetrics) -> dict[str, Any]:
        return {
            "name": r.name,
            "full_name": r.full_name,
            "description": r.description,
            "stars": r.stars,
            "forks": r.forks,
            "language": r.language,
            "topics": r.topics,
            "is_fork": r.is_fork,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "updated_at": r.updated_at.isoformat() if r.updated_at else None,
            "size_kb": r.size_kb,
            "complexity": r.complexity.value,
            "focus_areas": [a.value for a in r.focus_areas],
            "iot_score": r.iot_score,
        }

    return {
        "username": profile.username,
        "generated_at": profile.generated_at.isoformat() if profile.generated_at else None,
        "total_repos_analyzed": profile.total_repos_analyzed,
        "iot_repos_count": profile.iot_repos_count,
        "skills": [skill_to_dict(s) for s in profile.skills],
        "focus_areas": {k.value: v for k, v in profile.focus_areas.items()},
        "complexity_distribution": {k.value: v for k, v in profile.complexity_distribution.items()},
        "top_repositories": [repo_to_dict(r) for r in profile.top_repositories],
        "narrative_summary": profile.narrative_summary,
        "key_strengths": profile.key_strengths,
        "growth_areas": profile.growth_areas,
        "github_stats": profile.github_stats,
        "esphome_analyses": [_esphome_to_dict(e) for e in profile.esphome_analyses],
        "dbus_analyses": [_dbus_to_dict(d) for d in profile.dbus_analyses],
    }


def profile_from_dict(value: dict[str, Any]) -> EngineeringProfile:
    """Reconstruct the published schema without scanning or changing its metadata.

    Unknown fields fail instead of being silently lost. Component configuration
    is not part of the published schema and is reconstructed as an empty object.
    """

    def record(data: Any, fields: str, label: str) -> dict[str, Any]:
        if not isinstance(data, dict) or set(data) != set(fields.split()):
            raise ValueError(f"Unexpected or missing fields in {label}")
        return cast(dict[str, Any], data)

    def sequence(data: Any, label: str) -> list[Any]:
        if not isinstance(data, list):
            raise ValueError(f"Expected a list for {label}")
        return data

    def text(data: Any, label: str) -> str:
        if not isinstance(data, str):
            raise ValueError(f"Expected text for {label}")
        return data

    def optional_text(data: Any, label: str) -> str | None:
        return None if data is None else text(data, label)

    def texts(data: Any, label: str) -> list[str]:
        return [text(item, label) for item in sequence(data, label)]

    def integer(data: Any, label: str, minimum: int = 0) -> int:
        if type(data) is not int or data < minimum:
            raise ValueError(f"Expected an integer >= {minimum} for {label}")
        return data

    def score(data: Any, label: str) -> float:
        if type(data) not in (int, float) or not isfinite(data) or not 0 <= data <= 1:
            raise ValueError(f"Expected a finite score between 0 and 1 for {label}")
        return cast(float, data)

    def date(data: Any, label: str) -> datetime:
        try:
            return datetime.fromisoformat(text(data, label).replace("Z", "+00:00"))
        except ValueError:
            raise ValueError(f"Invalid ISO timestamp for {label}") from None

    def areas(data: Any) -> list[FocusArea]:
        return [FocusArea(item) for item in texts(data, "focus areas")]

    def metadata(data: Any, label: str) -> dict[str, Any]:
        if not isinstance(data, dict):
            raise ValueError(f"Expected an object for {label}")
        try:
            json.dumps(data, allow_nan=False)
        except (TypeError, ValueError):
            raise ValueError(f"Expected finite JSON metadata for {label}") from None
        return deepcopy(data)

    def repository(data: Any) -> RepositoryMetrics:
        item = record(
            data,
            "name full_name description stars forks language topics is_fork "
            "created_at updated_at size_kb complexity focus_areas iot_score",
            "repository",
        )
        if type(item["is_fork"]) is not bool:
            raise ValueError("Expected a boolean for repository is_fork")
        return RepositoryMetrics(
            name=text(item["name"], "repository name"),
            full_name=text(item["full_name"], "repository full_name"),
            description=optional_text(item["description"], "repository description"),
            stars=integer(item["stars"], "repository stars"),
            forks=integer(item["forks"], "repository forks"),
            language=optional_text(item["language"], "repository language"),
            topics=texts(item["topics"], "repository topics"),
            is_fork=item["is_fork"],
            created_at=date(item["created_at"], "repository created_at"),
            updated_at=date(item["updated_at"], "repository updated_at"),
            size_kb=integer(item["size_kb"], "repository size"),
            complexity=ComplexityLevel(item["complexity"]),
            focus_areas=areas(item["focus_areas"]),
            iot_score=score(item["iot_score"], "repository IoT score"),
        )

    def skill(data: Any) -> SkillAssessment:
        item = record(data, "name category proficiency evidence confidence", "skill")
        proficiency = integer(item["proficiency"], "skill proficiency", 1)
        if proficiency > 10:
            raise ValueError("Skill proficiency must not exceed 10")
        return SkillAssessment(
            name=text(item["name"], "skill name"),
            category=text(item["category"], "skill category"),
            proficiency=proficiency,
            evidence=texts(item["evidence"], "skill evidence"),
            confidence=score(item["confidence"], "skill confidence"),
        )

    def component(data: Any) -> ESPHomeComponent:
        item = record(data, "type platform name integrations", "ESPHome component")
        return ESPHomeComponent(
            type=text(item["type"], "component type"),
            platform=optional_text(item["platform"], "component platform"),
            name=text(item["name"], "component name"),
            config={},
            integrations=texts(item["integrations"], "component integrations"),
        )

    def esphome(data: Any) -> ESPHomeAnalysis:
        item = record(
            data,
            "file_path devices components custom_components external_libs complexity focus_areas",
            "ESPHome analysis",
        )
        return ESPHomeAnalysis(
            file_path=text(item["file_path"], "ESPHome path"),
            devices=texts(item["devices"], "ESPHome devices"),
            components=[component(x) for x in sequence(item["components"], "components")],
            custom_components=texts(item["custom_components"], "custom components"),
            external_libs=texts(item["external_libs"], "external libraries"),
            complexity=ComplexityLevel(item["complexity"]),
            focus_areas=areas(item["focus_areas"]),
        )

    def interface(data: Any) -> DBusInterface:
        item = record(data, "name path methods signals properties", "D-Bus interface")
        return DBusInterface(
            name=text(item["name"], "D-Bus interface name"),
            path=text(item["path"], "D-Bus interface path"),
            methods=[metadata(x, "methods") for x in sequence(item["methods"], "methods")],
            signals=[metadata(x, "signals") for x in sequence(item["signals"], "signals")],
            properties=[
                metadata(x, "properties") for x in sequence(item["properties"], "properties")
            ],
        )

    def dbus(data: Any) -> DBusAnalysis:
        item = record(
            data, "service_name interfaces object_paths complexity focus_areas", "D-Bus analysis"
        )
        return DBusAnalysis(
            service_name=text(item["service_name"], "D-Bus service name"),
            interfaces=[interface(x) for x in sequence(item["interfaces"], "interfaces")],
            object_paths=texts(item["object_paths"], "D-Bus object paths"),
            complexity=ComplexityLevel(item["complexity"]),
            focus_areas=areas(item["focus_areas"]),
        )

    data = record(
        value,
        "username generated_at total_repos_analyzed iot_repos_count skills focus_areas "
        "complexity_distribution top_repositories narrative_summary key_strengths growth_areas "
        "github_stats esphome_analyses dbus_analyses",
        "profile",
    )
    return EngineeringProfile(
        username=text(data["username"], "username"),
        generated_at=date(data["generated_at"], "generated_at"),
        total_repos_analyzed=integer(data["total_repos_analyzed"], "repository count"),
        iot_repos_count=integer(data["iot_repos_count"], "IoT repository count"),
        skills=[skill(x) for x in sequence(data["skills"], "skills")],
        focus_areas={
            FocusArea(k): score(v, "focus score")
            for k, v in metadata(data["focus_areas"], "focus areas").items()
        },
        complexity_distribution={
            ComplexityLevel(k): integer(v, "complexity count")
            for k, v in metadata(data["complexity_distribution"], "complexity distribution").items()
        },
        top_repositories=[
            repository(x) for x in sequence(data["top_repositories"], "repositories")
        ],
        narrative_summary=text(data["narrative_summary"], "narrative summary"),
        key_strengths=texts(data["key_strengths"], "key strengths"),
        growth_areas=texts(data["growth_areas"], "growth areas"),
        github_stats=metadata(data["github_stats"], "GitHub metadata"),
        esphome_analyses=[
            esphome(x) for x in sequence(data["esphome_analyses"], "ESPHome analyses")
        ],
        dbus_analyses=[dbus(x) for x in sequence(data["dbus_analyses"], "D-Bus analyses")],
    )
