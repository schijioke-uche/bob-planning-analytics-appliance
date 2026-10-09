# 13. Planning Analytics for Microsoft Excel

Install the right add-in, then validate a complete planning transaction.

Planning Analytics for Excel retains Excel as a user interface while connecting it to governed TM1 models. Current single-XLL installation instructions replace older multi-component installation assumptions. IBM documents a single .xll add-in for versions 2.0.65 and later and publishes separate conformance requirements.  [R83] [R33] [R32] [R31]

## Recommended deployment procedure

1. Inventory Office version / channel and bitness, PAfE build, Workspace endpoint and Spreadsheet Services version.

2. Download the add-in from the authorized administration experience or IBM distribution channel for the offering.

3. Close Excel, preserve an approved rollback copy and remove conflicting obsolete add-ins according to the applicable IBM instructions.

4. Place the correct .xll in an approved managed location. Apply enterprise signing and trust controls rather than globally weakening Excel security.

5. Load the add-in for a controlled session or register it in Excel Add-ins for repeated use, following the chosen deployment method.

6. Configure the environment connection and sign in with the intended business identity.

7. Open a representative report, refresh it, change an authorized input, submit / commit as appropriate, and reconcile the result with Workspace.

## Dependencies that are easy to miss

IBM documents that Universal Reports and TM1SET-related capabilities use the EvaluationService component of Spreadsheet Services. Distributed TM1 deployments need its proper configuration. Do not diagnose every Excel formula or rendering failure as a local Office issue; confirm the service and supported component combination.  [R89]

| Test | Pass criterion |
| --- | --- |
| Read and refresh | Expected totals match the same model slice in Workspace. |
| Write-back | Only authorized cells accept values; calculated cells behave as designed. |
| Reopen and reconnect | The workbook works after Excel restart without hidden local dependencies. |
| Shared use | Another entitled user can run it with that user's own permissions. |

| OPERATIONAL TIP / Treat the add-in as a managed enterprise client: version inventory, pilot ring, signed distribution, regression workbook and a documented rollback. |
| --- |

---
Source: user-supplied comprehensive guide, section 13. Citation IDs R01-R90 resolve in ../reference-catalog.md and ../references.json. This is source-derived material, not a new IBM support certification.
