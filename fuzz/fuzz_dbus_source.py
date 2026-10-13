import sys
import types
from pathlib import Path
from typing import TYPE_CHECKING

import atheris

# Typeshed does not yet re-export the instrumentation APIs at the package root.
if TYPE_CHECKING:
    from atheris.import_hook import instrument_imports
    from atheris.instrument_bytecode import instrument_func
else:
    instrument_imports = atheris.instrument_imports
    instrument_func = atheris.instrument_func

ROOT = Path(__file__).resolve().parents[1]
package = types.ModuleType("iot_profile_builder")
package.__path__ = [str(ROOT / "iot_profile_builder")]
sys.modules[package.__name__] = package
package = types.ModuleType("iot_profile_builder.analyzers")
package.__path__ = [str(ROOT / "iot_profile_builder/analyzers")]
sys.modules[package.__name__] = package

with instrument_imports():
    from iot_profile_builder.analyzers.dbus_analyzer import DBusAnalyzer


def test_one_input(data: bytes) -> None:
    content = data.decode("utf-8", errors="replace")
    first = DBusAnalyzer().analyze_content(content, "synthetic.py")
    second = DBusAnalyzer().analyze_content(content, "synthetic.py")
    assert first == second  # nosec B101 - intentional test oracle
    assert isinstance(first.service_name, str)  # nosec B101 - intentional test oracle
    assert all(isinstance(path, str) for path in first.object_paths)  # nosec B101 - intentional test oracle


if __name__ == "__main__":
    atheris.Setup(sys.argv, instrument_func(test_one_input))
    atheris.Fuzz()
