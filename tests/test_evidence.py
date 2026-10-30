"""Evidence survives model failures without serializing source configuration."""

import copy
import io
import json
import os
from contextlib import redirect_stdout
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
from unittest import IsolatedAsyncioTestCase, TestCase
from unittest.mock import AsyncMock, MagicMock, patch

from iot_profile_builder import evidence
from iot_profile_builder.cli import IoTProfileBuilder
from iot_profile_builder.evidence import (
    EvidenceError,
    EvidenceSnapshot,
    load_evidence,
    write_evidence,
)
from iot_profile_builder.generator.profile_generator import (
    GenerationError,
    ProfileGenerator,
    generate_heuristic_profile,
)
from iot_profile_builder.models import (
    ComplexityLevel,
    DBusAnalysis,
    DBusInterface,
    ESPHomeAnalysis,
    ESPHomeComponent,
    FocusArea,
    RepositoryMetrics,
    ScanConfig,
)
from iot_profile_builder.scanner.github_scanner import ScanResult
from tests.test_application import repository_metrics


def fixture() -> tuple[
    ScanConfig,
    list[RepositoryMetrics],
    list[ESPHomeAnalysis],
    list[DBusAnalysis],
    dict[str, Any],
]:
    config = ScanConfig(username="example", include_orgs=[], strict_scan=True, token="TOKEN-CANARY")
    repos = [repository_metrics()]
    esp = [
        ESPHomeAnalysis(
            file_path="example/mqtt-battery/device.yaml",
            devices=["ESP32"],
            components=[
                ESPHomeComponent(
                    type="sensor",
                    platform="template",
                    name="Battery",
                    config={"password": "CONFIG-CANARY", "lambda": "RAW-CODE-CANARY"},
                    integrations=["mqtt"],
                )
            ],
            custom_components=["battery"],
            external_libs=["public-library"],
            complexity=ComplexityLevel.MEDIUM,
            focus_areas=[FocusArea.BMS],
        )
    ]
    dbus = [
        DBusAnalysis(
            service_name="com.example.Battery",
            interfaces=[
                DBusInterface(
                    name="com.example.Battery",
                    path="/Battery",
                    methods=[{"name": "Read", "type": "method", "body": "METHOD-CANARY"}],
                    signals=[{"name": "Changed", "type": "signal"}],
                    properties=[{"name": "Voltage", "type": "property"}],
                )
            ],
            object_paths=["/Battery"],
            complexity=ComplexityLevel.MEDIUM,
            focus_areas=[FocusArea.BMS],
        )
    ]
    stats = {
        "total_repos": 3,
        "iot_repos": 1,
        "errors": [],
        "scanned_at": (datetime.now(UTC) - timedelta(minutes=1)).isoformat(),
        "analysis_scope": {
            "max_repositories_per_owner": 100,
            "max_repositories_per_analyzer": 25,
            "max_files_per_repository_per_analyzer": 80,
            "max_esphome_matches_per_repository": 15,
            "max_dbus_matches_per_repository": 10,
        },
    }
    return config, repos, esp, dbus, stats


