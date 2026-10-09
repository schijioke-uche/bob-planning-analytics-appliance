# 12. Workspace configuration and Administration agent

Join the user interface to the right database and management endpoints.

## Recommended configuration map

| Item | What to establish | Validation |
| --- | --- | --- |
| Workspace URL | An approved external FQDN, certificate and routing path. | Users reach the expected environment without certificate warnings. |
| Database connectivity | Correct Admin Server / database addresses and the required REST connectivity. | The intended databases are discoverable and usable. |
| Authentication | A coherent supported identity configuration across Workspace and TM1. | Admin and contributor sign-ins map to the correct users. |
| Spreadsheet Services | The service address and trust needed for websheets / dependent reports. | A representative websheet opens and works. |
| Local Administration agent | Agent on each relevant TM1 host; matched credentials / API-key configuration where required. | Database status, logs and permitted management actions are available. |
| Monitoring and alerts | Actionable thresholds and named notification recipients. | An approved test alert reaches an accountable operator. |

IBM requires the Administration agent wherever TM1 Server is installed for Local administration. Supported capabilities include database start / stop, activity inspection, log access, alerts and selected configuration tasks. Install and upgrade the agent in line with the Workspace documentation.  [R34] [R35]

## Hardening and operational acceptance

Do not expose the installation administration tool broadly after setup. Restrict runtime socket access and administrative permissions, record the certificate renewal procedure, and verify that a normal reboot restores the intended services. Keep install-time credentials separate from business-user credentials.

## What to capture in the build record

Record the Workspace build, host OS, runtime, image / kit source, configuration location, connected TM1 databases, authentication choice, certificate owner, backup procedure and test results. Keep secrets in approved secret storage; a build record should reference secret locations, not contain secret values.

| AGENT CONFUSION TO AVOID / A working browser login does not prove that database administration is configured. Test the Administration agent explicitly; conversely, monitoring access does not grant business users access to cube data. |
| --- |

---
Source: user-supplied comprehensive guide, section 12. Citation IDs R01-R90 resolve in ../reference-catalog.md and ../references.json. This is source-derived material, not a new IBM support certification.
