# Quickstart: Zigbee Demo Infrastructure

## Overview

This demo runs locally on a macOS laptop using Docker, Zigbee2MQTT, ser2net, and
a local Mosquitto MQTT broker. Expected setup time: 20 minutes.

## Prerequisites

- macOS laptop
- Docker Desktop installed and running
- A compatible Zigbee coordinator USB adapter connected to the laptop (or a
  small host on the same network)
- ser2net installed and running on the host that has the Zigbee adapter

## Setup

1. Open a terminal and go to the repo root:

```bash
cd /Users/caffeinatedgaze/workspace/horn/zigbee-infra
```

2. Create environment file from the example:

```bash
cp .env.example .env
```

3. Ensure ser2net is exposing the Zigbee adapter as a serial-over-TCP endpoint.
   Record the host and port (for example, `192.168.1.50:3333`).

4. Start the demo stack:

```bash
docker compose up -d
```

## Pairing Bulbs

1. Put a bulb into pairing mode.
2. Start pairing from the control API or UI.
3. Verify the bulb appears in the device list.

## Basic Control

- Toggle a device on/off.
- Set brightness for a device or group.

## Smoke Check

Run the smoke check script to validate the demo path:

```bash
./scripts/smoke-check.sh
```

Expected result: the script completes in under 5 minutes and confirms pairing
and control endpoints are responsive.

## Data Reset

To clear demo data and re-pair devices:

```bash
./scripts/reset-demo.sh
```

This removes local state and MQTT retained messages so the next demo starts
cleanly.
