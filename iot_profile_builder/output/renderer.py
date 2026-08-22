"""Output generation for engineering profiles (Markdown, HTML, charts)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

import plotly.graph_objects as go  # type: ignore[import-untyped]
from jinja2 import Environment, FileSystemLoader

from ..models import (
    EngineeringProfile,
    RepositoryMetrics,
)

if TYPE_CHECKING:
    pass


class ProfileRenderer:
    """Renders engineering profiles to Markdown and HTML."""

    def __init__(self, template_dir: Path | None = None):
        if template_dir is None:
            template_dir = Path(__file__).parent / "templates"
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=True,
        )
        self._ensure_templates(template_dir)

    def _ensure_templates(self, template_dir: Path) -> None:
        """Create default templates if they don't exist."""
        template_dir.mkdir(parents=True, exist_ok=True)

        md_template = template_dir / "profile.md.j2"
        if not md_template.exists():
            md_template.write_text(self._default_markdown_template())

        html_template = template_dir / "profile.html.j2"
        if not html_template.exists():
            html_template.write_text(self._default_html_template())

    def _default_markdown_template(self) -> str:
        return (
            "# IoT Engineering Profile: {{ profile.username }}\n\n"
            "*Generated: {{ profile.generated_at.strftime('%Y-%m-%d %H:%M') }}*\n\n"
            "## Summary\n\n"
            "{{ profile.narrative_summary }}\n\n"
            "---\n\n"
            "## 📊 Repository Overview\n\n"
            "- **Total Repositories Analyzed**: {{ profile.total_repos_analyzed }}\n"
            "- **IoT-Related Repositories**: {{ profile.iot_repos_count }}\n"
            "- **ESPHome Configurations**: {{ profile.esphome_analyses|length }}\n"
            "- **D-Bus Services**: {{ profile.dbus_analyses|length }}\n\n"
            "### Complexity Distribution\n\n"
            "{% for level, count in profile.complexity_distribution.items() %}\n"
            "- **{{ level.value.capitalize() }}**: {{ count }}\n"
            "{% endfor %}\n\n"
            "---\n\n"
            "## 🎯 Focus Areas\n\n"
            "{% for area, score in profile.focus_areas.items() %}\n"
            "### {{ area.value.replace('_', ' ').title() }}: {{ \"%.1f\"|format(score * 100) }}%\n\n"
            "![{{ area.value }}]({{ area.value }}_chart.png)\n"
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
            "- **Focus Areas**: {{ [a.value for a in esphome.focus_areas]|join(', ') }}\n\n"
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
            "- **Focus Areas**: {{ [a.value for a in dbus.focus_areas]|join(', ') }}\n\n"
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
        return "".join(
            [
                "<!DOCTYPE html>\n",
                '<html lang="en">\n',
                "<head>\n",
                '    <meta charset="UTF-8">\n',
                '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n',
                "    <title>IoT Engineering Profile: {{ profile.username }}</title>\n",
                '    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>\n',
                "    <style>\n",
                "        * { box-sizing: border-box; margin: 0; padding: 0; }\n",
                "        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', ",
                "Roboto, sans-serif; line-height: 1.6; color: #1a1a2e; background: #f8f9fa; }\n",
                "        .container { max-width: 1000px; margin: 0 auto; padding: 2rem; }\n",
                "        header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); ",
                "color: white; padding: 3rem 2rem; border-radius: 16px; margin-bottom: 2rem; ",
                "text-align: center; }\n",
                "        header h1 { font-size: 2.5rem; margin-bottom: 0.5rem; }\n",
                "        header p { opacity: 0.9; }\n",
                "        section { background: white; border-radius: 12px; padding: 2rem; ",
                "margin-bottom: 2rem; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }\n",
                "        h2 { color: #667eea; margin-bottom: 1rem; padding-bottom: 0.5rem; ",
                "border-bottom: 2px solid #eef; }\n",
                "        h3 { color: #333; margin: 1.5rem 0 0.5rem; }\n",
                "        table { width: 100%; border-collapse: collapse; margin: 1rem 0; }\n",
                "        th, td { padding: 0.75rem; text-align: left; border-bottom: 1px solid #eee; }\n",
                "        th { background: #f8f9fa; font-weight: 600; }\n",
                "        tr:hover { background: #fafbff; }\n",
                "        .badge { display: inline-block; padding: 0.25rem 0.75rem; ",
                "border-radius: 9999px; font-size: 0.8rem; font-weight: 500; margin: 0.25rem; }\n",
                "        .badge-primary { background: #eef; color: #667eea; }\n",
                "        .badge-success { background: #d4edda; color: #155724; }\n",
                "        .badge-warning { background: #fff3cd; color: #856404; }\n",
                "        .badge-danger { background: #f8d7da; color: #721c24; }\n",
                "        .chart-container { height: 300px; margin: 1rem 0; }\n",
                "        .repo-card { border: 1px solid #eee; border-radius: 8px; padding: 1rem; ",
                "margin: 1rem 0; }\n",
                "        .repo-card h4 { color: #667eea; }\n",
                "        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, ",
                "minmax(150px, 1fr)); gap: 1rem; margin: 1rem 0; }\n",
                "        .stat-card { background: #f8f9fa; padding: 1rem; border-radius: 8px; ",
                "text-align: center; }\n",
                "        .stat-value { font-size: 2rem; font-weight: 700; color: #667eea; }\n",
                "        .stat-label { font-size: 0.9rem; color: #666; }\n",
                "        .skills-table th:nth-child(3), .skills-table td:nth-child(3) { ",
                "text-align: center; }\n",
                "        .skill-bar { height: 6px; background: #eee; border-radius: 3px; ",
                "overflow: hidden; }\n",
                "        .skill-bar-fill { height: 100%; background: linear-gradient(90deg, ",
                "#667eea, #764ba2); border-radius: 3px; }\n",
                "    </style>\n",
                "</head>\n",
                "<body>\n",
                '    <div class="container">\n',
                "        <header>\n",
                "            <h1>IoT Engineering Profile</h1>\n",
                "            <p>{{ profile.username }} • Generated ",
                "{{ profile.generated_at.strftime('%B %d, %Y') }}</p>\n",
                "        </header>\n\n",
                "        <section>\n",
                "            <h2>\U0001f4ca Overview</h2>\n",
                '            <div class="stats-grid">\n',
                '                <div class="stat-card">\n',
                '                    <div class="stat-value">{{ profile.total_repos_analyzed }}</div>\n',
                '                    <div class="stat-label">Total Analyzed</div>\n',
                "                </div>\n",
                '                <div class="stat-card">\n',
                '                    <div class="stat-value">{{ profile.iot_repos_count }}</div>\n',
                '                    <div class="stat-label">IoT Repositories</div>\n',
                "                </div>\n",
                '                <div class="stat-card">\n',
                '                    <div class="stat-value">{{ profile.esphome_analyses|length }}</div>\n',
                '                    <div class="stat-label">ESPHome Configs</div>\n',
                "                </div>\n",
                '                <div class="stat-card">\n',
                '                    <div class="stat-value">{{ profile.dbus_analyses|length }}</div>\n',
                '                    <div class="stat-label">D-Bus Services</div>\n',
                "                </div>\n",
                "            </div>\n",
                "        </section>\n\n",
                "        <section>\n",
                "            <h2>\U0001f3af Focus Areas</h2>\n",
                '            <div id="focus-chart" class="chart-container"></div>\n',
                '            <div class="focus-details">\n',
                "                {% for area, score in profile.focus_areas.items() %}\n",
                "                <span class=\"badge badge-primary\">{{ area.value.replace('_', ' ').title() }}: ",
                '{{ "%.0f"|format(score * 100) }}%</span>\n',
                "                {% endfor %}\n",
                "            </div>\n",
                "        </section>\n\n",
                "        <section>\n",
                "            <h2>\U0001f4c8 Complexity Distribution</h2>\n",
                '            <div id="complexity-chart" class="chart-container"></div>\n',
                "        </section>\n\n",
                "        <section>\n",
                "            <h2>\U0001f6e0 Skills Assessment</h2>\n",
                '            <table class="skills-table">\n',
                "                <thead>\n",
                "                    <tr>\n",
                "                        <th>Skill</th>\n",
                "                        <th>Category</th>\n",
                "                        <th>Proficiency</th>\n",
                "                        <th>Confidence</th>\n",
                "                        <th>Evidence</th>\n",
                "                    </tr>\n",
                "                </thead>\n",
                "                <tbody>\n",
                "                    {% for skill in profile.skills|sort(attribute='proficiency', reverse=True) %}\n",
                "                    <tr>\n",
                "                        <td><strong>{{ skill.name }}</strong></td>\n",
                '                        <td><span class="badge badge-primary">{{ skill.category }}</span></td>\n',
                "                        <td>\n",
                '                            <div class="skill-bar">\n',
                '                                <div class="skill-bar-fill" style="width: ',
                '{{ skill.proficiency * 10 }}%"></div>\n',
                "                            </div>\n",
                "                            <small>{{ skill.proficiency }}/10</small>\n",
                "                        </td>\n",
                '                        <td>{{ "%.0f"|format(skill.confidence * 100) }}%</td>\n',
                "                        <td>{{ skill.evidence|join(', ') }}</td>\n",
                "                    </tr>\n",
                "                    {% endfor %}\n",
                "                </tbody>\n",
                "            </table>\n",
                "        </section>\n\n",
                "        <section>\n",
                "            <h2>\U0001f4aa Key Strengths</h2>\n",
                "            <ul>\n",
                "                {% for strength in profile.key_strengths %}\n",
                "                <li>{{ strength }}</li>\n",
                "                {% endfor %}\n",
                "            </ul>\n",
                "        </section>\n\n",
                "        <section>\n",
                "            <h2>\U0001f4c8 Growth Areas</h2>\n",
                "            <ul>\n",
                "                {% for area in profile.growth_areas %}\n",
                "                <li>{{ area }}</li>\n",
                "                {% endfor %}\n",
                "            </ul>\n",
                "        </section>\n\n",
                "        <section>\n",
                "            <h2>\U0001f3c6 Top Repositories</h2>\n",
                "            {% for repo in profile.top_repositories %}\n",
                '            <div class="repo-card">\n',
                "                <h4>{{ repo.name }}</h4>\n",
                "                <p>{{ repo.description or 'No description' }}</p>\n",
                '                <div style="display: flex; gap: 1rem; flex-wrap: wrap; margin-top: 0.5rem;">\n',
                "                    <span class=\"badge badge-primary\">{{ repo.language or 'N/A' }}</span>\n",
                '                    <span class="badge badge-success">{{ repo.complexity.value }}</span>\n',
                '                    <span class="badge badge-warning">{{ "%.2f"|format(repo.iot_score) }} ',
                "IoT Score</span>\n",
                '                    <span class="badge">{{ repo.stars }}⭐</span>\n',
                "                </div>\n",
                '                <p style="margin-top: 0.5rem; color: #666;">Topics: ',
                "{{ repo.topics|join(', ') }}</p>\n",
                "            </div>\n",
                "            {% endfor %}\n",
                "        </section>\n\n",
                "        <section>\n",
                "            <h2>\U0001f527 ESPHome Configurations</h2>\n",
                "            {% for esphome in profile.esphome_analyses %}\n",
                '            <div class="repo-card">\n',
                "                <h4>{{ esphome.file_path }}</h4>\n",
                "                <p>Devices: {{ esphome.devices|join(', ') }}</p>\n",
                "                <p>Components: {{ esphome.components|length }} | Complexity: ",
                '<span class="badge badge-success">{{ esphome.complexity.value }}</span></p>\n',
                "                <p>Focus: {{ [a.value for a in esphome.focus_areas]|join(', ') }}</p>\n",
                "            </div>\n",
                "            {% endfor %}\n",
                "        </section>\n\n",
                "        <section>\n",
                "            <h2>\U0001f4e1 D-Bus Services</h2>\n",
                "            {% for dbus in profile.dbus_analyses %}\n",
                '            <div class="repo-card">\n',
                "                <h4>{{ dbus.service_name }}</h4>\n",
                "                <p>Interfaces: {{ dbus.interfaces|length }} | Methods: ",
                "{{ dbus.interfaces|map(attribute='methods')|map('length')|sum }} | Signals: ",
                "{{ dbus.interfaces|map(attribute='signals')|map('length')|sum }}</p>\n",
                '                <p>Complexity: <span class="badge badge-success">{{ dbus.complexity.value }}',
                "</span> | Focus: {{ [a.value for a in dbus.focus_areas]|join(', ') }}</p>\n",
                "            </div>\n",
                "            {% endfor %}\n",
                "        </section>\n",
                "    </div>\n\n",
                "    <script>\n",
                "        // Focus Areas Radar Chart\n",
                "        const focusData = [{\n",
                "            type: 'scatterpolar',\n",
                "            r: [{{ profile.focus_areas.values()|map('round')|join(', ') }}],\n",
                "            theta: [{{ profile.focus_areas.keys()|map('replace', '_', ' ')|map('title')",
                "|map('escapejs')|join(', ') }}],\n",
                "            fill: 'toself',\n",
                "            name: 'Focus Areas',\n",
                "            line: { color: '#667eea' }\n",
                "        }];\n",
                "        Plotly.newPlot('focus-chart', focusData, {\n",
                "            polar: { radialaxis: { visible: true, range: [0, 100] } },\n",
                "            showlegend: false,\n",
                "            margin: { t: 20, b: 20, l: 20, r: 20 }\n",
                "        });\n\n",
                "        // Complexity Distribution Pie Chart\n",
                "        const complexityLabels = [{{ profile.complexity_distribution.keys()|map",
                "('value')|map('capitalize')|map('escapejs')|join(', ') }}];\n",
                "        const complexityValues = [{{ profile.complexity_distribution.values()|join",
                "(', ') }}];\n",
                "        Plotly.newPlot('complexity-chart', [{\n",
                "            values: complexityValues,\n",
                "            labels: complexityLabels,\n",
                "            type: 'pie',\n",
                "            hole: 0.4,\n",
                "            marker: { colors: ['#28a745', '#ffc107', '#fd7e14', '#dc3545'] }\n",
                "        }], {\n",
                "            showlegend: true,\n",
                "            margin: { t: 20, b: 20, l: 20, r: 20 }\n",
                "        });\n",
                "    </script>\n",
                "</body>\n",
                "</html>\n",
            ]
        )

    def render_markdown(self, profile: EngineeringProfile, output_path: Path) -> None:
        """Render profile to Markdown."""
        template = self.env.get_template("profile.md.j2")
        content = template.render(profile=profile)
        output_path.write_text(content, encoding="utf-8")

    def render_html(self, profile: EngineeringProfile, output_path: Path) -> None:
        """Render profile to HTML with embedded charts."""
        template = self.env.get_template("profile.html.j2")
        content = template.render(profile=profile)
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
        chart_paths = renderer.generate_charts(profile, output_dir / "charts")
        results.update(chart_paths)

    return results


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
    }
