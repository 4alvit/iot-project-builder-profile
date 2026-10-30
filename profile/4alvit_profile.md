# IoT Engineering Profile: 4alvit

*Generated: 2026-10-30 12:38*

## Summary

The developer specializes in Victron Venus OS energy systems, building D-Bus and MQTT bridges for JBD/Daly BMS batteries, Tasmota PV meters, and grid-zero inverter control. ESPHome BLE sensor patterns for ESP32 proxies integrate battery monitors and environmental sensors into Home Assistant, demonstrating end-to-end energy and battery management. Additional work includes MQTT observability with OpenTelemetry, Prometheus, and Grafana, RAG pipelines for Victron documentation, and voice assistant gateways for Alexa and Google Home. Infrastructure experience spans K3s and Docker Compose edge deployments, with a focus on production-ready IoT patterns rather than low-level embedded firmware.

---

## 📊 Repository Overview

- **Public repositories scanned**: 91
- **IoT-Related Repositories**: 80
- **ESPHome Configurations**: 37
- **D-Bus analysis records**: 40

### Complexity Distribution

Analysis records from IoT repositories, ESPHome configurations and D-Bus analyses.


- **Medium**: 73

- **High**: 15

- **Low**: 69


---

## 🎯 Focus Areas


### Energy Management: 90.0%


### Battery Management: 85.0%


### Home Automation: 80.0%


### Networking Protocols: 75.0%


### Data Pipeline: 60.0%


### Edge Computing: 50.0%


### Voice Assistant: 50.0%


### Environmental Monitoring: 40.0%


### Firmware Development: 35.0%



---

## 🛠️ Skills Assessment

| Skill | Category | Proficiency | Confidence | Evidence |
|-------|----------|-------------|------------|----------|

| Victron Venus OS | energy_systems | 9/10 | 95.0% | victron-venus/inverter-control, victron-venus/dbus-mqtt-battery, 4alvit/mcp-venus-os |

| ESPHome | home_automation | 8/10 | 95.0% | 4alvit/esphome-ble-sensor-patterns, victron-venus/esphome-jbd-bms-mqtt |

| MQTT | protocols_networking | 8/10 | 90.0% | 4alvit/fastapi-mqtt-gateway, victron-venus/dbus-mqtt-battery |

| Battery Management Systems (BMS) | energy_systems | 8/10 | 90.0% | victron-venus/dbus-mqtt-battery, 4alvit/esphome-ble-sensor-patterns/patterns/jbd-bms |

| D-Bus | protocols_networking | 8/10 | 85.0% | 4alvit/dbus-service-template, victron-venus/dbus-tasmota-pv |

| Python IoT | python_iot | 8/10 | 85.0% | 4alvit/mcp-venus-os, 4alvit/energy-data-rag-pipeline |

| Data Pipeline &amp; Observability | data_pipeline | 7/10 | 80.0% | 4alvit/mqtt-observability-opentelemetry, 4alvit/energy-data-rag-pipeline |

| Edge Computing | edge_computing | 6/10 | 75.0% | 4alvit/cisco-home-telephony, 4alvit/mqtt-observability-opentelemetry |

| Voice Assistant Integration | voice_ai | 5/10 | 80.0% | 4alvit/amazon-echo-home-voice, 4alvit/google-home-voice-stats |


---

## 💪 Key Strengths


- Venus OS D-Bus/MQTT integration for batteries and inverters

- ESPHome BLE proxy patterns for JBD and Daly BMS

- IoT observability with OpenTelemetry and Prometheus/Grafana

- Energy forecasting and Victron documentation RAG pipeline

- Multi-protocol bridging across MQTT, D-Bus, WebSocket, and BLE


---

## 📈 Growth Areas


- Low-level embedded firmware in C/C++ or RTOS environments

- Industrial IoT protocols such as Modbus TCP/RTU and CANbus

- BMS hardware design and cell balancing implementation


---

## 🏆 Top Repositories


### esphome-ble-sensor-patterns

- **Description**: Production-ready patterns for ESPHome BLE sensors — iBeacon, Eddystone, and custom BLE service parsing with lambda filters. Covers ESP32 Bluetooth proxy, passive scanning, and Home Assistant integration for battery-powered sensors.
- **Language**: Python
- **Stars**: 1 ⭐ | **Forks**: 1
- **IoT Score**: 1.00
- **Complexity**: medium
- **Focus Areas**: home_automation, energy_management, battery_management, voice_assistant, networking_protocols
- **Topics**: ble, bluetooth-low-energy, bluetooth-proxy, bms, esp32, esphome, home-assistant, ibeacon, iot, lambda, passive-scanning, plant-sensor, reference-implementation, sensor, temperature-sensor, venus-os, victron, xiaomi

### dbus-mqtt-battery

- **Description**: MQTT to D-Bus bridge for JBD BMS batteries on Victron Venus OS with DVCC support
- **Language**: Python
- **Stars**: 0 ⭐ | **Forks**: 1
- **IoT Score**: 1.00
- **Complexity**: high
- **Focus Areas**: energy_management, battery_management, networking_protocols, data_pipeline
- **Topics**: battery, battery-management, bms, cerbo-gx, dbus, dvcc, energy, jbd-bms, lifepo4, mqtt, power, python, sensor, solar, venus-os, victron

### dbus-tasmota-pv

- **Description**: Tasmota power meter to Victron D-Bus PV inverter bridge for Venus OS
- **Language**: Python
- **Stars**: 0 ⭐ | **Forks**: 1
- **IoT Score**: 1.00
- **Complexity**: medium
- **Focus Areas**: energy_management, networking_protocols, data_pipeline
- **Topics**: dbus, energy, inverter, meter, mqtt, power, pv-inverter, python, sensor, solar, tasmota, venus-os, victron

### esphome-jbd-bms-mqtt

- **Description**: ESPHome ESP32 Bluetooth proxy for JBD BMS batteries, publishing to MQTT for Victron Venus OS
- **Language**: YAML
- **Stars**: 1 ⭐ | **Forks**: 1
- **IoT Score**: 1.00
- **Complexity**: medium
- **Focus Areas**: energy_management, battery_management, networking_protocols, data_pipeline
- **Topics**: battery, battery-monitor, ble, bluetooth, bms, cerbo-gx, energy, esp32, esphome, jbd-bms, lifepo4, mqtt, sensor, venus-os, victron

### inverter-control

- **Description**: Grid-zero feed-in control for Victron Venus OS with D-Bus, MQTT and optional Home Assistant integration
- **Language**: Python
- **Stars**: 0 ⭐ | **Forks**: 1
- **IoT Score**: 1.00
- **Complexity**: high
- **Focus Areas**: home_automation, energy_management, voice_assistant, networking_protocols, data_pipeline
- **Topics**: battery, cerbo-gx, dbus, emporia-vue, energy, energy-management, ess, external-control, grid-tie, hass, home-assistant, inverter, meter, mqtt, power, python, quattro, raspberry-pi, sensor, solar

### inverter-monitoring

- **Description**: Telegraf + InfluxDB + Grafana monitoring stack for Victron inverter systems
- **Language**: Python
- **Stars**: 0 ⭐ | **Forks**: 1
- **IoT Score**: 1.00
- **Complexity**: high
- **Focus Areas**: energy_management, networking_protocols, edge_computing, data_pipeline
- **Topics**: battery, cerbo-gx, dbus, docker, energy, energy-monitoring, grafana, influxdb, inverter, iot, meter, mqtt, power, python, sensor, solar, telegraf, time-series, venus-os, victron

### inverter-dashboard-go

- **Description**: Real-time Victron inverter web dashboard (Go) — same role as inverter-dashboard, implemented in Go with MQTT and optional Home Assistant direct control
- **Language**: Go
- **Stars**: 0 ⭐ | **Forks**: 1
- **IoT Score**: 1.00
- **Complexity**: high
- **Focus Areas**: home_automation, energy_management, voice_assistant, networking_protocols, edge_computing, data_pipeline
- **Topics**: battery, cerbo-gx, dashboard, docker, energy, go, golang, hass, home-assistant, inverter, mqtt, power, real-time, sensor, solar, venus-os, victron, websocket

### inverter-desktop

