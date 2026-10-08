# System-build workflow

Use this workflow for a new system or a change that creates multiple interacting components. Keep artifacts in the repository only when they will remain useful; otherwise maintain them in the working notes and summarize the durable decisions in code or existing documentation.

## 1. Frame the system

Create a concise engineering brief containing:

- desired user or business outcome;
- actors and external systems;
- in-scope and out-of-scope behavior;
- functional acceptance criteria;
- quality attributes that actually matter, with measurable targets when supplied;
- constraints imposed by the repository, platform, timeline, compatibility, or regulation;
- assumptions and unresolved decisions.

Do not invent scale, latency, availability, compliance, or budget targets. If the user has not supplied them, choose a design that is easy to evolve and label any capacity assumptions used for decisions.

## 2. Understand the existing system

Inspect before proposing:

- repository instructions and current working-tree changes;
- build, package, lint, type-check, test, and deployment definitions;
- runtime entry points and dependency direction;
- domain model and persistent data ownership;
- public and internal contracts;
- authentication, authorization, and trust boundaries;
- failure handling, observability, configuration, and secrets flow;
- representative tests and established conventions.

Summarize the relevant current state and the change surface. Do not perform broad repository archaeology without a decision it is meant to inform.

## 3. Design the change

Describe the design at the level required to prevent contradictory implementation:

- components and their responsibilities;
- data/control flow for the primary scenario and major failure scenario;
- contracts, schemas, and error semantics;
- ownership of state and invariants;
- dependency direction and replaceable external adapters;
- consistency, concurrency, idempotency, timeout, and retry policy where relevant;
- compatibility, rollout, migration, and rollback strategy;
- security boundary and abuse cases;
- verification and observability strategy.

Compare alternatives only when a real tradeoff exists. Record a lightweight architecture decision when the choice is costly to reverse, surprising, or constrains later work: context, decision, alternatives rejected, consequences, and revisit trigger.

## 4. Plan vertical increments

Each increment should produce an observable, testable improvement. Prefer this order when dependencies permit:

1. establish contracts and a thin executable path;
2. implement domain behavior and invariants;
3. integrate storage and external boundaries;
4. add failure handling and operational signals;
5. complete migration, compatibility, and rollout mechanisms;
6. harden and remove temporary scaffolding.

For each increment, identify touched areas, evidence to collect, and rollback or containment if it fails. Avoid plans expressed only as a list of files.

## 5. Implement and continuously verify

Before editing, run or identify the relevant baseline checks. During implementation:

- keep commits or logical edit groups coherent;
- validate at the closest layer first;
- test contracts rather than implementation wording;
- keep test doubles at external boundaries, not around the behavior being proved;
- exercise the real integration boundary when correctness depends on serialization, queries, framework wiring, permissions, or network behavior;
- investigate unexpected failures instead of weakening assertions.

Revisit the design if implementation reveals a false assumption. Do not preserve a plan merely because it was written first.

## 6. Review and hand off

Review the complete diff as a system change. Trace every acceptance criterion to code and evidence. Inspect negative paths, cleanup behavior, logging safety, configuration defaults, and downstream callers.

The handoff should state:

- resulting behavior and architecture-relevant decisions;
- key files or modules changed;
- acceptance criteria and corresponding evidence;
- commands executed and their outcomes;
- deployment, migration, monitoring, and rollback notes when applicable;
- known limitations, residual risks, and checks not run.

Keep the report concise enough to audit. Raw command volume is not evidence unless its result is interpreted.
