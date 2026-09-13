"""Run committed tests or enforce the declared stable-release blocker."""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def main() -> None:
    """Distinguish an absent suite from a failed or empty pytest run."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("component", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    component = (root / args.component).resolve()
    component.relative_to(root)
    tests = list((component / "tests").rglob("test_*.py"))
    if not tests:
        policy = json.loads((root / ".release-policy.json").read_text())
        blockers = policy.get("stable_blockers", [])
        if not any("test" in str(blocker).lower() for blocker in blockers):
            raise SystemExit(
                "Unit tests are absent but no stable-release test blocker is configured"
            )
        message = f"Unit tests absent for {args.component}; stable release remains blocked.\n"
        sys.stdout.write(message)
        if os.environ.get("GITHUB_STEP_SUMMARY"):
            with Path(os.environ["GITHUB_STEP_SUMMARY"]).open("a", encoding="utf-8") as summary:
                summary.write(message)
        return
    subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "--cov-report=xml"],
        cwd=component,
        check=True,
    )


if __name__ == "__main__":
    main()
