"""Exercise signed profile publication with real local Git and an offline GitHub API."""

import base64
import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import ModuleType
from typing import Any
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/publish_profile.py"
REPOSITORY = "owner/profile"
BRANCH = "profile-update/test-run"
SIGNED = "b" * 40


class GitHub:
    """Only expose expected endpoints and record every attempted mutation."""

    def __init__(self, publisher: ModuleType) -> None:
        self.publisher = publisher
        self.base = publisher.git("rev-parse", "HEAD").decode().strip()
        self.calls: list[tuple[str, dict[str, Any] | None]] = []
        self.pr_calls: list[tuple[str, ...]] = []
        self.advance_base = False
        self.existing_branch = False
        self.race_commit = False
        self.advance_after_commit = False
        self.advance_default_after_commit = False
        self.valid_signature = True
        self.wrong_tree = False
        self.input: dict[str, Any] = {}

    def api(self, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        self.calls.append((path, payload))
        if path == f"repos/{REPOSITORY}":
            return {"default_branch": "main"}
        if path == f"repos/{REPOSITORY}/git/ref/heads/main":
            advanced = self.advance_base or (self.advance_default_after_commit and bool(self.input))
            return {"object": {"sha": "c" * 40 if advanced else self.base}}
        if path == f"repos/{REPOSITORY}/git/ref/heads/{BRANCH}":
            return {"object": {"sha": "d" * 40 if self.advance_after_commit else SIGNED}}
        if path == f"repos/{REPOSITORY}/git/refs":
            assert payload == {"ref": f"refs/heads/{BRANCH}", "sha": self.base}
            if self.existing_branch:
                raise RuntimeError("Reference already exists")
            return {"ref": f"refs/heads/{BRANCH}"}
        if path == "graphql":
            assert payload is not None
            self.input = payload["variables"]["input"]
            assert self.input["expectedHeadOid"] == self.base
            assert self.input["branch"] == {
                "repositoryNameWithOwner": REPOSITORY,
                "refName": BRANCH,
            }
            if self.race_commit:
                raise RuntimeError("expectedHeadOid no longer matches")
            tree = self.publisher.git("write-tree").decode().strip()
            return {
                "data": {
                    "createCommitOnBranch": {
                        "commit": {
                            "oid": SIGNED,
                            "tree": {"oid": "bad" if self.wrong_tree else tree},
                            "signature": {"isValid": self.valid_signature},
                        },
                        "ref": {"target": {"oid": SIGNED}},
                    }
                }
            }
        raise AssertionError(f"Unexpected GitHub endpoint: {path}")

    def gh(self, *args: str) -> str:
        self.pr_calls.append(args)
        assert args[:2] in (("label", "create"), ("pr", "create"))
        return "https://github.com/owner/profile/pull/1"


class ProfilePublisherTests(unittest.TestCase):
    def setUp(self) -> None:
        spec = importlib.util.spec_from_file_location("profile_publisher", SCRIPT)
        assert spec is not None and spec.loader is not None
        self.publisher = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.publisher)
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        previous = Path.cwd()
        os.chdir(self.temporary.name)
        self.addCleanup(os.chdir, previous)
        for args in (
            ("init", "-q"),
            ("config", "user.name", "Fixture"),
            ("config", "user.email", "fixture@example.invalid"),
        ):
            subprocess.run(["git", *args], check=True)
        Path("profile").mkdir()
        Path("docs").mkdir()
        Path("profile/alvit_profile.json").write_text('{"version": 1}')
        Path("docs/alvit_profile.md").write_text("old report")
        self.publisher.git("add", ".")
        self.publisher.git("-c", "commit.gpgsign=false", "commit", "-qm", "initial")
        Path("profile/alvit_profile.json").write_text('{"version": 2}')
        Path("docs/alvit_profile.md").unlink()
        Path("docs/index.html").write_text("<p>new report</p>")

    def publish(self, api: GitHub) -> str:
        with (
            patch.object(self.publisher, "api", api.api),
            patch.object(self.publisher, "gh", api.gh),
        ):
            result: str = self.publisher.publish(REPOSITORY, BRANCH)
            return result

    def test_signed_commit_preserves_additions_modifications_and_deletions(self) -> None:
        api = GitHub(self.publisher)
        self.assertTrue(self.publish(api).endswith("/pull/1"))
        files = api.input["fileChanges"]
        self.assertEqual(files["deletions"], [{"path": "docs/alvit_profile.md"}])
        additions = {
            item["path"]: base64.b64decode(item["contents"]) for item in files["additions"]
        }
        self.assertEqual(
            additions,
            {
                "docs/index.html": b"<p>new report</p>",
                "profile/alvit_profile.json": b'{"version": 2}',
            },
        )
        self.assertEqual(api.pr_calls[-1][0:2], ("pr", "create"))
        self.assertEqual(self.publisher.git("rev-parse", "HEAD").decode().strip(), api.base)

    def test_races_and_snapshot_mismatch_never_open_pr(self) -> None:
        for flag in (
            "advance_base",
            "existing_branch",
            "race_commit",
            "advance_after_commit",
            "advance_default_after_commit",
            "wrong_tree",
        ):
            with self.subTest(flag=flag):
                api = GitHub(self.publisher)
                setattr(api, flag, True)
                with self.assertRaises(RuntimeError):
                    self.publish(api)
                self.assertFalse(api.pr_calls)
                if flag == "advance_base":
                    self.assertTrue(all(payload is None for _, payload in api.calls))

    def test_unverified_commit_never_opens_pr(self) -> None:
        api = GitHub(self.publisher)
        api.valid_signature = False
        with self.assertRaisesRegex(RuntimeError, "signature"):
            self.publish(api)
        self.assertFalse(api.pr_calls)

    def test_unrelated_dirty_files_fail_before_api_calls(self) -> None:
        Path("credentials.txt").write_text("not a generated report")
        for staged in (False, True):
            with self.subTest(staged=staged):
                if staged:
                    self.publisher.git("add", "credentials.txt")
                api = GitHub(self.publisher)
                with self.assertRaisesRegex(RuntimeError, "workspace is dirty"):
                    self.publish(api)
                self.assertFalse(api.calls)

    def test_symlink_is_not_dereferenced_or_published(self) -> None:
        api = GitHub(self.publisher)
        Path("docs/index.html").unlink()
        Path("docs/index.html").symlink_to("../profile/alvit_profile.json")
        with self.assertRaisesRegex(RuntimeError, "regular"):
            self.publish(api)
        self.assertFalse(api.calls)

    def test_clean_generation_creates_no_remote_branch(self) -> None:
        self.publisher.git("restore", ".")
        Path("docs/index.html").unlink()
        api = GitHub(self.publisher)
        self.assertEqual(self.publish(api), "No profile changes to land")
        self.assertFalse(api.calls)

    def test_api_errors_are_not_treated_as_a_signed_commit(self) -> None:
        def reject(*_args: str, **_kwargs: Any) -> str:
            return json.dumps({"errors": [{"message": "stale expectedHeadOid"}]})

        with (
            patch.object(self.publisher, "gh", reject),
            self.assertRaisesRegex(RuntimeError, "rejected"),
        ):
            self.publisher.api("graphql", {"query": "mutation"})
