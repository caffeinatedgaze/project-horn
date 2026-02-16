# Implementation Plan: Zigbee Demo Infrastructure

**Branch**: `001-zigbee-demo-infra` | **Date**: 2026-02-10 | **Spec**: /Users/caffeinatedgaze/workspace/horn/zigbee-infra/specs/001-zigbee-demo-infra/spec.md
**Input**: Feature specification from `/specs/001-zigbee-demo-infra/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Provide a macOS-friendly, containerized Zigbee demo stack that pairs 3-10 bulbs,
controls them individually or by group, and exposes simple status recovery. The
technical approach keeps the Zigbee dongle on the host (or small host), exposes
it via ser2net as a serial-over-TCP endpoint, and runs Zigbee2MQTT in Docker
pointed at that TCP serial endpoint. Mosquitto runs in Docker as the local MQTT
broker. A lightweight control API offers a simple HTTP interface for demos and
smoke checks.

## Technical Context

**Language/Version**: Node.js 20 LTS (for the optional local control API)
**Primary Dependencies**: Docker, Docker Compose, Zigbee2MQTT, Mosquitto MQTT, ser2net
**Storage**: Local Docker volumes for Zigbee2MQTT state and device registry
**Testing**: Shell-based smoke check script
**Target Platform**: macOS laptop with Docker Desktop and USB Zigbee coordinator
**Project Type**: single (infra + scripts + docs)
**Performance Goals**: device control actions reflect within 5 seconds for 95%
**Constraints**: offline-capable, one-command setup, 3-10 bulbs, local-only
**Scale/Scope**: 3-10 devices, single demo operator, single laptop

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Demo-First Simplicity: only Zigbee2MQTT, Mosquitto, ser2net, and a thin
      control API are included; the API is justified for demo clarity and testing
- [x] One-Command Reproducibility: plan includes a single setup command and
      expected setup time in quickstart
- [x] Clear Component Contracts: contracts defined in
      `/Users/caffeinatedgaze/workspace/horn/zigbee-infra/specs/001-zigbee-demo-infra/contracts/openapi.yaml`
- [x] Safe Demo Data & Secrets: `.env.example` required and data reset steps
      documented in quickstart
- [x] Fast Feedback Smoke Check: smoke check command defined in quickstart

## Project Structure

### Documentation (this feature)

```text
specs/001-zigbee-demo-infra/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
# Single project (infra + docs + scripts)
infra/
├── docker-compose.yml
├── mosquitto/
│   ├── mosquitto.conf
│   └── data/
├── zigbee2mqtt/
│   ├── configuration.yaml
│   └── data/
└── control-api/
    └── (minimal local API service)

scripts/
├── smoke-check.sh
└── reset-demo.sh

docs/
└── components.md
```

**Structure Decision**: Use a single infra folder with Docker Compose and minimal
supporting scripts to keep the demo simple and explainable.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
