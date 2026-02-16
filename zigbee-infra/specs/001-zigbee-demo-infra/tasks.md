---

description: "Task list template for feature implementation"
---

# Tasks: Zigbee Demo Infrastructure

**Input**: Design documents from `/specs/001-zigbee-demo-infra/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/, quickstart.md

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create infra structure per plan in infra/ and scripts/ directories
- [X] T002 [P] Add Docker Compose file in infra/docker-compose.yml
- [X] T003 [P] Add Mosquitto config in infra/mosquitto/mosquitto.conf
- [X] T004 [P] Add Zigbee2MQTT config in infra/zigbee2mqtt/configuration.yaml
- [X] T005 [P] Add control API scaffold in infra/control-api/README.md
- [X] T006 [P] Add smoke check script in scripts/smoke-check.sh
- [X] T007 [P] Add data reset script in scripts/reset-demo.sh
- [X] T008 [P] Add component contracts doc in docs/components.md
- [X] T009 [P] Add `.env.example` in .env.example

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T010 Configure Mosquitto service in infra/docker-compose.yml
- [X] T011 Configure Zigbee2MQTT service to connect via ser2net in infra/docker-compose.yml
- [X] T012 Configure Zigbee2MQTT runtime settings in infra/zigbee2mqtt/configuration.yaml
- [X] T013 Document ser2net endpoint config in docs/components.md
- [X] T014 Document demo setup and prerequisites in specs/001-zigbee-demo-infra/quickstart.md

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Pair and Register Bulbs (Priority: P1) 🎯 MVP

**Goal**: Pair 3-10 bulbs and register them so they appear in the device list

**Independent Test**: Start the stack, initiate pairing, and confirm the bulb appears as paired in the device list

### Implementation for User Story 1

- [X] T015 [P] [US1] Implement pairing start endpoint in infra/control-api/src/routes/pairing.ts
- [X] T016 [P] [US1] Implement pairing stop endpoint in infra/control-api/src/routes/pairing.ts
- [X] T017 [P] [US1] Add pairing session model in infra/control-api/src/models/pairing_session.ts
- [X] T018 [US1] Add MQTT publish for pairing start/stop in infra/control-api/src/services/mqtt_client.ts
- [X] T019 [US1] Implement device list endpoint in infra/control-api/src/routes/devices.ts
- [X] T020 [US1] Map Zigbee2MQTT device registry to API response in infra/control-api/src/services/device_registry.ts

**Checkpoint**: User Story 1 is fully functional and testable independently

---

## Phase 4: User Story 2 - Control Individual and Group Lighting (Priority: P2)

**Goal**: Toggle and dim individual bulbs and named groups

**Independent Test**: Send on/off and brightness commands to a device and group and verify responses

### Implementation for User Story 2

- [X] T021 [P] [US2] Add device state endpoint in infra/control-api/src/routes/devices.ts
- [X] T022 [P] [US2] Add group create/list endpoints in infra/control-api/src/routes/groups.ts
- [X] T023 [P] [US2] Add group state endpoint in infra/control-api/src/routes/groups.ts
- [X] T024 [P] [US2] Add group model in infra/control-api/src/models/group.ts
- [X] T025 [US2] Implement MQTT command mapping in infra/control-api/src/services/mqtt_client.ts
- [X] T026 [US2] Persist group definitions in infra/control-api/src/services/group_store.ts

**Checkpoint**: User Stories 1 AND 2 are independently functional

---

## Phase 5: User Story 3 - Monitor Status and Recover from Disconnects (Priority: P3)

**Goal**: Show device availability and recover status after disconnects

**Independent Test**: Power off a bulb, see it marked unavailable, power on, and confirm it returns

### Implementation for User Story 3

- [X] T027 [P] [US3] Add device refresh endpoint in infra/control-api/src/routes/devices.ts
- [X] T028 [P] [US3] Add status tracking to device model in infra/control-api/src/models/device.ts
- [X] T029 [US3] Implement availability polling or MQTT subscription handling in infra/control-api/src/services/device_status.ts
- [X] T030 [US3] Expose device status in device list response in infra/control-api/src/routes/devices.ts

**Checkpoint**: All user stories are independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T031 [P] Update quickstart smoke check instructions in specs/001-zigbee-demo-infra/quickstart.md
- [X] T032 [P] Add example API calls to docs/components.md
- [X] T033 [P] Validate docker compose startup and teardown steps in docs/components.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch pairing endpoints and model tasks together:
Task: "Implement pairing start endpoint in infra/control-api/src/routes/pairing.ts"
Task: "Implement pairing stop endpoint in infra/control-api/src/routes/pairing.ts"
Task: "Add pairing session model in infra/control-api/src/models/pairing_session.ts"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
