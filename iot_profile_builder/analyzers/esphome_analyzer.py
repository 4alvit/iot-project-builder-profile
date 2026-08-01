"""ESPHome configuration analyzer."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

import yaml

from ..models import (
    ComplexityLevel,
    ESPHomeAnalysis,
    ESPHomeComponent,
    FocusArea,
)

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

COMPONENT_TYPES = {
    "sensor", "binary_sensor", "switch", "light", "climate", "cover",
    "fan", "number", "text", "select", "button", "lock", "valve",
    "alarm_control_panel", "camera", "media_player", "remote_transmitter",
    "remote_receiver", "i2c", "spi", "uart", "canbus", "wifi", "ethernet",
    "ble_client", "ble_server", "bluetooth_proxy", "esp32_ble_tracker",
    "esp32_ble", "esp32_camera", "mqtt", "api", "ota", "web_server",
    "logger", "captive_portal", "time", "sun", "display", "touchscreen",
    "font", "image", "color", "lambda", "script", "automation", "interval",
}

PLATFORM_KEYWORDS: dict[str, set[str]] = {
    "homeassistant": {"homeassistant", "ha", "home_assistant"},
    "mqtt": {"mqtt", "mosquitto"},
    "ble": {"ble", "bluetooth", "esp32_ble", "ble_client", "ble_server"},
    "modbus": {"modbus", "modbus_controller"},
    "canbus": {"canbus", "can_bus"},
    "i2c": {"i2c"},
    "spi": {"spi"},
    "uart": {"uart"},
    "gpio": {"gpio", "binary_sensor", "switch", "output"},
    "display": {"display", "lcd", "oled", "eink", "epaper", "ili9xxx", "st7789"},
    "audio": {"i2s_audio", "es8311", "es7210", "microphone", "speaker"},
    "voice": {"voice_assistant", "wake_word", "stt", "tts", "piper", "whisper"},
}

FOCUS_AREA_KEYWORDS: dict[FocusArea, set[str]] = {
    FocusArea.HOME_AUTOMATION: {
        "light", "switch", "climate", "cover", "fan", "lock", "valve",
        "binary_sensor", "sensor", "automation", "script",
    },
    FocusArea.ENERGY_MANAGEMENT: {
        "power", "energy", "voltage", "current", "battery", "solar",
        "inverter", "mppt", "energy_meter", "ct_clamp",
    },
    FocusArea.BMS: {
        "bms", "cell", "balancing", "battery", "jbd", "daly", "ant_bms",
    },
    FocusArea.ENVIRONMENTAL: {
        "temperature", "humidity", "pressure", "co2", "pm25", "pm10",
        "air_quality", "voc", "weather", "bme280", "bme680", "scd40",
        "sht30", "sht40", "aht10", "aht20",
    },
    FocusArea.VOICE_ASSISTANT: {
        "voice_assistant", "microphone", "speaker", "i2s_audio", "es8311",
        "es7210", "wake_word", "piper", "whisper", "wyoming",
    },
    FocusArea.NETWORKING: {
        "mqtt", "wifi", "ethernet", "ble", "bluetooth", "espnow",
        "thread", "matter", "zigbee", "zwave", "modbus", "canbus",
    },
    FocusArea.FIRMWARE: {
        "ota", "deep_sleep", "watchdog", "gpio", "i2c", "spi", "uart",
        "adc", "dac", "pwm", "rtc", "preferences", "flash",
    },
}


class ESPHomeAnalyzer:
    """Analyzes ESPHome YAML configurations."""

    def __init__(self):
        self.custom_components: set[str] = set()

    def analyze_file(self, file_path: str | Path) -> ESPHomeAnalysis:
        """Analyze a single ESPHome YAML file."""
        path = Path(file_path)
        content = path.read_text(encoding="utf-8")
        return self.analyze_content(content, str(path))

    def analyze_content(self, content: str, file_path: str) -> ESPHomeAnalysis:
        """Analyze ESPHome YAML content."""
        try:
            config = yaml.safe_load(content)
        except yaml.YAMLError as e:
            logger.error(f"Failed to parse YAML {file_path}: {e}")
            return ESPHomeAnalysis(
                file_path=file_path,
                devices=[],
                components=[],
                custom_components=[],
                external_libs=[],
                complexity=ComplexityLevel.LOW,
                focus_areas=[FocusArea.UNKNOWN],
            )

        devices = self._extract_devices(config)
        components = self._extract_components(config)
        custom_components = self._extract_custom_components(config)
        external_libs = self._extract_external_libs(config)
        complexity = self._assess_complexity(config, components, custom_components)
        focus_areas = self._detect_focus_areas(components, config)

        return ESPHomeAnalysis(
            file_path=file_path,
            devices=devices,
            components=components,
            custom_components=list(custom_components),
            external_libs=external_libs,
            complexity=complexity,
            focus_areas=focus_areas,
        )

    def analyze_directory(self, directory: str | Path) -> list[ESPHomeAnalysis]:
        """Analyze all ESPHome YAML files in a directory."""
        path = Path(directory)
        analyses = []

        for yaml_file in path.rglob("*.yaml"):
            if self._is_esphome_file(yaml_file):
                analyses.append(self.analyze_file(yaml_file))

        for yml_file in path.rglob("*.yml"):
            if self._is_esphome_file(yml_file):
                analyses.append(self.analyze_file(yml_file))

        return analyses

    def _is_esphome_file(self, path: Path) -> bool:
        """Check if YAML file is ESPHome config."""
        try:
            content = path.read_text(encoding="utf-8")
            config = yaml.safe_load(content)
            if not isinstance(config, dict):
                return False
            # ESPHome configs typically have 'esphome:' or 'esp32:' or 'esp8266:' keys
            return any(k in config for k in ("esphome", "esp32", "esp8266", "rp2040"))
        except Exception:
            return False

    def _extract_devices(self, config: dict) -> list[str]:
        """Extract target devices from config."""
        devices = []
        for key in ("esp32", "esp8266", "rp2040", "bk72xx", "rtl87xx"):
            if key in config:
                board = config[key].get("board") if isinstance(config[key], dict) else None
                if board:
                    devices.append(f"{key}:{board}")
                else:
                    devices.append(key)
        return devices

    def _extract_components(self, config: dict) -> list[ESPHomeComponent]:
        """Extract all components from config."""
        components = []

        for comp_type in COMPONENT_TYPES:
            if comp_type in config:
                comp_configs = config[comp_type]
                if not isinstance(comp_configs, list):
                    comp_configs = [comp_configs]

                for comp_config in comp_configs:
                    if not isinstance(comp_config, dict):
                        continue

                    component = ESPHomeComponent(
                        type=comp_type,
                        platform=comp_config.get("platform"),
                        name=comp_config.get("name", ""),
                        config=comp_config,
                        integrations=self._detect_integrations(comp_type, comp_config),
                    )
                    components.append(component)

        return components

    def _detect_integrations(self, comp_type: str, comp_config: dict) -> list[str]:
        """Detect integrations used by a component."""
        integrations = []
        text = str(comp_config).lower()

        for integration, keywords in PLATFORM_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                integrations.append(integration)

        # Component type itself implies some integrations
        if comp_type in ("mqtt", "api", "homeassistant"):
            integrations.append(comp_type)

        return list(set(integrations))

    def _extract_custom_components(self, config: dict) -> list[str]:
        """Extract custom component references."""
        custom = set()

        # Check for external_components
        if "external_components" in config:
            ext = config["external_components"]
            if isinstance(ext, list):
                for item in ext:
                    if isinstance(item, dict) and "components" in item:
                        for comp in item["components"]:
                            custom.add(comp)
                    elif isinstance(item, str):
                        custom.add(item)

        # Check for custom_component in individual components
        for comp_list in config.values():
            if isinstance(comp_list, list):
                for comp in comp_list:
                    if isinstance(comp, dict):
                        platform = comp.get("platform", "")
                        if platform and "." in platform:
                            custom.add(platform)

        return list(custom)

    def _extract_external_libs(self, config: dict) -> list[str]:
        """Extract external library dependencies."""
        libs = set()

        # Check for libraries in esphome section
        if "esphome" in config and isinstance(config["esphome"], dict):
            libs_config = config["esphome"].get("libraries", [])
            if isinstance(libs_config, list):
                libs.update(libs_config)
            elif isinstance(libs_config, str):
                libs.add(libs_config)

        # Check for platformio libs
        if "platformio" in config and isinstance(config["platformio"], dict):
            pio_libs = config["platformio"].get("lib_deps", [])
            if isinstance(pio_libs, list):
                libs.update(pio_libs)
            elif isinstance(pio_libs, str):
                libs.add(pio_libs)

        return list(libs)

    def _assess_complexity(
        self,
        config: dict,
        components: list[ESPHomeComponent],
        custom_components: list[str],
    ) -> ComplexityLevel:
        """Assess configuration complexity."""
        factors = 0

        # Number of components
        if len(components) > 30:
            factors += 3
        elif len(components) > 15:
            factors += 2
        elif len(components) > 5:
            factors += 1

        # Custom components
        if len(custom_components) > 5:
            factors += 2
        elif len(custom_components) > 1:
            factors += 1

        # Advanced features
        advanced_keys = {
            "lambda", "script", "automation", "deep_sleep", "web_server",
            "bluetooth_proxy", "voice_assistant", "esp32_camera",
            "i2s_audio", "display", "touchscreen", "canbus",
        }
        factors += sum(1 for k in advanced_keys if k in config)

        # Multiple devices / variants
        device_count = sum(1 for k in ("esp32", "esp8266", "rp2040") if k in config)
        if device_count > 1:
            factors += 1

        # Substitutions / packages (modularity)
        if "substitutions" in config:
            factors += 1
        if "packages" in config:
            factors += 1

        if factors >= 8:
            return ComplexityLevel.EXPERT
        elif factors >= 5:
            return ComplexityLevel.HIGH
        elif factors >= 3:
            return ComplexityLevel.MEDIUM
        return ComplexityLevel.LOW

    def _detect_focus_areas(
        self,
        components: list[ESPHomeComponent],
        config: dict,
    ) -> list[FocusArea]:
        """Detect focus areas from components and config."""
        areas = set()
        all_text = " ".join([
            c.type for c in components
        ] + [c.platform or "" for c in components] + [c.name for c in components]).lower()

        config_text = str(config).lower()

        for area, keywords in FOCUS_AREA_KEYWORDS.items():
            if any(kw in all_text for kw in keywords) or any(kw in config_text for kw in keywords):
                areas.add(area)

        return list(areas) if areas else [FocusArea.UNKNOWN]
