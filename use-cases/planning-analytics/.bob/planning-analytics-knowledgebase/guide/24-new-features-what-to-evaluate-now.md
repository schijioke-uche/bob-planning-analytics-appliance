# 24. New features: what to evaluate now

Keep release, offering and feature availability together.

| Feature area | Reviewed change | Qualification / action |
| --- | --- | --- |
| Release alignment | Local 2.1.24 is the September 2026 refresh. | Use its recommended companion components and fix list. |
| Forecasting | Extended engine provides additional model choices. | Verify the deployed release and evaluate forecast quality on held-out data. |
| SaaS data sources | 3.1.11 adds Redshift, Box, Dremio, Dropbox, FTP, Google Cloud Storage, Netezza and Azure Fabric Warehouse connections. | The notice scopes this list to SaaS and Advanced Certified Containers. |
| AI provider | 3.1.11 adds an Amazon Bedrock provider option alongside watsonx.ai. | Feature-flag, credentials and model configuration apply; do not assume entitlement. |
| Database APIs | Workspace REST database-management capabilities expand. | Create, delete and backup-management operations cited in the notice are TM1 12-specific. |
| Plans and reporting | 3.1.11 updates task action logs, approval navigation and exploration reports. | Regression-test existing planning workflows and book interactions. |
| Agent / API integration | 3.1.9 includes agent, modeling, notification and API changes. | Review integrations and endpoint changes rather than only the visual UI. |

Release sources: Local download notice, SaaS 3.1.11 / 3.1.9 announcements and IBM's forecasting introduction.  [R17] [R69] [R70] [R71]

## How to evaluate a feature

Record the business problem, target release and offering, feature flag / entitlement, data exposed, permissions, test method, expected result and rollback. Test with ordinary users. Update training and runbooks only after validating the actual deployed behavior.

| HISTORICAL NEW-FEATURE MANUAL / The requested 2.0 New Features manual remains in the reference catalog. For current deployment decisions, pair it with the 2.1 Workspace, 3.1 Excel and TM1 12 release sources. |
| --- |

See the component new-feature indexes.  [R05] [R76] [R77] [R75]

---
Source: user-supplied comprehensive guide, section 24. Citation IDs R01-R90 resolve in ../reference-catalog.md and ../references.json. This is source-derived material, not a new IBM support certification.
