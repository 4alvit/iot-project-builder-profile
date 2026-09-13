# IoT Engineering Profile: 4alvit

*Generated: 2026-09-10 04:57*

## Summary

The developer demonstrates a strong specialization in the Victron Venus OS ecosystem, building extensive middleware that connects D-Bus services, MQTT, and Home Assistant. Their work includes ESPHome-based BLE sensor patterns for battery management, MQTT-to-DBus bridges for JBD and Daly BMS, and observability stacks using OpenTelemetry, Prometheus, and Grafana. They have produced full-stack solutions for solar forecasting, inverter control, and energy management, often layering Python backends with frontend dashboards in Go, Rust, and Vue.

Beyond the Venus OS focus, they exhibit solid skills in data pipeline construction, utilizing InfluxDB, TimescaleDB, and LangChain-based RAG pipelines for energy data. Their projects consistently integrate MQTT as a communication backbone, and they have implemented edge‑computing patterns via Docker Compose and containerized services. While their embedded firmware work is primarily YAML‑based ESPHome configurations, they show capability in systems programming with Go and Rust for performance‑critical dashboards.

Overall, the developer is an adept IoT systems integrator who excels at gluing together hardware, protocols, and cloud‑native services to create reliable, observable energy‑management solutions. Their breadth spans from low‑level BLE sensor parsing to high‑level forecasting workflows, indicating a versatile full‑stack IoT engineer.

---

## 📊 Repository Overview

- **Total Repositories Analyzed**: 76
- **IoT-Related Repositories**: 31
- **ESPHome Configurations**: 13
- **D-Bus Services**: 32

### Complexity Distribution


- **Low**: 38

- **Medium**: 37

- **High**: 1


---

## 🎯 Focus Areas


### Home Automation: 20.0%

![home_automation](home_automation_chart.png)

### Industrial Iot: 0.0%

![industrial_iot](industrial_iot_chart.png)

### Energy Management: 70.0%

![energy_management](energy_management_chart.png)

### Battery Management: 15.0%

![battery_management](battery_management_chart.png)

### Environmental Monitoring: 10.0%

![environmental_monitoring](environmental_monitoring_chart.png)

### Voice Assistant: 20.0%

![voice_assistant](voice_assistant_chart.png)

### Networking Protocols: 95.0%

![networking_protocols](networking_protocols_chart.png)

### Edge Computing: 25.0%

![edge_computing](edge_computing_chart.png)

### Firmware Development: 10.0%

![firmware_development](firmware_development_chart.png)

### Data Pipeline: 80.0%

![data_pipeline](data_pipeline_chart.png)

### Unknown: 5.0%

![unknown](unknown_chart.png)


---

## 🛠️ Skills Assessment

| Skill | Category | Proficiency | Confidence | Evidence |
|-------|----------|-------------|------------|----------|

| Python | python_iot | 9/10 | 95.0% | fastapi-mqtt-gateway, energy-data-rag-pipeline, solar-forecast-langgraph, mqtt-observability-opentelemetry, mcp-venus-os, dbus-service-template, dbus-mqtt-battery, dbus-tasmota-pv, esphome-jbd-bms-mqtt, inverter-control, inverter-dashboard, inverter-monitoring, inverter-dashboard-go, inverter-desktop, venus-os-observability, dbus-event-log |

| MQTT | protocols_networking | 9/10 | 90.0% | fastapi-mqtt-gateway, mqtt-observability-opentelemetry, esphome-ble-sensor-patterns, esphome-jbd-bms-mqtt, inverter-control, inverter-dashboard, inverter-dashboard-go, inverter-desktop, venus-os-observability, dbus-event-log |

| Energy Systems (Solar, Inverter, Victron) | energy_systems | 9/10 | 90.0% | solar-forecast-langgraph, inverter-control, inverter-dashboard, inverter-monitoring, inverter-dashboard-go, inverter-desktop, venus-os-observability, dbus-event-log, dbus-tasmota-pv, fastapi-mqtt-gateway |

| D-Bus | protocols_networking | 8/10 | 85.0% | dbus-service-template, dbus-mqtt-battery, dbus-tasmota-pv, venus-os-observability, dbus-event-log, mcp-venus-os |

| ESPHome / Home Assistant | home_automation | 8/10 | 80.0% | esphome-ble-sensor-patterns, esphome-jbd-bms-mqtt, inverter-control, inverter-dashboard-go, inverter-desktop |

| Battery Management / BMS | energy_systems | 8/10 | 75.0% | esphome-ble-sensor-patterns, dbus-mqtt-battery, esphome-jbd-bms-mqtt |

| Data Pipeline (InfluxDB, TimescaleDB, Prometheus, Grafana, Telegraf) | data_pipeline | 8/10 | 85.0% | inverter-monitoring, venus-os-observability, dbus-event-log, energy-data-rag-pipeline, fastapi-mqtt-gateway, solar-forecast-langgraph |

| Edge Computing (Docker / Containers) | edge_computing | 7/10 | 80.0% | mqtt-observability-opentelemetry, inverter-dashboard, inverter-monitoring, inverter-dashboard-go, inverter-desktop |

| Go | edge_computing | 6/10 | 60.0% | inverter-dashboard-go |

| Rust | edge_computing | 6/10 | 60.0% | inverter-desktop |

| Voice Assistant Integration | voice_ai | 5/10 | 70.0% | esphome-ble-sensor-patterns, inverter-control, inverter-dashboard-go, inverter-desktop |


---

## 💪 Key Strengths


- Deep expertise in Victron Venus OS D-Bus and MQTT bridging

- ESPHome BLE sensor patterns for battery‑powered devices

- End‑to‑end observability stacks (OpenTelemetry, Prometheus, Grafana)

- Solar forecasting and energy‑management workflows using LangGraph

- Full‑stack dashboard development across Python, Go, Rust, and Vue


---

## 📈 Growth Areas


- Industrial IoT protocols (Modbus, CANbus, OPC-UA)

- Low‑level embedded firmware in C/C++/Rust (ESP-IDF, Zephyr)

- Kubernetes/K3s edge orchestration beyond Docker Compose

- Advanced voice AI integration (wake word, offline STT/TTS)

- Expanding into Matter/Thread for broader home‑automation interoperability


---

## 🏆 Top Repositories


### esphome-ble-sensor-patterns

- **Description**: Production-ready patterns for ESPHome BLE sensors — iBeacon, Eddystone, and custom BLE service parsing with lambda filters. Covers ESP32 Bluetooth proxy, passive scanning, and Home Assistant integration for battery-powered sensors.
- **Language**: N/A
- **Stars**: 0 ⭐ | **Forks**: 0
- **IoT Score**: 1.00
- **Complexity**: medium
- **Focus Areas**: home_automation, energy_management, battery_management, voice_assistant, networking_protocols, firmware_development, data_pipeline
- **Topics**: ble, bms, esp32, esphome, plant-sensor, reference-implementation, bluetooth-low-energy, bluetooth-proxy, home-assistant, iot, lambda, passive-scanning, sensor, ibeacon, battery, bluetooth, energy, firmware, mqtt, power

### dbus-mqtt-battery

