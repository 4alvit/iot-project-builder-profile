"""Offline application contracts for scanning, analysis and published profile formats."""

import json
import shutil
from datetime import datetime
from pathlib import Path
from tempfile import mkdtemp
from types import SimpleNamespace
from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch

from iot_profile_builder.analyzers.dbus_analyzer import DBusAnalyzer
from iot_profile_builder.analyzers.esphome_analyzer import ESPHomeAnalyzer
from iot_profile_builder.cli import IoTProfileBuilder
from iot_profile_builder.generator.profile_generator import (
    ProfileGenerator,
    generate_heuristic_profile,
)
from iot_profile_builder.models import ComplexityLevel, FocusArea, RepositoryMetrics, ScanConfig
from iot_profile_builder.output import renderer
from iot_profile_builder.scanner.github_scanner import GitHubScanner


def github_repo(full_name: str, *, private: bool = False, fork: bool = False) -> MagicMock:
    """Represent external GitHub metadata without replacing application scoring."""
    repo = MagicMock()
    repo.full_name = full_name
    repo.name = full_name.split("/")[-1]
    repo.description = "ESPHome MQTT battery solar energy monitoring for Home Assistant"
    repo.language = "Python"
    repo.private = private
    repo.fork = fork
    repo.stargazers_count = 0
    repo.forks_count = 0
    repo.size = 1500
    repo.created_at = datetime(2020, 1, 1)
    repo.updated_at = datetime.now()
    repo.get_topics.return_value = ["esphome", "mqtt", "battery", "solar"]
    repo.get_languages.return_value = {"Python": 100}
    return repo


def repository_metrics() -> RepositoryMetrics:
    """A public battery project with known evidence for profile aggregation."""
    return RepositoryMetrics(
        name="mqtt-battery",
        full_name="example/mqtt-battery",
        description="ESPHome MQTT battery",
        stars=0,
        forks=0,
        language="Python",
        topics=["esphome", "battery"],
        is_fork=False,
        created_at=datetime(2020, 1, 1),
        updated_at=datetime(2026, 1, 1),
        size_kb=100,
        complexity=ComplexityLevel.MEDIUM,
        focus_areas=[FocusArea.BMS],
        iot_score=0.8,
    )


