"""The hosted fallback preserves each required OS/browser and extended coverage."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_required_browser_targets_preserve_five_os_engine_pairs() -> None:
    rows = json.loads((ROOT / ".github/browser-compatibility.json").read_text())
    required = [row for row in rows if row["tier"] == "required"]
    assert {(row["os"], row["engine"]) for row in required} == {
        ("ubuntu-latest", "chromium"),
        ("ubuntu-latest", "firefox"),
        ("ubuntu-latest", "webkit"),
        ("windows-2022", "chromium"),
        ("macos-15-intel", "webkit"),
    }
    assert len(required) == 5
    assert all(row["playwright"] == "1.64.0" for row in required)
    intel = next(row for row in required if row["os"] == "macos-15-intel")
    assert intel["id"] == "macos-15-intel-webkit-1-64-0"
    assert intel["browser_version"] == "27.2"
    assert intel["toolchain"] == "tools/browser-compatibility/playwright-1-64-0"


def test_extended_inventory_is_not_replaced_by_fallback() -> None:
    rows = json.loads((ROOT / ".github/browser-compatibility.json").read_text())
    assert len(rows) == 35
    assert len({row["id"] for row in rows}) == 35
    extended = [row for row in rows if row["tier"] == "extended"]
    assert len(extended) == 30
    assert sum(row["os"] == "macos-15" for row in extended) == 10
    assert not any(row["os"] == "macos-15-intel" for row in extended)