- **Description**: Desktop version of Web dashboard for Victron inverter control with Home Assistant integration
- **Language**: Rust
- **Stars**: 0 ⭐ | **Forks**: 1
- **IoT Score**: 1.00
- **Complexity**: high
- **Focus Areas**: home_automation, energy_management, voice_assistant, networking_protocols, data_pipeline
- **Topics**: battery, cerbo-gx, dashboard, energy, energy-management, grid-tie, hass, home-assistant, inverter, mqtt, power, sensor, solar, venus-os, victron, web-dashboard

### venus-os-observability

- **Description**: OpenTelemetry/Prometheus observability for Venus OS — D-Bus event tracing, inverter metrics, distributed tracing
- **Language**: Python
- **Stars**: 0 ⭐ | **Forks**: 1
- **IoT Score**: 1.00
- **Complexity**: high
- **Focus Areas**: energy_management, networking_protocols, data_pipeline
- **Topics**: cerbo-gx, dbus, distributed-tracing, energy, grafana, inverter, mqtt, opentelemetry, power, prometheus, python, sensor, solar, tempo, venus-os, victron

### dbus-esphome-grid-sensor

- **Description**: ESP32 CT sensor for grid power monitoring with D-Bus service for Venus OS
- **Language**: Python
- **Stars**: 1 ⭐ | **Forks**: 2
- **IoT Score**: 1.00
- **Complexity**: high
- **Focus Areas**: energy_management, networking_protocols, edge_computing, data_pipeline
- **Topics**: ct-sensor, dbus, docker, energy, esp32, esphome, grid, grid-meter, home-automation, meter, mqtt, power, python, sensor, solar, venus-os, victron


---

## 🔧 ESPHome Configurations


### 4alvit/esphome-ble-sensor-patterns/patterns/ble-temp-sensor/generic-ble-temp.yaml

- **Devices**: esp32:esp32dev
- **Components**: 11
- **Custom Components**: None
- **External Libraries**: None
- **Complexity**: low
- **Focus Areas**: battery_management, energy_management, home_automation, networking_protocols, environmental_monitoring

**Component Breakdown**:

- binary_sensor (status): ESP32 Status

- sensor (template): Temperature

- sensor (template): Humidity

- sensor (template): Battery

- sensor (uptime): Uptime

- sensor (wifi_signal): WiFi Signal

- wifi: unnamed

- mqtt: unnamed

- logger: unnamed

- api: unnamed

- esp32_ble_tracker: unnamed


### 4alvit/esphome-ble-sensor-patterns/patterns/ble-temp-sensor/inkbird-ibs-th1.yaml

- **Devices**: esp32:esp32dev
- **Components**: 11
- **Custom Components**: None
- **External Libraries**: None
- **Complexity**: low
- **Focus Areas**: battery_management, energy_management, home_automation, networking_protocols, environmental_monitoring

**Component Breakdown**:

- binary_sensor (status): ESP32 Status

- sensor (template): Inkbird Temperature

- sensor (template): Inkbird Humidity

- sensor (template): Inkbird Battery

- sensor (uptime): Uptime

- sensor (wifi_signal): WiFi Signal

- wifi: unnamed

- mqtt: unnamed

- logger: unnamed

- api: unnamed

- esp32_ble_tracker: unnamed


### 4alvit/esphome-ble-sensor-patterns/patterns/ble-temp-sensor/xiaomi-lywsd03mmc.yaml

- **Devices**: esp32:esp32dev
- **Components**: 10
- **Custom Components**: None
- **External Libraries**: None
- **Complexity**: low
- **Focus Areas**: battery_management, energy_management, home_automation, networking_protocols, environmental_monitoring

**Component Breakdown**:

- binary_sensor (status): ESP32 Status

- sensor (xiaomi_lywsd03mmc): unnamed

- sensor (wifi_signal): WiFi Signal

- sensor (uptime): Uptime

- button (restart): Restart

- wifi: unnamed

- mqtt: unnamed

- logger: unnamed

- api: unnamed

- esp32_ble_tracker: unnamed


### 4alvit/esphome-ble-sensor-patterns/patterns/daly-bms/multi-bms.yaml

- **Devices**: esp32:esp32dev
- **Components**: 19
- **Custom Components**: daly_bms_ble
- **External Libraries**: None
- **Complexity**: low
- **Focus Areas**: firmware_development, battery_management, energy_management, home_automation, networking_protocols, environmental_monitoring

**Component Breakdown**:

- ble_client: unnamed

- ble_client: unnamed

- ble_client: unnamed

- binary_sensor (daly_bms_ble): unnamed

- binary_sensor (daly_bms_ble): unnamed

- binary_sensor (daly_bms_ble): unnamed

- binary_sensor (status): ESP32 Status

- sensor (daly_bms_ble): unnamed

- sensor (daly_bms_ble): unnamed

- sensor (daly_bms_ble): unnamed

- sensor (wifi_signal): WiFi Signal

- sensor (uptime): Uptime

- wifi: unnamed

- mqtt: unnamed

- logger: unnamed

- api: unnamed

- interval: unnamed

- esp32_ble: unnamed

- esp32_ble_tracker: unnamed


### 4alvit/esphome-ble-sensor-patterns/patterns/daly-bms/single-bms.yaml

- **Devices**: esp32:esp32dev
- **Components**: 16
- **Custom Components**: daly_bms_ble
- **External Libraries**: None
- **Complexity**: low
- **Focus Areas**: firmware_development, battery_management, energy_management, home_automation, networking_protocols, environmental_monitoring

**Component Breakdown**:

- ble_client: unnamed

- binary_sensor (daly_bms_ble): unnamed

- binary_sensor (daly_bms_ble): unnamed

- binary_sensor (status): ESP32 Status

- sensor (daly_bms_ble): unnamed

- sensor (daly_bms_ble): unnamed

- sensor (daly_bms_ble): unnamed

- sensor (template): Pack Energy

- sensor (wifi_signal): WiFi Signal

- sensor (uptime): Uptime

- button (restart): Restart

- wifi: unnamed

- mqtt: unnamed

- logger: unnamed

- api: unnamed

- esp32_ble_tracker: unnamed


### 4alvit/esphome-ble-sensor-patterns/patterns/jbd-bms/multi-bms.yaml

- **Devices**: esp32:esp32dev
- **Components**: 23
- **Custom Components**: jbd_bms_ble
- **External Libraries**: None
- **Complexity**: low
- **Focus Areas**: firmware_development, battery_management, energy_management, home_automation, networking_protocols, environmental_monitoring

**Component Breakdown**:

- ble_client: unnamed

- ble_client: unnamed

- ble_client: unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (status): ESP32 Status

- sensor (jbd_bms_ble): unnamed

- sensor (jbd_bms_ble): unnamed

- sensor (jbd_bms_ble): unnamed

- sensor (wifi_signal): WiFi Signal

- sensor (uptime): Uptime

- sensor (template): Total Voltage (All)

- sensor (template): Total Power (All)

- sensor (template): Min SOC (All)

- button (restart): Restart

- wifi: unnamed

- mqtt: unnamed

- logger: unnamed

- api: unnamed

- interval: unnamed

- esp32_ble: unnamed

- esp32_ble_tracker: unnamed


### 4alvit/esphome-ble-sensor-patterns/patterns/jbd-bms/single-bms.yaml

- **Devices**: esp32:esp32dev
- **Components**: 14
- **Custom Components**: jbd_bms_ble
- **External Libraries**: None
- **Complexity**: low
- **Focus Areas**: firmware_development, battery_management, energy_management, home_automation, networking_protocols, environmental_monitoring

**Component Breakdown**:

- ble_client: unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (status): ESP32 Status

- sensor (jbd_bms_ble): unnamed

- sensor (jbd_bms_ble): unnamed

- sensor (jbd_bms_ble): unnamed

- sensor (wifi_signal): WiFi Signal

- sensor (uptime): Uptime

- button (restart): Restart

- wifi: unnamed

- mqtt: unnamed

- logger: unnamed

- api: unnamed

- esp32_ble_tracker: unnamed


### 4alvit/esphome-ble-sensor-patterns/patterns/xiaomi-mi-flora/mi-flora.yaml

- **Devices**: esp32:esp32dev
- **Components**: 9
- **Custom Components**: None
- **External Libraries**: None
- **Complexity**: low
- **Focus Areas**: battery_management, energy_management, home_automation, networking_protocols, environmental_monitoring

**Component Breakdown**:

- binary_sensor (status): ESP32 Status

- sensor (xiaomi_hhccjcy01): unnamed

- sensor (uptime): Uptime

- sensor (wifi_signal): WiFi Signal

