"""Validate fresh profile output before staging exact files for signed publication."""

import argparse
import json
import re
import tempfile
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

USERNAME = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?")
EXTENSIONS = ("html", "md", "json")


def timestamp(value: Any) -> datetime:
    """Historical output uses naive timestamps; refresh jobs explicitly run in UTC."""
    if not isinstance(value, str):
        raise ValueError("Profile timestamps must be ISO strings")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed.replace(tzinfo=UTC) if parsed.tzinfo is None else parsed.astimezone(UTC)


def positive_integer(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def stage_profile(
    source: Path, root: Path, username: str, generated_after: str, *, require_llm: bool = False
) -> dict[str, Any]:
    """Leave publication untouched unless this run produced a complete, current scan."""
    if USERNAME.fullmatch(username) is None:
        raise ValueError("Expected a GitHub username, not a path")
    if source.is_symlink() or not source.is_dir():
        raise ValueError("Profile source must be a real directory")
    earliest = timestamp(generated_after)
    contents: dict[str, bytes] = {}
    for extension in EXTENSIONS:
        name = f"{username}_profile.{extension}"
        path = source / name
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"Missing regular profile file: {name}")
        data = path.read_bytes()
        if not data.decode("utf-8").strip():
            raise ValueError(f"Empty profile file: {name}")
        contents[name] = data
    profile = json.loads(contents[f"{username}_profile.json"])
    if not isinstance(profile, dict) or profile.get("username") != username:
        raise ValueError("Profile username does not match the requested user")
    stats = profile.get("github_stats")
    if not isinstance(stats, dict) or stats.get("errors") != []:
        raise ValueError("Incomplete or failed scan; existing published profile is preserved")
    generation = stats.get("generation", {})
    if require_llm and (
        not isinstance(generation, dict)
        or generation.get("mode") != "llm"
        or not generation.get("requested_model")
    ):
        raise ValueError("This refresh requires a successful model-generated profile")
    if not all(
        positive_integer(value)
        for value in (
            profile.get("total_repos_analyzed"),
            profile.get("iot_repos_count"),
            stats.get("total_repos"),
            stats.get("iot_repos"),
        )
    ):
        raise ValueError("Refusing an empty repository scan")
    repositories = profile.get("top_repositories")
    if not isinstance(repositories, list) or not repositories:
        raise ValueError("Profile has no repository evidence")
    generated = timestamp(profile.get("generated_at"))
    scanned = timestamp(stats.get("scanned_at"))
    if not earliest <= scanned <= generated <= datetime.now(UTC) + timedelta(minutes=5):
        raise ValueError("Profile dates do not belong to this refresh run")

    targets: dict[Path, bytes] = {}
    for directory in (root / "profile", root / "docs"):
        if directory.is_symlink() or (directory.exists() and not directory.is_dir()):
            raise ValueError("Publication destinations must be real directories")
        targets.update({directory / name: data for name, data in contents.items()})
    targets[root / "docs" / "index.html"] = contents[f"{username}_profile.html"]
    for target in targets:
        if target.is_symlink() or (target.exists() and not target.is_file()):
            raise ValueError("Refusing a non-regular publication target")
    for target, data in targets.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as staged:
            temporary = Path(staged.name)
            staged.write(data)
        try:
            temporary.chmod(0o644)
            temporary.replace(target)
        finally:
            temporary.unlink(missing_ok=True)
    return {
        "username": username,
        "generated_at": generated.isoformat(),
        "total_repos": stats["total_repos"],
        "iot_repos": stats["iot_repos"],
        "staged_files": len(targets),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--username", required=True)
    parser.add_argument("--generated-after", required=True)
    parser.add_argument("--summary", type=Path)
    parser.add_argument("--require-llm", action="store_true")
    args = parser.parse_args()
    receipt = stage_profile(
        args.source, args.root, args.username, args.generated_after, require_llm=args.require_llm
    )
    if args.summary is not None:
        with args.summary.open("a", encoding="utf-8") as summary:
            summary.write(
                "## Profile refresh ready for review\n\n"
                f"User: `{receipt['username']}` · Generated: `{receipt['generated_at']}`\n\n"
                f"Scanned {receipt['total_repos']} repositories; "
                f"{receipt['iot_repos']} matched IoT criteria. "
                "Seven exact profile/Pages files were staged. "
                "Publication follows the signed PR, required checks and merge.\n"
            )
    print(json.dumps(receipt, sort_keys=True))


if __name__ == "__main__":
    main()
