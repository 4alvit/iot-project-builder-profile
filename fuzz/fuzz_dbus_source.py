import sys
import types
from pathlib import Path

import atheris

ROOT = Path(__file__).resolve().parents[1]
package = types.ModuleType("iot_profile_builder")
package.__path__ = [str(ROOT / "iot_profile_builder")]
sys.modules[package.__name__] = package
package = types.ModuleType("iot_profile_builder.analyzers")
package.__path__ = [str(ROOT / "iot_profile_builder/analyzers")]
sys.modules[package.__name__] = package

with atheris.instrument_imports():
    from iot_profile_builder.analyzers.dbus_analyzer import DBusAnalyzer


def test_one_input(data: bytes) -> None:
    content = data.decode("utf-8", errors="replace")
    first = DBusAnalyzer().analyze_content(content, "synthetic.py")
    second = DBusAnalyzer().analyze_content(content, "synthetic.py")
    assert first == second  # nosec B101 - intentional test oracle
    assert isinstance(first.service_name, str)  # nosec B101 - intentional test oracle
    assert all(isinstance(path, str) for path in first.object_paths)  # nosec B101 - intentional test oracle


if __name__ == "__main__":
    atheris.Setup(sys.argv, atheris.instrument_func(test_one_input))
    atheris.Fuzz()
