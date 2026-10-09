# 6. Planning Analytics on Cloud: first access

Hosted deployment means onboarding and configuration, not server installation.

The dedicated on Cloud offering is IBM-hosted. IBM onboarding guidance covers IBMid access, the welcome kit, support entitlement, user invitations, Excel tooling and notifications. Parts of older checklists describe retired Rich Tier or gateway arrangements; use the current Cloud 101 notices to identify the replacement workflow.  [R03] [R51] [R14]

| Stage | Action | Evidence of completion |
| --- | --- | --- |
| Identity and subscription | Identify the subscription owner; accept the invitation using the correct IBMid; associate the support entitlement. | Named owner, environment URL and working support access. |
| Environment handover | Retrieve the welcome / environment information using the available administration experience; inventory development and production. | Recorded URLs, administrators and approved environment purpose. |
| Initial administration | Open Workspace, review users / groups and establish a second authorized administrator. | A second administrator can sign in independently. |
| Business users | Invite the pilot cohort, assign subscription roles, content access and database permissions. | A non-admin user sees only the intended data and books. |
| First usable model | Build or migrate a small validated database, load actuals and publish a pilot book. | Totals reconcile; authorized input and refresh work. |
| Client and service readiness | Install a compatible Excel add-in; subscribe to maintenance and status notices. | Excel connects and operational contacts receive notifications. |

## Recommended onboarding control

Keep an environment register containing the exact offering, tenant / environment identifiers, owner, URLs, identity domain, model inventory, connector responsibility and support escalation contacts. Store credentials in approved secret management, not in the register.

| ACCEPTANCE TEST / Use an ordinary contributor account to open a book, read an approved slice, enter a test value, refresh it from Excel and confirm that an unauthorized slice remains inaccessible. Administrator-only testing is insufficient. |
| --- |

---
Source: user-supplied comprehensive guide, section 6. Citation IDs R01-R90 resolve in ../reference-catalog.md and ../references.json. This is source-derived material, not a new IBM support certification.
