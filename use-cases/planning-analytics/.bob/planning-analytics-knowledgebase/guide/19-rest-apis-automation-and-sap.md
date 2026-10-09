# 19. REST APIs, automation and SAP

Select authentication before writing the integration.

TM1 REST exposes model entities and operations; its metadata describes objects such as cubes, dimensions, processes and configuration. Workspace APIs and TM1 database APIs are different interfaces. SaaS API-key workflows must not be replaced with a Local username / password example.  [R36] [R37] [R39] [R57]

## Read-only Local connectivity example

Illustrative Bash commands for a Local TM1 endpoint where native Basic authentication is explicitly enabled and approved. They are not a Cognos or SaaS authentication recipe. curl prompts for the password rather than embedding it in shell history.

| TM1_BASE="https://tm1.example.com:12354"<br>TM1_USER="your-authorized-user"<br><br>curl --fail --show-error --user "$TM1_USER" \<br>  "$TM1_BASE/api/v1/\$metadata"<br><br>curl --fail --show-error --user "$TM1_USER" \<br>  "$TM1_BASE/api/v1/Cubes?\$select=Name" |
| --- |

Use the trusted CA configuration appropriate to the environment. Do not add -k to bypass TLS checks. The hostname, account and port are illustrative; use an authorized test model first.  [R38]

## Recommended integration controls

Use least-privilege identities, protected secret storage, bounded retries, request identifiers, explicit timeout handling and reconciliation. Before automating writes or process execution, define duplicate-request behavior and partial-failure recovery. Log identifiers and outcomes, not passwords, API keys or complete sensitive payloads.

## SAP connectivity

IBM describes its Planning Analytics Connector for SAP as supporting bidirectional exchange with SAP BW, S/4HANA and HANA Cloud through OData gateways. Use the connector manual and entitlement terms for the specific source and direction. This is not evidence that an arbitrary TI ODBC connection has identical SAP integration behavior.  [R01] [R85]

| API LIFECYCLE / Record which API surface, database generation and release each integration uses. Regression-test those dependencies before every platform upgrade. |
| --- |

---
Source: user-supplied comprehensive guide, section 19. Citation IDs R01-R90 resolve in ../reference-catalog.md and ../references.json. This is source-derived material, not a new IBM support certification.
