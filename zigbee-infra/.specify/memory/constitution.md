<!--
Sync Impact Report
- Version change: N/A → 1.0.0
- Modified principles: N/A (initial adoption)
- Added sections: Core Principles, Additional Constraints, Development Workflow, Governance
- Removed sections: None
- Templates requiring updates:
  - ✅ updated: .specify/templates/plan-template.md
  - ✅ updated: .specify/templates/spec-template.md
  - ✅ updated: .specify/templates/tasks-template.md
- Follow-up TODOs: None
-->
# Zigbee Infra Demo Constitution

## Core Principles

### I. Demo-First Simplicity
Build the minimum infrastructure that proves the demo. Default to a single
project and the smallest number of services. Any added component MUST include a
written "why needed for the demo" justification in the implementation plan.
Rationale: simplicity keeps build time fast and the system easy to explain.

### II. One-Command Reproducibility
A clean machine MUST be able to bring the demo up using a single documented
command or script. The quickstart MUST state the expected setup time and any
prerequisites. Rationale: repeatable setup is required for reliable demos.

### III. Clear Component Contracts
Every component MUST document its purpose, inputs, outputs, and dependencies in a
single, discoverable location (e.g., `docs/components.md` or per-component
README). Provide at least one concrete example interaction (CLI or HTTP).
Rationale: explicit contracts make the system easy to understand and explain.

### IV. Safe Demo Data & Secrets
No production credentials or real user data may be used. Required secrets MUST be
represented via `.env.example` with safe dummy values. A data reset path MUST be
provided (script or documented steps). Rationale: demos must be safe and
repeatable.

### V. Fast Feedback Smoke Check
Provide a lightweight end-to-end smoke check (script or command) that validates
the demo path in minutes. Full test suites are optional unless a spec explicitly
requires them. Rationale: quick verification prevents demo breakage.

## Additional Constraints

- Prefer Docker Compose for multi-service demos; avoid Kubernetes unless a demo
  requirement explicitly needs it.
- Avoid nonessential infrastructure (queues, caches, service meshes) unless the
  demo requires them and the plan documents the need.
- Keep defaults and configuration minimal; expose only the knobs needed to
  support the demo.

## Development Workflow

- Every feature MUST have a spec, plan, and tasks list using the templates under
  `.specify/templates/`.
- The plan MUST include a Constitution Check section with explicit pass/fail for
  each principle.
- Any change that impacts setup steps, contracts, or demo flow MUST update
  `quickstart.md` (or equivalent) and the smoke check.
- Reviews MUST verify compliance with this constitution before approval.

## Governance

- This constitution supersedes all other guidelines in the repository.
- Amendments require a PR that updates this file and any dependent templates or
  guidance documents.
- Versioning follows semantic versioning: MAJOR for breaking governance changes
  or removed principles, MINOR for added principles or material expansions, PATCH
  for clarifications and non-semantic edits.
- Compliance review is mandatory in every plan and code review, with explicit
  evidence in the Constitution Check section.

**Version**: 1.0.0 | **Ratified**: 2026-02-10 | **Last Amended**: 2026-02-10