- **Description**: MQTT to D-Bus bridge for JBD BMS batteries on Victron Venus OS with DVCC support
- **Language**: Python
- **Stars**: 0 ⭐ | **Forks**: 1
- **IoT Score**: 1.00
- **Complexity**: medium
- **Focus Areas**: energy_management, battery_management, networking_protocols, data_pipeline
- **Topics**: bms, dbus, lifepo4, mqtt, python, venus-os, victron, battery-management, cerbo-gx, dvcc, jbd-bms, battery, energy, power, sensor, solar

### dbus-tasmota-pv

- **Description**: Tasmota power meter to Victron D-Bus PV inverter bridge for Venus OS
- **Language**: Python
- **Stars**: 0 ⭐ | **Forks**: 1
- **IoT Score**: 1.00
- **Complexity**: medium
- **Focus Areas**: energy_management, networking_protocols, data_pipeline
- **Topics**: dbus, mqtt, python, solar, tasmota, venus-os, victron, pv-inverter, energy, inverter, meter, power, sensor

### esphome-jbd-bms-mqtt

- **Description**: ESPHome ESP32 Bluetooth proxy for JBD BMS batteries, publishing to MQTT for Victron Venus OS
- **Language**: YAML
- **Stars**: 1 ⭐ | **Forks**: 1
- **IoT Score**: 1.00
- **Complexity**: medium
- **Focus Areas**: energy_management, battery_management, networking_protocols, data_pipeline
- **Topics**: bluetooth, esp32, esphome, jbd-bms, lifepo4, mqtt, venus-os, victron, battery-monitor, cerbo-gx, battery, ble, bms, energy, sensor

### inverter-control

- **Description**: Grid-zero feed-in control for Victron inverters with Home Assistant integration and web dashboard
- **Language**: Python
- **Stars**: 0 ⭐ | **Forks**: 1
- **IoT Score**: 1.00
- **Complexity**: medium
- **Focus Areas**: home_automation, energy_management, voice_assistant, networking_protocols, data_pipeline
- **Topics**: dbus, energy-management, grid-tie, home-assistant, python, raspberry-pi, solar, cerbo-gx, emporia-vue, hass, quattro, ess, external-control, mqtt, battery, energy, inverter, meter, power, sensor

### inverter-monitoring

- **Description**: Telegraf + InfluxDB + Grafana monitoring stack for Victron inverter systems
- **Language**: Python
- **Stars**: 0 ⭐ | **Forks**: 1
- **IoT Score**: 1.00
- **Complexity**: medium
- **Focus Areas**: energy_management, networking_protocols, edge_computing, data_pipeline
- **Topics**: cerbo-gx, docker, energy-monitoring, grafana, influxdb, iot, mqtt, telegraf, time-series, venus-os, victron, python, battery, dbus, energy, inverter, meter, power, sensor, solar

### inverter-dashboard-go

- **Description**: Real-time Victron inverter web dashboard (Go) — same role as inverter-dashboard, implemented in Go with MQTT and optional Home Assistant direct control
- **Language**: Go
- **Stars**: 0 ⭐ | **Forks**: 1
- **IoT Score**: 1.00
- **Complexity**: medium
- **Focus Areas**: home_automation, energy_management, voice_assistant, networking_protocols, edge_computing, data_pipeline
- **Topics**: cerbo-gx, dashboard, docker, go, golang, hass, home-assistant, mqtt, real-time, venus-os, victron, websocket, battery, energy, inverter, power, sensor, solar

### inverter-desktop

- **Description**: Desktop version of Web dashboard for Victron inverter control with Home Assistant integration
- **Language**: Rust
- **Stars**: 0 ⭐ | **Forks**: 1
- **IoT Score**: 1.00
- **Complexity**: high
- **Focus Areas**: home_automation, energy_management, voice_assistant, networking_protocols, data_pipeline
- **Topics**: cerbo-gx, dashboard, energy-management, grid-tie, hass, home-assistant, mqtt, venus-os, victron, web-dashboard, battery, energy, inverter, power, sensor, solar

### venus-os-observability

- **Description**: OpenTelemetry/Prometheus observability for Venus OS — D-Bus event tracing, inverter metrics, distributed tracing
- **Language**: Python
- **Stars**: 0 ⭐ | **Forks**: 0
- **IoT Score**: 1.00
- **Complexity**: medium
- **Focus Areas**: energy_management, networking_protocols, data_pipeline
- **Topics**: cerbo-gx, dbus, distributed-tracing, grafana, mqtt, opentelemetry, prometheus, tempo, venus-os, victron, python, energy, inverter, power, sensor, solar

### dbus-esphome-grid-sensor

- **Description**: ESP32 CT sensor for grid power monitoring with D-Bus service for Venus OS
- **Language**: Python
- **Stars**: 0 ⭐ | **Forks**: 0
- **IoT Score**: 1.00
- **Complexity**: medium
- **Focus Areas**: energy_management, networking_protocols, edge_computing, data_pipeline
- **Topics**: ct-sensor, dbus, docker, esp32, esphome, grid-meter, home-automation, mqtt, python, venus-os, victron, energy, grid, meter, power, sensor, solar


---

## 🔧 ESPHome Configurations


### 4alvit/esphome-ble-sensor-patterns/patterns/ble-temp-sensor/generic-ble-temp.yaml

- **Devices**: esp32:esp32dev
- **Components**: 14
- **Custom Components**: None
- **External Libraries**: None
- **Complexity**: low
- **Focus Areas**: environmental_monitoring, networking_protocols, home_automation, energy_management, firmware_development, battery_management

**Component Breakdown**:

- logger: unnamed

- ota (esphome): unnamed

- binary_sensor (status): ESP32 Status

- wifi: unnamed

- api: unnamed

- web_server: unnamed

- mqtt: unnamed

- sensor (ble_client): unnamed

- sensor (template): Temperature

- sensor (template): Humidity

- sensor (template): Battery

- sensor (uptime): Uptime

- sensor (wifi_signal): WiFi Signal

- esp32_ble_tracker: unnamed


### 4alvit/esphome-ble-sensor-patterns/patterns/ble-temp-sensor/inkbird-ibs-th1.yaml

- **Devices**: esp32:esp32dev
- **Components**: 13
- **Custom Components**: None
- **External Libraries**: None
- **Complexity**: low
- **Focus Areas**: environmental_monitoring, networking_protocols, home_automation, energy_management, firmware_development, battery_management

**Component Breakdown**:

- logger: unnamed

- ota (esphome): unnamed

- binary_sensor (status): ESP32 Status

- wifi: unnamed

- api: unnamed

- web_server: unnamed

- mqtt: unnamed

- sensor (template): Inkbird Temperature

- sensor (template): Inkbird Humidity

- sensor (template): Inkbird Battery

- sensor (uptime): Uptime

- sensor (wifi_signal): WiFi Signal

- esp32_ble_tracker: unnamed


### 4alvit/esphome-ble-sensor-patterns/patterns/ble-temp-sensor/xiaomi-lywsd03mmc.yaml

- **Devices**: esp32:esp32dev
- **Components**: 12
- **Custom Components**: xiaomi_ble
- **External Libraries**: None
- **Complexity**: low
- **Focus Areas**: environmental_monitoring, networking_protocols, home_automation, energy_management, firmware_development, battery_management

**Component Breakdown**:

- logger: unnamed

- ota (esphome): unnamed

- binary_sensor (status): ESP32 Status

- wifi: unnamed

- button (restart): Restart

- api: unnamed

