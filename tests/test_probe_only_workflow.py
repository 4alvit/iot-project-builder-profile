"""Exercise the real workflow's branch conditions without dispatching a job."""

import ast
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import Any

import yaml

WORKFLOW = Path(__file__).resolve().parents[1] / ".github/workflows/update-profile.yml"
REFRESH_STEPS = {
    "Prepare a fresh refresh directory",
    "Generate profile",
    "Retain complete public scan evidence",
    "Validate and stage this run's profile",
    "Retain the validated snapshot",
    "Open signed profile update PR",
}


def evaluate_condition(expression: str, values: dict[str, Any]) -> bool:
    """Evaluate only the typed boolean subset used by these workflow guards."""
    source = expression.removeprefix("${{").removesuffix("}}").strip()
    for name, value in values.items():
        source = source.replace(name, repr(value))
    source = re.sub(r"\btrue\b", "True", source)
    source = re.sub(r"\bfalse\b", "False", source)
    source = source.replace("&&", " and ").replace("||", " or ")

    def visit(node: ast.AST) -> Any:
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.BoolOp):
            operands = [bool(visit(item)) for item in node.values]
            if isinstance(node.op, ast.And):
                return all(operands)
            if isinstance(node.op, ast.Or):
                return any(operands)
        if isinstance(node, ast.Compare) and len(node.ops) == 1:
            left, right = visit(node.left), visit(node.comparators[0])
            if isinstance(node.ops[0], ast.Eq):
                return left == right
            if isinstance(node.ops[0], ast.NotEq):
                return left != right
        raise AssertionError(f"Unsupported workflow condition node: {type(node).__name__}")

    return bool(visit(ast.parse(source, mode="eval").body))


class ProbeOnlyWorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workflow = yaml.safe_load(WORKFLOW.read_text())
        self.job = self.workflow["jobs"]["generate-profile"]
        self.steps = {step["name"]: step for step in self.job["steps"]}

    def enabled(
        self,
        name: str,
        *,
        event: str = "workflow_dispatch",
        probe: bool | None = False,
        llm: bool | None = True,
        success: bool = True,
        directory: str = "fresh/generated",
    ) -> bool:
        expression = self.steps[name].get("if", "${{ true }}")
        if not success and not any(
            status in expression for status in ("always()", "success()", "failure()")
        ):
            return False
        return evaluate_condition(
            expression,
            {
                "github.event_name": event,
                "inputs.probe_only": probe,
                "inputs.use-llm": llm,
                "steps.refresh.outputs.directory": directory,
                "always()": True,
                "success()": success,
                "failure()": not success,
            },
        )

    def test_default_is_typed_false_and_existing_triggers_are_unchanged(self) -> None:
        triggers = self.workflow["on"]
        option = triggers["workflow_dispatch"]["inputs"]["probe_only"]
        self.assertEqual(option["type"], "boolean")
        self.assertIs(option["default"], False)
        self.assertIs(option["required"], False)
        self.assertIs(triggers["workflow_dispatch"]["inputs"]["use-llm"]["default"], True)
        self.assertEqual(triggers["schedule"], [{"cron": "0 6 * * 1"}])
        self.assertNotIn("github.event.inputs.probe_only", WORKFLOW.read_text())

    def test_schedule_refresh_and_both_probe_modes_execute_expected_steps(self) -> None:
        cases = [
            ("schedule", None, None, True, False),
            ("workflow_dispatch", False, True, True, False),
            ("workflow_dispatch", False, False, False, False),
            ("workflow_dispatch", True, True, True, True),
            ("workflow_dispatch", True, False, True, True),
        ]
        for event, probe, llm, expected_preflight, only_probe in cases:
            values = {"event": event, "probe": probe, "llm": llm}
            with self.subTest(**values):
                self.assertEqual(
                    self.enabled(
                        "Check model access before scanning", event=event, probe=probe, llm=llm
                    ),
                    expected_preflight,
                )
                for name in REFRESH_STEPS:
                    self.assertEqual(
                        self.enabled(name, event=event, probe=probe, llm=llm), not only_probe, name
                    )
                self.assertEqual(
                    self.enabled(
                        "Summarize successful model probe", event=event, probe=probe, llm=llm
                    ),
                    only_probe,
                )
                self.assertFalse(
                    self.enabled("Explain a failed model probe", event=event, probe=probe, llm=llm)
                )

    def test_failed_probe_cannot_upload_or_publish_even_with_stale_directory(self) -> None:
        for llm in (True, False):
            for name in REFRESH_STEPS:
                self.assertFalse(self.enabled(name, probe=True, llm=llm, success=False), name)
        self.assertTrue(self.enabled("Explain a failed model probe", probe=True, success=False))
        self.assertFalse(
            self.enabled("Summarize successful model probe", probe=True, success=False)
        )
        self.assertFalse(self.enabled("Explain a blocked refresh", probe=True, success=False))
        self.assertTrue(self.enabled("Retain complete public scan evidence", success=False))
        self.assertFalse(
            self.enabled("Retain complete public scan evidence", success=False, directory="")
        )

    def test_probe_has_no_enabled_publication_credentials_or_artifact_actions(self) -> None:
        for name, step in self.steps.items():
            if "BOT_PAT" in str(step) or "actions/upload-artifact@" in step.get("uses", ""):
                self.assertIn(name, REFRESH_STEPS)
                for success in (True, False):
                    self.assertFalse(self.enabled(name, probe=True, success=success), name)
        probe = self.steps["Check model access before scanning"]
        self.assertEqual(probe["run"], "uv run --locked python scripts/probe_profile_model.py")
        self.assertEqual(probe["timeout-minutes"], 3)
        self.assertNotIn("continue-on-error", probe)
        self.assertNotIn("GITHUB_TOKEN", probe["env"])
        self.assertNotIn("BOT_PAT", str(probe))

    def test_hosted_probe_preserves_default_branch_queue_and_security(self) -> None:
        runner = self.job["runs-on"]
        self.assertTrue(
            runner.startswith(
                "${{ fromJSON(github.event_name == 'workflow_dispatch' && "
                "inputs.probe_only == true && '[\"ubuntu-latest\"]' || ("
            )
        )
        self.assertIn("vars.PROFILE_RUNNER_MODE || vars.CI_RUNNER_MODE", runner)
        self.assertIn("vars.CI_RUNNER_AUTOMATION_LABELS", runner)
        self.assertIn("github.event.repository.default_branch", self.job["if"])
        self.assertEqual(self.job["timeout-minutes"], 45)
        self.assertEqual(self.workflow["permissions"], {"contents": "read"})
        self.assertEqual(self.job["permissions"], {"contents": "read"})
        self.assertFalse(self.workflow["concurrency"]["cancel-in-progress"])
        self.assertFalse(self.steps["Checkout repository"]["with"]["persist-credentials"])
        hardening = self.steps["Harden the runner (Enforce permitted endpoints)"]["with"]
        self.assertEqual(hardening["egress-policy"], "block")
        self.assertTrue(hardening["disable-telemetry"])
        for name in ("Mask the private inference hostname", "Install locked dependencies"):
            self.assertTrue(self.enabled(name, probe=True))

    def test_probe_summaries_are_static_and_do_not_include_environment_values(self) -> None:
        for name in ("Summarize successful model probe", "Explain a failed model probe"):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                summary = Path(directory) / "summary.md"
                step = self.steps[name]
                self.assertNotIn("${{", step["run"])
                self.assertNotIn("env", step)
                result = subprocess.run(
                    ["bash", "-euc", step["run"]],
                    env={
                        **os.environ,
                        "GITHUB_STEP_SUMMARY": str(summary),
                        "ANTHROPIC_BASE_URL": "https://private-endpoint.invalid",
                        "PROFILE_ACCESS_CLIENT_SECRET": "private-credential",
                    },
                    capture_output=True,
                    text=True,
                    check=True,
                )
                self.assertEqual(result.stdout, "")
                self.assertEqual(result.stderr, "")
                content = summary.read_text()
                self.assertNotIn("private-endpoint", content)
                self.assertNotIn("private-credential", content)
                self.assertIn("probe", content)
