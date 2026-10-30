"""Offline application contracts for scanning, analysis and published profile formats."""

import json
import shutil
from datetime import datetime
from pathlib import Path
from tempfile import mkdtemp
from types import SimpleNamespace
from typing import Any
from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch

from iot_profile_builder.analyzers.dbus_analyzer import DBusAnalyzer
from iot_profile_builder.analyzers.esphome_analyzer import ESPHomeAnalyzer
from iot_profile_builder.cli import IoTProfileBuilder
from iot_profile_builder.generator.profile_generator import (
    GenerationError,
    ProfileGenerator,
    generate_heuristic_profile,
)
from iot_profile_builder.models import ComplexityLevel, FocusArea, RepositoryMetrics, ScanConfig
from iot_profile_builder.output import renderer
from iot_profile_builder.scanner.github_scanner import GitHubScanner, ScanError


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
        # Unit-only fake client has no PyGithub transport; real TLS is tested separately.
        self.enterContext(
            patch(
                "iot_profile_builder.scanner.github_scanner.enforce_github_tls",
                lambda client: client,
            )
        )
        self.enterContext(
            patch(
                "iot_profile_builder.scanner.github_scanner.Github",
                lambda **_kwargs: self.github_client,
            )
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
        assert profile.generated_at.isoformat().endswith("+00:00")
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

    def test_repository_totals_do_not_count_nested_analysis_records(self) -> None:
        """Both generators distinguish scanned repositories from per-file evidence."""
        repos = [repository_metrics()]
        esphome = [
            ESPHomeAnalyzer().analyze_content(
                "esphome:\n  name: battery\nesp32:\n  board: esp32dev\n", path
            )
            for path in ("devices/battery.yaml", "devices/backup.yaml")
        ]
        dbus = [
            DBusAnalyzer().analyze_content(
                "service = VeDbusService('com.victronenergy.battery.demo')\n"
                "service.add_path('/Soc', 75)\n",
                "service.py",
            )
        ]
        self.enterContext(patch("anthropic.Anthropic"))
        self.enterContext(
            patch.object(
                ProfileGenerator,
                "_call_llm",
                return_value={"skills": [], "narrative_summary": "Repository evidence."},
            )
        )
        generator = ProfileGenerator(ScanConfig(username="owner"))
        cases: list[tuple[dict[str, Any], int]] = [({"total_repos": 7}, 7), ({}, 1)]
        cases.extend(
            ({"total_repos": invalid}, 1) for invalid in (None, True, False, 0, -1, 7.0, "7")
        )
        for stats, expected in cases:
            with self.subTest(stats=stats):
                profiles = [
                    generator.generate(repos, esphome, dbus, stats),
                    generate_heuristic_profile(repos, esphome, dbus, stats, "owner"),
                ]
                for profile in profiles:
                    self.assertIs(type(profile.total_repos_analyzed), int)
                    self.assertEqual(profile.total_repos_analyzed, expected)
                    self.assertEqual(profile.iot_repos_count, 1)
                    self.assertEqual(len(profile.esphome_analyses), 2)
                    self.assertEqual(len(profile.dbus_analyses), 1)
                    self.assertEqual(sum(profile.complexity_distribution.values()), 4)
                    self.assertEqual(
                        renderer._profile_to_dict(profile)["total_repos_analyzed"], expected
                    )

    def test_llm_failure_preserves_repository_evidence(self) -> None:
        """Provider errors degrade to a report without discarding scanned projects."""
        metrics = repository_metrics()
        self.enterContext(
            patch.dict("os.environ", {"ANTHROPIC_API_KEY": "", "ANTHROPIC_AUTH_TOKEN": ""})
        )
        client = MagicMock()
        client.messages.stream.side_effect = RuntimeError("provider unavailable")
        self.enterContext(patch("anthropic.Anthropic", lambda **_kwargs: client))
        profile = ProfileGenerator(ScanConfig(username="owner")).generate([metrics], [], [], {})
        assert profile.generated_at.isoformat().endswith("+00:00")
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
        llm_constructor = self.enterContext(
            patch("anthropic.Anthropic", side_effect=AssertionError("LLM must stay disabled"))
        )
        builder = IoTProfileBuilder(
            ScanConfig(username="owner", include_orgs=[], analyze_esphome=False, analyze_dbus=False)
        )
        output = await builder.run(tmp_path / "outputs", use_llm=False)
        llm_constructor.assert_not_called()
        assert output.is_file()
        assert "mqtt-battery" in output.read_text()
        report = json.loads(output.with_suffix(".json").read_text())
        assert report["generated_at"].endswith("+00:00")
        assert report["github_stats"]["scanned_at"].endswith("+00:00")
        assert report["top_repositories"][0]["full_name"] == "owner/mqtt-battery"
        assert report["iot_repos_count"] == 1
        html = output.with_suffix(".html").read_text()
        assert "<html" in html.lower()
        assert '<script src="https://cdn.plot.ly' not in html
        assert 'class="score-track"' in html
        assert "plotly.js v" not in html

    async def test_public_scan_reuses_topics_repository_head_tree_and_content(self) -> None:
        """Both analyzers reuse one public snapshot without repeated metadata requests."""
        repo = github_repo("owner/mqtt")
        repo.raw_data = {"topics": ["mqtt", "battery"]}
        repo.get_branch.return_value.commit.sha = "a" * 40
        repo.get_git_tree.return_value = SimpleNamespace(
            truncated=False,
            tree=[
                SimpleNamespace(path=path, type="blob", size=12)
                for path in ["device.yaml", "service.py"]
            ],
        )
        repo.get_contents.return_value = SimpleNamespace(decoded_content=b"mqtt source")
        self.github_client.get_user.return_value.get_repos.return_value = [repo]
        scanner = GitHubScanner(ScanConfig(username="owner", include_orgs=[]))
        await scanner.scan()
        yaml = await scanner.list_repo_files("owner/mqtt", suffixes=(".yaml",))
        python = await scanner.list_repo_files("owner/mqtt", suffixes=(".py",))
        assert [item["path"] for item in yaml] == ["device.yaml"]
        assert [item["path"] for item in python] == ["service.py"]
        assert await scanner.get_file_content("owner/mqtt", "device.yaml") == "mqtt source"
        assert await scanner.get_file_content("mqtt", "device.yaml") == "mqtt source"
        self.github_client.get_repo.assert_not_called()
        repo.get_topics.assert_not_called()
        repo.get_branch.assert_called_once()
        repo.get_git_tree.assert_called_once_with("a" * 40, recursive=True)
        repo.get_contents.assert_called_once_with("device.yaml", ref="a" * 40)

    async def test_new_scan_drops_prior_snapshot_and_topic_cache(self) -> None:
        """A second run must not attach a fresh date to cached old evidence."""
        repo = github_repo("owner/mqtt")
        repo.raw_data = {}
        repo.get_branch.return_value.commit.sha = "a" * 40
        repo.get_contents.return_value = SimpleNamespace(decoded_content=b"old source")
        self.github_client.get_user.return_value.get_repos.return_value = [repo]
        scanner = GitHubScanner(ScanConfig(username="owner", include_orgs=[]))
        await scanner.scan()
        assert await scanner.get_file_content("mqtt", "device.yaml") == "old source"
        repo.get_topics.assert_called_once()
        repo.get_branch.return_value.commit.sha = "b" * 40
        repo.get_contents.return_value = SimpleNamespace(decoded_content=b"new source")
        await scanner.scan()
        assert await scanner.get_file_content("mqtt", "device.yaml") == "new source"
        assert repo.get_topics.call_count == 2
        assert repo.get_branch.call_count == 2
        repo.get_contents.assert_called_with("device.yaml", ref="b" * 40)

    async def test_all_owners_scanned_without_hidden_global_cutoff(self) -> None:
        """The per-owner limit must not silently discard the third configured owner."""
        self.github_client.get_user.return_value.get_repos.return_value = [
            github_repo("owner/mqtt")
        ]
        self.github_client.get_organization.side_effect = [
            SimpleNamespace(get_repos=lambda **_kwargs: [github_repo("one/mqtt")]),
            SimpleNamespace(get_repos=lambda **_kwargs: [github_repo("two/mqtt")]),
            SimpleNamespace(get_repos=lambda **_kwargs: [github_repo("three/mqtt")]),
        ]
        scanner = GitHubScanner(
            ScanConfig(
                username="owner",
                include_orgs=["one", "two", "three"],
                max_repos=1,
                strict_scan=True,
            )
        )
        result = await scanner.scan()
        assert result.total_scanned == 4
        assert len(result.repositories) == 4
        assert not result.errors

    async def test_strict_scan_rejects_owner_truncation_and_api_failures(self) -> None:
        """Partial enumeration and missing metadata cannot become a published profile."""
        for case in ("limit", "organization", "languages"):
            with self.subTest(case=case):
                repo = github_repo("owner/mqtt")
                self.github_client.get_user.return_value.get_repos.return_value = [repo]
                self.github_client.get_organization.side_effect = None
                config = ScanConfig(username="owner", include_orgs=[], strict_scan=True)
                if case == "limit":
                    config.max_repos = 1
                    self.github_client.get_user.return_value.get_repos.return_value.append(
                        github_repo("owner/second")
                    )
                elif case == "organization":
                    config.include_orgs = ["unavailable"]
                    self.github_client.get_organization.side_effect = RuntimeError(
                        "API unavailable"
                    )
                else:
                    repo.get_languages.side_effect = RuntimeError("API unavailable")
                with self.assertRaises(ScanError):
                    await GitHubScanner(config).scan()

    async def test_strict_scan_rejects_incomplete_tree_and_failed_file_reads(self) -> None:
        """Every evidence request contributes to strict scan integrity."""
        for case in ("tree-error", "tree-truncated", "file-error", "private"):
            with self.subTest(case=case):
                repo = github_repo("owner/mqtt", private=case == "private")
                repo.get_branch.return_value.commit.sha = "a" * 40
                repo.get_git_tree.return_value = SimpleNamespace(truncated=True, tree=[])
                if case == "tree-error":
                    repo.get_git_tree.side_effect = RuntimeError("tree unavailable")
                repo.get_contents.side_effect = RuntimeError("file unavailable")
                self.github_client.get_repo.return_value = repo
                scanner = GitHubScanner(ScanConfig(username="owner", strict_scan=True))
                with self.assertRaises(ScanError):
                    if case.startswith("tree"):
                        await scanner.list_repo_files("mqtt")
                    else:
                        await scanner.get_file_content("mqtt", "device.yaml")
                if case == "private":
                    repo.get_contents.assert_not_called()

    async def test_strict_pipeline_writes_nothing_after_analysis_exception(self) -> None:
        """A failed analyzer cannot drop evidence from a fresh publication."""
        repo = github_repo("owner/esphome")
        repo.get_branch.return_value.commit.sha = "a" * 40
        repo.get_git_tree.return_value = SimpleNamespace(
            truncated=False, tree=[SimpleNamespace(path="device.yaml", type="blob", size=32)]
        )
        repo.get_contents.return_value = SimpleNamespace(
            decoded_content=b"esphome:\n  name: node\n"
        )
        self.github_client.get_user.return_value.get_repos.return_value = [repo]
        builder = IoTProfileBuilder(
            ScanConfig(
                username="owner",
                include_orgs=[],
                strict_scan=True,
                analyze_dbus=False,
            )
        )
        destination = self.tmp_path / "strict-output"
        with (
            patch.object(
                builder.esphome_analyzer, "analyze_content", side_effect=ValueError("bad input")
            ),
            self.assertRaises(ScanError),
        ):
            await builder.run(destination, use_llm=False)
        assert not destination.exists()

    async def test_strict_pipeline_writes_nothing_for_empty_scan(self) -> None:
        """An empty report must not replace an existing published profile."""
        self.github_client.get_user.return_value.get_repos.return_value = []
        builder = IoTProfileBuilder(ScanConfig(username="owner", include_orgs=[], strict_scan=True))
        destination = self.tmp_path / "strict-empty"
        with self.assertRaises(ScanError):
            await builder.run(destination, use_llm=False)
        assert not destination.exists()

    async def test_strict_pipeline_writes_nothing_after_model_failure(self) -> None:
        """An unavailable provider cannot replace the last valid published report."""
        self.github_client.get_user.return_value.get_repos.return_value = [
            github_repo("owner/mqtt")
        ]
        client = MagicMock()
        client.messages.stream.side_effect = TimeoutError("private-provider-detail")
        builder = IoTProfileBuilder(
            ScanConfig(
                username="owner",
                include_orgs=[],
                strict_scan=True,
                analyze_dbus=False,
                analyze_esphome=False,
            )
        )
        destination = self.tmp_path / "strict-model-failure"
        with (
            patch("anthropic.Anthropic", return_value=client),
            self.assertRaises(GenerationError),
        ):
            await builder.run(destination, use_llm=True)
        assert not destination.exists()