- web_server: unnamed

- mqtt: unnamed

- sensor (xiaomi_ble): unnamed

- sensor (wifi_signal): WiFi Signal

- sensor (uptime): Uptime

- esp32_ble_tracker: unnamed


### 4alvit/esphome-ble-sensor-patterns/patterns/daly-bms/multi-bms.yaml

- **Devices**: esp32:esp32dev
- **Components**: 21
- **Custom Components**: daly_bms_ble
- **External Libraries**: None
- **Complexity**: medium
- **Focus Areas**: environmental_monitoring, networking_protocols, home_automation, energy_management, firmware_development, battery_management

**Component Breakdown**:

- logger: unnamed

- ota (esphome): unnamed

- binary_sensor (daly_bms_ble): unnamed

- binary_sensor (daly_bms_ble): unnamed

- binary_sensor (daly_bms_ble): unnamed

- binary_sensor (status): ESP32 Status

- wifi: unnamed

- esp32_ble: unnamed

- api: unnamed

- ble_client: unnamed

- ble_client: unnamed

- ble_client: unnamed

- web_server: unnamed

- interval: unnamed

- mqtt: unnamed

- sensor (daly_bms_ble): unnamed

- sensor (daly_bms_ble): unnamed

- sensor (daly_bms_ble): unnamed

- sensor (wifi_signal): WiFi Signal

- sensor (uptime): Uptime

- esp32_ble_tracker: unnamed


### 4alvit/esphome-ble-sensor-patterns/patterns/daly-bms/single-bms.yaml

- **Devices**: esp32:esp32dev
- **Components**: 17
- **Custom Components**: daly_bms_ble
- **External Libraries**: None
- **Complexity**: medium
- **Focus Areas**: environmental_monitoring, networking_protocols, home_automation, energy_management, firmware_development, battery_management

**Component Breakdown**:

- logger: unnamed

- ota (esphome): unnamed

- binary_sensor (daly_bms_ble): unnamed

- binary_sensor (daly_bms_ble): unnamed

- binary_sensor (status): ESP32 Status

- wifi: unnamed

- button (restart): Restart

- api: unnamed

- ble_client: unnamed

- web_server: unnamed

- mqtt: unnamed

- sensor (daly_bms_ble): unnamed

- sensor (daly_bms_ble): unnamed

- sensor (daly_bms_ble): unnamed

- sensor (wifi_signal): WiFi Signal

- sensor (uptime): Uptime

- esp32_ble_tracker: unnamed


### 4alvit/esphome-ble-sensor-patterns/patterns/jbd-bms/multi-bms.yaml

- **Devices**: esp32:esp32dev
- **Components**: 25
- **Custom Components**: jbd_bms_ble
- **External Libraries**: None
- **Complexity**: medium
- **Focus Areas**: environmental_monitoring, networking_protocols, home_automation, energy_management, firmware_development, battery_management

**Component Breakdown**:

- logger: unnamed

- ota (esphome): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (status): ESP32 Status

- wifi: unnamed

- button (restart): Restart

- esp32_ble: unnamed

- api: unnamed

- ble_client: unnamed

- ble_client: unnamed

- ble_client: unnamed

- web_server: unnamed

- interval: unnamed

- mqtt: unnamed

- sensor (jbd_bms_ble): unnamed

- sensor (jbd_bms_ble): unnamed

- sensor (jbd_bms_ble): unnamed

- sensor (wifi_signal): WiFi Signal

- sensor (uptime): Uptime

- sensor (template): Total Voltage (All)

- sensor (template): Total Power (All)

- sensor (template): Min SOC (All)

- esp32_ble_tracker: unnamed


### 4alvit/esphome-ble-sensor-patterns/patterns/jbd-bms/single-bms.yaml

- **Devices**: esp32:esp32dev
- **Components**: 16
- **Custom Components**: jbd_bms_ble
- **External Libraries**: None
- **Complexity**: medium
- **Focus Areas**: environmental_monitoring, networking_protocols, home_automation, energy_management, firmware_development, battery_management

**Component Breakdown**:

- logger: unnamed

- ota (esphome): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (status): ESP32 Status

- wifi: unnamed

- button (restart): Restart

- api: unnamed

- ble_client: unnamed

- web_server: unnamed

- mqtt: unnamed

- sensor (jbd_bms_ble): unnamed

- sensor (jbd_bms_ble): unnamed

- sensor (jbd_bms_ble): unnamed

- sensor (wifi_signal): WiFi Signal

- sensor (uptime): Uptime

- esp32_ble_tracker: unnamed


### 4alvit/esphome-ble-sensor-patterns/patterns/xiaomi-mi-flora/mi-flora.yaml

- **Devices**: esp32:esp32dev
- **Components**: 17
- **Custom Components**: xiaomi_ble
- **External Libraries**: None
- **Complexity**: medium
- **Focus Areas**: environmental_monitoring, networking_protocols, home_automation, energy_management, firmware_development, battery_management

**Component Breakdown**:

- logger: unnamed

- ota (esphome): unnamed

- binary_sensor (status): ESP32 Status

- wifi: unnamed

- api: unnamed

- ble_client: unnamed

- web_server: unnamed

- mqtt: unnamed

- sensor (xiaomi_ble): unnamed

- sensor (xiaomi_ble): unnamed

- sensor (xiaomi_ble): unnamed

- sensor (xiaomi_ble): unnamed

- sensor (xiaomi_ble): unnamed

- sensor (xiaomi_ble): unnamed

- sensor (uptime): Uptime

- sensor (wifi_signal): WiFi Signal

- esp32_ble_tracker: unnamed


### victron-venus/esphome-jbd-bms-mqtt/jbd-all-batteries.yaml

- **Devices**: esp32:esp32dev
- **Components**: 47
- **Custom Components**: jbd_bms_ble
- **External Libraries**: None
- **Complexity**: medium
- **Focus Areas**: environmental_monitoring, networking_protocols, home_automation, energy_management, firmware_development, battery_management

**Component Breakdown**:

- logger: unnamed

- ota (esphome): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (status): esp32_status

- wifi: unnamed

- button (restart): restart

- esp32_ble: unnamed

- api: unnamed

- ble_client: unnamed

- ble_client: unnamed

- ble_client: unnamed

- ble_client: unnamed

- ble_client: unnamed

- ble_client: unnamed

- ble_client: unnamed

- ble_client: unnamed

- web_server: unnamed

- interval: unnamed

- mqtt: unnamed

- sensor (jbd_bms_ble): unnamed

- sensor (jbd_bms_ble): unnamed

- sensor (jbd_bms_ble): unnamed

- sensor (jbd_bms_ble): unnamed

- sensor (jbd_bms_ble): unnamed

- sensor (jbd_bms_ble): unnamed

- sensor (jbd_bms_ble): unnamed

- sensor (jbd_bms_ble): unnamed

- sensor (wifi_signal): wifi_signal

- sensor (uptime): uptime

- sensor (template): voltage_total_c1

- sensor (template): power_total_c1

- sensor (template): current_total_c1

- sensor (template): soc_total_c1

- sensor (template): capacity_total_c1

- sensor (template): voltage_total_c2

- sensor (template): power_total_c2

- sensor (template): current_total_c2

- sensor (template): soc_total_c2

- sensor (template): capacity_total_c2

- esp32_ble_tracker: unnamed


