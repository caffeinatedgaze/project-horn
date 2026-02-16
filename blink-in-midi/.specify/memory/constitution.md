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
  - ⚠ pending: .specify/templates/commands/*.md (directory not present in repository)
- Follow-up TODOs:
  - TODO(RATIFICATION_DATE_SOURCE): No prior constitution history exists; ratified on initial adoption date.
-->
# Blink in MIDI Constitution

## Core Principles

### I. Simplicity First (NON-NEGOTIABLE)
Every implementation decision MUST prefer the smallest solution that can run the
demo end-to-end. Added components, abstractions, or dependencies are allowed
only when the plan includes a one-sentence demo-critical justification.
Rationale: this project is a demo, and complexity directly reduces reliability
and maintainability.

### II. One-Command Demo
A clean environment MUST be able to set up and run the demo using one documented
command or script. The quickstart MUST include prerequisites and expected setup
time.
Rationale: reproducibility is mandatory for credible demos.

### III. Minimal Moving Parts
The default architecture MUST stay single-process and single-project unless a
feature explicitly cannot work that way. Any split into multiple services,
queues, or background workers MUST be justified in the plan's Constitution
Check.
Rationale: fewer moving parts means fewer failure modes during demo execution.

### IV. Safe Demo State
The project MUST use dummy data and non-production credentials only.
`.env.example` MUST exist for required configuration, and a reset path MUST be
documented so the demo can return to a known-good state.
Rationale: safe, disposable state is required for repeatable demonstrations.

### V. Fast Verification
Every change to demo behavior MUST include a smoke check command that validates
the core demo flow in a few minutes. Full test suites are optional unless a spec
explicitly requires them.
Rationale: quick feedback keeps the demo stable without heavyweight process.

## Additional Constraints

- New dependencies MUST be limited to demo-critical needs and justified in the
  plan.
- Default source layout MUST be a single project (`src/` and `tests/`) unless
  the feature spec requires another layout.
- Runtime configuration MUST expose only values needed to run the demo.

## Development Workflow

- Every feature MUST include `spec.md`, `plan.md`, and `tasks.md` using
  `.specify/templates/`.
- `plan.md` MUST include a Constitution Check with explicit pass/fail for every
  principle.
- Any change that affects setup, demo flow, or configuration MUST update
  `quickstart.md` (or equivalent) in the same change.
- Reviews MUST reject changes that add unjustified complexity.

## Governance

- This constitution takes precedence over other project guidance.
- Amendments require a pull request that updates this file and any impacted
  templates or docs in the same change.
- Versioning policy uses semantic versioning:
  MAJOR for removed or redefined principles,
  MINOR for new principles or materially stronger requirements,
  PATCH for wording clarifications and non-semantic edits.
- Compliance review is required in planning and code review, with explicit
  evidence in the Constitution Check.

**Version**: 1.0.0 | **Ratified**: 2026-02-10 | **Last Amended**: 2026-02-10
