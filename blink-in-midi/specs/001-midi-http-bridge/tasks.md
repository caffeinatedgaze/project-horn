---

description: "Task list for implementing MIDI to Local API Bridge"

---

# Tasks: MIDI to Local API Bridge

**Input**: Design documents from `/specs/001-midi-http-bridge/`  
**Prerequisites**: `plan.md` (required), `spec.md` (required), `research.md`, `data-model.md`, `contracts/openapi.yaml`, `quickstart.md`

**Tests**: Include unit and integration tests to satisfy the documented fast-verification and deterministic-mapping goals.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Every task includes an exact file path

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize Python/uv project and baseline structure for the demo.

- [X] T001 Initialize project metadata and dependencies in `pyproject.toml`
- [X] T002 Create package layout and module entrypoints in `src/blink_midi/__init__.py` and `src/blink_midi/cli.py`
- [X] T003 [P] Create environment template and defaults in `.env.example`
- [X] T004 [P] Add Python/macOS ignore patterns in `.gitignore`
- [X] T005 [P] Create pytest configuration in `tests/conftest.py`
- [X] T006 Create one-command smoke runner in `scripts/smoke_check.sh`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Build shared core pieces required by all user stories.

**⚠️ CRITICAL**: No user story work begins until this phase is complete.

- [X] T007 Implement runtime configuration model in `src/blink_midi/config.py`
- [X] T008 Implement core domain models (`MidiInputEvent`, `OutboundRequestIntent`, `BridgeSession`) in `src/blink_midi/models.py`
- [X] T009 [P] Implement payload mapping contract helpers in `src/blink_midi/mapper.py`
- [X] T010 [P] Implement local API request-intent builder with commented send TODO in `src/blink_midi/sender.py`
- [X] T011 Implement MIDI input adapter and supported-message filter in `src/blink_midi/midi_listener.py`
- [X] T012 Wire top-level app command flow in `src/blink_midi/cli.py`

**Checkpoint**: Foundation complete; user stories can be implemented and validated independently.

---

## Phase 3: User Story 1 - Trigger API from MIDI Input (Priority: P1) 🎯 MVP

**Goal**: Receive supported MIDI input events and produce one outbound request intent per event.

**Independent Test**: Run bridge with a selected device, emit one supported event, and verify one intent log line with mapped payload.

### Tests for User Story 1

- [X] T013 [P] [US1] Add mapper unit tests for note/control conversion in `tests/unit/test_mapper.py`
- [X] T014 [P] [US1] Add sender unit tests for request-intent object creation in `tests/unit/test_sender.py`
- [X] T015 [US1] Add integration test for event-to-intent flow in `tests/integration/test_midi_to_intent.py`

### Implementation for User Story 1

- [X] T016 [P] [US1] Implement deterministic note/control mapping logic in `src/blink_midi/mapper.py`
- [X] T017 [US1] Implement one-event-to-one-intent dispatch flow in `src/blink_midi/cli.py`
- [X] T018 [US1] Implement structured intent logging for successful mapped events in `src/blink_midi/sender.py`
- [X] T019 [US1] Update usage examples for run command and device selection in `specs/001-midi-http-bridge/quickstart.md`

**Checkpoint**: US1 delivers a runnable MVP path from MIDI event to logged outbound intent.

---

## Phase 4: User Story 2 - Preserve Message Meaning in Outbound Data (Priority: P2)

**Goal**: Guarantee stable payload schema and consistent value handling for repeated/representative messages.

**Independent Test**: Replay representative note/control messages and verify payload fields remain stable and complete.

### Tests for User Story 2

- [X] T020 [P] [US2] Add schema validation tests for required payload fields in `tests/unit/test_models.py`
- [X] T021 [P] [US2] Add repeatability tests for identical input stability in `tests/unit/test_mapper.py`
- [X] T022 [US2] Add contract conformance tests against OpenAPI payload schema in `tests/contract/test_midi_events_contract.py`

### Implementation for User Story 2

- [X] T023 [P] [US2] Enforce payload field/value validation rules in `src/blink_midi/models.py`
- [X] T024 [US2] Enforce deterministic transform path for all supported event types in `src/blink_midi/mapper.py`
- [X] T025 [US2] Align request-intent payload serialization to contract schema in `src/blink_midi/sender.py`
- [X] T026 [US2] Document payload contract examples in `specs/001-midi-http-bridge/contracts/openapi.yaml`

**Checkpoint**: US1 and US2 together provide stable and contract-aligned payload behavior.

---