### victron-venus/esphome-jbd-bms-mqtt/jbd-all-batteries1.yaml

- **Devices**: esp32:esp32dev
- **Components**: 30
- **Custom Components**: jbd_bms_ble
- **External Libraries**: None
- **Complexity**: medium
- **Focus Areas**: environmental_monitoring, networking_protocols, home_automation, energy_management, firmware_development, battery_management

**Component Breakdown**:

- logger: unnamed

- ota (esphome): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (status): esp32_status

- wifi: unnamed

- button (restart): restart

- esp32_ble: unnamed

- api: unnamed

- ble_client: unnamed

- ble_client: unnamed

- ble_client: unnamed

- ble_client: unnamed

- web_server: unnamed

- mqtt: unnamed

- sensor (jbd_bms_ble): unnamed

- sensor (jbd_bms_ble): unnamed

- sensor (jbd_bms_ble): unnamed

- sensor (jbd_bms_ble): unnamed

- sensor (wifi_signal): wifi_signal

- sensor (uptime): uptime

- sensor (template): voltage_total

- sensor (template): power_total

- sensor (template): current_total

- sensor (template): soc_total

- sensor (template): capacity_total

- esp32_ble_tracker: unnamed

- script: unnamed


### victron-venus/esphome-jbd-bms-mqtt/jbd-all-batteries2.yaml

- **Devices**: esp32:esp32dev
- **Components**: 30
- **Custom Components**: jbd_bms_ble
- **External Libraries**: None
- **Complexity**: medium
- **Focus Areas**: environmental_monitoring, networking_protocols, home_automation, energy_management, firmware_development, battery_management

**Component Breakdown**:

- logger: unnamed

- ota (esphome): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (status): esp32_status

- wifi: unnamed

- button (restart): restart

- esp32_ble: unnamed

- api: unnamed

- ble_client: unnamed

- ble_client: unnamed

- ble_client: unnamed

- ble_client: unnamed

- web_server: unnamed

- mqtt: unnamed

- sensor (jbd_bms_ble): unnamed

- sensor (jbd_bms_ble): unnamed

- sensor (jbd_bms_ble): unnamed

- sensor (jbd_bms_ble): unnamed

- sensor (wifi_signal): wifi_signal

- sensor (uptime): uptime

- sensor (template): voltage_total

- sensor (template): power_total

- sensor (template): current_total

- sensor (template): soc_total

- sensor (template): capacity_total

- esp32_ble_tracker: unnamed

- script: unnamed


### victron-venus/dbus-esphome-grid-sensor/esphome/grid-sensor.yaml

- **Devices**: esp32:esp32dev
- **Components**: 16
- **Custom Components**: None
- **External Libraries**: None
- **Complexity**: low
- **Focus Areas**: energy_management, networking_protocols, home_automation, firmware_development

**Component Breakdown**:

- logger: unnamed

- ota (esphome): unnamed

- binary_sensor (status): Grid Sensor Status

- binary_sensor (template): Grid Feed-In Active

- wifi: unnamed

- button (restart): Grid Sensor Restart

- button (template): Toggle Calibration Mode

- api: unnamed

- i2c: unnamed

- mqtt: unnamed

- sensor (adc): Grid Current

- sensor (template): Grid Power

- sensor (integration): Grid Energy Forward

- sensor (integration): Grid Energy Reverse

- light (binary): Grid Sensor LED

- switch (template): MQTT Publishing


### victron-venus/dbus-esphome-grid-sensor/docker-compose.yml

- **Devices**: 
- **Components**: 0
- **Custom Components**: None
- **External Libraries**: None
- **Complexity**: low
- **Focus Areas**: networking_protocols, home_automation

**Component Breakdown**:



---

## 📡 D-Bus Services


### com.victronenergy.battery.

- **Interfaces**: 1
- **Object Paths**: /Alarms/CellImbalance, /Alarms/CommunicationError, /Alarms/HighCellVoltage, /Alarms/HighTemperature, /Alarms/HighVoltage, /Alarms/InternalFailure, /Alarms/LowCellVoltage, /Alarms/LowSoc, /Alarms/LowTemperature, /Alarms/LowVoltage, /Capacity, /Connected, /ConsumedAmphours, /Dc/0/Temperature, /History/ChargeCycles, /Info/MaxChargeCellVoltage, /Info/MaxChargeCurrent, /Info/MaxChargeVoltage, /Info/MaxDischargeCurrent, /InstalledCapacity, /Io/AllowToBalance, /Io/AllowToCharge, /Io/AllowToDischarge, /Soc, /System/BatteriesParallel, /System/BatteriesSeries, /System/MOSTemperature, /System/MaxCellTemperature, /System/MaxCellVoltage, /System/MaxTemperatureCellId, /System/MaxVoltageCellId, /System/MinCellTemperature, /System/MinCellVoltage, /System/MinTemperatureCellId, /System/MinVoltageCellId, /System/NrOfBatteries, /System/NrOfCells, /System/NrOfCellsPerBattery, /System/NrOfModulesBlockingCharge, /System/NrOfModulesBlockingDischarge, /System/NrOfModulesOffline, /System/NrOfModulesOnline, /System/StaleData, /Voltages/Diff, /Voltages/Sum
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 40
- **Complexity**: medium
- **Focus Areas**: energy_management, networking_protocols, battery_management

**Interfaces**:

#### com.victronenergy.battery. (/Alarms/CellImbalance)
- Methods: None
- Signals: None
- Properties: /Alarms/CellImbalance, /Alarms/CommunicationError, /Alarms/HighCellVoltage, /Alarms/HighTemperature, /Alarms/HighVoltage, /Alarms/InternalFailure, /Alarms/LowCellVoltage, /Alarms/LowSoc, /Alarms/LowTemperature, /Alarms/LowVoltage, /Capacity, /Connected, /ConsumedAmphours, /Dc/0/Temperature, /History/ChargeCycles, /Info/MaxChargeCellVoltage, /Info/MaxChargeCurrent, /Info/MaxChargeVoltage, /Info/MaxDischargeCurrent, /InstalledCapacity, /Io/AllowToBalance, /Io/AllowToCharge, /Io/AllowToDischarge, /Soc, /System/BatteriesParallel, /System/BatteriesSeries, /System/MOSTemperature, /System/MaxCellTemperature, /System/MaxCellVoltage, /System/MaxTemperatureCellId, /System/MaxVoltageCellId, /System/MinCellTemperature, /System/MinCellVoltage, /System/MinTemperatureCellId, /System/MinVoltageCellId, /System/NrOfBatteries, /System/NrOfCells, /System/NrOfCellsPerBattery, /System/NrOfModulesBlockingCharge, /System/NrOfModulesBlockingDischarge


### dbus_utils

- **Interfaces**: 1
- **Object Paths**: /Connected, /CustomName, /Dc/0/Current, /Dc/0/Power, /Dc/0/Temperature, /Dc/0/Voltage, /DeviceInstance, /FirmwareVersion, /HardwareVersion, /Mgmt/Connection, /Mgmt/ProcessName, /Mgmt/ProcessVersion, /ProductId, /ProductName, /TimeToGo
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 15
- **Complexity**: low
- **Focus Areas**: energy_management, networking_protocols, battery_management

**Interfaces**:

#### com.victronenergy.dbus_utils (/Connected)
- Methods: None
- Signals: None
- Properties: /Connected, /CustomName, /Dc/0/Current, /Dc/0/Power, /Dc/0/Temperature, /Dc/0/Voltage, /DeviceInstance, /FirmwareVersion, /HardwareVersion, /Mgmt/Connection, /Mgmt/ProcessName, /Mgmt/ProcessVersion, /ProductId, /ProductName, /TimeToGo


### com.victronenergy.pvinverter.tasmota_

- **Interfaces**: 1
- **Object Paths**: /Ac/Energy/Daily, /Ac/Energy/Forward, /Ac/L1/Current, /Ac/L1/Power, /Ac/L1/Voltage, /Ac/Power, /Connected, /CustomName, /DeviceInstance, /Energy/Daily/Yesterday, /ErrorCode, /FirmwareVersion, /Mgmt/ProcessName, /Mgmt/ProcessVersion, /Position, /ProductId, /ProductName, /Serial
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 18
- **Complexity**: medium
- **Focus Areas**: energy_management, networking_protocols, home_automation

**Interfaces**:

#### com.victronenergy.pvinverter.tasmota_ (/Ac/Energy/Daily)
- Methods: None
- Signals: None
- Properties: /Ac/Energy/Daily, /Ac/Energy/Forward, /Ac/L1/Current, /Ac/L1/Power, /Ac/L1/Voltage, /Ac/Power, /Connected, /CustomName, /DeviceInstance, /Energy/Daily/Yesterday, /ErrorCode, /FirmwareVersion, /Mgmt/ProcessName, /Mgmt/ProcessVersion, /Position, /ProductId, /ProductName, /Serial


### com.victronenergy.acload.

- **Interfaces**: 1
- **Object Paths**: /Ac/Power, /CustomName, /org/freedesktop/DBus
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 3
- **Complexity**: low
- **Focus Areas**: energy_management, home_automation

**Interfaces**:

#### com.victronenergy.acload. (/Ac/Power)
- Methods: None
- Signals: None
- Properties: /Ac/Power, /CustomName, /org/freedesktop/DBus


### com.victronenergy.BusItem

- **Interfaces**: 1
- **Object Paths**: /org/freedesktop/DBus, {path}
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 2
- **Complexity**: low
- **Focus Areas**: energy_management, home_automation, battery_management

**Interfaces**:

#### com.victronenergy.BusItem (/org/freedesktop/DBus)
- Methods: None
- Signals: None
- Properties: /org/freedesktop/DBus, {path}


### com.victronenergy.tank.ha_tank

- **Interfaces**: 1
- **Object Paths**: /Ac/Power, /Soc, /sys/class/net/eth0/address
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 3
- **Complexity**: low
- **Focus Areas**: energy_management, networking_protocols, home_automation, battery_management

**Interfaces**:

#### com.victronenergy.tank.ha_tank (/Ac/Power)
- Methods: None
- Signals: None
- Properties: /Ac/Power, /Soc, /sys/class/net/eth0/address


### com.victronenergy.evcharger.

- **Interfaces**: 1
- **Object Paths**: /Ac/L1/Voltage, /Ac/Power, /Current, /Mgmt/Connection, /Soc, /VIN
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 6
- **Complexity**: low
- **Focus Areas**: energy_management, battery_management

**Interfaces**:

#### com.victronenergy.evcharger. (/Ac/L1/Voltage)
- Methods: None
- Signals: None
- Properties: /Ac/L1/Voltage, /Ac/Power, /Current, /Mgmt/Connection, /Soc, /VIN


### com.victronenergy.settings

- **Interfaces**: 1
- **Object Paths**: /Ac/Consumption/L1/Power, /Ac/Consumption/L2/Power, /Ac/Energy/Daily, /Ac/Energy/Forward, /Ac/Grid/L1/Power, /Ac/Grid/L2/Power, /Ac/Power, /CustomName, /Dc/0/Current, /Dc/0/Power, /Dc/0/Voltage, /Dc/Battery/Soc, /Dc/Pv/Power, /Devices/0/Ac/Inverter/P, /Energy/Daily/Yesterday, /History/Daily/0/Yield, /History/Daily/1/Yield, /Hub4/L1/AcPowerSetpoint, /Info/AllowCharge, /Info/AllowDischarge, /ProductName, /Pv/V, /Settings, /Settings/CGwacs/BatteryLife/State, /Settings/InverterControl/TouExpensiveEndHour, /Settings/InverterControl/TouExpensiveStartHour, /Settings/System/TimeZone, /Soc, /State, /TimeToGo, /Yield/Power
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 31
- **Complexity**: medium
- **Focus Areas**: energy_management, networking_protocols, home_automation, battery_management

**Interfaces**:

#### com.victronenergy.settings (/Ac/Consumption/L1/Power)
- Methods: None
- Signals: None
- Properties: /Ac/Consumption/L1/Power, /Ac/Consumption/L2/Power, /Ac/Energy/Daily, /Ac/Energy/Forward, /Ac/Grid/L1/Power, /Ac/Grid/L2/Power, /Ac/Power, /CustomName, /Dc/0/Current, /Dc/0/Power, /Dc/0/Voltage, /Dc/Battery/Soc, /Dc/Pv/Power, /Devices/0/Ac/Inverter/P, /Energy/Daily/Yesterday, /History/Daily/0/Yield, /History/Daily/1/Yield, /Hub4/L1/AcPowerSetpoint, /Info/AllowCharge, /Info/AllowDischarge, /ProductName, /Pv/V, /Settings, /Settings/CGwacs/BatteryLife/State, /Settings/InverterControl/TouExpensiveEndHour, /Settings/InverterControl/TouExpensiveStartHour, /Settings/System/TimeZone, /Soc, /State, /TimeToGo, /Yield/Power


### com.victronenergy.tank.ha_tank

- **Interfaces**: 1
- **Object Paths**: /Level, /State
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 2
- **Complexity**: low
- **Focus Areas**: energy_management, home_automation

**Interfaces**:

#### com.victronenergy.tank.ha_tank (/Level)
- Methods: None
- Signals: None
- Properties: /Level, /State


### com.victronenergy.BusItem

- **Interfaces**: 1
- **Object Paths**: /, /Ac/Grid/L1/P, /Ac/L1/Power, /Ac/Out/L1/P, /Ac/Power, /CustomName, /Dc/0/Current, /Dc/0/Power, /Dc/0/Temperature, /Dc/0/Voltage, /Soc, /State, /Yield/Power, /org/freedesktop/DBus, {path}
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 15
- **Complexity**: low
- **Focus Areas**: energy_management, battery_management

**Interfaces**:

#### com.victronenergy.BusItem (/)
- Methods: None
- Signals: None
- Properties: /, /Ac/Grid/L1/P, /Ac/L1/Power, /Ac/Out/L1/P, /Ac/Power, /CustomName, /Dc/0/Current, /Dc/0/Power, /Dc/0/Temperature, /Dc/0/Voltage, /Soc, /State, /Yield/Power, /org/freedesktop/DBus, {path}


### com.victronenergy.battery.ttyO1

- **Interfaces**: 1
- **Object Paths**: /ac/grid/power, /ac/loads/power, /ac/power, /dc/0/power, /dc/0/voltages/cell, /dc/pv/power, /power, /soc, /state, /temperatures/cell, /yield/power
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 11
- **Complexity**: low
- **Focus Areas**: energy_management, networking_protocols, battery_management