class ApplicationTests(IsolatedAsyncioTestCase):
    """Exercise profile behavior without network or LLM credentials."""

    def setUp(self) -> None:
        """Isolate filesystem outputs and replace only the external GitHub client."""
        temporary = mkdtemp()
        self.addCleanup(shutil.rmtree, temporary)
        self.tmp_path = Path(temporary)
        self.github_client = MagicMock()
        self.enterContext(
            patch("iot_profile_builder.scanner.github_scanner.Github", lambda: self.github_client)
        )

    async def test_scan_preserves_org_owners_and_excludes_private_forks_duplicates(self) -> None:
        """Only distinct public originals become profile evidence."""
        github_client = self.github_client
        public = github_repo("owner/mqtt-battery")
        org_repo = github_repo("sensors/esphome")
        github_client.get_user.return_value.get_repos.return_value = [
            public,
            github_repo("owner/private", private=True),
            github_repo("owner/fork", fork=True),
        ]
        github_client.get_organization.return_value.get_repos.return_value = [public, org_repo]
        scan = await GitHubScanner(ScanConfig(username="owner", include_orgs=["sensors"])).scan()
        assert {repo.full_name for repo in scan.repositories} == {
            public.full_name,
            org_repo.full_name,
        }
        assert scan.iot_repos == 2
        assert scan.total_scanned == 4
        assert scan.errors == []
        github_client.get_organization.return_value.get_repos.assert_called_once_with(type="public")

    async def test_scan_org_failure_keeps_user_results(self) -> None:
        """One inaccessible organization must not erase successfully scanned evidence."""
        github_client = self.github_client
        github_client.get_user.return_value.get_repos.return_value = [github_repo("owner/mqtt")]
        github_client.get_organization.side_effect = RuntimeError("organization unavailable")
        scan = await GitHubScanner(ScanConfig(username="owner", include_orgs=["missing"])).scan()
        assert [repo.full_name for repo in scan.repositories] == ["owner/mqtt"]
        assert len(scan.errors) == 1
        assert "org:missing" in scan.errors[0]

    async def test_scan_explicitly_includes_forks(self) -> None:
        """The operator's include-forks setting remains effective."""
        github_client = self.github_client
        github_client.get_user.return_value.get_repos.return_value = [
            github_repo("owner/mqtt", fork=True)
        ]
        scan = await GitHubScanner(
            ScanConfig(username="owner", include_orgs=[], include_forks=True)
        ).scan()
        assert scan.iot_repos == 1
        assert scan.repositories[0].is_fork

    async def test_recursive_files_keep_templates_and_skip_dependencies(self) -> None:
        """Find nested device/template sources without analyzing vendored environments."""
        github_client = self.github_client
        repo = github_client.get_repo.return_value
        repo.get_git_tree.return_value.tree = [
            SimpleNamespace(path=path, type="blob", size=12)
            for path in [
                ".venv/noise.py",
                "vendor/driver.py",
                "templates/service.py.j2",
                "src/bridge.py",
            ]
        ]
        files = await GitHubScanner(ScanConfig(username="owner")).list_repo_files(
            "sensors/bridge", suffixes=(".py",), max_files=1
        )
        assert [entry["path"] for entry in files] == ["templates/service.py.j2"]
        github_client.get_repo.assert_called_once_with("sensors/bridge")

    async def test_file_fetch_rejects_directory(self) -> None:
        """A directory response is not interpreted as file source."""
        github_client = self.github_client
        github_client.get_repo.return_value.get_contents.return_value = []
        assert (
            await GitHubScanner(ScanConfig(username="owner")).get_file_content("repo", "dir")
            is None
        )
        github_client.get_repo.assert_called_once_with("owner/repo")

    def test_esphome_custom_tags_and_component_evidence(self) -> None:
        """ESPHome secret/lambda tags are data, and nested component evidence survives."""
        analysis = ESPHomeAnalyzer().analyze_content(
            (
                "esphome:\n"
                "  name: battery\n"
                "  libraries: [Wire]\n"
                "esp32:\n"
                "  board: esp32dev\n"
                "wifi:\n"
                "  password: !secret wifi_password\n"
                "sensor:\n"
                "  - platform: template\n"
                "    name: Battery voltage\n"
                "    lambda: !lambda return 12.8;\n"
                "mqtt:\n"
                "  broker: broker.example\n"
                "external_components:\n"
                "  - source: local\n"
                "    components: [battery_driver]\n"
            ),
            "devices/battery.yaml",
        )
        assert analysis.devices == ["esp32:esp32dev"]
        sensor = next(component for component in analysis.components if component.type == "sensor")
        assert sensor.name == "Battery voltage"
        assert sensor.config["lambda"] == "return 12.8;"
        assert analysis.custom_components == ["battery_driver"]
        assert analysis.external_libs == ["Wire"]
        assert FocusArea.ENERGY_MANAGEMENT in analysis.focus_areas
        assert FocusArea.NETWORKING in analysis.focus_areas

    def test_non_mapping_or_invalid_yaml_is_an_empty_analysis(self) -> None:
        """Unusable input should be reported as unknown rather than crashing a scan."""
        for content in ["sensor: [", "", "null", "- sensor", "plain text"]:
            with self.subTest(content=content):
                analysis = ESPHomeAnalyzer().analyze_content(content, "invalid.yaml")
                assert analysis.devices == []
                self.assertEqual(analysis.components, [])
                assert analysis.complexity == ComplexityLevel.LOW
                assert analysis.focus_areas == [FocusArea.UNKNOWN]

    def test_vedbus_paths_are_retained_without_decorators(self) -> None:
        """Typical Venus OS services expose add_path properties instead of decorators."""
        analysis = DBusAnalyzer().analyze_content(
            (
                "service = VeDbusService('com.victronenergy.battery.demo')\n"
                "service.add_path('/Soc', 75)\n"
                "service.add_path('/Dc/0/Voltage', 12.8)\n"
            ),
            "service.py.j2",
        )
        assert analysis.service_name == "com.victronenergy.battery.demo"
        assert set(analysis.object_paths) == {"/Soc", "/Dc/0/Voltage"}
        assert {prop["name"] for prop in analysis.interfaces[0].properties} == set(
            analysis.object_paths
        )
        assert FocusArea.BMS in analysis.focus_areas

    def test_dbus_xml_members_are_preserved(self) -> None:
        """Introspection method, signal and property names are actual profile evidence."""
        tmp_path = self.tmp_path
        xml = tmp_path / "battery.xml"
        xml.write_text(
            '<node><interface name="com.victronenergy.battery">\n'
            '<method name="GetValue"/><signal name="PropertiesChanged"/>\n'
            '<property name="Soc" type="d" access="read"/>\n'
            "</interface></node>"
        )
        analysis = DBusAnalyzer().analyze_xml_introspection(xml)
        assert analysis is not None
        interface = analysis.interfaces[0]
        assert interface.methods[0]["name"] == "GetValue"
        assert interface.signals[0]["name"] == "PropertiesChanged"
        assert interface.properties[0]["name"] == "Soc"

    def test_non_dbus_source_is_ignored(self) -> None:
        """An unrelated Python file does not create invented D-Bus evidence."""
        tmp_path = self.tmp_path
        source = tmp_path / "ordinary.py"
        source.write_text("value = 1\n")
        assert DBusAnalyzer().analyze_file(source) is None

    def test_heuristic_profile_ranks_evidence_and_normalizes_focus(self) -> None:
        """A profile carries repository identity and bounded focus/skill scores."""
        metrics = repository_metrics()
        profile = generate_heuristic_profile([metrics], [], [], {"total_repos": 1}, "owner")
        assert profile.iot_repos_count == 1
        assert profile.top_repositories[0].full_name == "example/mqtt-battery"
        assert profile.focus_areas[FocusArea.BMS] == 1.0
        assert all(0 <= score <= 1 for score in profile.focus_areas.values())
        mqtt = next(skill for skill in profile.skills if skill.name == "MQTT")
        assert mqtt.evidence == ["mqtt-battery"]
        assert 1 <= mqtt.proficiency <= 10

    def test_empty_profile_has_no_invented_skills(self) -> None:
        """An empty scan is a valid report and contains no inferred expertise."""
        profile = generate_heuristic_profile([], [], [], {}, "owner")
        self.assertEqual(profile.skills, [])
        assert profile.iot_repos_count == 0
        assert all(score == 0 for score in profile.focus_areas.values())

    def test_llm_failure_preserves_repository_evidence(self) -> None:
        """Provider errors degrade to a report without discarding scanned projects."""
        metrics = repository_metrics()
        self.enterContext(
            patch.dict("os.environ", {"ANTHROPIC_API_KEY": "", "ANTHROPIC_AUTH_TOKEN": ""})
        )
        client = MagicMock()
        client.messages.stream.side_effect = RuntimeError("provider unavailable")
        self.enterContext(patch("anthropic.Anthropic", lambda: client))
        profile = ProfileGenerator(ScanConfig(username="owner")).generate([metrics], [], [], {})
        assert profile.top_repositories == [metrics]
        assert "unavailable" in profile.narrative_summary
        self.assertEqual(profile.skills, [])

    async def test_no_llm_pipeline_writes_readable_outputs_without_credentials(self) -> None:
        """Run the real scanner, heuristic generator and three renderers without API calls."""
        github_client = self.github_client
        tmp_path = self.tmp_path
        self.enterContext(
            patch.dict("os.environ", {"ANTHROPIC_API_KEY": "", "ANTHROPIC_AUTH_TOKEN": ""})
        )
        github_client.get_user.return_value.get_repos.return_value = [
            github_repo("owner/mqtt-battery")
        ]
        self.enterContext(
            patch.object(renderer.ProfileRenderer, "generate_charts", lambda *_args: {})
        )
        original_renderer = renderer.ProfileRenderer
        self.enterContext(
            patch.object(
                renderer, "ProfileRenderer", lambda: original_renderer(tmp_path / "templates")
            )
        )
        builder = IoTProfileBuilder(
            ScanConfig(username="owner", include_orgs=[], analyze_esphome=False, analyze_dbus=False)
        )
        output = await builder.run(tmp_path / "outputs", use_llm=False)
        assert output.is_file()
        assert "mqtt-battery" in output.read_text()
        report = json.loads(output.with_suffix(".json").read_text())
        assert report["top_repositories"][0]["full_name"] == "owner/mqtt-battery"
        assert report["iot_repos_count"] == 1
        assert "<html" in output.with_suffix(".html").read_text().lower()
