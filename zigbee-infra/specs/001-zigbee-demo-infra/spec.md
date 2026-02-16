# Feature Specification: Zigbee Demo Infrastructure

**Feature Branch**: `001-zigbee-demo-infra`  
**Created**: 2026-02-10  
**Status**: Draft  
**Input**: User description: "I need containerized infra to connected 3-10 zigbee ligth bulbs. It should run on my macos laptop."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Pair and Register Bulbs (Priority: P1)

As a demo operator, I need to pair 3-10 Zigbee light bulbs to my laptop so the
system can recognize and control them during a demo.

**Why this priority**: Without paired bulbs, no demo is possible.

**Independent Test**: Start the system, put a bulb into pairing mode, and verify
it appears as a controllable device.

**Acceptance Scenarios**:

1. **Given** the system is running, **When** I initiate pairing and put a bulb
   into pairing mode, **Then** the bulb appears in the device list as paired.
2. **Given** a bulb is already paired, **When** I attempt to pair it again,
   **Then** the system prevents duplicate entries and reports the existing device.

---

### User Story 2 - Control Individual and Group Lighting (Priority: P2)

As a demo operator, I need to control on/off and brightness for individual bulbs
and a named group so I can demonstrate core lighting behavior.

**Why this priority**: Control is the primary value shown in the demo.

**Independent Test**: Issue a command to toggle and dim a single bulb and a
predefined group and verify the bulbs respond.

**Acceptance Scenarios**:

1. **Given** paired bulbs exist, **When** I send an on/off command to a single
   bulb, **Then** that bulb changes state within a short, observable time.
2. **Given** a group is defined, **When** I send a brightness change to the group,
   **Then** all bulbs in the group update to the requested level.

---

### User Story 3 - Monitor Status and Recover from Disconnects (Priority: P3)

As a demo operator, I need to see basic device status and recover from temporary
disconnects so the demo remains reliable.

**Why this priority**: Demo reliability depends on quick visibility and recovery.

**Independent Test**: Temporarily power off a bulb, observe a status update, then
power it back on and verify it is usable again.

**Acceptance Scenarios**:

1. **Given** a paired bulb is unreachable, **When** I view device status,
   **Then** the bulb is marked as unavailable.
2. **Given** an unavailable bulb becomes reachable again, **When** the system
   refreshes status, **Then** the bulb returns to available without re-pairing.

---

### Edge Cases

- What happens when a coordinator or adapter is disconnected during pairing?
- How does the system handle more than 10 bulbs attempting to pair?
- What happens when a paired bulb is reset to factory settings?

### Assumptions

- A compatible Zigbee coordinator hardware adapter is available and connected to
  the laptop.
- The demo is intended for local control on the laptop without external internet
  dependency.
- The goal is a simple, understandable demo flow over advanced automation.
- The Zigbee dongle stays on the host (or a small host) and is exposed via
  ser2net as a serial-over-TCP endpoint.
- Zigbee2MQTT runs in Docker (or VM) and connects to the remote adapter over
  TCP.
- Mosquitto runs in Docker as the local MQTT broker.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow pairing of 3-10 Zigbee light bulbs.
- **FR-002**: System MUST maintain a persistent list of paired bulbs across
  restarts.
- **FR-003**: Users MUST be able to toggle on/off and set brightness for a single
  bulb.
- **FR-004**: Users MUST be able to issue the same control commands to a named
  group of bulbs.
- **FR-005**: System MUST show basic device status (available/unavailable) for
  each paired bulb.
- **FR-006**: System MUST prevent duplicate entries when re-pairing an existing
  bulb.
- **FR-007**: System MUST support a simple recovery path when bulbs reconnect
  after temporary loss of power.
- **FR-008**: System MUST run on a macOS laptop in a containerized environment.
- **FR-009**: System MUST expose the Zigbee dongle as a serial-over-TCP endpoint
  using ser2net on the host (or a small host).
- **FR-010**: System MUST run Zigbee2MQTT in Docker and connect it to the remote
  serial endpoint.
- **FR-011**: System MUST use Mosquitto in Docker as the local MQTT broker.

### Demo Requirements *(mandatory for demo infrastructure)*

- **DR-001**: Provide a single demo setup command or script and document it.
- **DR-002**: State expected setup time and prerequisites in quickstart.md.
- **DR-003**: Document component contracts and example I/O.
- **DR-004**: Provide `.env.example` with safe dummy values.
- **DR-005**: Define a smoke check command/script and a data reset path.

### Key Entities *(include if feature involves data)*

- **Device**: A paired Zigbee bulb with identifiers, name, and status.
- **Group**: A named collection of devices for bulk control.
- **Pairing Session**: The user-initiated pairing window and its results.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A new user can pair at least 3 bulbs in under 15 minutes.
- **SC-002**: A control command (on/off or brightness) affects a target bulb or
  group within 5 seconds in 95% of attempts.
- **SC-003**: The demo setup completes in under 20 minutes on a macOS laptop.
- **SC-004**: The smoke check validates the demo path in under 5 minutes.
