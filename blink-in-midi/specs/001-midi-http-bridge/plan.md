# Implementation Plan: MIDI to Local API Bridge

**Branch**: `001-midi-http-bridge` | **Date**: 2026-02-11 | **Spec**: `/Users/caffeinatedgaze/workspace/horn/blink-in-midi/specs/001-midi-http-bridge/spec.md`
**Input**: Feature specification from `/specs/001-midi-http-bridge/spec.md`

**Note**: This template is filled in by the planning command/workflow used in this repository.

## Summary

Build a macOS-only Python service that listens to a selected MIDI input source,
transforms supported MIDI events into a stable payload, and triggers outbound
request intent handling for a local API endpoint. For this iteration, the
network send path is present but intentionally commented out; runtime behavior is
logging outbound request intent and continuing processing.

## Technical Context

**Language/Version**: Python 3.11  
**Primary Dependencies**: `mido`, `python-rtmidi`, `httpx`, `pydantic`, `typer`  
**Storage**: N/A  
**Testing**: `pytest`  
**Target Platform**: macOS (Apple Silicon and Intel)  
**Project Type**: single  
**Performance Goals**: Process and map 95% of supported MIDI events during a 10-minute demo run  
**Constraints**: Single process, single project, one active MIDI input source, HTTP send call intentionally commented out in sender, no queue/retry subsystem  
**Scale/Scope**: One demo operator, one local API endpoint, event-level request intent handling

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Simplicity First (NON-NEGOTIABLE): single-process design with minimal
      dependencies; each dependency is demo-critical and justified
- [x] One-Command Demo: setup and run documented with one command path via `uv`
      and quickstart prerequisites
- [x] Minimal Moving Parts: no extra services, queues, workers, or background
      infrastructure
- [x] Safe Demo State: `.env.example` required and reset instructions defined in
      quickstart
- [x] Fast Verification: smoke-check command defined for core MIDI-to-intent
      flow

## Project Structure

### Documentation (this feature)

```text
specs/001-midi-http-bridge/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── openapi.yaml
└── tasks.md
```

### Source Code (repository root)

```text
src/
├── blink_midi/
│   ├── cli.py
│   ├── config.py
│   ├── midi_listener.py
│   ├── mapper.py
│   ├── sender.py
│   └── models.py

scripts/
└── smoke_check.sh

tests/
├── unit/
│   ├── test_mapper.py
│   └── test_models.py
└── integration/
    └── test_midi_to_intent.py
```

**Structure Decision**: Single project is selected to satisfy simplicity and
minimal moving parts. No frontend/backend split is required for this feature.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |

## Post-Design Constitution Check

- [x] Simplicity First (NON-NEGOTIABLE): design remains single-process and uses
      only demo-critical dependencies.
- [x] One-Command Demo: `quickstart.md` documents a single setup/run path.
- [x] Minimal Moving Parts: no extra services, workers, or queueing added.
- [x] Safe Demo State: quickstart includes local endpoint-only safety guidance
      and reset path.
- [x] Fast Verification: smoke-check flow is documented in `quickstart.md`.
