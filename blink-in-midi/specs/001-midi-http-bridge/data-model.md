# Data Model: MIDI to Local API Bridge

## Entity: MidiInputEvent

### Description
Normalized representation of one incoming MIDI message from the selected input
device.

### Fields
- `event_type` (enum): `note_on`, `note_off`, `control_change`
- `channel` (int): MIDI channel 0-15
- `key` (int): note number or control number, range 0-127
- `value` (int): velocity or control value, range 0-127
- `timestamp` (string): ISO-8601 UTC timestamp
- `source_device` (string): selected MIDI input device name

### Validation Rules
- Ignore messages not in supported `event_type` set.
- Reject values outside MIDI range boundaries.
- Timestamp must be generated at event handling time.

## Entity: OutboundRequestIntent

### Description
A deterministic request intent produced from one `MidiInputEvent` for the local
API.

### Fields
- `method` (string): `POST`
- `url` (string): target local API endpoint URL
- `headers` (object): request headers map, default includes content type
- `payload` (object): stable mapped JSON object
- `simulated_sent` (bool): always `true` for current stubbed-send phase
- `failure_reason` (string|null): reason when intent processing fails

### Validation Rules
- `method` is fixed to `POST` in current scope.
- `url` must be non-empty and parse as local HTTP URL.
- `payload` must include all required schema keys.

## Entity: BridgeSession

### Description
Runtime state for one bridge execution.

### Fields
- `session_id` (string): unique ID per run
- `started_at` (string): ISO-8601 UTC timestamp
- `selected_device` (string): active input device
- `api_url` (string): resolved endpoint URL
- `processed_events` (int): count of supported events handled
- `ignored_events` (int): unsupported events ignored
- `intent_failures` (int): failed intent processing attempts

### State Transitions
- `initialized` -> `running`: device selected and listener active.
- `running` -> `running`: per-event processing, including failures.
- `running` -> `stopped`: user interrupt or unrecoverable startup failure.
