# Production readiness

Apply only the sections relevant to the system's actual operational profile. This is a decision guide, not a checkbox mandate.

## Reliability and failure behavior

- Define dependencies, their failure modes, timeouts, cancellation behavior, and degraded service behavior.
- Bound queues, concurrency, retries, payloads, and resource consumption.
- Prevent retry amplification. Use idempotency where an operation may be repeated.
- Define recovery for partial writes, orphaned work, poison messages, and process restarts.
- Make health checks describe the right thing: liveness for process recovery, readiness for traffic eligibility.

## Data lifecycle

- Identify the source of truth, invariants, retention, deletion, backup, and restore expectations.
- Make migrations compatible with the rollout order. Avoid assuming all application instances change simultaneously.
- Validate migrations with representative volume and problematic historical shapes.
- Provide reconciliation or repair paths for operations spanning consistency boundaries.

## Security and privacy

- Identify trust boundaries, assets, actors, abuse cases, and least-privilege requirements.
- Validate and normalize untrusted input; encode output for its destination.
- Keep secrets out of source, logs, errors, metrics, and client bundles.
- Enforce object- and tenant-level authorization at every protected access path.
- Audit sensitive state transitions with useful attribution while minimizing retained personal data.
- Review new dependencies, exposed ports, file permissions, and network destinations.

## Observability

- Instrument user-visible and correctness-critical outcomes, not merely implementation activity.
- Use stable structured fields and correlation identifiers across boundaries.
- Define actionable error categories and avoid alerting on unactionable noise.
- For important background processing, expose lag, failure, retry, dead-letter, and age signals.
- Redact or omit credentials, tokens, personal data, and payloads that do not belong in telemetry.

## Capacity and performance

- Optimize against an explicit workload or measured bottleneck.
- Check algorithmic growth, query count and indexes, fan-out, payload size, memory bounds, and connection pools.
- Test representative concurrency and data volume when performance is an acceptance criterion.
- Record the test conditions with the result; a latency number without workload context is not evidence.

## Release and rollback

- State rollout order, compatibility window, feature-control mechanism, and success/failure signals.
- Prefer reversible configuration or behavior rollout. For irreversible data changes, provide a forward-fix and recovery strategy.
- Make startup and configuration validation fail clearly before serving traffic.
- Confirm artifacts are reproducible enough for the project's release model and contain the intended versions.
- Document operator actions only when the repository has an operational documentation home.

## Readiness outcome

Summarize applicable risks as one of:

- **Demonstrated:** verified by a named check or exercise.
- **Designed:** addressed structurally but not exercised in the available environment.
- **Open:** unresolved and requiring a named action or decision.

Do not label a system “production ready” while material items remain merely assumed.