class EvidenceTests(TestCase):
    def setUp(self) -> None:
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.path = self.root / "evidence.json"
        self.config, self.repos, self.esp, self.dbus, self.stats = fixture()

    def save(self) -> EvidenceSnapshot:
        return write_evidence(self.path, self.config, self.repos, self.esp, self.dbus, self.stats)

    def test_roundtrip_preserves_model_context_without_private_configuration(self) -> None:
        stats = {**self.stats, "local_token": "STATS-CANARY"}
        vars(self.esp[0])["raw_config"] = {"private": "RAW-CONFIG-CANARY"}
        write_evidence(self.path, self.config, self.repos, self.esp, self.dbus, stats)
        serialized = self.path.read_text()
        self.assertNotIn("CANARY", serialized)
        self.assertNotIn('"config"', serialized)
        self.assertNotIn('"raw_config"', serialized)
        self.assertEqual(os.stat(self.path).st_mode & 0o777, 0o600)
        self.assertEqual(json.loads(serialized)["mode"], "evidence_only")
        restored = load_evidence(self.path, self.config)
        self.assertEqual(restored.esphome_analyses[0].components[0].config, {})
        self.assertEqual(
            restored.dbus_analyses[0].interfaces[0].methods, [{"name": "Read", "type": "method"}]
        )
        generator = object.__new__(ProfileGenerator)
        self.assertEqual(
            generator._build_context(self.repos, self.esp, self.dbus, self.stats),
            generator._build_context(
                restored.repositories,
                restored.esphome_analyses,
                restored.dbus_analyses,
                restored.github_stats,
            ),
        )

    def test_rejects_wrong_user_options_and_non_strict_resume(self) -> None:
        self.save()
        for config in [
            replace(self.config, username="other"),
            replace(self.config, include_orgs=["other"]),
            replace(self.config, max_repos=50),
            replace(self.config, analyze_dbus=False),
            replace(self.config, strict_scan=False),
        ]:
            with (
                self.subTest(config=config.username, max_repos=config.max_repos),
                self.assertRaises(EvidenceError),
            ):
                load_evidence(self.path, config)

    def test_rejects_stale_future_and_naive_scan_dates(self) -> None:
        self.save()
        original = json.loads(self.path.read_text())
        for stamp in [
            (datetime.now(UTC) - timedelta(hours=25)).isoformat(),
            (datetime.now(UTC) + timedelta(minutes=10)).isoformat(),
            datetime.now().isoformat(),
        ]:
            with self.subTest(stamp=stamp):
                data = copy.deepcopy(original)
                data["github_stats"]["scanned_at"] = stamp
                data["captured_at"] = stamp
                self.path.write_text(json.dumps(data))
                with self.assertRaises(EvidenceError):
                    load_evidence(self.path, self.config)

    def test_rejects_injected_configuration_bad_counts_and_unknown_fields(self) -> None:
        self.save()
        original = json.loads(self.path.read_text())
        cases = []
        mutations: list[tuple[list[str | int], str, Any]] = [
            ([], "raw_config", {"password": "CANARY"}),
            (["github_stats"], "token", "CANARY"),
            (["github_stats"], "errors", ["CANARY"]),
            (["github_stats"], "total_repos", True),
            (["github_stats"], "iot_repos", 2),
            (["esphome_analyses", 0, "components", 0], "config", {"password": "CANARY"}),
            (["dbus_analyses", 0, "interfaces", 0, "methods", 0], "body", "CANARY"),
            (["repositories", 0], "complexity", "unknown"),
            (["repositories", 0], "full_name", "other/mqtt-battery"),
            ([], "repositories", []),
        ]
        for location, key, value in mutations:
            data = copy.deepcopy(original)
            target: Any = data
            for part in location:
                target = target[part]
            target[key] = value
            cases.append(data)
        duplicate = copy.deepcopy(original)
        duplicate["repositories"] *= 2
        duplicate["github_stats"]["iot_repos"] = 2
        cases.append(duplicate)
        for index, data in enumerate(cases):
            with self.subTest(index=index):
                self.path.write_text(json.dumps(data))
                with self.assertRaises(EvidenceError) as raised:
                    load_evidence(self.path, self.config)
                self.assertNotIn("CANARY", str(raised.exception))

    def test_invalid_write_preserves_previous_checkpoint_and_symlinks_are_rejected(self) -> None:
        self.save()
        original = self.path.read_bytes()
        self.stats["errors"] = ["failure"]
        with self.assertRaises(EvidenceError):
            self.save()
        self.assertEqual(self.path.read_bytes(), original)
        link = self.root / "link.json"
        link.symlink_to(self.path)
        with self.assertRaises(EvidenceError):
            load_evidence(link, self.config)
        self.stats["errors"] = []
        with self.assertRaises(EvidenceError):
            write_evidence(link, self.config, self.repos, self.esp, self.dbus, self.stats)

    def test_checkpoint_accepted_near_size_limit_is_readable(self) -> None:
        # The fixture fits as JSON, but indentation used to expand it past this
        # limit after validation, making a successful write impossible to resume.
        with patch.object(evidence, "MAX_BYTES", 2048):
            self.save()
            self.assertLessEqual(self.path.stat().st_size, 2048)
            restored = load_evidence(self.path, self.config)
        self.assertEqual(restored.github_stats["scanned_at"], self.stats["scanned_at"])

    def test_regular_file_and_symlink_guards_work_without_o_nofollow(self) -> None:
        self.save()
        link = self.root / "portable-link.json"
        link.symlink_to(self.path)
        # Windows does not define this POSIX flag. The lstat/fstat checks must
        # still accept regular files and refuse a symlink before opening it.
        with patch.dict(os.__dict__):
            os.__dict__.pop("O_NOFOLLOW", None)
            restored = load_evidence(self.path, self.config)
            self.assertEqual(len(restored.repositories), 1)
            with self.assertRaises(EvidenceError):
                load_evidence(link, self.config)
            with self.assertRaises(EvidenceError):
                load_evidence(self.root, self.config)


