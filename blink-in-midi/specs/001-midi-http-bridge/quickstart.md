# Quickstart: MIDI to Local API Bridge

## Prerequisites

- macOS host with at least one MIDI input source.
- Python 3.11 available.
- `uv` installed.
- Local API endpoint available (default target documented below).

Expected setup time: 5-10 minutes.

## Setup

From repository root:

```bash
uv sync
```

## Run

Single command path for demo run:

```bash
uv run blink-midi run --device "<MIDI_DEVICE_NAME>" --api-url "http://127.0.0.1:8000/midi/events"
```

For a no-hardware sanity check:

```bash
uv run blink-midi run --device "demo-device" --api-url "http://127.0.0.1:8000/midi/events" --demo-once
```

## Smoke Check

1. Start the bridge with the run command above.
2. Send a `note_on` or `control_change` message from the selected MIDI source.
3. Verify one outbound request intent log entry appears with mapped payload.
4. Optionally run `scripts/smoke_check.sh` for scripted verification.

## Demo Reset Path

- Stop the bridge process (`Ctrl+C`).
- Restart the local API if needed.
- Re-run the same `uv run blink-midi run ...` command.

## Environment Variables

- `API_URL`: optional fallback for endpoint URL.
- `LOG_LEVEL`: optional logging level (default `INFO`).

## Safety

- Use only local/non-production endpoints.
- Do not place real credentials in environment files.
