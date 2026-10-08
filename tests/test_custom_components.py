"""Keep all supported custom component sources in the public YAML analysis."""

import pytest

from iot_profile_builder.analyzers.esphome_analyzer import ESPHomeAnalyzer


def test_custom_sources_and_platforms_are_combined_without_duplicates() -> None:
    analysis = ESPHomeAnalyzer().analyze_content(
        """
esphome:
  name: example
external_components:
  - source: github://example/components
    components: [battery_driver, shared_driver]
  - github://example/other
  - components: [shared_driver]
sensor:
  - platform: custom.battery
  - platform: template
binary_sensor:
  - platform: custom.battery
  - platform: custom.switch
""",
        "example.yaml",
    )
    assert set(analysis.custom_components) == {
        "battery_driver",
        "shared_driver",
        "github://example/other",
        "custom.battery",
        "custom.switch",
    }
    assert len(analysis.custom_components) == 5


@pytest.mark.parametrize("external", ["null", "42", "{}", "[]"])
def test_non_list_external_sources_do_not_hide_custom_platforms(external: str) -> None:
    analysis = ESPHomeAnalyzer().analyze_content(
        "esphome: {name: example}\n"
        f"external_components: {external}\n"
        "sensor:\n  - platform: custom.battery\n",
        "example.yaml",
    )
    assert analysis.custom_components == ["custom.battery"]
