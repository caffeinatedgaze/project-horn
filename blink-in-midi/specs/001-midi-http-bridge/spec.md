# Feature Specification: MIDI to Local API Bridge

**Feature Branch**: `001-midi-http-bridge`  
**Created**: 2026-02-10  
**Status**: Draft  
**Input**: User description: "I want to create a MIDI input device. It should receive MIDI signals and make HTTP calls to a certain local API with the values supplied in MIDI."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Trigger API from MIDI Input (Priority: P1)

As a demo operator, I can connect a MIDI input device and have incoming MIDI
messages automatically trigger requests to a configured local service so I can
control the service in real time.

**Why this priority**: This is the core value of the feature and the minimum
behavior needed for the demo.

**Independent Test**: Send a MIDI message from a connected device and verify one
corresponding request is received by the local service with the expected values.

**Acceptance Scenarios**:

1. **Given** a configured MIDI device and active bridge, **When** a supported MIDI
   message is received, **Then** the bridge sends one request to the configured
   local service with mapped values from that message.
2. **Given** no incoming MIDI messages, **When** the bridge is running,
   **Then** no requests are sent.

---

### User Story 2 - Preserve Message Meaning in Outbound Data (Priority: P2)

As a demo operator, I can rely on outbound request fields to reflect MIDI
message type and value ranges consistently so downstream behavior is predictable.

**Why this priority**: Reliable mapping quality is required for a credible demo,
while still secondary to simply triggering requests.

**Independent Test**: Send a representative set of MIDI message types and verify
each outbound request includes expected field names and normalized values.

**Acceptance Scenarios**:

1. **Given** incoming note and control messages, **When** each is processed,
   **Then** outbound data includes message type, channel, identifier, and value.
2. **Given** repeated messages with the same payload, **When** processed,
   **Then** outbound data remains consistent across repeats.

---

### User Story 3 - Continue Operating Through Local Service Failures (Priority: P3)

As a demo operator, I can see failed request attempts and continue receiving new
MIDI processing so short service outages do not force a restart.

**Why this priority**: Demo resilience matters, but it is less critical than the
base data path.

**Independent Test**: Stop the local service temporarily, send MIDI messages,
restart the service, and verify later messages are still processed and delivered.

**Acceptance Scenarios**:

1. **Given** the local service is unreachable, **When** a MIDI message arrives,
   **Then** the failure is recorded and processing continues for later messages.
2. **Given** the local service becomes reachable again, **When** new MIDI
   messages arrive, **Then** requests are delivered without manual restart.

### Edge Cases

- MIDI device disconnects while the bridge is running.
- Unsupported MIDI message types are received.
- Message bursts arrive faster than the local service can process requests.
- Local service returns non-success responses.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow selection of one MIDI input source for active
  message intake.
- **FR-002**: System MUST process incoming MIDI note and control messages and
  transform them into outbound request payloads.
- **FR-003**: System MUST send one outbound request per processed MIDI message to
  a configured local service endpoint.
- **FR-004**: Outbound payloads MUST include at minimum message type, MIDI
  channel, message identifier, and message value.
- **FR-005**: System MUST enforce deterministic value transformation so the same
  MIDI input always produces the same outbound payload fields.
- **FR-006**: System MUST ignore unsupported MIDI message types without stopping
  active processing.
- **FR-007**: System MUST record request failures with enough detail to identify
  the failed message and reason.
- **FR-008**: System MUST continue processing new MIDI messages after an outbound
  request failure.
- **FR-009**: System MUST provide a runnable demo flow from startup through first
  successful MIDI-triggered request.

### Demo Requirements *(mandatory for demo infrastructure)*

- **DR-001**: Demo implementation MUST use the simplest architecture that works.
- **DR-002**: Any added dependency/component MUST include demo-critical
  justification.
- **DR-003**: Provide one documented setup-and-run command or script.
- **DR-004**: State expected setup time and prerequisites in quickstart.md.
- **DR-005**: Provide `.env.example` with safe dummy values and define a reset
  path.
- **DR-006**: Define a smoke check command/script for the core demo flow.

### Key Entities *(include if feature involves data)*

- **MIDI Input Event**: A single incoming message with type, channel,
  identifier, value, and timestamp.
- **Outbound Request Payload**: The transformed data sent to the local service
  for each MIDI event.
- **Bridge Session**: Runtime state containing selected input source,
  destination endpoint, and delivery outcomes.

## Assumptions

- The user has at least one MIDI input source available during demo execution.
- The local service endpoint is reachable on the same machine or local network.
- Outbound requests do not require user-specific authentication for demo use.

## Dependencies

- Access to a local service capable of accepting requests from the bridge.
- A repeatable MIDI signal source for smoke-check validation.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 95% of supported incoming MIDI messages trigger a corresponding
  outbound request during a 10-minute demo run.
- **SC-002**: In a test of 50 representative supported MIDI messages, 100%
  produce outbound payloads with all required fields.
- **SC-003**: After a temporary local service outage, processing resumes and the
  next 20 incoming MIDI messages are delivered without restart.
- **SC-004**: A new demo operator can complete setup and send the first
  successful MIDI-triggered request within 10 minutes using quickstart guidance.