**Interfaces**:

#### com.victronenergy.battery.ttyO1 (/ac/grid/power)
- Methods: None
- Signals: None
- Properties: /ac/grid/power, /ac/loads/power, /ac/power, /dc/0/power, /dc/0/voltages/cell, /dc/pv/power, /power, /soc, /state, /temperatures/cell, /yield/power


### com.victronenergy.grid

- **Interfaces**: 1
- **Object Paths**: /Ac/Energy/Forward, /Ac/Energy/Reverse, /Ac/Frequency, /Ac/L1/Current, /Ac/L1/Power, /Ac/L1/Voltage, /Ac/Power, /Connected, /CustomName, /DeviceInstance, /ErrorCode, /FirmwareVersion, /HardwareVersion, /Mgmt/Connection, /Mgmt/ProcessName, /Mgmt/ProcessVersion, /ProductId, /ProductName, /Status, /run/dbus-grid-service.pid
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 20
- **Complexity**: medium
- **Focus Areas**: energy_management, networking_protocols

**Interfaces**:

#### com.victronenergy.grid (/Ac/Energy/Forward)
- Methods: None
- Signals: None
- Properties: /Ac/Energy/Forward, /Ac/Energy/Reverse, /Ac/Frequency, /Ac/L1/Current, /Ac/L1/Power, /Ac/L1/Voltage, /Ac/Power, /Connected, /CustomName, /DeviceInstance, /ErrorCode, /FirmwareVersion, /HardwareVersion, /Mgmt/Connection, /Mgmt/ProcessName, /Mgmt/ProcessVersion, /ProductId, /ProductName, /Status, /run/dbus-grid-service.pid


### mqtt_to_dbus

- **Interfaces**: 1
- **Object Paths**: /Connected, /CustomName, /DeviceInstance, /FirmwareVersion, /ProductId, /ProductName
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 6
- **Complexity**: low
- **Focus Areas**: energy_management, networking_protocols

**Interfaces**:

#### com.victronenergy.mqtt_to_dbus (/Connected)
- Methods: None
- Signals: None
- Properties: /Connected, /CustomName, /DeviceInstance, /FirmwareVersion, /ProductId, /ProductName


### com.victronenergy.BusItem

- **Interfaces**: 1
- **Object Paths**: /, /Array, /AsyncItem, /DeviceInstance, /Double, /DoubleArray, /Int, /Text
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 8
- **Complexity**: low
- **Focus Areas**: energy_management

**Interfaces**:

#### com.victronenergy.BusItem (/)
- Methods: None
- Signals: None
- Properties: /, /Array, /AsyncItem, /DeviceInstance, /Double, /DoubleArray, /Int, /Text


### com.victronenergy.BusItem

- **Interfaces**: 3
- **Object Paths**: /, /Double, /Int, /Nothing, /Settings/Vrmlogger/LogInterval, /Text, /org/freedesktop/DBus
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 0
- **Complexity**: low
- **Focus Areas**: energy_management, home_automation

**Interfaces**:

#### com.example.servicehandler (/servicehandler)
- Methods: None
- Signals: None
- Properties: None

#### com.example.gridservice (/gridservice)
- Methods: None
- Signals: None
- Properties: None

#### com.example.settingsservice (/settingsservice)
- Methods: None
- Signals: None
- Properties: None


### com.victronenergy.settings

- **Interfaces**: 1
- **Object Paths**: /Settings, /Settings/AioVelib/OptionA, /Settings/AioVelib/OptionB
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 3
- **Complexity**: low
- **Focus Areas**: energy_management, home_automation

**Interfaces**:

#### com.victronenergy.settings (/Settings)
- Methods: None
- Signals: None
- Properties: /Settings, /Settings/AioVelib/OptionA, /Settings/AioVelib/OptionB


### com.victronenergy.acload.emporia_ch

- **Interfaces**: 1
- **Object Paths**: /api, /states, /websocket, config.json
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 4
- **Complexity**: low
- **Focus Areas**: energy_management, home_automation, battery_management

**Interfaces**:

#### com.victronenergy.acload.emporia_ch (/api)
- Methods: None
- Signals: None
- Properties: /api, /states, /websocket, config.json


### com.victronenergy.acload.

- **Interfaces**: 1
- **Object Paths**: /Ac/Energy/Forward, /Ac/L1/Power, /Ac/Power, /Connected, /CustomName, /DeviceInstance, /FirmwareVersion, /IsGenericEnergyMeter, /Mgmt/Connection, /Mgmt/ProcessName, /Mgmt/ProcessVersion, /Position, /ProductId, /ProductName, /Status
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 15
- **Complexity**: low
- **Focus Areas**: energy_management, networking_protocols, battery_management

**Interfaces**:

#### com.victronenergy.acload. (/Ac/Energy/Forward)
- Methods: None
- Signals: None
- Properties: /Ac/Energy/Forward, /Ac/L1/Power, /Ac/Power, /Connected, /CustomName, /DeviceInstance, /FirmwareVersion, /IsGenericEnergyMeter, /Mgmt/Connection, /Mgmt/ProcessName, /Mgmt/ProcessVersion, /Position, /ProductId, /ProductName, /Status


### monitor

- **Interfaces**: 1
- **Object Paths**: /, /org/freedesktop/DBus
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 2
- **Complexity**: low
- **Focus Areas**: energy_management

**Interfaces**:

#### com.victronenergy.monitor (/)
- Methods: None
- Signals: None
- Properties: /, /org/freedesktop/DBus


### com.victronenergy.battery.

- **Interfaces**: 1
- **Object Paths**: /Alarms/HighTemperature, /Alarms/HighVoltage, /Alarms/InternalFailure, /Alarms/LowSoc, /Alarms/LowTemperature, /Alarms/LowVoltage, /Capacity, /Connected, /ConsumedAmphours, /CustomName, /Info/DataComplete, /Info/MissingSources, /Info/SourceStatus, /InstalledCapacity, /Io/AllowToCharge, /Io/AllowToDischarge, /Soc, /System/BatteriesParallel, /System/BatteriesSeries, /System/MaxCellVoltage, /System/MaxVoltageCellId, /System/MinCellVoltage, /System/MinVoltageCellId, /System/NrOfBatteries, /System/NrOfCellsPerBattery, /System/NrOfModulesBlockingCharge, /System/NrOfModulesBlockingDischarge, /System/NrOfModulesOffline, /System/NrOfModulesOnline, /TimeToGo, /Voltages/Diff, /Voltages/Sum
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 32
- **Complexity**: medium
- **Focus Areas**: energy_management, networking_protocols, home_automation, battery_management

**Interfaces**:

#### com.victronenergy.battery. (/Alarms/HighTemperature)
- Methods: None
- Signals: None
- Properties: /Alarms/HighTemperature, /Alarms/HighVoltage, /Alarms/InternalFailure, /Alarms/LowSoc, /Alarms/LowTemperature, /Alarms/LowVoltage, /Capacity, /Connected, /ConsumedAmphours, /CustomName, /Info/DataComplete, /Info/MissingSources, /Info/SourceStatus, /InstalledCapacity, /Io/AllowToCharge, /Io/AllowToDischarge, /Soc, /System/BatteriesParallel, /System/BatteriesSeries, /System/MaxCellVoltage, /System/MaxVoltageCellId, /System/MinCellVoltage, /System/MinVoltageCellId, /System/NrOfBatteries, /System/NrOfCellsPerBattery, /System/NrOfModulesBlockingCharge, /System/NrOfModulesBlockingDischarge, /System/NrOfModulesOffline, /System/NrOfModulesOnline, /TimeToGo, /Voltages/Diff, /Voltages/Sum


