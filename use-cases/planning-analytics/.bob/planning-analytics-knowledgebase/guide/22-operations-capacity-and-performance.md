# 22. Operations, capacity and performance

Measure the business workload before tuning the platform.

Planning Analytics Administration provides a database operational view; the Local agent enables management capabilities such as activity inspection, logs and alerts. IBM Local and SaaS 101 hubs organize component-specific must-gathers and operational knowledge. Use these as the starting point for runbooks.  [R35] [R15] [R16]

| Signal | What it can indicate | Recommended next step |
| --- | --- | --- |
| Memory growth | Larger models, calculation / feeder effects, concurrent workload or content changes. | Compare against the baseline, release changes and representative model tests. |
| Long calculation or TI time | Source latency, inefficient process logic, contention or model design. | Separate source time from model time; inspect the relevant logs and workload. |
| Waiting users / threads | Contention or long-running activities. | Identify the owner and business impact before canceling a process. |
| Slow workbook / book | Large result set, report design, service dependency or client issue. | Reproduce with a small controlled view and compare web / Excel behavior. |
| Container / service exits | Host restart, runtime or service-level problem. | Inspect host and component health; do not repeatedly restart without evidence. |

## Recommended service runbook

Record the daily validation procedure, scheduled processing windows, capacity thresholds, incident contacts and approved interventions. For each intervention identify the operator, reason, affected business process and rollback. Tie monitoring to user outcomes such as data freshness and planning-cycle completion, not only CPU usage.

## Performance-test design

Use realistic concurrent contributors, representative rules, TI jobs and report refreshes. Record the data size, version matrix, response-time distribution, peak memory and errors. Compare like-for-like runs after tuning. Avoid promising capacity from a small sample model or a single-user demonstration.

| STOP-CONDITION DISCIPLINE / Do not repeatedly retry a heavy load or calculation while the system is contended. A bounded retry policy and a named operator are safer than an uncontrolled loop that amplifies an outage. |
| --- |

---
Source: user-supplied comprehensive guide, section 22. Citation IDs R01-R90 resolve in ../reference-catalog.md and ../references.json. This is source-derived material, not a new IBM support certification.
