# Control API (Python)

Minimal local HTTP API for pairing and controlling Zigbee bulbs via MQTT.

## Run (via Docker Compose)

```bash
docker compose up -d
```

## Health

```bash
curl http://localhost:8080/health
```

## MIDI mapping (10 bulbs + group channel)

Configure optional bulb IDs with `MIDI_BULB_IDS` as a comma-separated list of 10
friendly names/device IDs. `channel=0` maps to the first ID, `channel=9` maps
to the tenth. `channel=10` publishes to group `all_bulbs`, and `channel=11`
publishes to group `except_ceiling`. Use `NONE` for intentionally unmapped bulb
channels.

```bash
curl http://localhost:8080/midi/mapping
```

## MIDI event ingest

`channel` selects the target (`0..9` bulbs, `10` group `all_bulbs`, `11` group
`except_ceiling`). `key`
(note number, `0..17`) is mapped with a
step function to Zigbee brightness (`1..254`). If `key` is missing (no note),
the API sets `brightness=0`.

If `event_type` is `note_off`, the API forces `brightness=0` even if `key` is present.

```bash
curl -X POST http://localhost:8080/midi/events \
  -H "content-type: application/json" \
  -d '{"channel":0,"key":17,"timestamp":"2026-02-11T12:15:22.871252+00:00"}'
```

No note (turn OFF):

```bash
curl -X POST http://localhost:8080/midi/events \
  -H "content-type: application/json" \
  -d '{"channel":0,"timestamp":"2026-02-11T12:15:22.871252+00:00"}'
```

Note ended (turn OFF):

```bash
curl -X POST http://localhost:8080/midi/events \
  -H "content-type: application/json" \
  -d '{"event_type":"note_off","channel":0,"key":17,"timestamp":"2026-02-11T12:15:22.871252+00:00"}'
```
