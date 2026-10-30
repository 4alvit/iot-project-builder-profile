"""Output generation for engineering profiles (Markdown, HTML, charts)."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any

import plotly.graph_objects as go  # type: ignore[import-untyped]
from jinja2 import ChoiceLoader, DictLoader, Environment, FileSystemLoader
from plotly.offline import get_plotlyjs  # type: ignore[import-untyped]

from ..models import (
    DBusAnalysis,
    EngineeringProfile,
    ESPHomeAnalysis,
    RepositoryMetrics,
)
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

    def render_html(self, profile: EngineeringProfile, output_path: Path) -> None:
        """Render portable HTML with inline charts and source evidence."""
        template = self.env.get_template("profile.html.j2")
        # Only the installed, locked Plotly library is trusted as executable code.
        # Repository and model data retain Jinja escaping / JSON serialization.
        content = template.render(profile=profile, plotly_js=get_plotlyjs())
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
    from ..models import SkillAssessment

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
