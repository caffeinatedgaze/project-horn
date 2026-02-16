#!/usr/bin/env bash
set -euo pipefail

API_URL="${API_URL:-http://127.0.0.1:8000/midi/events}"

echo "[smoke] verifying CLI starts"
uv run blink-midi --help >/dev/null

echo "[smoke] run with --demo-once to emit one simulated event"
uv run blink-midi run --device "demo-device" --api-url "$API_URL" --demo-once

echo "[smoke] success"
