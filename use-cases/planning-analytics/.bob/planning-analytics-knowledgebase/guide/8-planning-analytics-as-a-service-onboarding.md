# 8. Planning Analytics as a Service: onboarding

Keep the SaaS control plane distinct from dedicated on Cloud.

IBM SaaS onboarding guidance starts with provisioning through the SaaS console, preparing the environment, creating a database, adding users and configuring connectivity. The associated 101 hub has separate engine, migration and ODBC connector support resources. Use these rather than reusing dedicated-cloud administrative credentials or paths.  [R52] [R56] [R16]

| Step | Configuration task | Acceptance outcome |
| --- | --- | --- |
| 1 | Confirm tenant owner, subscription, region and environments in the console. | Owner can administer the correct service instance. |
| 2 | Create or allocate the planning database using the supported administration workflow. | Database is available within the approved capacity allocation. |
| 3 | Invite users and assign environment, Workspace and database access. | Pilot contributor has only the intended privileges. |
| 4 | Create approved data connections and migrate / build a small representative model. | Source-to-cube reconciliation and error reporting are proven. |
| 5 | Configure compatible Excel access and publish the pilot planning content. | Web and Excel produce consistent results. |
| 6 | Test API access, backups, administrative handover and support access. | The service can be operated without dependence on one individual. |

## Automation identity

IBM states that a dedicated noninteractive account cannot be created in this offering in the same way as older cloud accounts. Invite an appropriate user from the company directory, grant the required permissions and generate an API key. A key has the rights of its user; lifecycle, licensing and rotation must be considered.  [R57] [R58]

## Ownership handover

Assign the replacement owner / administrator before removing an existing owner. Keep at least two authorized operational contacts as a project control and test the handover. Consult IBM administrative ownership guidance for the supported service workflow.  [R59]

| TM1 12 AWARENESS / Database generation affects migration, endpoints and available administrative operations. Do not assume local TM1 11 file paths or authentication examples apply unchanged to this service. |
| --- |

---
Source: user-supplied comprehensive guide, section 8. Citation IDs R01-R90 resolve in ../reference-catalog.md and ../references.json. This is source-derived material, not a new IBM support certification.