- wifi: unnamed

- mqtt: unnamed

- logger: unnamed

- api: unnamed

- esp32_ble_tracker: unnamed


### victron-venus/esphome-jbd-bms-mqtt/jbd-all-batteries.yaml

- **Devices**: esp32:esp32dev
- **Components**: 46
- **Custom Components**: jbd_bms_ble
- **External Libraries**: None
- **Complexity**: medium
- **Focus Areas**: firmware_development, battery_management, energy_management, home_automation, networking_protocols, environmental_monitoring

**Component Breakdown**:

- ota (esphome): unnamed

- ble_client: unnamed

- ble_client: unnamed

- ble_client: unnamed

- ble_client: unnamed

- ble_client: unnamed

- ble_client: unnamed

- ble_client: unnamed

- ble_client: unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (status): esp32_status

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

- button (restart): restart

- wifi: unnamed

- mqtt: unnamed

- logger: unnamed

- api: unnamed

- interval: unnamed

- esp32_ble: unnamed

- esp32_ble_tracker: unnamed


### victron-venus/esphome-jbd-bms-mqtt/jbd-all-batteries1.yaml

- **Devices**: esp32:esp32dev
- **Components**: 29
- **Custom Components**: jbd_bms_ble
- **External Libraries**: None
- **Complexity**: medium
- **Focus Areas**: firmware_development, battery_management, energy_management, home_automation, networking_protocols, environmental_monitoring

**Component Breakdown**:

- ota (esphome): unnamed

- ble_client: unnamed

- ble_client: unnamed

- ble_client: unnamed

- ble_client: unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (status): esp32_status

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

- button (restart): restart

- wifi: unnamed

- mqtt: unnamed

- logger: unnamed

- api: unnamed

- esp32_ble: unnamed

- script: unnamed

- esp32_ble_tracker: unnamed


### victron-venus/esphome-jbd-bms-mqtt/jbd-all-batteries2.yaml

- **Devices**: esp32:esp32dev
- **Components**: 29
- **Custom Components**: jbd_bms_ble
- **External Libraries**: None
- **Complexity**: medium
- **Focus Areas**: firmware_development, battery_management, energy_management, home_automation, networking_protocols, environmental_monitoring

**Component Breakdown**:

- ota (esphome): unnamed

- ble_client: unnamed

- ble_client: unnamed

- ble_client: unnamed

- ble_client: unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (jbd_bms_ble): unnamed

- binary_sensor (status): esp32_status

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

- button (restart): restart

- wifi: unnamed

- mqtt: unnamed

- logger: unnamed

- api: unnamed

- esp32_ble: unnamed

- script: unnamed

- esp32_ble_tracker: unnamed


### victron-venus/dbus-esphome-grid-sensor/esphome/grid-sensor.yaml

- **Devices**: esp32:esp32dev
- **Components**: 16
- **Custom Components**: None
- **External Libraries**: None
- **Complexity**: low
- **Focus Areas**: energy_management, firmware_development, networking_protocols, home_automation

**Component Breakdown**:

- ota (esphome): unnamed

- binary_sensor (status): Grid Sensor Status

- binary_sensor (template): Grid Feed-In Active

- sensor (adc): Grid Current

- sensor (template): Grid Power

- sensor (integration): Grid Energy Forward

- sensor (integration): Grid Energy Reverse

- light (binary): Grid Sensor LED

- button (restart): Grid Sensor Restart

- button (template): Toggle Calibration Mode

- wifi: unnamed

- mqtt: unnamed

- logger: unnamed

- api: unnamed

- switch (template): MQTT Publishing

- i2c: unnamed


### victron-venus/dbus-esphome-grid-sensor/docker-compose.yml

- **Devices**: 
- **Components**: 0
- **Custom Components**: None
- **External Libraries**: None
- **Complexity**: low
- **Focus Areas**: networking_protocols, home_automation

**Component Breakdown**:


### victron-venus/esphome-emporia-vue2-ethernet/firmware/validation/fixture-4signal.yaml

- **Devices**: 
- **Components**: 0
- **Custom Components**: None
- **External Libraries**: None
- **Complexity**: low
- **Focus Areas**: networking_protocols, firmware_development

**Component Breakdown**:


### victron-venus/esphome-emporia-vue2-ethernet/firmware/validation/fixture-common.yaml

- **Devices**: esp32:esp32dev
- **Components**: 5
- **Custom Components**: emporia_vue
- **External Libraries**: None
- **Complexity**: low
- **Focus Areas**: energy_management, firmware_development, home_automation

**Component Breakdown**:

- ota (esphome): unnamed

- sensor (emporia_vue): unnamed

- logger: unnamed

- api: unnamed

- i2c: unnamed


### victron-venus/esphome-emporia-vue2-ethernet/firmware/validation/fixture.yaml

- **Devices**: 
- **Components**: 0
- **Custom Components**: None
- **External Libraries**: None
- **Complexity**: low
- **Focus Areas**: networking_protocols, firmware_development

**Component Breakdown**:


### ha-homelab/ha-tuya-esphome/examples/me201w-cbu-recovery.yaml

- **Devices**: bk72xx:cbu
- **Components**: 6
- **Custom Components**: None
- **External Libraries**: None
- **Complexity**: low
- **Focus Areas**: networking_protocols, firmware_development, home_automation

**Component Breakdown**:

- ota (esphome): unnamed

- binary_sensor (status): Status

- sensor (wifi_signal): WiFi Signal

- wifi: unnamed

- logger: unnamed

- api: unnamed


### ha-homelab/ha-tuya-esphome/examples/supernight-cv01.yaml

- **Devices**: 
- **Components**: 7
- **Custom Components**: None
- **External Libraries**: None
- **Complexity**: low
- **Focus Areas**: energy_management, firmware_development, home_automation

**Component Breakdown**:

- binary_sensor (gpio): unnamed

- binary_sensor (template): unnamed

- sensor (adc): unnamed

- sensor (hlw8012): unnamed

- logger: unnamed

- switch (gpio): Left Outlet

- switch (gpio): Right Outlet


### ha-homelab/ha-tuya-esphome/examples/swp1-pw2-v5.yaml

- **Devices**: esp8266:esp_wroom_02
- **Components**: 9
- **Custom Components**: None
- **External Libraries**: None
- **Complexity**: low
- **Focus Areas**: networking_protocols, firmware_development, home_automation

**Component Breakdown**:

- ota (esphome): unnamed

- binary_sensor (gpio): unnamed

- binary_sensor (status): Status

- sensor (wifi_signal): WiFi Signal

- button (restart): Restart

- wifi: unnamed

- logger: unnamed

- api: unnamed

- switch (gpio): None


### ha-homelab/ha-tuya-esphome/examples/teckin-sp20-metered.yaml

- **Devices**: esp8266:esp01_1m
- **Components**: 21
- **Custom Components**: None
- **External Libraries**: None
- **Complexity**: low
- **Focus Areas**: energy_management, firmware_development, networking_protocols, home_automation

**Component Breakdown**:

- ota (esphome): unnamed

- binary_sensor (gpio): Physical Button

- binary_sensor (status): Status

- sensor (hlw8012): unnamed

- sensor (template): Energy Total

- sensor (template): Energy Today

- sensor (template): Energy Yesterday

- sensor (template): Energy ApparentPower

- sensor (template): Energy ReactivePower

- sensor (template): Energy Factor

- sensor (wifi_signal): WiFi Signal

- sensor (uptime): Uptime

- light (binary): unnamed

- button (restart): Restart

- wifi: unnamed

- logger: unnamed

- api: unnamed

- time (homeassistant): unnamed

- time (sntp): unnamed

- interval: unnamed

- switch (gpio): Relay


### ha-homelab/ha-tuya-esphome/examples/tuya-plug.yaml

- **Devices**: esp8266:esp01_1m
- **Components**: 6
- **Custom Components**: None
- **External Libraries**: None
- **Complexity**: low
- **Focus Areas**: networking_protocols, firmware_development, home_automation

**Component Breakdown**:

- ota (esphome): unnamed

- binary_sensor (status): Status

- sensor (wifi_signal): WiFi Signal

- wifi: unnamed

- logger: unnamed

- api: unnamed


### ha-homelab/ha-radio-hub/firmware/external-antenna/hub.yaml

