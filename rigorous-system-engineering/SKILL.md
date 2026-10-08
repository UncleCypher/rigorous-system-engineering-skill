---
name: rigorous-system-engineering
description: Structure the design, implementation, verification, and delivery of production-quality software systems. Use when Codex is asked to create a system, add a substantial subsystem, perform architecture-sensitive work, or turn a prototype into maintainable engineering. Do not invoke for tiny isolated edits unless they affect critical data, security, concurrency, compatibility, or operations.
---

# Rigorous System Engineering

Build systems whose behavior, boundaries, and evidence are understandable after the implementation session ends. Scale the ceremony to the risk; rigor means closing the important loops, not producing maximum documentation.

## Operating contract

- Preserve the user's stated objective, technology choices, constraints, and authorization boundaries.
- Inspect the repository, its instructions, build system, tests, and current changes before choosing an architecture. Treat existing conventions as evidence, not automatically as ideal design.
- Separate facts observed in the repository from assumptions and proposals. Resolve an uncertainty before implementation when different answers would materially change public interfaces, data models, security boundaries, irreversible operations, or cost.
- Prefer the smallest coherent design that satisfies the acceptance criteria. Avoid speculative frameworks, generic abstractions, and unrelated cleanup.
- Keep requirements traceable through implementation and verification. Do not claim completion without observable evidence.
- Preserve user changes. Do not hide failures, silently weaken tests, or substitute mocks for required integration evidence.

## Choose the operating mode

Classify the work before editing:

- **Focused change:** a bounded change with no new architectural boundary. Use the compact workflow below.
- **System build:** a new application, service, subsystem, or substantial cross-cutting feature. Read [references/system-workflow.md](references/system-workflow.md).
- **Production hardening:** reliability, security, performance, migration, deployment, or operational-readiness work. Read both [references/system-workflow.md](references/system-workflow.md) and [references/production-readiness.md](references/production-readiness.md).

Use [references/risk-and-verification.md](references/risk-and-verification.md) whenever the change touches persistent data, authentication or authorization, secrets, money, untrusted input, concurrency, background work, external services, public compatibility, deployment, or destructive actions.

## Compact workflow

1. **Establish the contract.** State the intended outcome, relevant constraints, non-goals, acceptance criteria, and material unknowns. Infer low-impact details from repository evidence; ask only when a missing choice changes the product or risk materially.
2. **Map the impact.** Locate entry points, state owners, interfaces, dependencies, tests, and operational surfaces. Identify invariants that must remain true.
3. **Design before diffusion.** Choose module boundaries, contracts, data flow, failure behavior, and migration or compatibility strategy before spreading edits across the repository. Record a decision only when future maintainers need the rationale.
4. **Implement vertical slices.** Make the smallest end-to-end increment that can be validated. Keep domain logic separate from transport, storage, and framework glue when that separation makes behavior independently testable.
5. **Verify by risk.** Run the narrowest useful checks early, then broader checks. Cover success, boundary, and important failure paths. Follow [references/risk-and-verification.md](references/risk-and-verification.md) for elevated-risk work.
6. **Audit the result.** Review the actual diff and runtime behavior against acceptance criteria. Check for incomplete call sites, compatibility breaks, unsafe defaults, accidental scope growth, dead code, and misleading documentation.
7. **Deliver evidence.** Report what changed, where, which acceptance criteria were demonstrated, exact checks and outcomes, and any residual risk or unverified behavior. Distinguish passed, failed, and not run.

## Engineering invariants

Apply these when relevant rather than mechanically:

- One authoritative owner for each piece of mutable state.
- Explicit contracts at boundaries: inputs, outputs, errors, timeouts, cancellation, and compatibility.
- Validate untrusted input at the boundary; enforce authorization at the protected operation, not only in the UI.
- Make retryable effects idempotent or explicitly non-retryable. Bound retries and include backoff where appropriate.
- Preserve transactional invariants across partial failure. For multi-system operations, define reconciliation rather than pretending they are atomic.
- Use versioned, reversible, or forward-compatible migrations. Separate schema rollout from behavior rollout when zero-downtime compatibility matters.
- Make critical behavior observable through actionable logs, metrics, traces, or audit records without exposing secrets or sensitive data.
- Keep configuration validated, explicit, and environment-independent. Fail early on unsafe missing configuration.
- Treat dependency, generated-code, and lockfile changes as part of the reviewed system.

## Completion gate

Do not call the work complete until all applicable statements are true:

- The implemented behavior maps to explicit acceptance criteria.
- Changed code compiles, type-checks, or passes the ecosystem's equivalent static validation.
- Relevant automated tests pass, including material failure paths and regression coverage.
- Required integration behavior was exercised against a real boundary or clearly reported as unverified.
- Data and API compatibility, security, concurrency, and rollback concerns were addressed where applicable.
- The final diff contains no unintended files or unrelated changes.
- Operational instructions and maintained documentation match the resulting behavior.

If a gate cannot be satisfied, stop at the strongest truthful state: identify the missing evidence, its consequence, and the minimal next action. Never convert “not verified” into “works.”

## Deterministic repository inventory

For an unfamiliar repository, `scripts/repo_inventory.py <repository>` can produce a bounded JSON inventory of language indicators, manifests, CI, containers, migrations, tests, and likely entry documentation. Use it as a discovery aid, then inspect the relevant files directly; its output is not an architecture assessment.
