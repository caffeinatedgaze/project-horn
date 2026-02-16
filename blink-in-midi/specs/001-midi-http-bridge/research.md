# Research: MIDI to Local API Bridge

## Scope
Feature: `001-midi-http-bridge`  
Platform: macOS  
Runtime: Python 3.11 with `uv` and `pyproject.toml`

## Research Tasks Dispatched

- Research MIDI input handling for Python on macOS with minimal complexity.
- Research event modeling strategy for deterministic payload mapping.
- Research local HTTP client pattern that can be safely stubbed for demo.
- Research CLI ergonomics for one-command demo workflows.
- Research testing strategy for event-to-intent behavior.

## Decisions

### 1) MIDI library stack
- Decision: Use `mido` with `python-rtmidi` backend.
- Rationale: `mido` provides a concise event model and device enumeration,
  while `python-rtmidi` is the practical backend for live input on macOS.
- Alternatives considered:
  - `pygame.midi`: less direct for message abstraction.
  - CoreMIDI bindings directly: too complex for this demo-first scope.

### 2) Payload schema
- Decision: Use one stable payload schema for supported event types:
  `event_type`, `channel`, `key`, `value`, `timestamp`.
- Rationale: A unified schema simplifies downstream local API consumption and
  keeps tests deterministic.
- Alternatives considered:
  - Type-specific payloads per MIDI message: more branching and schema drift.
  - Raw byte-forwarding: weaker readability and harder acceptance testing.

### 3) Outbound request behavior for current iteration
- Decision: Build request metadata and payload, but leave actual HTTP send call
  commented out with a clear TODO marker.
- Rationale: Matches explicit user direction while preserving integration shape
  for future activation.
- Alternatives considered:
  - Fully active HTTP send now: conflicts with requested workflow.
  - Pure logging without request object creation: reduces forward compatibility.

### 4) Configuration approach
- Decision: Allow endpoint and runtime options via CLI flags with environment
  variable fallback (`API_URL`, `LOG_LEVEL`).
- Rationale: Supports one-command demo while remaining flexible.
- Alternatives considered:
  - Environment-only configuration: less discoverable for first-time usage.
  - Complex config file: unnecessary setup overhead.

### 5) Test approach
- Decision: Prioritize unit tests for mapping/model determinism and one
  integration test for event-to-intent logging behavior.
- Rationale: Fast verification aligns with constitution and keeps iteration
  lightweight.
- Alternatives considered:
  - Broad end-to-end suites: overkill for current scope.
  - No integration tests: weak confidence in runtime path.

## Dependency Justification

- `mido`: required for MIDI event intake and device-level message model.
- `python-rtmidi`: required backend for live MIDI on macOS.
- `httpx`: request object and future send path in Python.
- `pydantic`: payload validation and deterministic schema enforcement.
- `typer`: simple CLI surface for one-command demo.
- `pytest`: fast smoke-level and unit validation.

## Resolved Clarifications

All technical context fields are resolved; no remaining clarification markers are
required for planning.

## Validation Results

- 2026-02-11: `uv run ruff check .` -> All checks passed.
- 2026-02-11: `uv run pytest` -> 14 passed, 0 failed.
- 2026-02-11: `./scripts/smoke_check.sh` -> success (demo-once path verified).