- **Devices**: esp32:esp32dev
- **Components**: 10
- **Custom Components**: zigbee_tcp, low_power_ethernet, low_power_otbr, wk2132_uart
- **External Libraries**: None
- **Complexity**: high
- **Focus Areas**: firmware_development, home_automation, networking_protocols, energy_management, environmental_monitoring

**Component Breakdown**:

- ota (esphome): unnamed

- bluetooth_proxy: unnamed

- mqtt: unnamed

- logger: unnamed

- api: unnamed

- ethernet: unnamed

- uart: unnamed

- esp32_ble_tracker: unnamed

- i2c: unnamed

- spi: unnamed


### ha-homelab/ha-radio-hub/firmware/h2-quartet/h2-ble-ethernet.yaml

- **Devices**: esp32:esp32-h2-devkitm-1
- **Components**: 5
- **Custom Components**: None
- **External Libraries**: None
- **Complexity**: low
- **Focus Areas**: networking_protocols, firmware_development, home_automation

**Component Breakdown**:

- bluetooth_proxy: unnamed

- logger: unnamed

- api: unnamed

- ethernet: unnamed

- esp32_ble_tracker: unnamed


### ha-homelab/ha-radio-hub/firmware/hub-s3-eth.yaml

- **Devices**: esp32:esp32-s3-devkitc-1
- **Components**: 11
- **Custom Components**: None
- **External Libraries**: None
- **Complexity**: medium
- **Focus Areas**: networking_protocols, firmware_development, environmental_monitoring, home_automation

**Component Breakdown**:

- ota (esphome): unnamed

- binary_sensor (status): API Connected

- sensor (uptime): Uptime

- button (restart): Restart sensor controller

- bluetooth_proxy: unnamed

- logger: unnamed

- api: unnamed

- ethernet: unnamed

- uart: unnamed

- uart: unnamed

- i2c: unnamed


### ha-homelab/ha-radio-hub/firmware/low-power/proof.yaml

- **Devices**: esp32:esp32-s3-devkitc-1
- **Components**: 10
- **Custom Components**: low_power_ethernet, low_power_otbr
- **External Libraries**: None
- **Complexity**: high
- **Focus Areas**: firmware_development, home_automation, networking_protocols, energy_management, environmental_monitoring

**Component Breakdown**:

- ota (esphome): unnamed

- bluetooth_proxy: unnamed

- mqtt: unnamed

- logger: unnamed

- api: unnamed

- ethernet: unnamed

- uart: unnamed

- esp32_ble_tracker: unnamed

- i2c: unnamed

- spi: unnamed


### ha-homelab/ha-radio-hub/firmware/module-carrier/hub.yaml

- **Devices**: esp32:esp32-s3-devkitc-1
- **Components**: 10
- **Custom Components**: zigbee_tcp, low_power_ethernet, low_power_otbr, wk2132_uart
- **External Libraries**: None
- **Complexity**: high
- **Focus Areas**: firmware_development, home_automation, networking_protocols, energy_management, environmental_monitoring

**Component Breakdown**:

- ota (esphome): unnamed

- bluetooth_proxy: unnamed

- mqtt: unnamed

- logger: unnamed

- api: unnamed

- ethernet: unnamed

- uart: unnamed

- esp32_ble_tracker: unnamed

- i2c: unnamed

- spi: unnamed


### ha-homelab/ha-radio-hub/firmware/packages/rf-airbridge.yaml

- **Devices**: 
- **Components**: 6
- **Custom Components**: remote_receiver, rf_tx_startup
- **External Libraries**: None
- **Complexity**: medium
- **Focus Areas**: networking_protocols, firmware_development, home_automation

**Component Breakdown**:

- remote_transmitter: unnamed

- mqtt: unnamed

- api: unnamed

- switch (template): Raw RF learning

- remote_receiver: unnamed

- script: unnamed


### ha-homelab/ha-radio-hub/firmware/packages/rf-ethernet-base.yaml

- **Devices**: esp32:esp32-s3-devkitc-1
- **Components**: 6
- **Custom Components**: None
- **External Libraries**: None
- **Complexity**: medium
- **Focus Areas**: networking_protocols, firmware_development, home_automation

**Component Breakdown**:

- binary_sensor (status): API Connected

- sensor (uptime): Uptime

- logger: unnamed

- api: unnamed

- ethernet: unnamed

- spi: unnamed


### ha-homelab/rf-airbridge/device.example.yaml

- **Devices**: esp8266:nodemcuv2
- **Components**: 5
- **Custom Components**: None
- **External Libraries**: None
- **Complexity**: low
- **Focus Areas**: networking_protocols, firmware_development

**Component Breakdown**:

- ota (esphome): unnamed

- wifi: unnamed

- mqtt: unnamed

- api: unnamed

- spi: unnamed


### ha-homelab/rf-airbridge/packages/rf-airbridge.yaml

- **Devices**: 
- **Components**: 6
- **Custom Components**: remote_receiver
- **External Libraries**: None
- **Complexity**: medium
- **Focus Areas**: networking_protocols, firmware_development, home_automation

**Component Breakdown**:

- remote_transmitter: unnamed

- mqtt: unnamed

- api: unnamed

- switch (template): Raw RF learning

- remote_receiver: unnamed

- script: unnamed


### ha-homelab/rf-airbridge/packages/wake-on-lan.yaml

- **Devices**: 
- **Components**: 1
- **Custom Components**: None
- **External Libraries**: None
- **Complexity**: low
- **Focus Areas**: networking_protocols

**Component Breakdown**:

- api: unnamed


### ha-homelab/ruview-home-sensing/firmware/wisp-pilot/node-esp32s3.yaml

- **Devices**: esp32:esp32-s3-devkitc-1
- **Components**: 6
- **Custom Components**: wisp
- **External Libraries**: None
- **Complexity**: low
- **Focus Areas**: energy_management, firmware_development, networking_protocols, home_automation

**Component Breakdown**:

- ota (esphome): unnamed

- light (esp32_rmt_led_strip): unnamed

- wifi: unnamed

- logger: unnamed

- api: unnamed

- switch (template): Pilot raw CSI stream


### ha-homelab/zac93-esp32/firmware/adopt/esp32-s3.yaml

- **Devices**: esp32:esp32-s3-devkitc-1
- **Components**: 4
- **Custom Components**: None
- **External Libraries**: None
- **Complexity**: low
- **Focus Areas**: energy_management, firmware_development, networking_protocols

**Component Breakdown**:

- ota (esphome): unnamed

- wifi: unnamed

- logger: unnamed

- api: unnamed


### ha-homelab/zac93-esp32/firmware/adopt/esp32-wroom.yaml

- **Devices**: esp32:esp32dev
- **Components**: 4
- **Custom Components**: None
- **External Libraries**: None
- **Complexity**: low
- **Focus Areas**: energy_management, firmware_development, networking_protocols

**Component Breakdown**:

- ota (esphome): unnamed

- wifi: unnamed

- logger: unnamed

- api: unnamed


### ha-homelab/zac93-esp32/firmware/factory/esp32-s3.yaml

- **Devices**: esp32:esp32-s3-devkitc-1
- **Components**: 3
- **Custom Components**: None
- **External Libraries**: None
- **Complexity**: low
- **Focus Areas**: energy_management, firmware_development, networking_protocols

**Component Breakdown**:

- wifi: unnamed

- logger: unnamed

- api: unnamed


### ha-homelab/zac93-esp32/firmware/factory/esp32-wroom.yaml

- **Devices**: esp32:esp32dev
- **Components**: 3
- **Custom Components**: None
- **External Libraries**: None
- **Complexity**: low
- **Focus Areas**: energy_management, firmware_development, networking_protocols

**Component Breakdown**:

- wifi: unnamed

- logger: unnamed

- api: unnamed


### ha-homelab/zac93-esp32/firmware/common.yaml

- **Devices**: 
- **Components**: 4
- **Custom Components**: None
- **External Libraries**: None
- **Complexity**: low
- **Focus Areas**: energy_management, firmware_development, networking_protocols

**Component Breakdown**:

- ota (esphome): unnamed

- wifi: unnamed

- logger: unnamed

- api: unnamed



---

## 📡 D-Bus Services


### com.victronenergy.battery.

