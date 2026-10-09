# 23. Upgrade and migration strategy

Treat component alignment and rollback as first-class deliverables.

The 2.1.24 download notice recommends aligned Workspace, Excel and Spreadsheet Services builds. Other upgrade boundaries have special requirements: the 2.0.9.21 data-tier installer transition and the Workspace backup / restore boundary are examples. Consult release notes, fix lists, conformance and deprecation notices together.  [R17] [R27] [R19] [R31] [R24] [R49]

## Recommended upgrade procedure

1. Inventory the source offering, database generation, all component builds, custom integrations and unsupported dependencies.

2. Select the target and generate its supported-configuration report; read every intervening required migration step.

3. Create and test the recovery set; preserve installation kits, certificate material and a rollback decision point.

4. Clone or migrate a representative workload into an isolated test environment.

5. Run calculation, security, integration, workflow, Excel, websheet, API and performance regression tests.

6. Rehearse production cutover, including user communication, source-load freeze, credentials and rescheduling.

7. After cutover, reconcile results and obtain business sign-off before retiring the previous environment.

## TM1 12 is a distinct migration concern

Front-end version renumbering does not itself prove that the database generation changed. Review TM1 12 documentation, migration tooling and API / integration compatibility separately. The Local 3.1.11 technical preview is explicitly unsupported for official product support and requires its specified database and Workspace pair.  [R74] [R75] [R18]

| PREVIEW IS NOT PRODUCTION AUTHORIZATION / Evaluate technical-preview capabilities in an isolated environment with nonproduction data. A newer version number, downloadable kit or successful demo does not replace a production support statement and validated architecture. |
| --- |

Check lifecycle terms and extensions directly before planning an upgrade deadline; older lifecycle pages may not reflect a customer's current support position.  [R20]

---
Source: user-supplied comprehensive guide, section 23. Citation IDs R01-R90 resolve in ../reference-catalog.md and ../references.json. This is source-derived material, not a new IBM support certification.
