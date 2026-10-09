# 17. TurboIntegrator and data integration

Design data movement as a controlled, repeatable process.

TurboIntegrator (TI) organizes processing into four procedures. IBM describes Prolog as pre-source work, Metadata as structural work, Data as record-level value processing, and Epilog as post-source work. These phases provide a useful framework for separating validation, metadata maintenance and loading.  [R40]

| TI phase | Recommended use in a production process |
| --- | --- |
| Prolog | Validate parameters and source availability; initialize run context and confirm permissions. |
| Metadata | Create or update required dimensions / members according to approved mapping rules. |
| Data | Transform and load each record, using explicit reject rules and documented write semantics. |
| Epilog | Record completion, reconciliation results and follow-on actions appropriate to the actual outcome. |

## Recommended load contract

For each source, document the owner, frequency, input schema, extraction boundary, mapping, timezone, expected volumes, credentials, data retention and recovery behavior. Define whether a reload replaces a slice or adds transactions; a rerun must not silently double-count. Preserve enough run information to diagnose a failure without logging secrets.

## Data connectivity differs by offering

A Local process may rely on drivers and network routes on a customer-managed host. Dedicated on Cloud uses its approved cloud connectivity arrangements. SaaS has an offering-specific ODBC connector and data-connection model. Match the procedure to the offering and current connector documentation.  [R15] [R14] [R16]

| Validation point | Suggested evidence |
| --- | --- |
| Completeness | Source rows, accepted rows and rejected rows are accounted for. |
| Financial / operational balance | Control totals reconcile at agreed business grain. |
| Restartability | The same batch can be rerun without duplicate financial effect. |
| Failure handling | Operator receives the cause, run identifier and recovery action. |

| SCHEDULE ONLY AFTER VALIDATION / Chores and external schedulers should execute a proven process chain. Include dependency ordering, business calendars and a controlled rerun procedure rather than simply scheduling every load at the same time. |
| --- |

---
Source: user-supplied comprehensive guide, section 17. Citation IDs R01-R90 resolve in ../reference-catalog.md and ../references.json. This is source-derived material, not a new IBM support certification.