- **Interfaces**: 1
- **Object Paths**: /Alarms/CellImbalance, /Alarms/CommunicationError, /Alarms/HighCellVoltage, /Alarms/HighTemperature, /Alarms/HighVoltage, /Alarms/InternalFailure, /Alarms/LowCellVoltage, /Alarms/LowSoc, /Alarms/LowTemperature, /Alarms/LowVoltage, /Capacity, /Connected, /ConsumedAmphours, /Dc/0/Temperature, /History/ChargeCycles, /Info/DataAge, /Info/DataComplete, /Info/DataTimeout, /Info/LastMeasurementMonotonic, /Info/MaxChargeCellVoltage, /Info/MaxChargeCurrent, /Info/MaxChargeVoltage, /Info/MaxDischargeCurrent, /Info/MissingData, /Info/TelemetryPartial, /Info/TelemetrySource, /Info/TelemetryState, /InstalledCapacity, /Io/AllowToBalance, /Io/AllowToCharge, /Io/AllowToDischarge, /Soc, /System/BatteriesParallel, /System/BatteriesSeries, /System/MOSTemperature, /System/MaxCellTemperature, /System/MaxCellVoltage, /System/MaxTemperatureCellId, /System/MaxVoltageCellId, /System/MinCellTemperature, /System/MinCellVoltage, /System/MinTemperatureCellId, /System/MinVoltageCellId, /System/NrOfBatteries, /System/NrOfCells, /System/NrOfCellsPerBattery, /System/NrOfModulesBlockingCharge, /System/NrOfModulesBlockingDischarge, /System/NrOfModulesOffline, /System/NrOfModulesOnline, /System/StaleData, /Voltages/Diff, /Voltages/Sum
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 40
- **Complexity**: medium
- **Focus Areas**: networking_protocols, energy_management, battery_management

**Interfaces**:

#### com.victronenergy.battery. (/Alarms/CellImbalance)
- Methods: None
- Signals: None
- Properties: /Alarms/CellImbalance, /Alarms/CommunicationError, /Alarms/HighCellVoltage, /Alarms/HighTemperature, /Alarms/HighVoltage, /Alarms/InternalFailure, /Alarms/LowCellVoltage, /Alarms/LowSoc, /Alarms/LowTemperature, /Alarms/LowVoltage, /Capacity, /Connected, /ConsumedAmphours, /Dc/0/Temperature, /History/ChargeCycles, /Info/DataAge, /Info/DataComplete, /Info/DataTimeout, /Info/LastMeasurementMonotonic, /Info/MaxChargeCellVoltage, /Info/MaxChargeCurrent, /Info/MaxChargeVoltage, /Info/MaxDischargeCurrent, /Info/MissingData, /Info/TelemetryPartial, /Info/TelemetrySource, /Info/TelemetryState, /InstalledCapacity, /Io/AllowToBalance, /Io/AllowToCharge, /Io/AllowToDischarge, /Soc, /System/BatteriesParallel, /System/BatteriesSeries, /System/MOSTemperature, /System/MaxCellTemperature, /System/MaxCellVoltage, /System/MaxTemperatureCellId, /System/MaxVoltageCellId, /System/MinCellTemperature


### dbus_utils

- **Interfaces**: 1
- **Object Paths**: /Connected, /CustomName, /Dc/0/Current, /Dc/0/Power, /Dc/0/Temperature, /Dc/0/Voltage, /DeviceInstance, /FirmwareVersion, /HardwareVersion, /Mgmt/Connection, /Mgmt/ProcessName, /Mgmt/ProcessVersion, /ProductId, /ProductName, /TimeToGo
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 15
- **Complexity**: low
- **Focus Areas**: networking_protocols, energy_management, battery_management

**Interfaces**:

#### com.victronenergy.dbus_utils (/Connected)
- Methods: None
- Signals: None
- Properties: /Connected, /CustomName, /Dc/0/Current, /Dc/0/Power, /Dc/0/Temperature, /Dc/0/Voltage, /DeviceInstance, /FirmwareVersion, /HardwareVersion, /Mgmt/Connection, /Mgmt/ProcessName, /Mgmt/ProcessVersion, /ProductId, /ProductName, /TimeToGo


### com.victronenergy.pvinverter.tasmota_

- **Interfaces**: 1
- **Object Paths**: /Ac/Energy/Daily, /Ac/Energy/Forward, /Ac/L1/Current, /Ac/L1/Power, /Ac/L1/Voltage, /Ac/Power, /AllowedRoles, /Connected, /CustomName, /DeviceInstance, /Energy/Daily/Yesterday, /ErrorCode, /FirmwareVersion, /IsGenericEnergyMeter, /Mgmt/Connection, /Mgmt/ProcessName, /Mgmt/ProcessVersion, /PhaseSetting, /Position, /PositionIsAdjustable, /ProductId, /ProductName, /Role, /Serial
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 24
- **Complexity**: medium
- **Focus Areas**: energy_management, networking_protocols, home_automation

**Interfaces**:

#### com.victronenergy.pvinverter.tasmota_ (/Ac/Energy/Daily)
- Methods: None
- Signals: None
- Properties: /Ac/Energy/Daily, /Ac/Energy/Forward, /Ac/L1/Current, /Ac/L1/Power, /Ac/L1/Voltage, /Ac/Power, /AllowedRoles, /Connected, /CustomName, /DeviceInstance, /Energy/Daily/Yesterday, /ErrorCode, /FirmwareVersion, /IsGenericEnergyMeter, /Mgmt/Connection, /Mgmt/ProcessName, /Mgmt/ProcessVersion, /PhaseSetting, /Position, /PositionIsAdjustable, /ProductId, /ProductName, /Role, /Serial


### com.victronenergy.BusItem.GetValue

- **Interfaces**: 1
- **Object Paths**: /Ac/Power, /CustomName, /org/freedesktop/DBus
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 3
- **Complexity**: low
- **Focus Areas**: energy_management, battery_management, home_automation

**Interfaces**:

#### com.victronenergy.BusItem.GetValue (/Ac/Power)
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
- **Focus Areas**: energy_management, battery_management, home_automation

**Interfaces**:

#### com.victronenergy.BusItem (/org/freedesktop/DBus)
- Methods: None
- Signals: None
- Properties: /org/freedesktop/DBus, {path}


### read_provenance

- **Interfaces**: 1
- **Object Paths**: /org/freedesktop/DBus, /proc
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 2
- **Complexity**: low
- **Focus Areas**: energy_management, home_automation

**Interfaces**:

#### com.victronenergy.read_provenance (/org/freedesktop/DBus)
- Methods: None
- Signals: None
- Properties: /org/freedesktop/DBus, /proc


### com.victronenergy.tank.ha_tank

- **Interfaces**: 1
- **Object Paths**: /Ac/Power, /Soc, /sys/class/net/eth0/address
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 3
- **Complexity**: low
- **Focus Areas**: networking_protocols, energy_management, battery_management, home_automation

**Interfaces**:

#### com.victronenergy.tank.ha_tank (/Ac/Power)
- Methods: None
- Signals: None
- Properties: /Ac/Power, /Soc, /sys/class/net/eth0/address


### com.victronenergy.evcharger.

- **Interfaces**: 1
- **Object Paths**: /Ac/L1/Voltage, /Ac/Power, /Connected, /Current, /DeviceInstance, /Mgmt/Connection, /Soc, /VIN
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 8
- **Complexity**: low
- **Focus Areas**: energy_management, battery_management

**Interfaces**:

#### com.victronenergy.evcharger. (/Ac/L1/Voltage)
- Methods: None
- Signals: None
- Properties: /Ac/L1/Voltage, /Ac/Power, /Connected, /Current, /DeviceInstance, /Mgmt/Connection, /Soc, /VIN


### grid_backup

- **Interfaces**: 1
- **Object Paths**: /Ac/Power, /Connected, /CustomName, /DeviceInstance, /LastUpdate, /ProductName, /Role
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 7
- **Complexity**: low
- **Focus Areas**: energy_management, home_automation

**Interfaces**:

#### com.victronenergy.grid_backup (/Ac/Power)
- Methods: None
- Signals: None
- Properties: /Ac/Power, /Connected, /CustomName, /DeviceInstance, /LastUpdate, /ProductName, /Role


### com.victronenergy.grid.

- **Interfaces**: 1
- **Object Paths**: /Ac/Energy/Forward, /Ac/Energy/Reverse, /Connected, /DeviceInstance, /Serial
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 5
- **Complexity**: low
- **Focus Areas**: energy_management, home_automation

**Interfaces**:

#### com.victronenergy.grid. (/Ac/Energy/Forward)
- Methods: None
- Signals: None
- Properties: /Ac/Energy/Forward, /Ac/Energy/Reverse, /Connected, /DeviceInstance, /Serial


