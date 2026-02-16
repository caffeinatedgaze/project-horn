#!/usr/bin/env bash
set -euo pipefail

SERIAL_DEVICE="${SERIAL_DEVICE:-}"
SERIAL_PORT="${SERIAL_PORT:-3333}"
SERIAL_HOST="${SERIAL_HOST:-}"
SERIAL_BAUD="${SERIAL_BAUD:-115200}"

if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew is required. Install from https://brew.sh/" >&2
  exit 1
fi

echo "Installing ser2net..."
brew install ser2net

CONFIG_DIR="$(brew --prefix)/etc/ser2net"
CONFIG_FILE="$CONFIG_DIR/ser2net.yaml"

if [[ -z "$SERIAL_DEVICE" ]]; then
  echo "No SERIAL_DEVICE provided. Detected devices:"
  ls /dev/tty.* /dev/cu.* 2>/dev/null || true
  echo
  read -r -p "Enter Zigbee dongle device path (e.g., /dev/cu.usbserial-XXXX): " SERIAL_DEVICE
fi

if [[ -z "$SERIAL_DEVICE" ]]; then
  echo "SERIAL_DEVICE is required." >&2
  exit 1
fi

mkdir -p "$CONFIG_DIR"

if [[ -n "$SERIAL_HOST" ]]; then
  ACCEPTOR="tcp,${SERIAL_HOST},${SERIAL_PORT}"
else
  ACCEPTOR="tcp,${SERIAL_PORT}"
fi

cat <<YAML > "$CONFIG_FILE"
connection: &zigbee
  accepter: ${ACCEPTOR}
  connector: serialdev,${SERIAL_DEVICE},${SERIAL_BAUD}n81,local
YAML

echo "Wrote ser2net config to $CONFIG_FILE"

echo "Starting ser2net service..."
brew services restart ser2net

echo "Done. Verify with:"
echo "  lsof -iTCP:${SERIAL_PORT} -sTCP:LISTEN"
