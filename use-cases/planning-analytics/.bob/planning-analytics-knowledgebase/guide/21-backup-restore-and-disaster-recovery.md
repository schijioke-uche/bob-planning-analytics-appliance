# 21. Backup, restore and disaster recovery

Protect the whole planning service, not only cube files.

| Recovery scope | What to include in the recovery design |
| --- | --- |
| TM1 model and data | Database data, rules, processes, chores, security, required configuration and an application-consistent recovery method. |
| Workspace content | Books, applications, plans, preferences and other content using the supported Workspace backup / export procedure. |
| Spreadsheet Services and clients | Configuration, custom certificates, deployment settings and approved report artifacts. |
| Integration layer | Mappings, source contracts, connector configuration, schedules and protected secret references. |
| Identity and infrastructure | Identity mappings, service configuration, network / certificate dependencies and key-recovery arrangements. |

IBM Workspace installation guidance includes backup / restore as a distinct operation. A concrete upgrade notice requires Workspace content backup and restore at the 2.0.100 / 2.1.7 boundary because the backing database changed. This illustrates why a successful TM1 data backup is not proof of complete Workspace recovery.  [R21] [R49]

## Recommended recovery exercise

1. Agree business recovery-point and recovery-time objectives and document which offering / contract meets them.

2. Create a recovery set using the supported methods; retain version, timestamp and environment identifiers.

3. Restore into an isolated nonproduction target with compatible component versions.

4. Validate authentication, data totals, permissions, books, websheets, TI and scheduled processes.

5. Measure elapsed recovery time and record gaps, key dependencies and owner sign-off.

6. Repeat after material architecture, identity, encryption or version changes.

## Hosted-service boundary

Confirm IBM-managed backup coverage, customer export options, retention and recovery requests for the actual offering. Do not assume that a SaaS database backup includes all front-end assets or that Local file-copy instructions apply to a managed service.

| AVOID FALSE ASSURANCE / A backup job marked successful is only one control. Evidence of a usable restore and business reconciliation is the acceptance criterion. |
| --- |

---
Source: user-supplied comprehensive guide, section 21. Citation IDs R01-R90 resolve in ../reference-catalog.md and ../references.json. This is source-derived material, not a new IBM support certification.
