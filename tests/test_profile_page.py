"""Published profiles remain readable, linked and complete without third-party assets."""

from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from iot_profile_builder.models import (
    ComplexityLevel,
    DBusAnalysis,
    EngineeringProfile,
    ESPHomeAnalysis,
    ESPHomeComponent,
    FocusArea,
    RepositoryMetrics,
    SkillAssessment,
)
from iot_profile_builder.output.renderer import ProfileRenderer


class PageStructure(HTMLParser):
    def __init__(self, html: str) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.links: list[str] = []
        self.dependencies: list[str] = []
        self.repository_count = 0
        self.feed(html)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(str(values["id"]))
        if tag == "a" and values.get("href"):
            self.links.append(str(values["href"]))
        if tag in {"script", "link", "img"}:
            self.dependencies.extend(str(values[key]) for key in ("src", "href") if values.get(key))
        if tag == "article" and values.get("class") == "repo":
            self.repository_count += 1


class ProfilePageTests(TestCase):
    def setUp(self) -> None:
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.output = Path(self.temporary.name) / "profile.html"
        self.profile = EngineeringProfile(
            username="fixture",
            generated_at=datetime(2026, 1, 2),
            total_repos_analyzed=3,
            iot_repos_count=1,
            focus_areas={FocusArea.ENERGY_MANAGEMENT: 0.8},
            complexity_distribution={ComplexityLevel.MEDIUM: 2, ComplexityLevel.LOW: 1},
            skills=[SkillAssessment("Energy systems", "energy_systems", 8, ["meter-bridge"], 0.7)],
            narrative_summary="First source paragraph.\n\nSecond source paragraph.",
            top_repositories=[
                RepositoryMetrics(
                    name="meter-bridge",
                    full_name="example-org/meter-bridge",
                    description="A bridge for meter telemetry.",
                    stars=2,
                    forks=0,
                    language="Python",
                    topics=["mqtt", "meters"],
                    is_fork=False,
                    created_at=datetime(2025, 1, 1),
                    updated_at=datetime(2026, 1, 1),
                    size_kb=12,
                    complexity=ComplexityLevel.MEDIUM,
                    focus_areas=[FocusArea.ENERGY_MANAGEMENT],
                    iot_score=0.9,
                )
            ],
            esphome_analyses=[
                ESPHomeAnalysis(
                    file_path="devices/meter.yaml",
                    devices=["ESP32"],
                    components=[ESPHomeComponent("sensor", "template", "Watts", {}, ["mqtt"])],
                    custom_components=["local_meter"],
                    external_libs=[],
                    complexity=ComplexityLevel.LOW,
                    focus_areas=[FocusArea.ENERGY_MANAGEMENT],
                )
            ],
            dbus_analyses=[
                DBusAnalysis(
                    service_name="com.example.meter",
                    interfaces=[],
                    object_paths=["/Ac/Power"],
                    complexity=ComplexityLevel.LOW,
                    focus_areas=[FocusArea.ENERGY_MANAGEMENT],
                )
            ],
        )

    def render(self) -> str:
        ProfileRenderer().render_html(self.profile, self.output)
        return self.output.read_text()

    def test_portable_document_contains_all_chart_values_without_network_dependencies(self) -> None:
        html = self.render()
        page = PageStructure(html)
        self.assertEqual(page.dependencies, [])
        for content in ("80%", "70% assessment confidence", "3 classified repositories"):
            self.assertIn(content, html)
        self.assertNotIn("Plotly", html)
        self.assertNotIn("<canvas", html)
        self.assertIn("January 02, 2026", html)
        self.assertIn("not independent proficiency ratings or deployment verification", html)

    def test_navigation_and_evidence_use_real_targets(self) -> None:
        page = PageStructure(self.render())
        self.assertEqual(len(page.ids), len(set(page.ids)))
        for link in page.links:
            if link.startswith("#"):
                self.assertIn(link[1:], page.ids)
        self.assertEqual(page.repository_count, 1)
        # Both the repository card and the matching skill evidence use the actual owner.
        self.assertEqual(page.links.count("https://github.com/example-org/meter-bridge"), 2)
        self.assertNotIn("https://github.com/fixture/meter-bridge", page.links)

    def test_existing_metadata_and_source_records_are_preserved(self) -> None:
        html = self.render()
        for content in (
            "First source paragraph.",
            "Second source paragraph.",
            "devices/meter.yaml",
            "ESP32",
            "/ template",
            ": Watts",
            "local_meter",
            "com.example.meter",
            "/Ac/Power",
        ):
            self.assertIn(content, html)
        self.assertIn('<details class="source-row">', html)
        self.assertIn('<div class="filters" id="repository-filters" hidden>', html)
        self.assertNotIn('<article class="repo" hidden', html)

    def test_repository_metadata_is_escaped_in_content_attributes_and_urls(self) -> None:
        repo = self.profile.top_repositories[0]
        repo.description = '<script>alert("description")</script>'
        repo.language = '" onmouseover="invalid'
        repo.topics = ["<img src=x onerror=invalid>"]
        repo.full_name = 'example-org/repo?x="unsafe"'
        html = self.render()
        self.assertNotIn(repo.description, html)
        self.assertNotIn("<img src=x", html)
        self.assertNotIn('data-language="" onmouseover=', html)
        self.assertIn("&lt;script&gt;", html)
        page = PageStructure(html)
        self.assertIn("https://github.com/example-org/repo%3Fx%3D%22unsafe%22", page.links)

    def test_empty_profile_has_useful_fallbacks_and_valid_navigation(self) -> None:
        self.profile.skills = []
        self.profile.top_repositories = []
        self.profile.focus_areas = {}
        self.profile.complexity_distribution = {}
        self.profile.esphome_analyses = []
        self.profile.dbus_analyses = []
        self.profile.narrative_summary = ""
        html = self.render()
        for content in (
            "No focus scores",
            "No complexity data",
            "No repositories were retained",
            "No ESPHome records",
            "No D-Bus records",
        ):
            self.assertIn(content, html)
        self.assertNotIn("nan", html)
        self.assertEqual(PageStructure(html).repository_count, 0)
