"""Directory dispatch compatibility for ESPHomeAnalyzer.

Imports only the ESPHome analyzer, its dataclasses, and the standard library.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import asdict
from pathlib import Path
from tempfile import TemporaryDirectory
from types import MethodType
from typing import Any
from unittest import TestCase
from unittest.mock import patch

from iot_profile_builder.analyzers import esphome_analyzer
from iot_profile_builder.analyzers.esphome_analyzer import ESPHomeAnalyzer
from iot_profile_builder.models import ESPHomeAnalysis


def _plain(value: Any) -> Any:
    if isinstance(value, list):
        return [_plain(item) for item in value]
    if hasattr(value, "__dataclass_fields__"):
        return {key: _plain(item) for key, item in asdict(value).items()}
    if hasattr(value, "value"):
        return value.value
    return value


class DirectoryDispatchTests(TestCase):
    def setUp(self) -> None:
        self._temporary = TemporaryDirectory(prefix="esphome-dispatch-")
        self.root = Path(self._temporary.name)
        self.addCleanup(self._temporary.cleanup)

    def test_unchanged_base_matches_virtual_calls_and_reads_once(self) -> None:
        self._write_corpus()
        engine = ESPHomeAnalyzer()
        reads: list[str] = []
        loads = {"count": 0}
        original_read = Path.read_text
        original_load = esphome_analyzer._esphome_yaml_load

        def counted_read(path: Path, *args: Any, **kwargs: Any) -> str:
            reads.append(path.name)
            return original_read(path, *args, **kwargs)

        def counted_load(content: str) -> Any:
            loads["count"] += 1
            return original_load(content)

        with (
            patch.object(Path, "read_text", counted_read),
            patch.object(esphome_analyzer, "_esphome_yaml_load", counted_load),
        ):
            fast = engine.analyze_directory(self.root)
        virtual = engine._analyze_directory_with_virtual_calls(self.root)
        self.assertEqual(_plain(fast), _plain(virtual))
        self.assertEqual([item.file_path for item in fast], [item.file_path for item in virtual])
        accepted = [
            item for item in fast if item.file_path.endswith(("accepted.yaml", "accepted.yml"))
        ]
        self.assertEqual(len(accepted), 2)
        self.assertEqual(reads.count("accepted.yaml"), 1)
        self.assertEqual(reads.count("accepted.yml"), 1)
        self.assertEqual(reads.count("malformed.yaml"), 1)
        self.assertEqual(reads.count("bad-encoding.yaml"), 1)
        self.assertGreater(loads["count"], 0)
        self.assertNotIn("ignored.txt", reads)

    def test_subclass_file_content_filter_and_exception_use_virtual_calls(self) -> None:
        target = self.root / "node.yaml"
        target.write_text("esphome: {name: fixture}\nesp32: {board: synthetic}\n", encoding="utf-8")

        class FileEngine(ESPHomeAnalyzer):
            calls: list[str]

            def analyze_file(self, path: str | Path) -> ESPHomeAnalysis:
                self.calls.append("analyze_file")
                value = super().analyze_file(path)
                value.external_libs.append("public-file-override")
                return value

        class ContentEngine(ESPHomeAnalyzer):
            calls: list[str]

            def analyze_content(self, content: str, path: str) -> ESPHomeAnalysis:
                self.calls.append("analyze_content")
                value = super().analyze_content(content, path)
                value.external_libs.append("public-content-override")
                return value

        class FilterEngine(ESPHomeAnalyzer):
            calls: list[str]

            def _is_esphome_file(self, _path: Path) -> bool:
                self.calls.append("_is_esphome_file")
                return False

        class RaiseEngine(ESPHomeAnalyzer):
            calls: list[str]

            def analyze_file(self, _path: str | Path) -> ESPHomeAnalysis:
                self.calls.append("analyze_file")
                raise ValueError("public override rejected this input")

        file_engine = FileEngine()
        file_engine.calls = []
        file_result = file_engine.analyze_directory(self.root)
        self.assertEqual(file_engine.calls, ["analyze_file"])
        self.assertIn("public-file-override", file_result[0].external_libs)

        content_engine = ContentEngine()
        content_engine.calls = []
        content_result = content_engine.analyze_directory(self.root)
        self.assertEqual(content_engine.calls, ["analyze_content"])
        self.assertIn("public-content-override", content_result[0].external_libs)

        filter_engine = FilterEngine()
        filter_engine.calls = []
        self.assertEqual(filter_engine.analyze_directory(self.root), [])
        self.assertEqual(filter_engine.calls, ["_is_esphome_file"])

        raise_engine = RaiseEngine()
        raise_engine.calls = []
        with self.assertRaisesRegex(ValueError, "public override rejected this input"):
            raise_engine.analyze_directory(self.root)
        self.assertEqual(raise_engine.calls, ["analyze_file"])

    def test_instance_monkeypatches_are_not_treated_as_the_base_class(self) -> None:
        target = self.root / "node.yaml"
        target.write_text("esphome: {name: fixture}\nesp32: {board: synthetic}\n", encoding="utf-8")
        for method in ("analyze_file", "analyze_content", "_is_esphome_file"):
            engine = ESPHomeAnalyzer()
            original = getattr(engine, method)
            calls: list[str] = []

            def customized(
                _self: ESPHomeAnalyzer,
                *args: Any,
                _calls: list[str] = calls,
                _method: str = method,
                _original: Callable[..., ESPHomeAnalysis | bool] = original,
                **kwargs: Any,
            ) -> ESPHomeAnalysis | bool:
                _calls.append(_method)
                if _method == "_is_esphome_file":
                    return False
                value = _original(*args, **kwargs)
                assert isinstance(value, ESPHomeAnalysis)
                value.external_libs.append("instance-customization")
                return value

            setattr(engine, method, MethodType(customized, engine))
            self.assertIs(type(engine), ESPHomeAnalyzer)
            if method == "_is_esphome_file":
                self.assertEqual(engine.analyze_directory(self.root), [])
            else:
                result = engine.analyze_directory(self.root)
                self.assertIn("instance-customization", result[0].external_libs)
            self.assertEqual(calls, [method])

    def test_extraction_override_still_runs_on_the_single_pass_path(self) -> None:
        (self.root / "node.yaml").write_text(
            "esphome: {name: fixture}\nesp32: {board: synthetic}\n",
            encoding="utf-8",
        )

        class ExtractEngine(ESPHomeAnalyzer):
            calls: list[str]

            def _extract_devices(self, _config: dict[str, Any]) -> list[str]:
                self.calls.append("_extract_devices")
                return ["preserved-extraction-extension"]

        engine = ExtractEngine()
        engine.calls = []
        reads = {"count": 0}
        original_read = Path.read_text

        def counted_read(path: Path, *args: Any, **kwargs: Any) -> str:
            if path.name == "node.yaml":
                reads["count"] += 1
            return original_read(path, *args, **kwargs)

        with patch.object(Path, "read_text", counted_read):
            result = engine.analyze_directory(self.root)
        self.assertEqual(engine.calls, ["_extract_devices"])
        self.assertEqual(result[0].devices, ["preserved-extraction-extension"])
        self.assertEqual(reads["count"], 1)

    def test_rejections_custom_tags_and_unreadable_files_match_virtual_calls(self) -> None:
        self._write_corpus()
        (self.root / "tagged.yaml").write_text(
            "esphome: {name: !secret inert_name}\n"
            "esp32: {board: !lambda synthetic}\n"
            "sensor: !secret [{platform: template, name: probe}]\n",
            encoding="utf-8",
        )
        (self.root / "unsafe.yaml").write_text(
            "!!python/object/apply:builtins.str [inert]\n",
            encoding="utf-8",
        )
        engine = ESPHomeAnalyzer()
        self.assertEqual(
            _plain(engine.analyze_directory(self.root)),
            _plain(engine._analyze_directory_with_virtual_calls(self.root)),
        )
        tagged = next(
            item
            for item in engine.analyze_directory(self.root)
            if item.file_path.endswith("tagged.yaml")
        )
        self.assertEqual(tagged.devices, ["esp32:synthetic"])
        unsafe = ESPHomeAnalyzer().analyze_content(
            "!!python/object/apply:builtins.str [inert]\n",
            "unsafe.yaml",
        )
        self.assertEqual(unsafe.devices, [])
        self.assertEqual(unsafe.focus_areas[0].value, "unknown")

        missing = self.root / "missing.yaml"
        with self.assertRaises(FileNotFoundError):
            ESPHomeAnalyzer().analyze_file(missing)

        denied = self.root / "denied.yaml"
        denied.write_text("esphome: {name: fixture}\n", encoding="utf-8")
        original_read = Path.read_text

        def deny(path: Path, *args: Any, **kwargs: Any) -> str:
            if path == denied:
                raise PermissionError("synthetic denied read")
            return original_read(path, *args, **kwargs)

        with patch.object(Path, "read_text", deny):
            paths = [item.file_path for item in ESPHomeAnalyzer().analyze_directory(self.root)]
        self.assertFalse(any(path.endswith("denied.yaml") for path in paths))

    def test_filter_override_observes_a_file_that_disappears_before_analysis(self) -> None:
        target = self.root / "node.yaml"
        target.write_text("esphome: {name: fixture}\n", encoding="utf-8")

        class DisappearingFilter(ESPHomeAnalyzer):
            def _is_esphome_file(self, path: Path) -> bool:
                Path(path).unlink()
                return True

        with self.assertRaises(FileNotFoundError):
            DisappearingFilter().analyze_directory(self.root)

    def test_class_level_replacements_use_virtual_calls(self) -> None:
        target = self.root / "node.yaml"
        target.write_text("esphome: {name: fixture}\nesp32: {board: synthetic}\n", encoding="utf-8")

        def check(method: str, raises: bool = False) -> None:
            original = getattr(ESPHomeAnalyzer, method)
            calls: list[str] = []

            def customized(
                self: ESPHomeAnalyzer, *args: Any, **kwargs: Any
            ) -> ESPHomeAnalysis | bool:
                calls.append(method)
                if method == "_is_esphome_file":
                    return False
                if raises:
                    raise ValueError("Class-level public override rejected this input")
                value = original(self, *args, **kwargs)
                assert isinstance(value, ESPHomeAnalysis)
                value.external_libs.append("class-customization")
                return value

            with patch.object(ESPHomeAnalyzer, method, customized):
                engine = ESPHomeAnalyzer()
                self.assertIs(type(engine), ESPHomeAnalyzer)
                self.assertFalse(esphome_analyzer._directory_fast_path_allowed(engine))
                if method == "_is_esphome_file":
                    self.assertEqual(engine.analyze_directory(self.root), [])
                elif raises:
                    with self.assertRaisesRegex(
                        ValueError, "Class-level public override rejected this input"
                    ):
                        engine.analyze_directory(self.root)
                else:
                    result = engine.analyze_directory(self.root)
                    self.assertIn("class-customization", result[0].external_libs)
            self.assertEqual(calls, [method])

        check("analyze_file")
        check("analyze_content")
        check("_is_esphome_file")
        check("analyze_file", raises=True)

    def test_custom_getattribute_wrapper_is_called(self) -> None:
        target = self.root / "node.yaml"
        target.write_text("esphome: {name: fixture}\nesp32: {board: synthetic}\n", encoding="utf-8")
        calls: list[str] = []

        class DynamicEngine(ESPHomeAnalyzer):
            def __getattribute__(self, name: str) -> Any:
                original = super().__getattribute__(name)
                if name == "analyze_file":

                    def customized(*args: Any, **kwargs: Any) -> ESPHomeAnalysis:
                        calls.append("dynamic_analyze_file")
                        result = original(*args, **kwargs)
                        assert isinstance(result, ESPHomeAnalysis)
                        result.external_libs.append("dynamic-customization")
                        return result

                    return customized
                return original

        engine = DynamicEngine()
        self.assertFalse(esphome_analyzer._directory_fast_path_allowed(engine))
        result = engine.analyze_directory(self.root)
        self.assertEqual(calls, ["dynamic_analyze_file"])
        self.assertIn("dynamic-customization", result[0].external_libs)

    def _write_corpus(self) -> None:
        (self.root / "accepted.yaml").write_text(
            "esphome:\n  name: synthetic\nesp32:\n  board: esp32dev\n",
            encoding="utf-8",
        )
        (self.root / "nested").mkdir()
        (self.root / "nested" / "accepted.yml").write_text(
            "esp8266:\n  board: d1_mini\n",
            encoding="utf-8",
        )
        (self.root / "scalar.yaml").write_text("just-a-scalar\n", encoding="utf-8")
        (self.root / "list.yaml").write_text("- one\n- two\n", encoding="utf-8")
        (self.root / "null.yaml").write_text("null\n", encoding="utf-8")
        (self.root / "malformed.yaml").write_text(":\n  - [\n", encoding="utf-8")
        (self.root / "plain.yaml").write_text("name: not-esphome\n", encoding="utf-8")
        (self.root / "bad-encoding.yaml").write_bytes(b"\xff\xfe not-utf8")
        (self.root / "ignored.txt").write_text("esphome: true\n", encoding="utf-8")
