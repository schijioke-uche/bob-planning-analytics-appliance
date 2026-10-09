# 1. Product scope and deployment choices

Start with the offering, not the installation media.

IBM Planning Analytics combines governed business planning with the multidimensional TM1 engine. Business users plan, analyze and write back through web and Excel experiences; modelers define the structures and logic behind those experiences. It is not simply a dashboard product or a shared workbook repository.  [R01] [R81]

| Offering | Operating model | What you deploy |
| --- | --- | --- |
| Planning Analytics on Cloud | Dedicated private hosted service managed by IBM. | Provision access, identities, models, integrations and client tools; do not install IBM-managed servers. |
| Planning Analytics as a Service | Multitenant SaaS; IBM describes AWS and Azure purchasing / deployment options. | Use the SaaS console and administration experience to establish environments, databases and access. |
| Planning Analytics Local | Customer-managed installation on supported infrastructure. | Install and operate the TM1 data tier, Workspace and selected client / web components. |
| Certified Containers / Software Hub | Separate containerized offering and platform-specific deployment path. | Use the matching service, entitlement and platform documentation; do not reuse a Windows installer runbook. |

IBM distinguishes dedicated on Cloud from as a Service; its pricing page also describes a Cloud Pak for Data deployment option. These are not interchangeable labels. Confirm the exact ordered SKU, region, identity model, database generation and operational responsibilities before design approval.  [R13] [R88]

## Recommended selection questions

Who must operate the infrastructure? Which source systems must be reached privately? Are there residency or enterprise-identity constraints? Is the goal an existing TM1 migration or a new SaaS model? Which Excel and AI capabilities are licensed? Establish these answers before choosing a topology or project estimate.

| INTERPRETATION RULE / A feature documented for SaaS, TM1 12 or a technical preview is not automatically available in Planning Analytics Local 2.1 or in every hosted subscription. |
| --- |

---
Source: user-supplied comprehensive guide, section 1. Citation IDs R01-R90 resolve in ../reference-catalog.md and ../references.json. This is source-derived material, not a new IBM support certification.
