# Research: Zigbee Demo Infrastructure

## Decision 1: Containerized stack with Docker Compose
**Decision**: Use Docker Compose to orchestrate the demo services.
**Rationale**: Single-command startup aligns with demo reproducibility and
macOS portability requirements.
**Alternatives considered**: Native installs on macOS; Kubernetes.

## Decision 2: Remote adapter access via ser2net
**Decision**: Keep the Zigbee dongle on the host and expose it via ser2net as a
serial-over-TCP endpoint.
**Rationale**: Enables Zigbee2MQTT to run in Docker while still accessing local
USB hardware in a simple, documented way.
**Alternatives considered**: USB passthrough directly into container; running
Zigbee2MQTT on the host.

## Decision 3: Zigbee2MQTT in Docker
**Decision**: Run Zigbee2MQTT in Docker and connect it to the remote serial
endpoint.
**Rationale**: Keeps the demo stack containerized while using the standard
"remote adapter" approach.
**Alternatives considered**: Host installation; VM-only deployment.

## Decision 4: Mosquitto as MQTT broker in Docker
**Decision**: Use Mosquitto as the local MQTT broker in Docker.
**Rationale**: Lightweight, widely used, and simple to run in containers.
**Alternatives considered**: EMQX; HiveMQ Community Edition.

## Decision 5: Minimal control API for demo clarity
**Decision**: Provide a lightweight local control API that maps HTTP actions to
MQTT commands.
**Rationale**: Offers a simple, explainable interface for demos and smoke checks
without requiring MQTT tooling from the operator.
**Alternatives considered**: Direct MQTT CLI usage; Zigbee2MQTT web UI only.
