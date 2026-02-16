#!/usr/bin/env bash
set -euo pipefail

echo "Checking docker compose services..."
docker compose ps

echo "Checking control API health..."
STATUS=$(curl -s http://localhost:8080/health | tr -d '\n')
if [[ "$STATUS" != *"ok"* ]]; then
  echo "Health check failed: $STATUS"
  exit 1
fi

echo "Smoke check passed."
