# 2. Versions, release lines and evidence

Research baseline: 8 October 2026. Recheck release notices before deployment.

| Line / component | What the reviewed IBM sources establish | Deployment implication |
| --- | --- | --- |
| 2.0 documentation | The supplied links remain useful for terminology, historical behavior and manual navigation. | Do not assume an old page describes the installer or support terms of a new build. |
| Local 2.1.24 | IBM published the download on 25 September 2026 and recommends Workspace, Excel and Spreadsheet Services 2.1.24 alongside it. | Use a release-aligned bill of materials and verify compatibility before installation. |
| Dedicated on Cloud | Workspace and Excel adopted 2.1 numbering beginning October 2025. | A cloud environment need not use the same numbering as multitenant SaaS. |
| SaaS 3.1 | AWS / Azure SaaS adopted 3.1 front-end numbering beginning October 2025; that renumbering did not itself change TM1 Database. | Track Workspace, Excel and database versions separately. |
| Local 3.1.11 preview | IBM labels it a technical preview without official product support; it requires TM1 12.6.4 and Workspace 3.1.11. | Evaluation only unless IBM subsequently publishes production support for the chosen release. |

Sources: original documentation, current Local download notices, and IBM product-management version announcements.  [R02] [R17] [R73] [R74] [R18]

## How to read this guide

Numbered citations such as [R17] point to the reference catalog. IBM product facts and version-specific instructions are cited. Deployment checklists, acceptance criteria and sample designs are practical recommendations, not additional IBM product guarantees. Commands marked illustrative require adaptation and testing.

| ACCESS AND SCOPE / Some IBM Docs, manual downloads and My Support pages restrict automated retrieval or require a browser / entitlement. These are labeled in the catalog; no unavailable contents have been inferred. This guide is a cross-functional reference, not a reproduction of every IBM manual or a compatibility certification. |
| --- |

---
Source: user-supplied comprehensive guide, section 2. Citation IDs R01-R90 resolve in ../reference-catalog.md and ../references.json. This is source-derived material, not a new IBM support certification.