### com.victronenergy.grid.

- **Interfaces**: 1
- **Object Paths**: /Ac/Grid/NumberOfPhases, /Connected, /NrOfPhases, /ServiceName
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 4
- **Complexity**: low
- **Focus Areas**: energy_management, home_automation

**Interfaces**:

#### com.victronenergy.grid. (/Ac/Grid/NumberOfPhases)
- Methods: None
- Signals: None
- Properties: /Ac/Grid/NumberOfPhases, /Connected, /NrOfPhases, /ServiceName


### com.victronenergy.settings

- **Interfaces**: 1
- **Object Paths**: /Ac/Consumption/L1/Power, /Ac/Consumption/L2/Power, /Ac/Energy/Daily, /Ac/Energy/Forward, /Ac/Grid/L1/Power, /Ac/Grid/L2/Power, /Ac/Power, /Connected, /CustomName, /Dc/0/Current, /Dc/0/Power, /Dc/0/Voltage, /Dc/Battery/Soc, /Dc/Pv/Power, /Devices/0/Ac/Inverter/P, /Energy/Daily/Yesterday, /History/Daily/0/Yield, /History/Daily/1/Yield, /Hub4/L1/AcPowerSetpoint, /Info/AllowCharge, /Info/AllowDischarge, /Info/DataComplete, /Info/DataTimeout, /Info/LastMeasurementMonotonic, /Mode, /ModeIsAdjustable, /ProductName, /Pv/V, /Settings, /Settings/CGwacs/BatteryLife/State, /Settings/InverterControl/TouExpensiveEndHour, /Settings/InverterControl/TouExpensiveStartHour, /Settings/System/TimeZone, /Soc, /State, /TimeToGo, /Yield/Power, /usr/bin/dbus
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 38
- **Complexity**: medium
- **Focus Areas**: networking_protocols, energy_management, battery_management, home_automation

**Interfaces**:

#### com.victronenergy.settings (/Ac/Consumption/L1/Power)
- Methods: None
- Signals: None
- Properties: /Ac/Consumption/L1/Power, /Ac/Consumption/L2/Power, /Ac/Energy/Daily, /Ac/Energy/Forward, /Ac/Grid/L1/Power, /Ac/Grid/L2/Power, /Ac/Power, /Connected, /CustomName, /Dc/0/Current, /Dc/0/Power, /Dc/0/Voltage, /Dc/Battery/Soc, /Dc/Pv/Power, /Devices/0/Ac/Inverter/P, /Energy/Daily/Yesterday, /History/Daily/0/Yield, /History/Daily/1/Yield, /Hub4/L1/AcPowerSetpoint, /Info/AllowCharge, /Info/AllowDischarge, /Info/DataComplete, /Info/DataTimeout, /Info/LastMeasurementMonotonic, /Mode, /ModeIsAdjustable, /ProductName, /Pv/V, /Settings, /Settings/CGwacs/BatteryLife/State, /Settings/InverterControl/TouExpensiveEndHour, /Settings/InverterControl/TouExpensiveStartHour, /Settings/System/TimeZone, /Soc, /State, /TimeToGo, /Yield/Power, /usr/bin/dbus


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
- **Object Paths**: /, /Ac/Grid/L1/P, /Ac/L1/Power, /Ac/Out/L1/P, /Ac/Power, /CustomName, /Dc/0/Current, /Dc/0/Power, /Dc/0/Temperature, /Dc/0/Voltage, /Soc, /State, /Yield/Power, /org/freedesktop/DBus
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 14
- **Complexity**: low
- **Focus Areas**: energy_management, battery_management

**Interfaces**:

#### com.victronenergy.BusItem (/)
- Methods: None
- Signals: None
- Properties: /, /Ac/Grid/L1/P, /Ac/L1/Power, /Ac/Out/L1/P, /Ac/Power, /CustomName, /Dc/0/Current, /Dc/0/Power, /Dc/0/Temperature, /Dc/0/Voltage, /Soc, /State, /Yield/Power, /org/freedesktop/DBus


### com.victronenergy.BusItem

- **Interfaces**: 1
- **Object Paths**: /org/freedesktop/DBus
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 1
- **Complexity**: low
- **Focus Areas**: energy_management

**Interfaces**:

#### com.victronenergy.BusItem (/org/freedesktop/DBus)
- Methods: None
- Signals: None
- Properties: /org/freedesktop/DBus


### com.victronenergy.battery.ttyO1

- **Interfaces**: 1
- **Object Paths**: /ac/grid/power, /ac/loads/power, /ac/power, /dc/0/power, /dc/0/voltages/cell, /dc/pv/power, /power, /soc, /state, /temperatures/cell, /yield/power
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 11
- **Complexity**: low
- **Focus Areas**: networking_protocols, energy_management, battery_management

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
- **Focus Areas**: energy_management, battery_management, home_automation

**Interfaces**:

#### com.victronenergy.acload.emporia_ch (/api)
- Methods: None
- Signals: None
- Properties: /api, /states, /websocket, config.json


### com.victronenergy.acload.

- **Interfaces**: 1
- **Object Paths**: /Ac/Energy/Forward, /Ac/L1/Power, /Ac/Power, /AllowedRoles, /Connected, /CustomName, /DeviceInstance, /Emporia/Channel, /Emporia/DeviceId, /FirmwareVersion, /IsGenericEnergyMeter, /LastUpdate, /Mgmt/Connection, /Mgmt/ProcessName, /Mgmt/ProcessVersion, /NrOfPhases, /Position, /ProductId, /ProductName, /RefreshTime, /Role, /Serial, /Source/EntityId, /Source/Type, /Status, /api, /websocket
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 27
- **Complexity**: medium
- **Focus Areas**: networking_protocols, energy_management, battery_management

**Interfaces**:

#### com.victronenergy.acload. (/Ac/Energy/Forward)
- Methods: None
- Signals: None
- Properties: /Ac/Energy/Forward, /Ac/L1/Power, /Ac/Power, /AllowedRoles, /Connected, /CustomName, /DeviceInstance, /Emporia/Channel, /Emporia/DeviceId, /FirmwareVersion, /IsGenericEnergyMeter, /LastUpdate, /Mgmt/Connection, /Mgmt/ProcessName, /Mgmt/ProcessVersion, /NrOfPhases, /Position, /ProductId, /ProductName, /RefreshTime, /Role, /Serial, /Source/EntityId, /Source/Type, /Status, /api, /websocket


### method_capture

- **Interfaces**: 1
- **Object Paths**: /org/freedesktop/DBus
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 1
- **Complexity**: low
- **Focus Areas**: energy_management

**Interfaces**:

#### com.victronenergy.method_capture (/org/freedesktop/DBus)
- Methods: None
- Signals: None
- Properties: /org/freedesktop/DBus


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
- **Object Paths**: /Alarms/HighTemperature, /Alarms/HighVoltage, /Alarms/InternalFailure, /Alarms/LowSoc, /Alarms/LowTemperature, /Alarms/LowVoltage, /Capacity, /Connected, /ConsumedAmphours, /CustomName, /Info/DataComplete, /Info/DataTimeout, /Info/LastMeasurementMonotonic, /Info/MissingSources, /Info/SourceStatus, /InstalledCapacity, /Io/AllowToCharge, /Io/AllowToDischarge, /ProductName, /Soc, /System/BatteriesParallel, /System/BatteriesSeries, /System/MaxCellVoltage, /System/MaxVoltageCellId, /System/MinCellVoltage, /System/MinVoltageCellId, /System/NrOfBatteries, /System/NrOfCellsPerBattery, /System/NrOfModulesBlockingCharge, /System/NrOfModulesBlockingDischarge, /System/NrOfModulesOffline, /System/NrOfModulesOnline, /TimeToGo, /Voltages/Diff, /Voltages/Sum
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 35
- **Complexity**: medium
- **Focus Areas**: networking_protocols, energy_management, battery_management, home_automation

**Interfaces**:

