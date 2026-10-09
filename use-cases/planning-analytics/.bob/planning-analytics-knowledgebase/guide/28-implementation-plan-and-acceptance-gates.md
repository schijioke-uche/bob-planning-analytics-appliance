# 28. Implementation plan and acceptance gates

Suggested delivery framework - not a vendor-mandated schedule.

| Phase | Core deliverables | Exit gate |
| --- | --- | --- |
| Discover | Business process, data inventory, stakeholders, offering and initial risk register. | Sponsor approves scope and measurable outcomes. |
| Design | Model grain, integration contracts, security matrix, version bill of materials and capacity assumptions. | Architecture and control owners approve the design. |
| Build | Environment, model, TI, reports, planning workflow and monitoring. | Repeatable development deployment and reconciliation. |
| Validate | Security, calculation, concurrency, integration, restore and user-acceptance evidence. | Business and operations accept the critical tests. |
| Deploy | Cutover rehearsal, communication, backups, rollback and production access. | Named go / no-go authority approves release. |
| Operate | Runbooks, ownership, training, incident process and improvement backlog. | Service ownership formally handed over. |

## Minimum recommended acceptance tests

Reconcile imported totals to source; verify parent / ratio calculations; reject invalid input; test authorized and unauthorized slices; rerun a failed load safely; complete a contributor-to-approver workflow; refresh and write back from the supported Excel client; validate representative APIs; restore the recovery set; test post-maintenance startup; measure peak-user behavior.

## Suggested learning sequence

Business users: start with Workspace navigation, input, scenarios and plan tasks. Modelers: learn dimensions, cubes, rules, TI and security before advanced automation. Administrators: learn the offering, deployment, monitoring, backup and support process. Integrators: study authentication and API contracts before implementing write operations.

IBM provides guided demonstrations, case studies and product resources. Pair these with the manuals and an isolated training model rather than treating a demonstration as production certification.  [R87] [R80]

| SUCCESS CRITERION / The implementation is complete when the business can run an approved planning cycle and operations can support and recover it. Installation alone does not meet that criterion. |
| --- |

---
Source: user-supplied comprehensive guide, section 28. Citation IDs R01-R90 resolve in ../reference-catalog.md and ../references.json. This is source-derived material, not a new IBM support certification.