### com.victronenergy.Battery

- **Interfaces**: 1
- **Object Paths**: /org/freedesktop/DBus
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 1
- **Complexity**: low
- **Focus Areas**: energy_management, battery_management

**Interfaces**:

#### com.victronenergy.Battery (/org/freedesktop/DBus)
- Methods: None
- Signals: None
- Properties: /org/freedesktop/DBus


### server

- **Interfaces**: 1
- **Object Paths**: /Level, Dc/0/MaxChargeCurrent, Mode, SocLimit
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 4
- **Complexity**: low
- **Focus Areas**: energy_management, networking_protocols, home_automation, battery_management

**Interfaces**:

#### com.victronenergy.server (/Level)
- Methods: None
- Signals: None
- Properties: /Level, Dc/0/MaxChargeCurrent, Mode, SocLimit


### server

- **Interfaces**: 1
- **Object Paths**: /, /api/settings, /api/state, /api/update, /app/src/inverter_dashboard/static, /assets, /static, /ws
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 8
- **Complexity**: low
- **Focus Areas**: energy_management, networking_protocols, home_automation, battery_management

**Interfaces**:

#### com.victronenergy.server (/)
- Methods: None
- Signals: None
- Properties: /, /api/settings, /api/state, /api/update, /app/src/inverter_dashboard/static, /assets, /static, /ws


### com.victronenergy.tank.

- **Interfaces**: 1
- **Object Paths**: /ActiveTankService, /Capacity, /Connected, /CustomName, /DeviceInstance, /FirmwareVersion, /FluidType, /HardwareVersion, /Level, /Mgmt/Connection, /Mgmt/ProcessName, /Mgmt/ProcessVersion, /Mode, /ProductId, /ProductName, /Remaining, /Serial, /State, /Status
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 19
- **Complexity**: low
- **Focus Areas**: energy_management

**Interfaces**:

#### com.victronenergy.tank. (/ActiveTankService)
- Methods: None
- Signals: None
- Properties: /ActiveTankService, /Capacity, /Connected, /CustomName, /DeviceInstance, /FirmwareVersion, /FluidType, /HardwareVersion, /Level, /Mgmt/Connection, /Mgmt/ProcessName, /Mgmt/ProcessVersion, /Mode, /ProductId, /ProductName, /Remaining, /Serial, /State, /Status


### com.victronenergy.ev.

- **Interfaces**: 1
- **Object Paths**: /Ac/Energy/Forward, /Ac/L1/Current, /Ac/L1/Power, /Ac/L1/Voltage, /Ac/L2/Power, /Ac/L3/Power, /Ac/Power, /AtSite, /BatteryCapacity, /ChargingState, /ChargingTime, /Connected, /Current, /CustomName, /DeviceInstance, /FirmwareVersion, /HardwareVersion, /IsGenericEnergyMeter, /MaxCurrent, /Mgmt/Connection, /Mgmt/ProcessName, /Mgmt/ProcessVersion, /Mode, /NrOfPhases, /Odometer, /Position, /Position/Latitude, /Position/Longitude, /PositionIsAdjustable, /ProductId, /ProductName, /RangeToGo, /Serial, /Session/Energy, /SetCurrent, /Soc, /StartStop, /Status, /TargetSoc, /VIN
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 40
- **Complexity**: medium
- **Focus Areas**: energy_management, networking_protocols, home_automation, battery_management

**Interfaces**:

#### com.victronenergy.ev. (/Ac/Energy/Forward)
- Methods: None
- Signals: None
- Properties: /Ac/Energy/Forward, /Ac/L1/Current, /Ac/L1/Power, /Ac/L1/Voltage, /Ac/L2/Power, /Ac/L3/Power, /Ac/Power, /AtSite, /BatteryCapacity, /ChargingState, /ChargingTime, /Connected, /Current, /CustomName, /DeviceInstance, /FirmwareVersion, /HardwareVersion, /IsGenericEnergyMeter, /MaxCurrent, /Mgmt/Connection, /Mgmt/ProcessName, /Mgmt/ProcessVersion, /Mode, /NrOfPhases, /Odometer, /Position, /Position/Latitude, /Position/Longitude, /PositionIsAdjustable, /ProductId, /ProductName, /RangeToGo, /Serial, /Session/Energy, /SetCurrent, /Soc, /StartStop, /Status, /TargetSoc, /VIN


### main

- **Interfaces**: 1
- **Object Paths**: /Ac/Energy/Forward, /Ac/Power, /Current, /MaxCurrent, /MinCurrent, /NrOfPhases, /Position, /Session/Cost, /Session/SavedCost, /Session/UserId, /Session/UserIdType, /StartStop, /Status
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 13
- **Complexity**: low
- **Focus Areas**: energy_management, networking_protocols, home_automation, battery_management

**Interfaces**:

#### com.victronenergy.main (/Ac/Energy/Forward)
- Methods: None
- Signals: None
- Properties: /Ac/Energy/Forward, /Ac/Power, /Current, /MaxCurrent, /MinCurrent, /NrOfPhases, /Position, /Session/Cost, /Session/SavedCost, /Session/UserId, /Session/UserIdType, /StartStop, /Status


### com.victronenergy.evcharger.

- **Interfaces**: 1
- **Object Paths**: /Ac/Energy/Forward, /Ac/Frequency, /Ac/L1/Current, /Ac/L1/Power, /Ac/L1/PowerFactor, /Ac/L1/Voltage, /Ac/L2/Current, /Ac/L2/Power, /Ac/L2/PowerFactor, /Ac/L2/Voltage, /Ac/L3/Current, /Ac/L3/Power, /Ac/L3/PowerFactor, /Ac/L3/Voltage, /Ac/Power, /Alarms/BlockedWarning, /Alarms/CPInputShortCircuit, /Alarms/DisplayFWUpdateFailure1, /Alarms/DisplayFWUpdateFailure2, /Alarms/DisplayFWUpdateInProgress, /Alarms/ExternalCurrentLimit, /Alarms/GNDNotPresent, /Alarms/GxCommWarning, /Alarms/HighTempWarning, /Alarms/LightSensorICFault, /Alarms/OverTemperature, /Alarms/OverloadActive, /Alarms/OverloadDetected, /Alarms/ResidualCurrent, /Alarms/SetupNeeded, /Alarms/SystemCausedCurrentLimit, /Alarms/TamperDetected, /Alarms/TimeSyncIssue, /Alarms/WeldedContacts, /AutoStart, /Connected, /Current, /CustomName, /DeviceInstance, /EnableDisplay, /FirmwareVersion, /HardwareVersion, /IsGenericEnergyMeter, /MaxCurrent, /Mgmt/Connection, /Mgmt/ProcessName, /Mgmt/ProcessVersion, /MinCurrent, /Mode, /Model, /NrOfPhases, /Position, /PositionIsAdjustable, /ProductId, /ProductName, /Serial, /Session/Cost, /Session/Energy, /Session/SavedCost, /Session/Time, /Session/UserId, /Session/UserIdType, /SetCurrent, /StartStop, /Status
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 40
- **Complexity**: low
- **Focus Areas**: energy_management, home_automation, battery_management

