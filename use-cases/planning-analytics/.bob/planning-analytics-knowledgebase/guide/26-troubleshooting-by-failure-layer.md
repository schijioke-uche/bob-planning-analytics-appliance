# 26. Troubleshooting by failure layer

Capture the failing transaction before changing the environment.

| Symptom | First checks | IBM reference |
| --- | --- | --- |
| User cannot sign in | Correct environment, invitation, identity / federation, time, URL and certificate chain. | [R46], [R55], [R67] |
| Database visible but access denied | User / group mapping, cube access and independent hierarchy security. | [R43], [R44] |
| Local administration unavailable | Agent placement, connectivity, matching configuration and supported version. | [R34], [R35] |
| Excel / websheet feature fails | Conformance, correct XLL, Spreadsheet Services and EvaluationService configuration. | [R31], [R32], [R89] |
| ODBCIS connection list resets | External routing, firewall and source / connector reachability. | [R62] |
| ODBCIS query returns 504 | Test the actual external path and load-balancer / WAF timeout behavior. | [R63] |
| TI cannot send HTTPS POST | Trusted root and intermediate certificate-chain completeness. | [R64] |
| Workspace containers exit | Host events, container status, startup logs and version-specific service behavior. | [R50] |

The ODBC entries are documented IBM support cases, not a claim that every similar symptom has the same cause.  [R62] [R63] [R64] [R50]

## Recommended diagnostic sequence

Identify the precise environment, user and transaction; reproduce once under controlled conditions; capture the timestamp and timezone; locate the relevant component log; compare with the last known good state; isolate identity, network, source, database and client layers; change one factor at a time.

## Before opening a case

Collect component versions, OS / runtime, failure frequency, affected users, business impact, exact error, minimal reproduction and sanitized logs. Never attach live keys, passwords, unrestricted customer extracts or an unredacted connector configuration.

| AVOID DESTRUCTIVE DIAGNOSIS / Do not remove data directories, reset production models, weaken TLS, or grant global administrative rights to make an error disappear. Use approved maintenance and rollback procedures. |
| --- |

---
Source: user-supplied comprehensive guide, section 26. Citation IDs R01-R90 resolve in ../reference-catalog.md and ../references.json. This is source-derived material, not a new IBM support certification.
