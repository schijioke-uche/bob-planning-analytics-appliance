# 16. Rules, feeders and model correctness

Performance tuning must preserve the meaning of the plan.

TM1 rules implement model calculations; feeders are relevant when sparse-consolidation optimization is used. IBM's FEEDERS documentation describes placing feeder statements after a FEEDERS section and identifying the rule-calculated cells needed for correct sparse consolidation. A faster view is not acceptable if its total is wrong.  [R41]

## Recommended design approach

| Concern | Implementation guidance | Test evidence |
| --- | --- | --- |
| Rule ownership | Assign a business definition, technical owner and intended cell scope. | Known examples reconcile to an independently calculated result. |
| Consolidations | Distinguish summable measures from ratios, rates and balances. | Parent totals remain correct after filter and hierarchy changes. |
| Feeders | Trace dependencies deliberately; avoid adding broad feeder patterns merely to hide missing totals. | Zero / nonzero transitions, sparse slices and cross-cube dependencies are tested. |
| Change control | Version rules with the related process and metadata changes. | Regression results accompany the promoted release. |
| Performance | Measure the effect of changes under representative concurrent load. | Calculation time, memory and load / restart behavior are recorded. |

## Illustrative validation set

Prepare a compact fixture with known input values, a zero-input case, a missing-input case, a newly introduced element, a consolidated view and a changed driver. Validate the result through both the user interface and an independent reconciliation. For cross-cube rules, test the source and target together.

## Avoid an anti-pattern

Do not fix a reporting mismatch only by changing the workbook. Determine whether it comes from source data, the mapping process, the model rule, the consolidation, the user's security slice or the report definition. A workbook-only workaround can conceal a shared-model defect.

| RELEASE DISCIPLINE / Promote a calculation change with its test fixture and reconciliation evidence. Keep a recoverable previous model version and document the business impact of rollback. |
| --- |

---
Source: user-supplied comprehensive guide, section 16. Citation IDs R01-R90 resolve in ../reference-catalog.md and ../references.json. This is source-derived material, not a new IBM support certification.