#### com.victronenergy.battery. (/Alarms/HighTemperature)
- Methods: None
- Signals: None
- Properties: /Alarms/HighTemperature, /Alarms/HighVoltage, /Alarms/InternalFailure, /Alarms/LowSoc, /Alarms/LowTemperature, /Alarms/LowVoltage, /Capacity, /Connected, /ConsumedAmphours, /CustomName, /Info/DataComplete, /Info/DataTimeout, /Info/LastMeasurementMonotonic, /Info/MissingSources, /Info/SourceStatus, /InstalledCapacity, /Io/AllowToCharge, /Io/AllowToDischarge, /ProductName, /Soc, /System/BatteriesParallel, /System/BatteriesSeries, /System/MaxCellVoltage, /System/MaxVoltageCellId, /System/MinCellVoltage, /System/MinVoltageCellId, /System/NrOfBatteries, /System/NrOfCellsPerBattery, /System/NrOfModulesBlockingCharge, /System/NrOfModulesBlockingDischarge, /System/NrOfModulesOffline, /System/NrOfModulesOnline, /TimeToGo, /Voltages/Diff, /Voltages/Sum


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
- **Object Paths**: Dc/0/MaxChargeCurrent, Mode, SocLimit
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 3
- **Complexity**: low
- **Focus Areas**: networking_protocols, energy_management, battery_management, home_automation

**Interfaces**:

#### com.victronenergy.server (Dc/0/MaxChargeCurrent)
- Methods: None
- Signals: None
- Properties: Dc/0/MaxChargeCurrent, Mode, SocLimit


### mqtt_bridge

- **Interfaces**: 1
- **Object Paths**: /Ac/Energy/Forward, /Ac/Energy/Reverse, /Ac/Frequency, /Ac/L1/Current, /Ac/L1/Voltage, /Ac/Power, /Alarm, /Capacity, /CellVoltages, /Dc/0/Current, /Dc/0/Power, /Dc/0/Temperature, /Dc/0/Voltage, /FluidType, /Level, /Remaining, /Soc, /Temperature, /Unit, /Value, /set
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 21
- **Complexity**: medium
- **Focus Areas**: networking_protocols, energy_management, battery_management

**Interfaces**:

#### com.victronenergy.mqtt_bridge (/Ac/Energy/Forward)
- Methods: None
- Signals: None
- Properties: /Ac/Energy/Forward, /Ac/Energy/Reverse, /Ac/Frequency, /Ac/L1/Current, /Ac/L1/Voltage, /Ac/Power, /Alarm, /Capacity, /CellVoltages, /Dc/0/Current, /Dc/0/Power, /Dc/0/Temperature, /Dc/0/Voltage, /FluidType, /Level, /Remaining, /Soc, /Temperature, /Unit, /Value, /set


### com.victronenergy.mock.

- **Interfaces**: 1
- **Object Paths**: /Ac/Energy/Forward, /Ac/Energy/Reverse, /Ac/Frequency, /Ac/L1/Current, /Ac/L1/Power, /Ac/L1/Voltage, /Ac/L2/Current, /Ac/L2/Power, /Ac/L2/Voltage, /Ac/L3/Current, /Ac/L3/Power, /Ac/L3/Voltage, /Ac/MaxPower, /Ac/Power, /Alarm/CellImbalance, /Alarm/HighTemperature, /Alarm/InternalFailure, /Alarm/LowSoc, /Alarm/LowTemperature, /Alarms, /Alarms/CellImbalance, /Alarms/HighTemperature, /Alarms/InternalFailure, /Alarms/LowSoc, /Alarms/LowTemperature, /Balancing, /BatteryState, /Capacity, /ChargeCurrent, /ChargeVoltage, /Connected, /CustomName, /Dc/0/AllowCharge, /Dc/0/AllowDischarge, /Dc/0/ConsumedAmphours, /Dc/0/Current, /Dc/0/MaxChargeCurrent, /Dc/0/MaxChargeVoltage, /Dc/0/MaxDischargeCurrent, /Dc/0/Power, /Dc/0/Temperature, /Dc/0/Voltage, /DeviceInstance, /FirmwareVersion, /FluidType, /HardwareVersion, /Level, /MaxChargeCurrent, /MaxDischargeCurrent, /Mgmt/Connection, /Mgmt/ProcessName, /Mgmt/ProcessVersion, /Model, /ProductId, /ProductName, /Remaining, /Serial, /Soc, /SystemMaxCellVoltage, /SystemMinCellVoltage, /Temperature, /TemperatureType, /TimeRemaining, /opt/victronenergy/velib_python
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 40
- **Complexity**: low
- **Focus Areas**: networking_protocols, energy_management, battery_management

**Interfaces**:

#### com.victronenergy.mock. (/Ac/Energy/Forward)
- Methods: None
- Signals: None
- Properties: /Ac/Energy/Forward, /Ac/Energy/Reverse, /Ac/Frequency, /Ac/L1/Current, /Ac/L1/Power, /Ac/L1/Voltage, /Ac/L2/Current, /Ac/L2/Power, /Ac/L2/Voltage, /Ac/L3/Current, /Ac/L3/Power, /Ac/L3/Voltage, /Ac/MaxPower, /Ac/Power, /Alarm/CellImbalance, /Alarm/HighTemperature, /Alarm/InternalFailure, /Alarm/LowSoc, /Alarm/LowTemperature, /Alarms, /Alarms/CellImbalance, /Alarms/HighTemperature, /Alarms/InternalFailure, /Alarms/LowSoc, /Alarms/LowTemperature, /Balancing, /BatteryState, /Capacity, /ChargeCurrent, /ChargeVoltage, /Connected, /CustomName, /Dc/0/AllowCharge, /Dc/0/AllowDischarge, /Dc/0/ConsumedAmphours, /Dc/0/Current, /Dc/0/MaxChargeCurrent, /Dc/0/MaxChargeVoltage, /Dc/0/MaxDischargeCurrent, /Dc/0/Power


### cerbo

- **Interfaces**: 1
- **Object Paths**: /, /AcPowerSetpoint, /Power
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 3
- **Complexity**: low
- **Focus Areas**: networking_protocols, energy_management, battery_management, home_automation

**Interfaces**:

#### com.victronenergy.cerbo (/)
- Methods: None
- Signals: None
- Properties: /, /AcPowerSetpoint, /Power


### server

- **Interfaces**: 1
- **Object Paths**: /api/settings, /api/state, /api/update, /app/src/inverter_dashboard/static, /assets, /health/live, /static, /ws
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 8
- **Complexity**: low
- **Focus Areas**: networking_protocols, energy_management, battery_management, home_automation

**Interfaces**:

#### com.victronenergy.server (/api/settings)
- Methods: None
- Signals: None
- Properties: /api/settings, /api/state, /api/update, /app/src/inverter_dashboard/static, /assets, /health/live, /static, /ws


### com.victronenergy.tank.ha_tank

- **Interfaces**: 1
- **Object Paths**: /ActiveTankService, /Capacity, /Connected, /CustomName, /DeviceInstance, /FirmwareVersion, /FluidType, /HardwareVersion, /Level, /Mgmt/Connection, /Mgmt/ProcessName, /Mgmt/ProcessVersion, /Mode, /ProductId, /ProductName, /Remaining, /Serial, /State, /Status
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 19
- **Complexity**: medium
- **Focus Areas**: energy_management

**Interfaces**:

#### com.victronenergy.tank.ha_tank (/ActiveTankService)
- Methods: None
- Signals: None
- Properties: /ActiveTankService, /Capacity, /Connected, /CustomName, /DeviceInstance, /FirmwareVersion, /FluidType, /HardwareVersion, /Level, /Mgmt/Connection, /Mgmt/ProcessName, /Mgmt/ProcessVersion, /Mode, /ProductId, /ProductName, /Remaining, /Serial, /State, /Status


### cerbo_mqtt

- **Interfaces**: 1
- **Object Paths**: /Ac/Current, /Ac/Energy/Forward, /Ac/Frequency, /Ac/Power, /Connected, /availability, /state
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 7
- **Complexity**: low
- **Focus Areas**: energy_management, networking_protocols

**Interfaces**:

#### com.victronenergy.cerbo_mqtt (/Ac/Current)
- Methods: None
- Signals: None
- Properties: /Ac/Current, /Ac/Energy/Forward, /Ac/Frequency, /Ac/Power, /Connected, /availability, /state


### charger

- **Interfaces**: 1
- **Object Paths**: /Ac/Current, /Ac/Energy/Forward, /Ac/Frequency, /Ac/Power, /Connected, /Current, /NrOfPhases, /Status
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 8
- **Complexity**: low
- **Focus Areas**: energy_management, networking_protocols

**Interfaces**:

#### com.victronenergy.charger (/Ac/Current)
- Methods: None
- Signals: None
- Properties: /Ac/Current, /Ac/Energy/Forward, /Ac/Frequency, /Ac/Power, /Connected, /Current, /NrOfPhases, /Status


### com.victronenergy.evcharger.

- **Interfaces**: 1
- **Object Paths**: /Ac/Energy/Forward, /Ac/Frequency, /Ac/L1/Current, /Ac/L1/Power, /Ac/L1/PowerFactor, /Ac/L1/Voltage, /Ac/L2/Current, /Ac/L2/Power, /Ac/L2/PowerFactor, /Ac/L2/Voltage, /Ac/L3/Current, /Ac/L3/Power, /Ac/L3/PowerFactor, /Ac/L3/Voltage, /Ac/Power, /Alarms/BlockedWarning, /Alarms/CPInputShortCircuit, /Alarms/DisplayFWUpdateFailure1, /Alarms/DisplayFWUpdateFailure2, /Alarms/DisplayFWUpdateInProgress, /Alarms/ExternalCurrentLimit, /Alarms/GNDNotPresent, /Alarms/GxCommWarning, /Alarms/HighTempWarning, /Alarms/LightSensorICFault, /Alarms/OverTemperature, /Alarms/OverloadActive, /Alarms/OverloadDetected, /Alarms/ResidualCurrent, /Alarms/SetupNeeded, /Alarms/SystemCausedCurrentLimit, /Alarms/TamperDetected, /Alarms/TimeSyncIssue, /Alarms/WeldedContacts, /AutoStart, /Connected, /Current, /CustomName, /DeviceInstance, /EnableDisplay, /FirmwareVersion, /HardwareVersion, /IsGenericEnergyMeter, /MaxCurrent, /Mgmt/Connection, /Mgmt/ProcessName, /Mgmt/ProcessVersion, /MinCurrent, /Mode, /Model, /NrOfPhases, /Position, /PositionIsAdjustable, /ProductId, /ProductName, /Serial, /Session/Cost, /Session/Energy, /Session/SavedCost, /Session/Time, /Session/UserId, /Session/UserIdType, /SetCurrent, /StartStop, /Status
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 40
- **Complexity**: medium
- **Focus Areas**: energy_management, battery_management, home_automation

**Interfaces**:

#### com.victronenergy.evcharger. (/Ac/Energy/Forward)
- Methods: None
- Signals: None
- Properties: /Ac/Energy/Forward, /Ac/Frequency, /Ac/L1/Current, /Ac/L1/Power, /Ac/L1/PowerFactor, /Ac/L1/Voltage, /Ac/L2/Current, /Ac/L2/Power, /Ac/L2/PowerFactor, /Ac/L2/Voltage, /Ac/L3/Current, /Ac/L3/Power, /Ac/L3/PowerFactor, /Ac/L3/Voltage, /Ac/Power, /Alarms/BlockedWarning, /Alarms/CPInputShortCircuit, /Alarms/DisplayFWUpdateFailure1, /Alarms/DisplayFWUpdateFailure2, /Alarms/DisplayFWUpdateInProgress, /Alarms/ExternalCurrentLimit, /Alarms/GNDNotPresent, /Alarms/GxCommWarning, /Alarms/HighTempWarning, /Alarms/LightSensorICFault, /Alarms/OverTemperature, /Alarms/OverloadActive, /Alarms/OverloadDetected, /Alarms/ResidualCurrent, /Alarms/SetupNeeded, /Alarms/SystemCausedCurrentLimit, /Alarms/TamperDetected, /Alarms/TimeSyncIssue, /Alarms/WeldedContacts, /AutoStart, /Connected, /Current, /CustomName, /DeviceInstance, /EnableDisplay


### client

- **Interfaces**: 1
- **Object Paths**: /v2/vehicles
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 1
- **Complexity**: low
- **Focus Areas**: energy_management, battery_management, home_automation

**Interfaces**:

#### com.victronenergy.client (/v2/vehicles)
- Methods: None
- Signals: None
- Properties: /v2/vehicles


### com.victronenergy.ev.

- **Interfaces**: 1
- **Object Paths**: /Ac/Energy/Forward, /Ac/L1/Current, /Ac/L1/Power, /Ac/L1/Voltage, /Ac/L2/Power, /Ac/L3/Power, /Ac/Power, /AtSite, /BatteryCapacity, /ChargingState, /ChargingTime, /Connected, /Current, /CustomName, /DeviceInstance, /FirmwareVersion, /HardwareVersion, /IsGenericEnergyMeter, /MaxCurrent, /Mgmt/Connection, /Mgmt/ProcessName, /Mgmt/ProcessVersion, /Mode, /NrOfPhases, /Odometer, /Position, /Position/Latitude, /Position/Longitude, /PositionIsAdjustable, /ProductId, /ProductName, /RangeToGo, /Serial, /Session/Energy, /SetCurrent, /Soc, /StartStop, /Status, /TargetSoc, /VIN
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 40
- **Complexity**: medium
- **Focus Areas**: networking_protocols, energy_management, battery_management, home_automation

**Interfaces**:

#### com.victronenergy.ev. (/Ac/Energy/Forward)
- Methods: None
- Signals: None
- Properties: /Ac/Energy/Forward, /Ac/L1/Current, /Ac/L1/Power, /Ac/L1/Voltage, /Ac/L2/Power, /Ac/L3/Power, /Ac/Power, /AtSite, /BatteryCapacity, /ChargingState, /ChargingTime, /Connected, /Current, /CustomName, /DeviceInstance, /FirmwareVersion, /HardwareVersion, /IsGenericEnergyMeter, /MaxCurrent, /Mgmt/Connection, /Mgmt/ProcessName, /Mgmt/ProcessVersion, /Mode, /NrOfPhases, /Odometer, /Position, /Position/Latitude, /Position/Longitude, /PositionIsAdjustable, /ProductId, /ProductName, /RangeToGo, /Serial, /Session/Energy, /SetCurrent, /Soc, /StartStop, /Status, /TargetSoc, /VIN


### com.victronenergy.BusItem

- **Interfaces**: 1
- **Object Paths**: /Climate/Control, /Climate/ControlAvailable, /Climate/ControlEnabled, /Climate/ControlOutcome, /Climate/ControlPending, /Climate/ControlReason, /Climate/Decision, /Climate/DecisionReason, /Climate/EstimatedHeatingPower, /Climate/HvacAction, /Climate/HvacMode, /Climate/IntegrationHealthy, /Climate/LastUpdate, /Climate/Phase, /Climate/ServiceMode, /Climate/TargetTemperature, /Connected, /CustomName, /DeviceInstance, /FirmwareVersion, /HardwareVersion, /Mgmt/Connection, /Mgmt/ProcessName, /Mgmt/ProcessVersion, /ProductId, /ProductName, /Serial, /Settings/System/Units/Temperature, /Status, /SwitchableOutput/0, /SwitchableOutput/1, /Temperature, /TemperatureType
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 0
- **Complexity**: low
- **Focus Areas**: networking_protocols, energy_management, battery_management, home_automation

**Interfaces**:

#### com.example.commanditem (/commanditem)
- Methods: None
- Signals: None
- Properties: None


### com.victronenergy.system

- **Interfaces**: 1
- **Object Paths**: /L, /Total/Power, /org/freedesktop/DBus
- **Total Methods**: 0
- **Total Signals**: 0
- **Total Properties**: 3
- **Complexity**: low
- **Focus Areas**: energy_management, battery_management, home_automation

**Interfaces**:

#### com.victronenergy.system (/L)
- Methods: None
- Signals: None
- Properties: /L, /Total/Power, /org/freedesktop/DBus



---

## 📈 GitHub Statistics

```json
{
  "analysis_scope": {
    "max_dbus_matches_per_repository": 10,
    "max_esphome_matches_per_repository": 15,
    "max_files_per_repository_per_analyzer": 80,
    "max_repositories_per_analyzer": 25,
    "max_repositories_per_owner": 100
  },
  "errors": [],
  "generation": {
    "mode": "llm",
    "provider_reported_model": "nvidia_nim/nvidia/nemotron-3.5-super-vl-120b-a12b",
    "requested_model": "nvidia_nim/nvidia/nemotron-3.5-super-vl-120b-a12b"
  },
  "iot_repos": 80,
  "scanned_at": "2026-10-30T12:35:46.926932+00:00",
  "total_repos": 91
}
```