class EvidencePipelineTests(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.path = self.root / "evidence.json"
        self.config, self.repos, self.esp, self.dbus, self.stats = fixture()
        self.scanner_type = self.enterContext(patch("iot_profile_builder.cli.GitHubScanner"))
        self.enterContext(redirect_stdout(io.StringIO()))
        self.builder = IoTProfileBuilder(self.config)
        self.collect = AsyncMock(
            return_value=(ScanResult(self.repos, 3, 1, []), self.esp, self.dbus, self.stats)
        )
        self.enterContext(patch.object(self.builder, "_collect_evidence", self.collect))

    async def test_model_failure_leaves_complete_resumable_evidence(self) -> None:
        self.builder.generator = MagicMock()
        self.builder.generator.generate.side_effect = GenerationError("model failed")
        with self.assertRaises(GenerationError):
            await self.builder.run(self.root / "output", checkpoint_path=self.path)
        restored = load_evidence(self.path, self.config)
        self.assertEqual(restored.github_stats["scanned_at"], self.stats["scanned_at"])
        self.assertFalse((self.root / "output").exists())

    async def test_evidence_only_never_initializes_model_or_renders_profile(self) -> None:
        with (
            patch("iot_profile_builder.cli.ProfileGenerator") as model,
            patch("iot_profile_builder.cli.generate_profile_outputs") as render,
        ):
            result = await self.builder.run(
                self.root / "output", checkpoint_path=self.path, evidence_only=True
            )
        self.assertEqual(result, self.path)
        model.assert_not_called()
        render.assert_not_called()
        self.assertFalse((self.root / "output").exists())

    async def test_resume_skips_all_scanning_and_preserves_original_timestamp(self) -> None:
        write_evidence(self.path, self.config, self.repos, self.esp, self.dbus, self.stats)
        self.collect.side_effect = AssertionError("A resume must not scan")
        with patch("iot_profile_builder.cli.generate_profile_outputs", return_value={}) as render:
            await self.builder.run(self.root / "output", use_llm=False, resume_from=self.path)
        self.collect.assert_not_awaited()
        self.scanner_type.return_value.scan.assert_not_called()
        profile = render.call_args.args[0]
        self.assertEqual(profile.github_stats["scanned_at"], self.stats["scanned_at"])
        self.assertEqual(profile.total_repos_analyzed, 3)
        expected = generate_heuristic_profile(
            self.repos, self.esp, self.dbus, self.stats, self.config.username
        )
        self.assertEqual(profile.complexity_distribution, expected.complexity_distribution)

    async def test_resume_rejects_wrong_user_before_generation(self) -> None:
        write_evidence(self.path, self.config, self.repos, self.esp, self.dbus, self.stats)
        self.builder.config = replace(self.config, username="other")
        self.builder.generator = MagicMock()
        with self.assertRaises(EvidenceError):
            await self.builder.run(self.root / "output", resume_from=self.path)
        self.collect.assert_not_awaited()
        self.builder.generator.generate.assert_not_called()
