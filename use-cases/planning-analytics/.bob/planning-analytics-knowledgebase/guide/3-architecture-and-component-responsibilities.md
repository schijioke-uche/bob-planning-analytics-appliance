# 3. Architecture and component responsibilities

Separate the calculation engine, user experiences and administration plane.

| Component | Responsibility | Design consideration |
| --- | --- | --- |
| TM1 database / server | Multidimensional storage, calculations, write-back and model security. | Size and protect the data layer independently from the web interface. |
| TM1 Admin Server | Database discovery for applicable TM1 Local architectures. | Record discovery endpoints separately from database and REST ports. |
| Planning Analytics Workspace | Web books, visualizations, modeling, applications and plans. | Manage Workspace content and its backup separately from TM1 database data. |
| Planning Analytics for Excel (PAfE) | Excel-based planning and reporting against governed models. | Validate Office, add-in, Workspace and Spreadsheet Services compatibility. |
| Spreadsheet Services / TM1 Web | Websheet and related spreadsheet-service capabilities. | Separate installation and lifecycle; not the obsolete TM1 Applications component. |
| Planning Analytics Administration | Monitoring and administrative user interface. | Local database administration requires the corresponding Administration agent. |
| TI and REST APIs | Data processing, automation and application integration. | Choose authentication and endpoints for the actual offering and database generation. |

Component descriptions and boundaries are drawn from the installation index, TM1 overview, Workspace overview, Spreadsheet Services FAQ and Administration guidance.  [R04] [R81] [R82] [R29] [R35]

## Reference flow

Source systems feed controlled integration processes. These populate TM1 dimensions and cubes. Workspace, Excel and websheets expose the approved model to users. Authentication establishes identity; model authorization controls data access. Monitoring, backup and change management span all of these layers.

| NAMING DISTINCTION / Planning Analytics Administration agent is a Local monitoring / management component. Planning Analytics Agent is an AI capability. Installing one does not install or entitle the other. |
| --- |

---
Source: user-supplied comprehensive guide, section 3. Citation IDs R01-R90 resolve in ../reference-catalog.md and ../references.json. This is source-derived material, not a new IBM support certification.