**Interfaces**:

#### com.victronenergy.evcharger. (/Ac/Energy/Forward)
- Methods: None
- Signals: None
- Properties: /Ac/Energy/Forward, /Ac/Frequency, /Ac/L1/Current, /Ac/L1/Power, /Ac/L1/PowerFactor, /Ac/L1/Voltage, /Ac/L2/Current, /Ac/L2/Power, /Ac/L2/PowerFactor, /Ac/L2/Voltage, /Ac/L3/Current, /Ac/L3/Power, /Ac/L3/PowerFactor, /Ac/L3/Voltage, /Ac/Power, /Alarms/BlockedWarning, /Alarms/CPInputShortCircuit, /Alarms/DisplayFWUpdateFailure1, /Alarms/DisplayFWUpdateFailure2, /Alarms/DisplayFWUpdateInProgress, /Alarms/ExternalCurrentLimit, /Alarms/GNDNotPresent, /Alarms/GxCommWarning, /Alarms/HighTempWarning, /Alarms/LightSensorICFault, /Alarms/OverTemperature, /Alarms/OverloadActive, /Alarms/OverloadDetected, /Alarms/ResidualCurrent, /Alarms/SetupNeeded, /Alarms/SystemCausedCurrentLimit, /Alarms/TamperDetected, /Alarms/TimeSyncIssue, /Alarms/WeldedContacts, /AutoStart, /Connected, /Current, /CustomName, /DeviceInstance, /EnableDisplay


### com.victronenergy.grid.

- **Interfaces**: 1
- **Object Paths**: /org/freedesktop/DBus
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 1
- **Complexity**: low
- **Focus Areas**: energy_management, home_automation

**Interfaces**:

#### com.victronenergy.grid. (/org/freedesktop/DBus)
- Methods: None
- Signals: None
- Properties: /org/freedesktop/DBus


### mqtt_bridge

- **Interfaces**: 1
- **Object Paths**: /Ac/Energy/Forward, /Ac/Energy/Reverse, /Ac/Frequency, /Ac/L1/Current, /Ac/L1/Voltage, /Ac/Power, /Alarm, /Capacity, /CellVoltages, /Dc/0/Current, /Dc/0/Power, /Dc/0/Temperature, /Dc/0/Voltage, /FluidType, /Level, /Remaining, /Soc, /Unit, /Value, /set
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 20
- **Complexity**: medium
- **Focus Areas**: energy_management, networking_protocols, battery_management

**Interfaces**:

#### com.victronenergy.mqtt_bridge (/Ac/Energy/Forward)
- Methods: None
- Signals: None
- Properties: /Ac/Energy/Forward, /Ac/Energy/Reverse, /Ac/Frequency, /Ac/L1/Current, /Ac/L1/Voltage, /Ac/Power, /Alarm, /Capacity, /CellVoltages, /Dc/0/Current, /Dc/0/Power, /Dc/0/Temperature, /Dc/0/Voltage, /FluidType, /Level, /Remaining, /Soc, /Unit, /Value, /set


### com.victronenergy.mock.

- **Interfaces**: 1
- **Object Paths**: /Ac/Energy/Forward, /Ac/Energy/Reverse, /Ac/Frequency, /Ac/L1/Current, /Ac/L1/Power, /Ac/L1/Voltage, /Ac/L2/Current, /Ac/L2/Power, /Ac/L2/Voltage, /Ac/L3/Current, /Ac/L3/Power, /Ac/L3/Voltage, /Ac/MaxPower, /Ac/Power, /Alarm/CellImbalance, /Alarm/HighTemperature, /Alarm/InternalFailure, /Alarm/LowSoc, /Alarm/LowTemperature, /Alarms, /Alarms/CellImbalance, /Alarms/HighTemperature, /Alarms/InternalFailure, /Alarms/LowSoc, /Alarms/LowTemperature, /Balancing, /BatteryState, /Capacity, /ChargeCurrent, /ChargeVoltage, /Connected, /CustomName, /Dc/0/AllowCharge, /Dc/0/AllowDischarge, /Dc/0/ConsumedAmphours, /Dc/0/Current, /Dc/0/MaxChargeCurrent, /Dc/0/MaxChargeVoltage, /Dc/0/MaxDischargeCurrent, /Dc/0/Power, /Dc/0/Temperature, /Dc/0/Voltage, /DeviceInstance, /FirmwareVersion, /FluidType, /HardwareVersion, /Level, /MaxChargeCurrent, /MaxDischargeCurrent, /Model, /ProductId, /ProductName, /Remaining, /Serial, /Soc, /SystemMaxCellVoltage, /SystemMinCellVoltage, /Temperature, /TemperatureType, /TimeRemaining, /opt/victronenergy/velib_python
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 40
- **Complexity**: low
- **Focus Areas**: energy_management, battery_management

**Interfaces**:

#### com.victronenergy.mock. (/Ac/Energy/Forward)
- Methods: None
- Signals: None
- Properties: /Ac/Energy/Forward, /Ac/Energy/Reverse, /Ac/Frequency, /Ac/L1/Current, /Ac/L1/Power, /Ac/L1/Voltage, /Ac/L2/Current, /Ac/L2/Power, /Ac/L2/Voltage, /Ac/L3/Current, /Ac/L3/Power, /Ac/L3/Voltage, /Ac/MaxPower, /Ac/Power, /Alarm/CellImbalance, /Alarm/HighTemperature, /Alarm/InternalFailure, /Alarm/LowSoc, /Alarm/LowTemperature, /Alarms, /Alarms/CellImbalance, /Alarms/HighTemperature, /Alarms/InternalFailure, /Alarms/LowSoc, /Alarms/LowTemperature, /Balancing, /BatteryState, /Capacity, /ChargeCurrent, /ChargeVoltage, /Connected, /CustomName, /Dc/0/AllowCharge, /Dc/0/AllowDischarge, /Dc/0/ConsumedAmphours, /Dc/0/Current, /Dc/0/MaxChargeCurrent, /Dc/0/MaxChargeVoltage, /Dc/0/MaxDischargeCurrent, /Dc/0/Power


### __main__

- **Interfaces**: 1
- **Object Paths**: /opt/victronenergy/velib_python
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 1
- **Complexity**: low
- **Focus Areas**: energy_management, networking_protocols

**Interfaces**:

#### com.victronenergy.__main__ (/opt/victronenergy/velib_python)
- Methods: None
- Signals: None
- Properties: /opt/victronenergy/velib_python


### com.victronenergy.veboard

- **Interfaces**: 1
- **Object Paths**: /org/freedesktop/DBus
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 1
- **Complexity**: low
- **Focus Areas**: energy_management, home_automation, battery_management

**Interfaces**:

#### com.victronenergy.veboard (/org/freedesktop/DBus)
- Methods: None
- Signals: None
- Properties: /org/freedesktop/DBus



---

## 📈 GitHub Statistics

```json
{
  "errors": [],
  "iot_repos": 31,
  "scanned_at": "2026-09-10T04:57:00.559660",
  "total_repos": 42
}
```