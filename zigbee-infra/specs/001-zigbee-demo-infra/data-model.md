# Data Model: Zigbee Demo Infrastructure

## Entity: Device

**Purpose**: Represents a paired Zigbee bulb.

**Fields**:
- `device_id` (string, required): Unique identifier from Zigbee2MQTT
- `friendly_name` (string, required): Human-readable name
- `status` (enum: available, unavailable, required): Current reachability
- `last_seen_at` (timestamp, optional): Last time the device reported in
- `capabilities` (object, optional): Supported features like on/off, brightness

**Validation Rules**:
- `device_id` must be unique
- `friendly_name` must be non-empty

**State Transitions**:
- `available` -> `unavailable` when device becomes unreachable
- `unavailable` -> `available` when device reconnects

## Entity: Group

**Purpose**: Named collection of devices for bulk control.

**Fields**:
- `group_id` (string, required): Unique identifier
- `name` (string, required): Display name
- `device_ids` (array of string, required): Member devices

**Validation Rules**:
- `name` must be unique
- `device_ids` must reference existing devices

## Entity: PairingSession

**Purpose**: Tracks a user-initiated pairing window.

**Fields**:
- `session_id` (string, required): Unique identifier
- `started_at` (timestamp, required)
- `ended_at` (timestamp, optional)
- `status` (enum: active, completed, cancelled, required)
- `paired_device_ids` (array of string, optional)

**Validation Rules**:
- Only one session can be `active` at a time

**State Transitions**:
- `active` -> `completed` when pairing stops normally
- `active` -> `cancelled` when user ends early
