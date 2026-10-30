"""Install only the locked renderer dependencies for synthetic browser fixtures."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import venv
from pathlib import Path


def main() -> None:
    if sys.version_info < (3, 11):  # noqa: UP036 - invoked before the project environment exists
        raise SystemExit("Browser fixture generation requires Python 3.11 or newer")
    root = Path(__file__).resolve().parents[1]
    destination = Path(tempfile.mkdtemp(prefix="iot-profile-browser-"))
    venv.EnvBuilder(with_pip=True).create(destination)
    executable = destination / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    subprocess.run(
        [
            str(executable),
            "-m",
            "pip",
            "install",
            "--disable-pip-version-check",
            "--require-hashes",
            "--only-binary=:all:",
            "-r",
            str(root / ".github/requirements-browser.txt"),
        ],
        check=True,
    )
    environment = os.environ.get("GITHUB_ENV")
    if environment:
        with Path(environment).open("a", encoding="utf-8") as stream:
            stream.write(f"PROFILE_PYTHON={executable}\n")
    print(f"Browser fixture interpreter: {executable}")


if __name__ == "__main__":
    main()
