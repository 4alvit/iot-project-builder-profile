"""D-Bus service analyzer for IoT projects."""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import TYPE_CHECKING, Any

from ..models import (
    ComplexityLevel,
    DBusAnalysis,
    DBusInterface,
    FocusArea,
)

__all__ = ["DBusAnalysis"]

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

DBUS_KEYWORDS = {
    "dbus",
    "dbus-python",
    "pydbus",
    "gi.repository",
    "GLib",
    "org.freedesktop",
    "com.victronenergy",
    "com.victron",
    "system-bus",
    "session-bus",
    "message-bus",
}

FOCUS_KEYWORDS: dict[FocusArea, set[str]] = {
    FocusArea.ENERGY_MANAGEMENT: {
        "com.victronenergy.solarcharger",
        "com.victronenergy.inverter",
        "com.victronenergy.grid",
        "com.victronenergy.vebus",
        "power",
        "energy",
        "voltage",
        "current",
        "ac",
        "dc",
    },
    FocusArea.BMS: {
        "com.victronenergy.battery",
        "com.victronenergy.bms",
        "cell",
        "balancing",
        "soc",
        "soh",
        "temperature",
    },
    FocusArea.HOME_AUTOMATION: {
        "com.victronenergy.settings",
        "com.victronenergy.system",
        "relay",
        "switch",
        "input",
        "output",
    },
    FocusArea.NETWORKING: {
        "org.freedesktop.DBus",
        "org.bluez",
        "org.freedesktop.NetworkManager",
        "org.freedesktop.ModemManager",
        "mqtt",
        "modbus",
        "canbus",
    },
}


