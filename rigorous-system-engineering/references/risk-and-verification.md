# Risk and verification

Choose verification based on plausible failure impact and reversibility. A small diff can be high risk; a large generated change can be low risk.

## Risk classification

Treat work as **elevated risk** if failure can cause data loss or corruption, unauthorized access, secret exposure, financial impact, incompatible public behavior, widespread outage, difficult rollback, or nondeterministic concurrency defects.

Treat work as **moderate risk** if it changes shared domain behavior, persistence queries, external integrations, background jobs, caching, configuration, build/release behavior, or multiple callers.

Treat work as **low risk** only when the impact is local, reversible, and covered by an existing reliable boundary.

Escalate one level when the repository has weak tests, unclear ownership, no reproducible environment, or a history of fragile behavior. Reduce ceremony only with positive evidence, not optimism.

## Verification matrix

Select all applicable rows:

| Change surface | Minimum useful evidence | Additional elevated-risk evidence |
| --- | --- | --- |
| Pure domain logic | Unit tests for success, boundary, and failure cases | Property/invariant tests or adversarial cases |
| Public API or event | Contract/schema tests and representative client path | Backward/forward compatibility and malformed-input tests |
| Database/schema | Query or repository integration test | Migration on representative data, rollback/forward-fix rehearsal, invariant checks |
| Authentication/authorization | Allowed and denied-path tests | Cross-tenant/object-level cases, privilege escalation review, audit evidence |
| External service | Adapter tests for response/error mapping | Sandbox integration, timeouts, retry budget, idempotency, degraded behavior |
| Concurrent/background work | Deterministic state-transition tests | Duplicate, reordering, cancellation, crash/restart, and race analysis |
| Cache | Hit/miss and invalidation tests | Stale data, stampede, partition, and source-of-truth recovery |
| UI workflow | Component/interaction test and build | Real user journey, accessibility, visual states, network/error behavior |
| Configuration/build | Clean build or config validation | Fresh-environment/release artifact smoke test |
| Deployment/operations | Health/readiness behavior | Staged rollout, monitoring threshold, rollback or forward-fix rehearsal |

## Verification sequence

1. Capture a baseline when existing behavior or pre-existing failures could be confused with the change.
2. Run focused static checks and tests during each vertical slice.
3. Run the repository's relevant broader suite after integration.
4. Exercise the executable path at the closest realistic boundary.
5. Review the final diff and generated artifacts.
6. For elevated-risk changes, deliberately test at least one partial-failure or recovery scenario.

Do not treat a passing unit test as proof of framework wiring, a mocked database as proof of a migration, a successful HTTP status as proof of the state transition, or compilation as proof of runtime behavior.

## Evidence ledger

Maintain a compact mapping during the work:

| Claim or acceptance criterion | Verification | Result | Residual limitation |
| --- | --- | --- | --- |
| Example: duplicate request creates one order | Integration test sends same idempotency key twice | Pass: one persisted order | Broker redelivery not exercised locally |

The ledger may live in working notes. Include it in the repository only if the project maintains such artifacts. In the final response, summarize it rather than claiming a confidence level without evidence.

## Stop conditions

Stop and seek direction before proceeding when:

- two plausible interpretations produce materially different product behavior;
- a destructive or externally mutating action lacks authorization;
- a migration or compatibility strategy cannot protect existing data or consumers;
- required credentials, infrastructure, or representative data are unavailable and no safe substitute can prove the behavior;
- continuing would require weakening a security or correctness invariant.

Otherwise, continue with bounded assumptions and disclose them.