## Phase 5: User Story 3 - Continue Operating Through Local Service Failures (Priority: P3)

**Goal**: Keep processing MIDI messages even when local API interaction fails.

**Independent Test**: Simulate local API failure and verify processing continues, failures are logged, and subsequent messages still produce intents.

### Tests for User Story 3

- [X] T027 [P] [US3] Add failure-path tests for sender exception and non-success handling in `tests/unit/test_sender.py`
- [X] T028 [US3] Add integration test for continue-on-failure behavior in `tests/integration/test_midi_failure_recovery.py`

### Implementation for User Story 3

- [X] T029 [US3] Implement failure logging with event correlation details in `src/blink_midi/sender.py`
- [X] T030 [US3] Implement continue-processing behavior after outbound failures in `src/blink_midi/cli.py`
- [X] T031 [US3] Track and expose failure counters in runtime session state in `src/blink_midi/models.py`

**Checkpoint**: All user stories are independently testable and resilient to local API failure.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, documentation sync, and release-readiness for demo use.

- [X] T032 [P] Validate one-command run path and smoke sequence in `scripts/smoke_check.sh`
- [X] T033 [P] Finalize quickstart prerequisites, setup time, and reset path in `specs/001-midi-http-bridge/quickstart.md`
- [X] T034 Run complete test suite and record results in `specs/001-midi-http-bridge/research.md`
- [X] T035 Perform code cleanup and consistency pass across `src/blink_midi/*.py`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; starts immediately.
- **Foundational (Phase 2)**: Depends on Phase 1 completion; blocks all user stories.
- **User Stories (Phases 3-5)**: Depend on Phase 2 completion.
- **Polish (Phase 6)**: Depends on all targeted user stories being complete.

### User Story Dependencies

- **US1 (P1)**: Starts after Foundational; no dependency on other stories.
- **US2 (P2)**: Starts after Foundational; builds on mapping and schema used by US1.
- **US3 (P3)**: Starts after Foundational; validates resilience over existing flow.

### Within Each User Story

- Tests before implementation tasks.
- Mapping/model logic before CLI wiring.
- Sender behavior before cross-story documentation updates.

## Parallel Opportunities

- Phase 1: T003, T004, T005 can run in parallel after T001/T002.
- Phase 2: T009 and T010 can run in parallel after T007/T008.
- US1: T013 and T014 can run in parallel; T016 can run while T015 is being prepared.
- US2: T020 and T021 can run in parallel; T023 and T026 can run in parallel.
- US3: T027 can run in parallel with setup for T028; T029 and T031 can run in parallel.
- Phase 6: T032 and T033 can run in parallel.

---

## Parallel Example: User Story 1

```bash
# Parallel test work:
Task: "T013 [US1] Add mapper unit tests in tests/unit/test_mapper.py"
Task: "T014 [US1] Add sender unit tests in tests/unit/test_sender.py"

# Parallel implementation work after core wiring:
Task: "T016 [US1] Implement deterministic mapping in src/blink_midi/mapper.py"
Task: "T018 [US1] Implement intent logging in src/blink_midi/sender.py"
```

## Parallel Example: User Story 2

```bash
# Parallel validation tasks:
Task: "T020 [US2] Add schema validation tests in tests/unit/test_models.py"
Task: "T021 [US2] Add repeatability tests in tests/unit/test_mapper.py"

# Parallel implementation/documentation tasks:
Task: "T023 [US2] Enforce payload validation in src/blink_midi/models.py"
Task: "T026 [US2] Document payload examples in specs/001-midi-http-bridge/contracts/openapi.yaml"
```

## Parallel Example: User Story 3

```bash
# Parallel robustness tasks:
Task: "T027 [US3] Add sender failure tests in tests/unit/test_sender.py"
Task: "T029 [US3] Implement failure logging in src/blink_midi/sender.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phases 1 and 2.
2. Deliver Phase 3 (US1).
3. Validate independent test criteria for US1.
4. Demo MVP before expanding scope.

### Incremental Delivery

1. Deliver US1 (event to intent).
2. Add US2 (payload correctness and contract stability).
3. Add US3 (failure resilience and continuity).
4. Execute polish tasks and final smoke validation.

### Suggested MVP Scope

- Include Phases 1, 2, and 3 only for first cut.
- Defer US2 and US3 if rapid demo timeline is required.

## Notes

- All tasks use explicit file paths and executable descriptions.
- `[P]` marks only tasks that can run without same-file conflicts.
- Keep sender network call commented in this phase per current feature decision.
