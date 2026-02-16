#!/usr/bin/env bash
set -euo pipefail

echo "Stopping stack..."
docker compose down

echo "Clearing Zigbee2MQTT data..."
rm -rf infra/zigbee2mqtt/data/*

echo "Clearing Mosquitto data..."
rm -rf infra/mosquitto/data/*

echo "Demo reset complete."
