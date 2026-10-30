"""Exercise fresh snapshot staging and scheduled workflow entry points offline."""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "stage_profile.py"
WORKFLOW = ROOT / ".github" / "workflows" / "update-profile.yml"


class ProfileRefreshTests(unittest.TestCase):
    def setUp(self) -> None:
        spec = importlib.util.spec_from_file_location("profile_refresh", SCRIPT)
        assert spec is not None and spec.loader is not None
        self.stager = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.stager)
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.source = self.directory / "new"
        self.root = self.directory / "repo"
        self.source.mkdir()
        (self.root / "docs").mkdir(parents=True)
        (self.root / "docs" / "index.html").write_text("previous page")
        self.started = datetime.now(UTC) - timedelta(seconds=5)
        self.profile: dict[str, Any] = {
            "username": "selected-user",
            "generated_at": datetime.now(UTC).isoformat(),
            "total_repos_analyzed": 4,
            "iot_repos_count": 2,
            "top_repositories": [{"full_name": "selected-user/sensor"}],
            "github_stats": {
                "total_repos": 4,
                "iot_repos": 2,
                "errors": [],
                "scanned_at": self.started.isoformat(),
            },
        }
        self.write_snapshot()

    def write_snapshot(self) -> None:
        (self.source / "selected-user_profile.json").write_text(json.dumps(self.profile))
        (self.source / "selected-user_profile.html").write_text("<p>Fresh selected user</p>")
        (self.source / "selected-user_profile.md").write_text("# Fresh selected user")

    def stage(self) -> dict[str, Any]:
        result: dict[str, Any] = self.stager.stage_profile(
            self.source, self.root, "selected-user", self.started.isoformat()
        )
        return result

    def write_v2_pages(self) -> None:
        for kind, filename in (
            ("overview", "selected-user_profile.html"),
            ("repositories", "repositories.html"),
            ("evidence", "evidence.html"),
        ):
            (self.source / filename).write_text(
                '<main id="main" data-profile-version="2" '
                f'data-profile-page="{kind}" data-profile-user="selected-user" '
                f'data-profile-generated="{self.profile["generated_at"]}">'
                f"<p>Fresh {kind}</p></main>"
            )

    def assert_site_preserved(self) -> None:
        self.assertEqual((self.root / "docs" / "index.html").read_text(), "previous page")
        self.assertFalse((self.root / "profile").exists())

    def test_v2_stages_all_eleven_exact_files(self) -> None:
        self.write_v2_pages()
        (self.source / "not-a-profile.html").write_text("unrelated")
        result = self.stage()
        self.assertEqual(result["staged_files"], 11)
        for directory in ("docs", "profile"):
            for name in ("repositories.html", "evidence.html"):
                self.assertEqual(
                    (self.root / directory / name).read_bytes(), (self.source / name).read_bytes()
                )
            self.assertFalse((self.root / directory / "not-a-profile.html").exists())
        self.assertEqual(
            (self.root / "docs" / "index.html").read_bytes(),
            (self.source / "selected-user_profile.html").read_bytes(),
        )

    def test_v2_rejects_missing_empty_symlinked_auxiliary_files_before_any_write(self) -> None:
        for name in ("repositories.html", "evidence.html"):
            for failure in ("missing", "empty", "symlink"):
                with self.subTest(name=name, failure=failure):
                    self.write_v2_pages()
                    path = self.source / name
                    path.unlink()
                    if failure == "empty":
                        path.write_text(" \n")
                    elif failure == "symlink":
                        path.symlink_to(self.source / "selected-user_profile.html")
                    with self.assertRaises(ValueError):
                        self.stage()
                    self.assert_site_preserved()
                    path.unlink(missing_ok=True)

    def test_v2_rejects_mismatched_or_ambiguous_page_identity(self) -> None:
        for name in ("selected-user_profile.html", "repositories.html", "evidence.html"):
            for old, new in (
                ('data-profile-page="', 'data-profile-page="wrong-'),
                ('data-profile-user="selected-user"', 'data-profile-user="other"'),
                ('data-profile-generated="', 'data-profile-generated="stale-'),
                ('data-profile-version="2"', 'data-profile-version="3"'),
                ('id="main"', 'id="main" id="other"'),
                ("</main>", '</main><main id="extra"></main>'),
                ("</main>", '</main><div id="main"></div>'),
            ):
                with self.subTest(name=name, change=new):
                    self.write_v2_pages()
                    path = self.source / name
                    path.write_text(path.read_text().replace(old, new))
                    with self.assertRaises(ValueError):
                        self.stage()
                    self.assert_site_preserved()

    def test_auxiliary_destinations_are_validated_before_any_write(self) -> None:
        self.write_v2_pages()
        target = self.root / "docs" / "evidence.html"
        target.symlink_to(self.root / "docs" / "index.html")
        with self.assertRaises(ValueError):
            self.stage()
        self.assert_site_preserved()

    def test_unmarked_legacy_snapshot_does_not_pick_up_auxiliary_files(self) -> None:
        (self.source / "repositories.html").write_text("unrelated legacy file")
        (self.source / "evidence.html").symlink_to(self.root / "docs" / "index.html")
        self.assertEqual(self.stage()["staged_files"], 7)
        self.assertFalse((self.root / "docs" / "repositories.html").exists())
        self.assertFalse((self.root / "docs" / "evidence.html").exists())

    def test_only_selected_fresh_files_become_the_entry_point(self) -> None:
        (self.root / "docs" / "aaa_profile.html").write_text("unrelated old profile")
        (self.root / "docs" / "pipeline.svg").write_text("maintained diagram")
        (self.source / "charts").mkdir()
        (self.source / "charts" / "chart.png").write_bytes(b"optional export")
        result = self.stage()
        self.assertEqual(result["staged_files"], 7)
        for extension in ("html", "md", "json"):
            name = f"selected-user_profile.{extension}"
            expected = (self.source / name).read_bytes()
            self.assertEqual((self.root / "profile" / name).read_bytes(), expected)
            self.assertEqual((self.root / "docs" / name).read_bytes(), expected)
        self.assertEqual(
            (self.root / "docs" / "index.html").read_bytes(),
            (self.source / "selected-user_profile.html").read_bytes(),
        )
        self.assertEqual(
            (self.root / "docs" / "aaa_profile.html").read_text(), "unrelated old profile"
        )
        self.assertEqual((self.root / "docs" / "pipeline.svg").read_text(), "maintained diagram")
        self.assertFalse((self.root / "profile" / "charts").exists())

    def test_failed_empty_wrong_user_or_stale_json_preserves_existing_site(self) -> None:
        original = json.dumps(self.profile)
        cases = [
            ("username", "other"),
            ("total_repos_analyzed", 0),
            ("iot_repos_count", False),
            ("top_repositories", []),
            ("generated_at", (self.started - timedelta(days=1)).isoformat()),
            ("generated_at", (self.started + timedelta(days=1)).isoformat()),
            ("generated_at", "invalid"),
        ]
        for field, value in cases:
            with self.subTest(field=field, value=value):
                self.profile = json.loads(original)
                self.profile[field] = value
                self.write_snapshot()
                with self.assertRaises(ValueError):
                    self.stage()
                self.assertEqual((self.root / "docs" / "index.html").read_text(), "previous page")
                self.assertFalse((self.root / "profile").exists())
        for errors in (["repository scan failed"], None, ""):
            self.profile = json.loads(original)
            self.profile["github_stats"]["errors"] = errors
            self.write_snapshot()
            with self.assertRaises(ValueError):
                self.stage()
        self.profile = json.loads(original)
        self.profile["github_stats"]["scanned_at"] = (
            self.started - timedelta(seconds=1)
        ).isoformat()
        self.write_snapshot()
        with self.assertRaises(ValueError):
            self.stage()

    def test_missing_empty_and_symlinked_files_are_not_published(self) -> None:
        file = self.source / "selected-user_profile.html"
        file.unlink()
        with self.assertRaises(ValueError):
            self.stage()
        file.write_text("  ")
        with self.assertRaises(ValueError):
            self.stage()
        file.unlink()
        file.symlink_to(self.root / "docs" / "index.html")
        with self.assertRaises(ValueError):
            self.stage()
        file.unlink()
        self.write_snapshot()
        target = self.root / "docs" / "selected-user_profile.html"
        target.symlink_to(self.root / "docs" / "index.html")
        with self.assertRaises(ValueError):
            self.stage()
        self.assertEqual((self.root / "docs" / "index.html").read_text(), "previous page")
        with self.assertRaises(ValueError):
            self.stager.stage_profile(self.source, self.root, "../other", self.started.isoformat())

    def test_model_refresh_rejects_heuristic_or_missing_provenance(self) -> None:
        for generation in (None, {"mode": "heuristic"}, {"mode": "llm"}):
            self.profile["github_stats"]["generation"] = generation
            self.write_snapshot()
            with self.assertRaises(ValueError):
                self.stager.stage_profile(
                    self.source,
                    self.root,
                    "selected-user",
                    self.started.isoformat(),
                    require_llm=True,
                )
            self.assertEqual((self.root / "docs" / "index.html").read_text(), "previous page")
        self.profile["github_stats"]["generation"] = {
            "mode": "llm",
            "requested_model": "fixture/model",
        }
        self.write_snapshot()
        self.stager.stage_profile(
            self.source, self.root, "selected-user", self.started.isoformat(), require_llm=True
        )
        self.assertIn("Fresh selected user", (self.root / "docs" / "index.html").read_text())

    def test_cli_produces_a_summary_without_claiming_deployment(self) -> None:
        self.write_v2_pages()
        summary = self.directory / "summary.md"
        result = subprocess.run(
            [
                sys.executable,
                "-I",
                str(SCRIPT),
                "--source",
                str(self.source),
                "--root",
                str(self.root),
                "--username",
                "selected-user",
                "--generated-after",
                self.started.isoformat(),
                "--summary",
                str(summary),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(json.loads(result.stdout)["staged_files"], 11)
        self.assertIn("ready for review", summary.read_text())
        self.assertIn("11 exact profile/Pages files", summary.read_text())
        self.assertIn("required checks and merge", summary.read_text())


class RefreshWorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workflow = yaml.safe_load(WORKFLOW.read_text())
        self.job = self.workflow["jobs"]["generate-profile"]
        self.steps = {step["name"]: step for step in self.job["steps"]}

    def test_validated_artifact_names_only_the_five_snapshot_files(self) -> None:
        paths = self.steps["Retain the validated snapshot"]["with"]["path"].splitlines()
        self.assertEqual(len(paths), 5)
        self.assertEqual(
            {path.rsplit("/", 1)[-1] for path in paths},
            {
                "${{ github.event.inputs.username || '4alvit' }}_profile.html",
                "${{ github.event.inputs.username || '4alvit' }}_profile.md",
                "${{ github.event.inputs.username || '4alvit' }}_profile.json",
                "repositories.html",
                "evidence.html",
            },
        )
        self.assertFalse(any("*" in path for path in paths))

    def test_model_preflight_precedes_scanning_and_hostname_is_masked(self) -> None:
        names = list(self.steps)
        self.assertLess(
            names.index("Check model access before scanning"), names.index("Generate profile")
        )
        self.assertLess(
            names.index("Mask the private inference hostname"),
            names.index("Harden the runner (Enforce permitted endpoints)"),
        )
        preflight = self.steps["Check model access before scanning"]
        self.assertIn("inputs.use-llm", preflight["if"])
        self.assertIn("probe_profile_model.py", preflight["run"])
        self.assertNotIn("GITHUB_TOKEN", preflight["env"])
        self.assertNotIn("BOT_PAT", str(preflight))
        hardening = self.steps["Harden the runner (Enforce permitted endpoints)"]["with"]
        self.assertEqual(hardening["egress-policy"], "block")
        self.assertTrue(hardening["disable-telemetry"])
        self.assertIn("secrets.PROFILE_INFERENCE_HOSTNAME", hardening["allowed-endpoints"])
        result = subprocess.run(
            ["bash", "-euc", self.steps["Mask the private inference hostname"]["run"]],
            env={**os.environ, "ANTHROPIC_BASE_URL": "https://inference.example.test"},
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(result.stdout, "::add-mask::inference.example.test\n")
        self.assertEqual(result.stderr, "")

    def test_schedule_routes_through_variables_and_requires_the_configured_model(self) -> None:
        self.assertEqual(self.workflow["on"]["schedule"], [{"cron": "0 6 * * 1"}])
        self.assertTrue(self.workflow["on"]["workflow_dispatch"]["inputs"]["use-llm"]["default"])
        self.assertIn("vars.CI_RUNNER_MODE", self.job["runs-on"])
        self.assertIn("vars.PROFILE_RUNNER_MODE || vars.CI_RUNNER_MODE", self.job["runs-on"])
        self.assertIn("vars.CI_RUNNER_AUTOMATION_LABELS", self.job["runs-on"])
        self.assertIn("ubuntu-latest", self.job["runs-on"])
        self.assertNotIn("fcc", self.job["runs-on"])
        self.assertIn("github.event.repository.default_branch", self.job["if"])
        self.assertEqual(self.job["timeout-minutes"], 45)
        self.assertFalse(self.workflow["concurrency"]["cancel-in-progress"])
        self.assertFalse(self.steps["Checkout repository"]["with"]["persist-credentials"])
        generate = self.steps["Generate profile"]
        self.assertIn("--strict-scan", generate["run"])
        self.assertIn("PROFILE_DIRECTORY", generate["run"])
        self.assertNotIn("cluster.local", WORKFLOW.read_text())
        self.assertNotIn("freecc", WORKFLOW.read_text())
        self.assertIn(
            "scripts/stage_profile.py", self.steps["Validate and stage this run's profile"]["run"]
        )
        self.assertIn(
            "secrets.BOT_PAT", self.steps["Open signed profile update PR"]["env"]["GH_TOKEN"]
        )
        self.assertIn(
            "scripts/publish_profile.py", self.steps["Open signed profile update PR"]["run"]
        )

    def test_repeated_jobs_prepare_distinct_directories_and_explicit_mode_arguments(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            env = {
                **os.environ,
                "RUNNER_TEMP": directory,
                "GITHUB_RUN_ID": "5",
                "GITHUB_RUN_ATTEMPT": "1",
            }
            directories = []
            for attempt in (1, 2):
                outputs = root / f"outputs-{attempt}"
                subprocess.run(
                    ["bash", "-euc", self.steps["Prepare a fresh refresh directory"]["run"]],
                    env={**env, "GITHUB_OUTPUT": str(outputs)},
                    check=True,
                )
                fields = dict(line.split("=", 1) for line in outputs.read_text().splitlines())
                directories.append(fields["directory"])
                self.assertIn("started-at", fields)
                self.assertTrue(Path(fields["directory"]).parent.is_dir())
            self.assertNotEqual(*directories)
            executable = root / "uv"
            executable.write_text('#!/bin/sh\nprintf "%s\\n" "$@" > "$ARGUMENT_LOG"\n')
            executable.chmod(0o755)
            argument_log = root / "args"
            env.update(
                {
                    "PATH": f"{root}{os.pathsep}{os.environ['PATH']}",
                    "ARGUMENT_LOG": str(argument_log),
                    "PROFILE_USERNAME": "fixture",
                    "GITHUB_TOKEN": "fixture",
                    "PROFILE_DIRECTORY": directories[0],
                    "PROFILE_USE_LLM": "false",
                    "ANTHROPIC_BASE_URL": "",
                    "ANTHROPIC_API_KEY": "",
                    "PROFILE_LLM_MODEL": "",
                }
            )
            subprocess.run(
                ["bash", "-euc", self.steps["Generate profile"]["run"]], env=env, check=True
            )
            self.assertIn("--no-llm", argument_log.read_text().splitlines())
            self.assertIn("--strict-scan", argument_log.read_text().splitlines())
            argument_log.unlink()
            result = subprocess.run(
                ["bash", "-euc", self.steps["Generate profile"]["run"]],
                env={**env, "PROFILE_USE_LLM": "true"},
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("requires", result.stderr)
            self.assertFalse(argument_log.exists())


if __name__ == "__main__":
    unittest.main()
