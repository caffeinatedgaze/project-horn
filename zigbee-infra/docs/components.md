# Components

## ser2net (Host)

**Purpose**: Exposes the Zigbee USB adapter as a serial-over-TCP endpoint so
containers can access it without direct USB passthrough.

**Inputs**: Serial device (USB Zigbee dongle)
**Outputs**: TCP socket (e.g., `192.168.1.50:3333`)

**Example**:
- TCP endpoint: `SERIAL_HOST=192.168.1.50`, `SERIAL_PORT=3333`

## Mosquitto (Docker)

**Purpose**: Local MQTT broker for Zigbee2MQTT and the control API.

**Inputs**: MQTT publish/subscribe messages on port 1883
**Outputs**: MQTT topics for device state and commands

**Example**:
- Broker URL: `mqtt://mosquitto:1883`

## Zigbee2MQTT (Docker)

**Purpose**: Bridges Zigbee devices to MQTT.

**Inputs**: Serial-over-TCP endpoint from ser2net, MQTT broker
**Outputs**: MQTT topics under `zigbee2mqtt/*`

**Example**:
- Serial endpoint: `tcp://192.168.1.50:3333`
- MQTT server: `mqtt://mosquitto:1883`

## Control API (Docker)

**Purpose**: Simple HTTP interface for demo pairing and device control.

**Inputs**: HTTP requests on port 8080
**Outputs**: MQTT commands to Zigbee2MQTT, JSON responses

**Example**:
- Health: `GET /health`
- Pairing: `POST /pairing/start`
- Device state: `POST /devices/{deviceId}/state`

## Example API Calls

```bash
curl -X POST http://localhost:8080/pairing/start
curl http://localhost:8080/devices
curl -X POST http://localhost:8080/devices/office-lamp/state \
  -H 'Content-Type: application/json' \
  -d '{"state":"ON","brightness":150}'
```

## Docker Compose Runbook

```bash
# Start stack
cd /Users/caffeinatedgaze/workspace/horn/zigbee-infra
cp .env.example .env
docker compose up -d

# Stop stack
docker compose down
```
