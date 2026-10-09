# 7. On Cloud: connectivity and administration

Treat private data access as a managed integration boundary.

Current Cloud 101 material highlights the retirement of the hosted Rich Tier desktop and the replacement of Secure Gateway by Satellite Connector. Consequently, an old RDP-based installation tutorial is not a current onboarding plan. Use the supported administration interface and confirm any service-side task with IBM Support.  [R14]

## Recommended connector implementation workflow

1. Inventory each source: hostname, database, driver, port, authentication method, data classification and required load frequency.

2. Confirm the connector technology and entitlement applicable to the ordered offering. Do not assume a SaaS ODBCIS procedure is the dedicated-cloud Satellite procedure.

3. Place the connector / agent in an approved network segment with reachability to the source and the IBM service.

4. Implement DNS, TLS trust and firewall rules for the documented flows; keep credentials outside scripts and shared files.

5. Test connectivity from the actual execution path, then run a small TI load and reconcile counts / totals.

6. Record ownership, availability monitoring, certificate renewal and failure-handling procedures.

IBM publishes Satellite Connector entitlement guidance and a dedicated must-gather. Entitlements and operational limits must be checked against the current contract. The must-gather can include sensitive connector configuration, so redact API keys before sharing diagnostics.  [R61] [R60]

## Recommended steady-state checks

| Frequency | Operational check |
| --- | --- |
| After each scheduled load | Check completion, rejected records, data recency and reconciliation totals. |
| Daily / business critical window | Review database availability, integration failures and capacity alerts. |
| Before maintenance | Confirm affected environments, business freeze periods, test ownership and communication. |
| After maintenance | Run login, load, calculation, Excel and websheet smoke tests; record results. |

Use IBM service-status and maintenance resources for actual notices rather than assuming a fixed maintenance time from an older onboarding article.  [R65] [R66]

---
Source: user-supplied comprehensive guide, section 7. Citation IDs R01-R90 resolve in ../reference-catalog.md and ../references.json. This is source-derived material, not a new IBM support certification.
