# 20. Security, identity and privacy readiness

Authentication, application access and data authorization are separate controls.

TM1 assigns object permissions to groups and users participate through group membership. Multiple group memberships can expand effective privileges. IBM also documents separate hierarchy security in applicable releases and a specific privilege controlling whether a TI process can modify security data.  [R44] [R43] [R45]

| Control layer | Recommended implementation / evidence |
| --- | --- |
| Identity | Document IBMid / federation or the selected Local authentication model; prove user removal and recovery. |
| Subscription and Workspace | Approve roles, groups, folder access and administrative scope. |
| Database authorization | Test cube, dimension, hierarchy, element and cell access with representative user personas. |
| Automation | Use individually accountable service identities / API access and controlled secret rotation. |
| Transport and storage | Maintain certificate trust, protect backups and document encryption-key custody. |
| Audit and retention | Define needed evidence, access to logs, retention and secure disposal with the responsible teams. |

IBM's cloud roles guidance distinguishes subscription, Workspace and database permissions. A broad Workspace role should not be treated as proof of appropriate data access.  [R46]

## GDPR readiness

The requested IBM GDPR-readiness paper is included at [R09]. Its full PDF text was not retrievable during this research. The following are implementation planning questions, not quoted IBM requirements or a legal compliance opinion: What personal data enters the model? Why is it needed? Who can access it? Where is it stored or exported? How are retention, correction and deletion handled? Who approves AI processing and international access?

Keep a data inventory spanning cubes, source extracts, logs, exported workbooks and backups. Ask the privacy / legal team to map the deployment to applicable obligations and contract terms. Product configuration alone does not establish organizational GDPR compliance.

| ENCRYPTION RECOVERY / IBM recommends testing encryption, encrypted backup, restore and decryption before production use. Loss of required keys can make data unavailable; key recovery must be tested with the backup procedure. |
| --- |

See IBM TM1Crypt troubleshooting guidance.  [R47]

---
Source: user-supplied comprehensive guide, section 20. Citation IDs R01-R90 resolve in ../reference-catalog.md and ../references.json. This is source-derived material, not a new IBM support certification.
