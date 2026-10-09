# 11. Local: install Planning Analytics Workspace

Choose the platform-specific container procedure from IBM documentation.

Workspace Local is a containerized web experience. IBM provides separate Windows and RHEL instructions, with prerequisites tied to the Workspace release. The installation entry point uses Start.ps1 on Windows and Start.sh on Linux. A dedicated Workspace host is recommended in IBM guidance.  [R21] [R26]

| Phase | Windows Server | RHEL |
| --- | --- | --- |
| Validate | Confirm the supported Server edition, container runtime and virtualization / container prerequisites. | Confirm the exact RHEL release and IBM-prescribed runtime; do not assume generic Ubuntu / Docker compatibility. |
| Prepare | Use approved administrative privileges, storage and network configuration. | Prepare container storage, runtime permissions, hostname and required network access. |
| Extract and start | Extract the selected kit to its intended location and use the shipped PowerShell startup script. | Extract the selected kit and use its Linux startup script. |
| Configure | Enter the applicable TM1, authentication and web endpoints in the administration tool. | Apply equivalent endpoints and authentication settings through the supported tool. |
| Verify | Confirm service / container health, user login and access to a test database. | Verify health and a controlled reboot / restart recovery test. |

## Startup entry points

| # Linux: from the extracted Workspace directory<br>./Start.sh<br><br># Windows PowerShell: from the extracted Workspace directory<br>.\Start.ps1 |
| --- |

Use only the operating-system block that applies to the selected kit. The scripts above are entry points, not substitutes for installing runtime prerequisites or following IBM setup prompts.

| SEPARATE OPENSHIFT PATH / Workspace Distributed is documented as an OpenShift-based deployment with its own installation and upgrade procedure. Its availability characteristics must not be generalized to every TM1 database, or to a standard Workspace Local installation. |
| --- |

See the dedicated Distributed guide when that architecture is selected.  [R22]

---
Source: user-supplied comprehensive guide, section 11. Citation IDs R01-R90 resolve in ../reference-catalog.md and ../references.json. This is source-derived material, not a new IBM support certification.
