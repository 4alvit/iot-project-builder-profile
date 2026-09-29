"""Publish generated profiles with a GitHub-signed commit and guarded branch update."""

import argparse
import base64
import json
import os
import re
import subprocess
from datetime import UTC, datetime
from typing import Any, cast

GENERATED = re.compile(
    r"(?:profile|docs)/[A-Za-z0-9_.-]+_profile\.(?:html|json|md)|docs/index\.html"
)
MUTATION = """mutation($input:CreateCommitOnBranchInput!){createCommitOnBranch(input:$input){
commit{oid tree{oid} signature{isValid}} ref{target{oid}}}}"""


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args])


def gh(*args: str, payload: dict[str, Any] | None = None) -> str:
    result = subprocess.run(
        ["gh", *args],
        input=json.dumps(payload) if payload is not None else None,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.strip()


def api(path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    args = ["api", path]
    if payload is not None:
        args.extend(["--method", "POST", "--input", "-"])
    try:
        result = cast(dict[str, Any], json.loads(gh(*args, payload=payload)))
    except subprocess.CalledProcessError:
        # GitHub errors can echo the complete input, including file contents.
        raise RuntimeError(
            f"GitHub API request failed for {path}; inspect the branch before retrying"
        ) from None
    if result.get("errors"):
        raise RuntimeError("GitHub rejected the commit; inspect the branch before retrying")
    return result


def snapshot() -> tuple[str, str, dict[str, list[dict[str, str]]]]:
    """Read exact staged blobs, including deletions; never publish other workspace changes."""
    base = git("rev-parse", "HEAD").decode().strip()
    paths = set(git("diff", "--no-renames", "--name-only", "-z", base).split(b"\0"))
    paths.update(git("ls-files", "--others", "--exclude-standard", "-z").split(b"\0"))
    names = sorted(path.decode() for path in paths if path)
    if any(GENERATED.fullmatch(name) is None for name in names):
        raise RuntimeError("Only generated profile/docs files may be published; workspace is dirty")
    if not names:
        return base, "", {}
    indexed = {path.decode() for path in git("ls-files", "-z").split(b"\0") if path}
    to_stage = [name for name in names if name in indexed or os.path.lexists(name)]
    if to_stage:
        git("add", "--all", "--", *to_stage)
    statuses = git("diff", "--cached", "--no-renames", "--name-status", "-z", base).split(b"\0")[
        :-1
    ]
    changes: dict[str, list[dict[str, str]]] = {"additions": [], "deletions": []}
    for status, raw_path in zip(statuses[::2], statuses[1::2], strict=True):
        path = raw_path.decode()
        if GENERATED.fullmatch(path) is None:
            raise RuntimeError("The staged snapshot contains a non-generated file")
        if status == b"D":
            changes["deletions"].append({"path": path})
        elif status in (b"A", b"M"):
            mode = git("ls-files", "--stage", "--", path).split()[0]
            if mode != b"100644":
                raise RuntimeError("Generated profiles must be regular non-executable files")
            contents = base64.b64encode(git("show", f":{path}")).decode("ascii")
            changes["additions"].append({"path": path, "contents": contents})
        else:
            raise RuntimeError("Unsupported generated file type change")
    tree = git("write-tree").decode().strip()
    if git("rev-parse", "HEAD").decode().strip() != base:
        raise RuntimeError("Local HEAD changed while collecting generated files")
    return base, tree, changes


def publish(repository: str, branch: str) -> str:
    if re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository) is None:
        raise ValueError("A repository owner/name is required")
    if re.fullmatch(r"profile-update/[A-Za-z0-9_-]+", branch) is None:
        raise ValueError("Use a new profile-update/ branch")
    base, tree, changes = snapshot()
    if not changes:
        return "No profile changes to land"
    default = api(f"repos/{repository}")["default_branch"]
    current = api(f"repos/{repository}/git/ref/heads/{default}")["object"]["sha"]
    if current != base:
        raise RuntimeError("Default branch advanced; regenerate the profile from its current head")
    # Creating an existing branch fails. Never reuse or force-update another run's branch.
    api(f"repos/{repository}/git/refs", {"ref": f"refs/heads/{branch}", "sha": base})
    commit = api(
        "graphql",
        {
            "query": MUTATION,
            "variables": {
                "input": {
                    "branch": {"repositoryNameWithOwner": repository, "branchName": branch},
                    "expectedHeadOid": base,
                    "message": {"headline": "chore: update IoT developer profile"},
                    "fileChanges": changes,
                }
            },
        },
    )["data"]["createCommitOnBranch"]
    signed = commit["commit"]
    if (signed.get("signature") or {}).get("isValid") is not True:
        raise RuntimeError("GitHub did not verify the new commit signature; no PR was opened")
    if signed["tree"]["oid"] != tree or commit["ref"]["target"]["oid"] != signed["oid"]:
        raise RuntimeError("GitHub commit does not match the generated snapshot; no PR was opened")
    if api(f"repos/{repository}/git/ref/heads/{branch}")["object"]["sha"] != signed["oid"]:
        raise RuntimeError("The profile branch changed before PR creation; no PR was opened")
    if api(f"repos/{repository}/git/ref/heads/{default}")["object"]["sha"] != base:
        raise RuntimeError("Default branch advanced before PR creation; regenerate the profile")
    gh(
        "label",
        "create",
        "automerge",
        "--repo",
        repository,
        "--description",
        "Eligible for automatic merge after checks",
        "--color",
        "0E8A16",
        "--force",
    )
    return gh(
        "pr",
        "create",
        "--repo",
        repository,
        "--base",
        default,
        "--head",
        branch,
        "--title",
        "chore: update IoT developer profile",
        "--body",
        "Automated regeneration with a verified GitHub-signed commit.",
        "--label",
        "automerge",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", default=os.environ.get("GITHUB_REPOSITORY", ""))
    parser.add_argument(
        "--branch",
        default="profile-update/signed-" + datetime.now(UTC).strftime("%Y%m%d-%H%M%S-%f"),
    )
    args = parser.parse_args()
    print(publish(args.repository, args.branch))


if __name__ == "__main__":
    main()