class DBusAnalyzer:
    """Analyzes D-Bus service implementations."""

    def __init__(self) -> None:
        self.xml_interface_cache: dict[str, dict[str, Any]] = {}

    def analyze_file(self, file_path: str | Path) -> DBusAnalysis | None:
        """Analyze a single Python file for D-Bus service."""
        path = Path(file_path)
        content = path.read_text(encoding="utf-8")

        if not self._is_dbus_file(content):
            return None

        return self.analyze_content(content, str(path))

    def analyze_content(self, content: str, file_path: str) -> DBusAnalysis:
        """Analyze D-Bus service from source code."""
        service_name = self._extract_service_name(content, file_path)
        interfaces = self._extract_interfaces(content)
        object_paths = self._extract_object_paths(content)
        complexity = self._assess_complexity(interfaces, content)
        focus_areas = self._detect_focus_areas(interfaces, content)

        return DBusAnalysis(
            service_name=service_name,
            interfaces=interfaces,
            object_paths=object_paths,
            complexity=complexity,
            focus_areas=focus_areas,
        )

    def analyze_directory(self, directory: str | Path) -> list[DBusAnalysis]:
        """Analyze all Python files in a directory for D-Bus services."""
        path = Path(directory)
        analyses = []

        for py_file in path.rglob("*.py"):
            analysis = self.analyze_file(py_file)
            if analysis:
                analyses.append(analysis)

        return analyses

    def analyze_xml_introspection(self, xml_path: str | Path) -> DBusAnalysis | None:
        """Analyze D-Bus introspection XML."""
        try:
            path = Path(xml_path)
            content = path.read_text(encoding="utf-8")
            return self._parse_introspection_xml(content, str(path))
        except Exception as e:
            logger.error(f"Failed to parse XML {xml_path}: {e}")
            return None

    def _is_dbus_file(self, content: str) -> bool:
        """Check if file contains D-Bus related code."""
        content_lower = content.lower()
        return any(kw in content_lower for kw in DBUS_KEYWORDS)

    def _extract_service_name(self, content: str, file_path: str) -> str:
        """Extract D-Bus service name from content."""
        patterns = [
            r'request_name\s*\(\s*["\']([^"\']+)["\']',
            r'BusName\s*\(\s*["\']([^"\']+)["\']',
            r'service_name\s*[=:]\s*["\']([^"\']+)["\']',
            r'NAME\s*[=:]\s*["\']([^"\']+)["\']',
        ]

        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                return match.group(1)

        return Path(file_path).stem

    def _extract_interfaces(self, content: str) -> list[DBusInterface]:
        """Extract D-Bus interfaces from content."""
        interfaces = []

        xml_interfaces = self._parse_xml_interfaces(content)
        interfaces.extend(xml_interfaces)

        python_interfaces = self._parse_python_interfaces(content)
        interfaces.extend(python_interfaces)

        return interfaces

    def _parse_xml_interfaces(self, content: str) -> list[DBusInterface]:
        """Parse interfaces from XML introspection data."""
        interfaces = []

        interface_blocks = re.findall(
            r'<interface\s+name\s*=\s*["\']([^"\']+)["\']>(.*?)</interface>', content, re.DOTALL
        )

        for name, block in interface_blocks:
            methods = self._extract_xml_methods(block)
            signals = self._extract_xml_signals(block)
            properties = self._extract_xml_properties(block)

            path_match = re.search(r'path\s*[=:]\s*["\']([^"\']+)["\']', block)
            path = path_match.group(1) if path_match else f"/{name.replace('.', '/')}"

            interfaces.append(
                DBusInterface(
                    name=name,
                    path=path,
                    methods=methods,
                    signals=signals,
                    properties=properties,
                )
            )

        return interfaces

    def _parse_python_interfaces(self, content: str) -> list[DBusInterface]:
        """Parse interfaces from Python code with decorators."""
        interfaces = []

        class_pattern = r"class\s+(\w+)\s*\([^)]*\):"
        class_matches = re.finditer(class_pattern, content)

        for match in class_matches:
            class_name = match.group(1)
            class_start = match.end()
            class_content = self._extract_class_content(content, class_start)

            if not self._is_dbus_class(class_content):
                continue

            interface_name = self._extract_interface_name(class_content, class_name)
            methods = self._extract_python_methods(class_content)
            signals = self._extract_python_signals(class_content)
            properties = self._extract_python_properties(class_content)
            path = self._extract_object_path(class_content, class_name)

            interfaces.append(
                DBusInterface(
                    name=interface_name,
                    path=path,
                    methods=methods,
                    signals=signals,
                    properties=properties,
                )
            )

        return interfaces

    def _extract_class_content(self, content: str, start: int) -> str:
        """Extract class body content."""
        lines = content[start:].split("\n")
        class_lines = []
        indent = None

        for line in lines:
            if indent is None:
                if line.strip():
                    indent = len(line) - len(line.lstrip())
                    class_lines.append(line)
                continue

            if line.strip() and len(line) - len(line.lstrip()) <= indent:
                break
            class_lines.append(line)

        return "\n".join(class_lines)

    def _is_dbus_class(self, content: str) -> bool:
        """Check if class is a D-Bus service."""
        content_lower = content.lower()
        return any(
            kw in content_lower
            for kw in [
                "@dbus",
                "@method",
                "@signal",
                "@property",
                "dbus.service",
                "pydbus",
                "gi.repository",
                "com.victronenergy",
                "org.freedesktop",
            ]
        )

    def _extract_interface_name(self, content: str, class_name: str) -> str:
        """Extract D-Bus interface name."""
        patterns = [
            r'INTERFACE\s*[=:]\s*["\']([^"\']+)["\']',
            r'interface_name\s*[=:]\s*["\']([^"\']+)["\']',
            r'__interface__\s*[=:]\s*["\']([^"\']+)["\']',
        ]

        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                return match.group(1)

        return f"com.example.{class_name.lower()}"

    def _extract_object_path(self, content: str, class_name: str) -> str:
        """Extract D-Bus object path."""
        patterns = [
            r'OBJECT_PATH\s*[=:]\s*["\']([^"\']+)["\']',
            r'object_path\s*[=:]\s*["\']([^"\']+)["\']',
            r'__object_path__\s*[=:]\s*["\']([^"\']+)["\']',
        ]

        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                return match.group(1)

        return f"/{class_name.lower()}"

    def _extract_python_methods(self, content: str) -> list[dict[str, Any]]:
        """Extract methods from Python class."""
        methods = []

        for match in re.finditer(r"@(?:dbus\.)?method\s+(?:async\s+)?def\s+(\w+)", content):
            methods.append({"name": match.group(1), "type": "method"})

        for match in re.finditer(
            r"async\s+def\s+(\w+)\s*\([^)]*\)\s*:(?=.*?dbus)",
            content,
            re.DOTALL,
        ):
            methods.append({"name": match.group(1), "type": "async_method"})

        return methods

    def _extract_python_signals(self, content: str) -> list[dict[str, Any]]:
        """Extract signals from Python class."""
        signals = []

        for match in re.finditer(r"@(?:dbus\.)?signal\s+(?:async\s+)?def\s+(\w+)", content):
            signals.append({"name": match.group(1), "type": "signal"})

        return signals

    def _extract_python_properties(self, content: str) -> list[dict[str, Any]]:
        """Extract properties from Python class."""
        properties = []

        for match in re.finditer(r"@(?:dbus\.)?property\s+(?:async\s+)?def\s+(\w+)", content):
            properties.append({"name": match.group(1), "type": "property"})

        return properties

    def _extract_xml_methods(self, block: str) -> list[dict[str, Any]]:
        """Extract methods from XML interface block."""
        methods = []
        for match in re.finditer(r'<method\s+name\s*=\s*["\']([^"\']+)["\']', block):
            methods.append({"name": match.group(1), "type": "method"})
        return methods

    def _extract_xml_signals(self, block: str) -> list[dict[str, Any]]:
        """Extract signals from XML interface block."""
        signals = []
        for match in re.finditer(r'<signal\s+name\s*=\s*["\']([^"\']+)["\']', block):
            signals.append({"name": match.group(1), "type": "signal"})
        return signals

    def _extract_xml_properties(self, block: str) -> list[dict[str, Any]]:
        """Extract properties from XML interface block."""
        properties = []
        for match in re.finditer(r'<property\s+name\s*=\s*["\']([^"\']+)["\']', block):
            properties.append({"name": match.group(1), "type": "property"})
        return properties

    def _extract_object_paths(self, content: str) -> list[str]:
        """Extract all object paths from content."""
        paths = set()

        for match in re.finditer(r'path\s*[=:]\s*["\']([^"\']+)["\']', content):
            paths.add(match.group(1))

        for match in re.finditer(r'OBJECT_PATH\s*[=:]\s*["\']([^"\']+)["\']', content):
            paths.add(match.group(1))

        return list(paths)

    def _parse_introspection_xml(self, content: str, file_path: str) -> DBusAnalysis:
        """Parse full introspection XML."""
        service_match = re.search(r'<node\s+name\s*=\s*["\']([^"\']+)["\']', content)
        service_name = service_match.group(1) if service_match else Path(file_path).stem

        interfaces = self._parse_xml_interfaces(content)
        object_paths = [i.path for i in interfaces]
        complexity = self._assess_complexity(interfaces, content)
        focus_areas = self._detect_focus_areas(interfaces, content)

        return DBusAnalysis(
            service_name=service_name,
            interfaces=interfaces,
            object_paths=object_paths,
            complexity=complexity,
            focus_areas=focus_areas,
        )

    def _assess_complexity(
        self,
        interfaces: list[DBusInterface],
        content: str,
    ) -> ComplexityLevel:
        """Assess D-Bus service complexity."""
        factors = 0

        total_methods = sum(len(i.methods) for i in interfaces)
        total_signals = sum(len(i.signals) for i in interfaces)
        total_properties = sum(len(i.properties) for i in interfaces)

        factors += self._score_methods(total_methods)
        factors += self._score_signals(total_signals)
        factors += self._score_properties(total_properties)
        factors += self._score_interface_count(len(interfaces))
        factors += self._score_async_methods(interfaces)
        factors += self._score_rw_properties(content)

        return self._complexity_from_factors(factors)

    def _score_methods(self, count: int) -> int:
        if count > 20:
            return 3
        if count > 10:
            return 2
        if count > 5:
            return 1
        return 0

    def _score_signals(self, count: int) -> int:
        if count > 10:
            return 2
        if count > 5:
            return 1
        return 0

    def _score_properties(self, count: int) -> int:
        if count > 15:
            return 2
        if count > 5:
            return 1
        return 0

    def _score_interface_count(self, count: int) -> int:
        if count > 3:
            return 2
        if count > 1:
            return 1
        return 0

    def _score_async_methods(self, interfaces: list[DBusInterface]) -> int:
        async_count = sum(
            1 for i in interfaces for m in i.methods if m.get("type") == "async_method"
        )
        return 1 if async_count > 5 else 0

    def _score_rw_properties(self, content: str) -> int:
        return 1 if "read" in content.lower() and "write" in content.lower() else 0

    def _complexity_from_factors(self, factors: int) -> ComplexityLevel:
        if factors >= 7:
            return ComplexityLevel.EXPERT
        if factors >= 5:
            return ComplexityLevel.HIGH
        if factors >= 3:
            return ComplexityLevel.MEDIUM
        return ComplexityLevel.LOW

    def _detect_focus_areas(
        self,
        interfaces: list[DBusInterface],
        content: str,
    ) -> list[FocusArea]:
        """Detect focus areas from interfaces and content."""
        areas = set()
        all_text = content.lower()

        for interface in interfaces:
            all_text += f" {interface.name} {' '.join(m['name'] for m in interface.methods)}"
            all_text += f" {' '.join(s['name'] for s in interface.signals)}"
            all_text += f" {' '.join(p['name'] for p in interface.properties)}"

        for area, keywords in FOCUS_KEYWORDS.items():
            if any(kw in all_text for kw in keywords):
                areas.add(area)

        return list(areas) if areas else [FocusArea.UNKNOWN]
