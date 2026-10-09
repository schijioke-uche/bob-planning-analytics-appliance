# 18. Books, plans, scenarios and Excel reporting

Build a complete user journey, not a collection of disconnected views.

Workspace supports books and visual analysis, model creation, and applications / plans that organize assets, contributors, dates and dependencies. PAfE provides the Excel experience against the same governed models. Design their roles together so the user understands where to analyze, enter, review and approve.  [R82] [R83]

| Experience | Recommended design choice | User acceptance test |
| --- | --- | --- |
| Books and dashboards | Use clear navigation, context selectors, units and status labels. | User can explain the source and scope of a displayed number. |
| Input views | Show editable assumptions separately from calculated results. | Only intended cells are editable and all totals recalculate correctly. |
| Applications / plans | Assign contributors, reviewers, due dates and dependencies. | A complete submission and rejection / revision cycle works. |
| Excel reports | Use reusable layouts and supported formulas / report types. | Refresh and reopen produce consistent results without manual repair. |
| What-if analysis | Use private sandboxes or governed scenario versions as appropriate. | User distinguishes a private experiment from an approved shared baseline. |

## Sandboxes are not automatically the approved plan

IBM documents sandboxes as private places to experiment before committing changes to base data. The commit is a deliberate action. A sandbox should not be described as a replacement for approval controls, and its results should be labeled clearly when shared outside the planning interface.  [R42]

## Suggested planning cycle

Load and reconcile actuals; publish approved assumptions; open input tasks; collect contributor changes; review exceptions; revise and approve; freeze the agreed scenario; distribute the final view; archive the control evidence. Adapt the sequence to the business process and the supported workflow capabilities of the release.

| USABILITY CONTROL / Test with a first-time contributor, not only a modeler. Check navigation, accessible labels, locale formatting, error messages and the consequences of pressing a submit or action button. |
| --- |

---
Source: user-supplied comprehensive guide, section 18. Citation IDs R01-R90 resolve in ../reference-catalog.md and ../references.json. This is source-derived material, not a new IBM support certification.
