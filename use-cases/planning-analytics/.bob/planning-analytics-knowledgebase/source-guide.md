# Source-derived guide extraction

Source: IBM_Planning_Analytics_Comprehensive_Guide.docx. Original wording and tables are retained; Markdown table layout is an extraction; zero-width URL wrapping characters are removed in the text copy. The unchanged DOCX is in sources/. Research date: 2026-10-08.

TECHNICAL ENABLEMENT REFERENCE

IBM
Planning Analytics

Comprehensive Implementation,
Administration & Knowledge Guide

Planning Analytics on Cloud  |  Planning Analytics as a Service
Planning Analytics Local  |  TM1 and Workspace

| BUILD THE RIGHT PLATFORM. RUN A GOVERNED PLANNING SERVICE. / An implementation-oriented guide to deployment choices, installation, modeling, data integration, security, forecasting, operations and support. Includes a curated catalog of 90 official IBM reference URLs and the requested manual resources. |
| --- |

| DEPLOY | BUILD | OPERATE |
| --- | --- | --- |
| Cloud onboarding<br>Local installation<br>Version and platform choices | Dimensions and cubes<br>TI, REST and reporting<br>Forecasting and AI | Security and recovery<br>Performance and troubleshooting<br>Support and knowledge resources |

RESEARCH EDITION
8 October 2026

Based on public IBM documentation, support notices and IBM-authored product guidance. This independently assembled reference is not an IBM product manual, entitlement statement or support certification. IBM and TM1 are trademarks of International Business Machines Corporation.

# Contents

Select a section or a reference to navigate within this document.

| 01 | Product scope and deployment choices | 3 |
| --- | --- | --- |
| 02 | Versions, release lines and evidence | 4 |
| 03 | Architecture and component responsibilities | 5 |
| 04 | Business scope and operating ownership | 6 |
| 05 | Prerequisites and supported environments | 7 |
| 06 | Planning Analytics on Cloud: first access | 8 |
| 07 | On Cloud: connectivity and administration | 9 |
| 08 | Planning Analytics as a Service: onboarding | 10 |
| 09 | Local: install and register the TM1 data tier | 11 |
| 10 | Local: database configuration and connectivity | 12 |
| 11 | Local: install Planning Analytics Workspace | 13 |
| 12 | Workspace configuration and Administration agent | 14 |
| 13 | Planning Analytics for Microsoft Excel | 15 |
| 14 | Spreadsheet Services and Cognos integration | 16 |
| 15 | Model design: dimensions, cubes and drivers | 17 |
| 16 | Rules, feeders and model correctness | 18 |
| 17 | TurboIntegrator and data integration | 19 |
| 18 | Books, plans, scenarios and Excel reporting | 20 |
| 19 | REST APIs, automation and SAP | 21 |
| 20 | Security, identity and privacy readiness | 22 |
| 21 | Backup, restore and disaster recovery | 23 |
| 22 | Operations, capacity and performance | 24 |
| 23 | Upgrade and migration strategy | 25 |
| 24 | New features: what to evaluate now | 26 |
| 25 | Forecasting and AI governance | 27 |
| 26 | Troubleshooting by failure layer | 28 |
| 27 | Languages, community and support | 29 |
| 28 | Implementation plan and acceptance gates | 30 |
| 29 | Manuals and knowledge-base reading map | 31 |
| R | Reference catalog - 90 official IBM links | 32 |

Reading route: deployment and architecture (1-14); model and integration (15-19); controls and operations (20-23); new capabilities and enablement (24-29). Version and access qualifications are explained in Section 2.

# 1. Product scope and deployment choices

Start with the offering, not the installation media.

IBM Planning Analytics combines governed business planning with the multidimensional TM1 engine. Business users plan, analyze and write back through web and Excel experiences; modelers define the structures and logic behind those experiences. It is not simply a dashboard product or a shared workbook repository.  [R01] [R81]

| Offering | Operating model | What you deploy |
| --- | --- | --- |
| Planning Analytics on Cloud | Dedicated private hosted service managed by IBM. | Provision access, identities, models, integrations and client tools; do not install IBM-managed servers. |
| Planning Analytics as a Service | Multitenant SaaS; IBM describes AWS and Azure purchasing / deployment options. | Use the SaaS console and administration experience to establish environments, databases and access. |
| Planning Analytics Local | Customer-managed installation on supported infrastructure. | Install and operate the TM1 data tier, Workspace and selected client / web components. |
| Certified Containers / Software Hub | Separate containerized offering and platform-specific deployment path. | Use the matching service, entitlement and platform documentation; do not reuse a Windows installer runbook. |

IBM distinguishes dedicated on Cloud from as a Service; its pricing page also describes a Cloud Pak for Data deployment option. These are not interchangeable labels. Confirm the exact ordered SKU, region, identity model, database generation and operational responsibilities before design approval.  [R13] [R88]

## Recommended selection questions

Who must operate the infrastructure? Which source systems must be reached privately? Are there residency or enterprise-identity constraints? Is the goal an existing TM1 migration or a new SaaS model? Which Excel and AI capabilities are licensed? Establish these answers before choosing a topology or project estimate.

| INTERPRETATION RULE / A feature documented for SaaS, TM1 12 or a technical preview is not automatically available in Planning Analytics Local 2.1 or in every hosted subscription. |
| --- |

# 2. Versions, release lines and evidence

Research baseline: 8 October 2026. Recheck release notices before deployment.

| Line / component | What the reviewed IBM sources establish | Deployment implication |
| --- | --- | --- |
| 2.0 documentation | The supplied links remain useful for terminology, historical behavior and manual navigation. | Do not assume an old page describes the installer or support terms of a new build. |
| Local 2.1.24 | IBM published the download on 25 September 2026 and recommends Workspace, Excel and Spreadsheet Services 2.1.24 alongside it. | Use a release-aligned bill of materials and verify compatibility before installation. |
| Dedicated on Cloud | Workspace and Excel adopted 2.1 numbering beginning October 2025. | A cloud environment need not use the same numbering as multitenant SaaS. |
| SaaS 3.1 | AWS / Azure SaaS adopted 3.1 front-end numbering beginning October 2025; that renumbering did not itself change TM1 Database. | Track Workspace, Excel and database versions separately. |
| Local 3.1.11 preview | IBM labels it a technical preview without official product support; it requires TM1 12.6.4 and Workspace 3.1.11. | Evaluation only unless IBM subsequently publishes production support for the chosen release. |

Sources: original documentation, current Local download notices, and IBM product-management version announcements.  [R02] [R17] [R73] [R74] [R18]

## How to read this guide

Numbered citations such as [R17] point to the reference catalog. IBM product facts and version-specific instructions are cited. Deployment checklists, acceptance criteria and sample designs are practical recommendations, not additional IBM product guarantees. Commands marked illustrative require adaptation and testing.

| ACCESS AND SCOPE / Some IBM Docs, manual downloads and My Support pages restrict automated retrieval or require a browser / entitlement. These are labeled in the catalog; no unavailable contents have been inferred. This guide is a cross-functional reference, not a reproduction of every IBM manual or a compatibility certification. |
| --- |

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

# 4. Business scope and operating ownership

Turn a planning platform into a measurable business service.

| Planning area | Illustrative model and business outcome | Suggested acceptance measure |
| --- | --- | --- |
| FP&A | Connect revenue, operating expense, balance sheet and cash-flow assumptions. | Reconciliation to approved financial actuals and a repeatable forecast cycle. |
| Sales and workforce | Relate territory / product drivers and staffing assumptions to the financial plan. | Named ownership, controlled inputs and traceable assumption changes. |
| Supply chain | Compare demand, inventory and operational capacity scenarios. | A reproducible scenario comparison with approved business constraints. |
| ESG / sustainability | Plan sustainability measures alongside operational drivers. | Documented units, factors, source lineage and calculation ownership. |
| IT and marketing | Link resource allocation, spend and expected activity to enterprise objectives. | A maintained driver model rather than uncontrolled spreadsheet copies. |

IBM identifies these planning domains on its product page and provides business demonstrations in its resources library. The measures above are suggested project outcomes, not vendor ROI claims.  [R01] [R87]

## Recommended responsibilities

A business sponsor owns value and scope. Finance or operational process owners approve definitions and workflows. A TM1 modeler owns cube design, rules and TI. Data engineers own source quality and connectivity. Platform administrators own identity, capacity and operations. Security and privacy owners approve sensitive-data handling. A release owner coordinates testing and production promotion.

## License and commercial due diligence

Obtain an entitlement-specific quote rather than copying a website starting price into a project budget. Confirm user roles, environments, capacity, interfaces, connectors, AI features, regional availability, backup options and support. IBM publishes an estimator and separate deployment choices; the effective commercial terms come from the order and applicable service documents.  [R88]

| SCOPE DISCIPLINE / Begin with one planning decision and one accountable business owner. Establish data quality and reconciliation before adding forecasting, agentic actions or an enterprise-wide rollout. |
| --- |

# 5. Prerequisites and supported environments

A supported stack is a release-specific combination, not an OS name.

Use IBM Software Product Compatibility Reports to generate the exact report for the product, release and component being installed. The interactive report, not a generic hardware checklist, is the authority for supported software and prerequisites. Archive the report with the approved deployment design.  [R07] [R25]

| Check | What to record before installation |
| --- | --- |
| Product identity | Offering, entitlement, release, database generation and every selected component version. |
| Server and runtime | OS edition / version, architecture, required libraries, container runtime and approved patch level. |
| Client stack | Browser, Windows / Office version, Excel bitness, PAfE build and required framework components. |
| Capacity | Representative model size, peak users, concurrent calculations, TI workload, memory growth and recovery objectives. |
| Network and identity | FQDNs, certificates, proxy bypasses, DNS, time synchronization, authentication mode and firewall flows. |
| Operations | Service identities, directory permissions, backup storage, monitoring, maintenance ownership and rollback artifacts. |

## Practical preparation sequence

1. Generate SPCR for the exact component set; do not reuse an older project report without checking it.

2. Record a port and certificate inventory for every environment, including connector paths and management interfaces.

3. Secure approved installation media from IBM channels and retain the associated release / fix documents.

4. Provision nonproduction first, with representative data and the same authentication approach planned for production.

5. Run concurrency, integration, restore and security tests before finalizing capacity and go-live dates.

| IMPORTANT PLATFORM BOUNDARY / A WSL Ubuntu workstation can be used for administrative tooling where appropriate. It is not evidence that TM1 Server or Workspace is supported for production on WSL or Ubuntu. Workspace Local documentation identifies supported Windows Server and RHEL paths; SPCR must confirm the exact combination. |
| --- |

For Workspace Local, use the component installation guide and its platform prerequisites, not only the data-tier requirements.  [R21]

# 6. Planning Analytics on Cloud: first access

Hosted deployment means onboarding and configuration, not server installation.

The dedicated on Cloud offering is IBM-hosted. IBM onboarding guidance covers IBMid access, the welcome kit, support entitlement, user invitations, Excel tooling and notifications. Parts of older checklists describe retired Rich Tier or gateway arrangements; use the current Cloud 101 notices to identify the replacement workflow.  [R03] [R51] [R14]

| Stage | Action | Evidence of completion |
| --- | --- | --- |
| Identity and subscription | Identify the subscription owner; accept the invitation using the correct IBMid; associate the support entitlement. | Named owner, environment URL and working support access. |
| Environment handover | Retrieve the welcome / environment information using the available administration experience; inventory development and production. | Recorded URLs, administrators and approved environment purpose. |
| Initial administration | Open Workspace, review users / groups and establish a second authorized administrator. | A second administrator can sign in independently. |
| Business users | Invite the pilot cohort, assign subscription roles, content access and database permissions. | A non-admin user sees only the intended data and books. |
| First usable model | Build or migrate a small validated database, load actuals and publish a pilot book. | Totals reconcile; authorized input and refresh work. |
| Client and service readiness | Install a compatible Excel add-in; subscribe to maintenance and status notices. | Excel connects and operational contacts receive notifications. |

## Recommended onboarding control

Keep an environment register containing the exact offering, tenant / environment identifiers, owner, URLs, identity domain, model inventory, connector responsibility and support escalation contacts. Store credentials in approved secret management, not in the register.

| ACCEPTANCE TEST / Use an ordinary contributor account to open a book, read an approved slice, enter a test value, refresh it from Excel and confirm that an unauthorized slice remains inaccessible. Administrator-only testing is insufficient. |
| --- |

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

# 9. Local: install and register the TM1 data tier

Apply the exact release procedure to supported Windows or Linux hosts.

The data-tier guide for 2.0.9.21 and later lists TM1 Server, Admin Server, tools, samples, core-dump support and the Administration agent. IBM changed the installer at that boundary and removed Cognos Configuration from the new data-tier installation. Older installation screenshots therefore need careful interpretation.  [R23] [R24]

## Recommended installation sequence

1. Obtain the matching IBM installation kit and read its prerequisites and upgrade notes. Confirm SPCR, platform, disk layout and service accounts.

2. For an upgrade, capture a restorable backup and the previous service definitions before uninstalling or replacing anything.

3. Keep production model data outside the product installation directory. Record separate data, log, backup and installation locations.

4. Run the supported installer, select the required components and retain the installer log.

5. Create / restore the database configuration and use the documented platform-specific service registration or startup procedure.

6. Start the Admin Server and database as applicable; verify logs and connectivity before enabling scheduled jobs.

## Windows service registration example

Illustrative commands for the newer TM1 data-tier packaging; run from an elevated Command Prompt after replacing the paths. They register services, not a complete secured deployment. Follow the selected release manual for service identities and startup.

| cd /d "C:\IBM\tm1_64\bin64"<br>tm1admsd.exe -install<br>tm1sd.exe -install -n "Finance" -z "D:\PA\Models\Finance" |
| --- |

IBM documents these registration switches and the new config.tm1admsrv.json configuration file. The transition from the older installer can require an uninstall rather than an in-place overwrite; preserve databases and custom configuration first.  [R24]

| PRODUCTION GATE / Do not enable integration schedules until the restored model, security, TLS, backup and rollback have been tested. A successfully installed binary is not yet an accepted planning service. |
| --- |

# 10. Local: database configuration and connectivity

Make every database and network path explicit.

For TM1 Local, tm1s.cfg identifies the model and its connections. The REST listener is controlled by HTTPPortNumber, which is distinct from the native database port. The API metadata exposes configuration information; use the proper endpoint rather than treating all TM1 ports as equivalent.  [R37] [R38]

| Configuration concern | Implementation action |
| --- | --- |
| Identity and directories | Assign a meaningful ServerName; keep database and logging locations outside installation media and grant only the required filesystem access. |
| Ports | Reserve distinct native and REST ports for databases on the same host; record every allowed source and destination. |
| TLS | Use trusted certificates and complete chains. Check FQDN matching, expiration, private-key protection and client trust. |
| Authentication | Select and document the supported TM1 / Cognos identity configuration for the release. Do not change modes without testing existing identities and permissions. |
| Administration | Separate business administration from OS / container access and protect management endpoints. |

## Illustrative TM1 11 configuration fragment

| ServerName=Finance<br>DataBaseDirectory=D:\PA\Models\Finance\data<br>LoggingDirectory=D:\PA\Models\Finance\logs<br>PortNumber=12345<br>HTTPPortNumber=12354<br>UseSSL=T |
| --- |

The ports and paths above are examples, not IBM-required values. This fragment omits environment-specific authentication and certificate settings; it is not a complete production configuration. Apply the correct reference parameters for your selected release.  [R37] [R38]

## Recommended verification

Check service start and logs, resolve the FQDN from each client tier, validate the TLS chain, authenticate with a non-admin account, retrieve REST metadata and open a governed cube view. A successful TCP connection alone does not validate identity or data permissions.

| AVOID UNSAFE SHORTCUTS / Do not use disabled certificate verification, broad firewall openings or a shared administrator password as a permanent fix. Diagnose the failed layer and correct that layer. |
| --- |

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

# 13. Planning Analytics for Microsoft Excel

Install the right add-in, then validate a complete planning transaction.

Planning Analytics for Excel retains Excel as a user interface while connecting it to governed TM1 models. Current single-XLL installation instructions replace older multi-component installation assumptions. IBM documents a single .xll add-in for versions 2.0.65 and later and publishes separate conformance requirements.  [R83] [R33] [R32] [R31]

## Recommended deployment procedure

1. Inventory Office version / channel and bitness, PAfE build, Workspace endpoint and Spreadsheet Services version.

2. Download the add-in from the authorized administration experience or IBM distribution channel for the offering.

3. Close Excel, preserve an approved rollback copy and remove conflicting obsolete add-ins according to the applicable IBM instructions.

4. Place the correct .xll in an approved managed location. Apply enterprise signing and trust controls rather than globally weakening Excel security.

5. Load the add-in for a controlled session or register it in Excel Add-ins for repeated use, following the chosen deployment method.

6. Configure the environment connection and sign in with the intended business identity.

7. Open a representative report, refresh it, change an authorized input, submit / commit as appropriate, and reconcile the result with Workspace.

## Dependencies that are easy to miss

IBM documents that Universal Reports and TM1SET-related capabilities use the EvaluationService component of Spreadsheet Services. Distributed TM1 deployments need its proper configuration. Do not diagnose every Excel formula or rendering failure as a local Office issue; confirm the service and supported component combination.  [R89]

| Test | Pass criterion |
| --- | --- |
| Read and refresh | Expected totals match the same model slice in Workspace. |
| Write-back | Only authorized cells accept values; calculated cells behave as designed. |
| Reopen and reconnect | The workbook works after Excel restart without hidden local dependencies. |
| Shared use | Another entitled user can run it with that user's own permissions. |

| OPERATIONAL TIP / Treat the add-in as a managed enterprise client: version inventory, pilot ring, signed distribution, regression workbook and a documented rollback. |
| --- |

# 14. Spreadsheet Services and Cognos integration

Keep modern components separate from legacy packaging.

TM1 Web is delivered as Planning Analytics Spreadsheet Services in a separate installation kit. IBM describes its independent service and directory layout and notes that separation began with the 2.0.9.2 data-tier release. It can be installed on a different host from TM1 Server.  [R29] [R30] [R04]

## Recommended implementation sequence

1. Confirm that websheets or report features actually require this component; include it in the release matrix when they do.

2. Install the matching package on a supported host using its own installation guide, paths and service account.

3. Configure database discovery, authentication and approved TLS trust between client, web service and database.

4. Integrate the endpoint with Workspace and configure EvaluationService when the selected reporting topology requires it.

5. Test real workbook patterns: selectors, calculations, action buttons, authentication, authorized write-back and export.

6. Back up configuration and custom certificates; include this service in restart, patch and disaster-recovery procedures.

The separate installer uses the IBM Planning Analytics Spreadsheet Service rather than relying on the historical Cognos Configuration workflow. Follow the current component guide rather than mixing files from legacy TM1 Web and newer Spreadsheet Services installations.  [R29]

## Cognos Analytics integration

The Local installation documentation includes Cognos integration and security paths. Treat a Cognos-based authentication design as an end-to-end identity architecture: document the namespace, relevant gateway / dispatcher routes, certificate trust and user mapping. Test the same user across all interfaces. Do not copy another environment's CAM settings blindly.  [R04]

| HISTORICAL COMPONENTS ARE NOT REQUIRED DEFAULTS / IBM's 2.0 deprecation notices identify removed or obsolete components such as Operations Console and PMHub. The newer data-tier explanation states that TM1 Applications is not part of the 2.1 release. Inventory dependencies before upgrade; do not reinstall obsolete components merely to match an old diagram. |
| --- |

Review the exact deprecation notices for the target line.  [R90] [R24] [R28]

# 15. Model design: dimensions, cubes and drivers

Illustrative model design - adapt to approved business definitions.

TM1 models organize values across dimensions such as time, accounts, organizational units, products and scenarios. Cubes hold multidimensional intersections; calculations and write-back turn those intersections into a planning model. Business definitions, not the number of source columns, should drive the design.  [R81]

| Model element | Illustrative finance design | Design control |
| --- | --- | --- |
| Time | Month and year, with an approved fiscal calendar. | Define how partial periods, actuals and forecast horizons are handled. |
| Organization | Entity and cost center with reporting hierarchies. | Assign an owner to reorganizations and effective-date decisions. |
| Scenario | Actual, Budget and Forecast versions. | Lock approved actuals / baselines and document copy-forward policy. |
| Measures | Units, price, revenue, cost and margin. | Distinguish additive values from percentages and ratios. |
| Drivers | Headcount, compensation assumptions, capacity or price changes. | Keep input assumptions distinct from calculated results. |
| Attributes and aliases | Descriptions, classification and display names. | Preserve stable identifiers when labels change. |

## Recommended modeling workflow

1. Agree the grain of each cube and document what one cell means.

2. Define dimensions, hierarchies, element types and naming conventions before loading facts.

3. Build a small model with known totals; prove consolidations, calculations and access rules.

4. Separate transaction staging from planning assumptions and published results where that improves clarity.

5. Test reorganization, new members, missing data, zero values, currency assumptions and read-only history.

6. Record the owner and test cases for every material calculation and integration.

| ILLUSTRATIVE BUSINESS RULE / Revenue = Units x Price. Gross Margin = Revenue - Cost. Margin % must be recomputed from consolidated Revenue and Cost, not summed across products. These are example requirements, not a packaged IBM financial model. |
| --- |

# 16. Rules, feeders and model correctness

Performance tuning must preserve the meaning of the plan.

TM1 rules implement model calculations; feeders are relevant when sparse-consolidation optimization is used. IBM's FEEDERS documentation describes placing feeder statements after a FEEDERS section and identifying the rule-calculated cells needed for correct sparse consolidation. A faster view is not acceptable if its total is wrong.  [R41]

## Recommended design approach

| Concern | Implementation guidance | Test evidence |
| --- | --- | --- |
| Rule ownership | Assign a business definition, technical owner and intended cell scope. | Known examples reconcile to an independently calculated result. |
| Consolidations | Distinguish summable measures from ratios, rates and balances. | Parent totals remain correct after filter and hierarchy changes. |
| Feeders | Trace dependencies deliberately; avoid adding broad feeder patterns merely to hide missing totals. | Zero / nonzero transitions, sparse slices and cross-cube dependencies are tested. |
| Change control | Version rules with the related process and metadata changes. | Regression results accompany the promoted release. |
| Performance | Measure the effect of changes under representative concurrent load. | Calculation time, memory and load / restart behavior are recorded. |

## Illustrative validation set

Prepare a compact fixture with known input values, a zero-input case, a missing-input case, a newly introduced element, a consolidated view and a changed driver. Validate the result through both the user interface and an independent reconciliation. For cross-cube rules, test the source and target together.

## Avoid an anti-pattern

Do not fix a reporting mismatch only by changing the workbook. Determine whether it comes from source data, the mapping process, the model rule, the consolidation, the user's security slice or the report definition. A workbook-only workaround can conceal a shared-model defect.

| RELEASE DISCIPLINE / Promote a calculation change with its test fixture and reconciliation evidence. Keep a recoverable previous model version and document the business impact of rollback. |
| --- |

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

# 18. Books, plans, scenarios and Excel reporting

Build a complete user journey, not a collection of disconnected views.

Workspace supports books and visual analysis, model creation, and applications / plans that organize assets, contributors, dates and dependencies. PAfE provides the Excel experience against the same governed models. Design their roles together so the user understands where to analyze, enter, review and approve.  [R82] [R83]

| Experience | Recommended design choice | User acceptance test |
| --- | --- | --- |
| Books and dashboards | Use clear navigation, context selectors, units and status labels. | User can explain the source and scope of a displayed number. |
| Input views | Show editable assumptions separately from calculated results. | Only intended cells are editable and all totals recalculate correctly. |
| Applications / plans | Assign contributors, reviewers, due dates and dependencies. | A complete submission and rejection / revision cycle works. |
| Excel reports | Use reusable layouts and supported formulas / report types. | Refresh and reopen produce consistent results without manual repair. |
| What-if analysis | Use private sandboxes or governed scenario versions as appropriate. | User distinguishes a private experiment from an approved shared baseline. |

## Sandboxes are not automatically the approved plan

IBM documents sandboxes as private places to experiment before committing changes to base data. The commit is a deliberate action. A sandbox should not be described as a replacement for approval controls, and its results should be labeled clearly when shared outside the planning interface.  [R42]

## Suggested planning cycle

Load and reconcile actuals; publish approved assumptions; open input tasks; collect contributor changes; review exceptions; revise and approve; freeze the agreed scenario; distribute the final view; archive the control evidence. Adapt the sequence to the business process and the supported workflow capabilities of the release.

| USABILITY CONTROL / Test with a first-time contributor, not only a modeler. Check navigation, accessible labels, locale formatting, error messages and the consequences of pressing a submit or action button. |
| --- |

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

# 22. Operations, capacity and performance

Measure the business workload before tuning the platform.

Planning Analytics Administration provides a database operational view; the Local agent enables management capabilities such as activity inspection, logs and alerts. IBM Local and SaaS 101 hubs organize component-specific must-gathers and operational knowledge. Use these as the starting point for runbooks.  [R35] [R15] [R16]

| Signal | What it can indicate | Recommended next step |
| --- | --- | --- |
| Memory growth | Larger models, calculation / feeder effects, concurrent workload or content changes. | Compare against the baseline, release changes and representative model tests. |
| Long calculation or TI time | Source latency, inefficient process logic, contention or model design. | Separate source time from model time; inspect the relevant logs and workload. |
| Waiting users / threads | Contention or long-running activities. | Identify the owner and business impact before canceling a process. |
| Slow workbook / book | Large result set, report design, service dependency or client issue. | Reproduce with a small controlled view and compare web / Excel behavior. |
| Container / service exits | Host restart, runtime or service-level problem. | Inspect host and component health; do not repeatedly restart without evidence. |

## Recommended service runbook

Record the daily validation procedure, scheduled processing windows, capacity thresholds, incident contacts and approved interventions. For each intervention identify the operator, reason, affected business process and rollback. Tie monitoring to user outcomes such as data freshness and planning-cycle completion, not only CPU usage.

## Performance-test design

Use realistic concurrent contributors, representative rules, TI jobs and report refreshes. Record the data size, version matrix, response-time distribution, peak memory and errors. Compare like-for-like runs after tuning. Avoid promising capacity from a small sample model or a single-user demonstration.

| STOP-CONDITION DISCIPLINE / Do not repeatedly retry a heavy load or calculation while the system is contended. A bounded retry policy and a named operator are safer than an uncontrolled loop that amplifies an outage. |
| --- |

# 23. Upgrade and migration strategy

Treat component alignment and rollback as first-class deliverables.

The 2.1.24 download notice recommends aligned Workspace, Excel and Spreadsheet Services builds. Other upgrade boundaries have special requirements: the 2.0.9.21 data-tier installer transition and the Workspace backup / restore boundary are examples. Consult release notes, fix lists, conformance and deprecation notices together.  [R17] [R27] [R19] [R31] [R24] [R49]

## Recommended upgrade procedure

1. Inventory the source offering, database generation, all component builds, custom integrations and unsupported dependencies.

2. Select the target and generate its supported-configuration report; read every intervening required migration step.

3. Create and test the recovery set; preserve installation kits, certificate material and a rollback decision point.

4. Clone or migrate a representative workload into an isolated test environment.

5. Run calculation, security, integration, workflow, Excel, websheet, API and performance regression tests.

6. Rehearse production cutover, including user communication, source-load freeze, credentials and rescheduling.

7. After cutover, reconcile results and obtain business sign-off before retiring the previous environment.

## TM1 12 is a distinct migration concern

Front-end version renumbering does not itself prove that the database generation changed. Review TM1 12 documentation, migration tooling and API / integration compatibility separately. The Local 3.1.11 technical preview is explicitly unsupported for official product support and requires its specified database and Workspace pair.  [R74] [R75] [R18]

| PREVIEW IS NOT PRODUCTION AUTHORIZATION / Evaluate technical-preview capabilities in an isolated environment with nonproduction data. A newer version number, downloadable kit or successful demo does not replace a production support statement and validated architecture. |
| --- |

Check lifecycle terms and extensions directly before planning an upgrade deadline; older lifecycle pages may not reflect a customer's current support position.  [R20]

# 24. New features: what to evaluate now

Keep release, offering and feature availability together.

| Feature area | Reviewed change | Qualification / action |
| --- | --- | --- |
| Release alignment | Local 2.1.24 is the September 2026 refresh. | Use its recommended companion components and fix list. |
| Forecasting | Extended engine provides additional model choices. | Verify the deployed release and evaluate forecast quality on held-out data. |
| SaaS data sources | 3.1.11 adds Redshift, Box, Dremio, Dropbox, FTP, Google Cloud Storage, Netezza and Azure Fabric Warehouse connections. | The notice scopes this list to SaaS and Advanced Certified Containers. |
| AI provider | 3.1.11 adds an Amazon Bedrock provider option alongside watsonx.ai. | Feature-flag, credentials and model configuration apply; do not assume entitlement. |
| Database APIs | Workspace REST database-management capabilities expand. | Create, delete and backup-management operations cited in the notice are TM1 12-specific. |
| Plans and reporting | 3.1.11 updates task action logs, approval navigation and exploration reports. | Regression-test existing planning workflows and book interactions. |
| Agent / API integration | 3.1.9 includes agent, modeling, notification and API changes. | Review integrations and endpoint changes rather than only the visual UI. |

Release sources: Local download notice, SaaS 3.1.11 / 3.1.9 announcements and IBM's forecasting introduction.  [R17] [R69] [R70] [R71]

## How to evaluate a feature

Record the business problem, target release and offering, feature flag / entitlement, data exposed, permissions, test method, expected result and rollback. Test with ordinary users. Update training and runbooks only after validating the actual deployed behavior.

| HISTORICAL NEW-FEATURE MANUAL / The requested 2.0 New Features manual remains in the reference catalog. For current deployment decisions, pair it with the 2.1 Workspace, 3.1 Excel and TM1 12 release sources. |
| --- |

See the component new-feature indexes.  [R05] [R76] [R77] [R75]

# 25. Forecasting and AI governance

Separate statistical prediction, explanation and authorized action.

IBM describes baseline forecasting, on-demand forecasting, spreading and saved statistical details. The Extended Forecasting Engine announcement identifies additional methods including Holt-Winters, MSTL, Auto ARIMA, BATS and XGBoost. Select the engine and method according to the release and forecast use case, not the appeal of an algorithm name.  [R86] [R71]

| Stage | Recommended control | Evidence |
| --- | --- | --- |
| Prepare | Define time grain, missing data, exclusions, history window and the business target. | A documented training / evaluation dataset. |
| Forecast | Compare an approved baseline with eligible methods using held-out periods. | Recorded error and bias measures appropriate to the business. |
| Review | Inspect anomalies, changing drivers, confidence and unusual events. | Named reviewer and rationale for overrides. |
| Publish | Keep forecast output separate from approved targets until accepted. | Versioned scenario and an accountable approval. |
| Monitor | Track degradation and changes in business assumptions. | A retraining / review trigger and rollback plan. |

## Planning Analytics Agent and extensions

IBM positions the Agent as model-aware assistance and describes watsonx Orchestrate integration and MCP extensibility. Generated explanations, suggested actions and model writes require different controls. A fluent explanation is not proof that a forecast is valid or that an action should be executed.  [R84]

## Recommended AI deployment policy

Approve the provider, region, data flows and retention terms. Limit identities to the model slices required. Require confirmation for material write-back or external actions, maintain auditability, and test whether unauthorized questions or actions are blocked. Use representative financial and operational examples to validate output, not only generic prompts.

IBM's September update distinguishes Workspace capabilities from Excel items still described as forthcoming. Do not convert a product roadmap statement into an implemented customer feature.  [R72]

| DECISION BOUNDARY / The business owner remains responsible for planning assumptions and approvals. AI should support the control process rather than bypass it. |
| --- |

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

# 27. Languages, community and support

Choose the right resource for learning, operations or an incident.

## Supported languages are component-specific

The language index separates Workspace, Excel, Local and Cloud. The reviewed Workspace 2.1 matrix lists English, French, German, Italian, Japanese, Spanish, Brazilian Portuguese and Simplified Chinese for both UI and documentation. It lists Korean documentation but not Korean UI, and several additional UI languages without translated manuals. Confirm your target release rather than extrapolating from another component.  [R08] [R78]

The reviewed PAfE matrix lists 27 UI languages, while documentation is available in a smaller subset. UI language availability does not guarantee translated documentation or the same behavior in AI features. Include number formats, dates, fiscal periods and multilingual names in user testing.  [R79]

| Resource | Best use | Boundary |
| --- | --- | --- |
| Planning Analytics community | Peer discussion, IBM product blogs, library and events. | Do not post confidential data or use a forum as an incident SLA. |
| Cloud / Local Support Communities | Entitlement-linked technical assistance for the correct offering. | Some content and case actions require IBMid authorization. |
| Offering-specific 101 hubs | Must-gathers, known issues, installation topics and support navigation. | Check date, version and component applicability. |
| Status / maintenance pages | Hosted incidents and planned service work. | Use the actual service notice for timing and scope. |
| Manuals and SPCR | Technical procedures and supported combinations. | Select the precise edition and preserve a project reference snapshot. |

Requested community and support destinations are preserved in the reference catalog, together with current IBM 101 hubs.  [R10] [R11] [R12] [R13] [R65]

## Recommended escalation record

State the business impact, affected environment, start time, available workaround and accountable contact. Attach the relevant must-gather and record the case number in the incident log. Support severity and response obligations come from IBM's applicable support terms, not an assumed generic promise.  [R54] [R53]

# 28. Implementation plan and acceptance gates

Suggested delivery framework - not a vendor-mandated schedule.

| Phase | Core deliverables | Exit gate |
| --- | --- | --- |
| Discover | Business process, data inventory, stakeholders, offering and initial risk register. | Sponsor approves scope and measurable outcomes. |
| Design | Model grain, integration contracts, security matrix, version bill of materials and capacity assumptions. | Architecture and control owners approve the design. |
| Build | Environment, model, TI, reports, planning workflow and monitoring. | Repeatable development deployment and reconciliation. |
| Validate | Security, calculation, concurrency, integration, restore and user-acceptance evidence. | Business and operations accept the critical tests. |
| Deploy | Cutover rehearsal, communication, backups, rollback and production access. | Named go / no-go authority approves release. |
| Operate | Runbooks, ownership, training, incident process and improvement backlog. | Service ownership formally handed over. |

## Minimum recommended acceptance tests

Reconcile imported totals to source; verify parent / ratio calculations; reject invalid input; test authorized and unauthorized slices; rerun a failed load safely; complete a contributor-to-approver workflow; refresh and write back from the supported Excel client; validate representative APIs; restore the recovery set; test post-maintenance startup; measure peak-user behavior.

## Suggested learning sequence

Business users: start with Workspace navigation, input, scenarios and plan tasks. Modelers: learn dimensions, cubes, rules, TI and security before advanced automation. Administrators: learn the offering, deployment, monitoring, backup and support process. Integrators: study authentication and API contracts before implementing write operations.

IBM provides guided demonstrations, case studies and product resources. Pair these with the manuals and an isolated training model rather than treating a demonstration as production certification.  [R87] [R80]

| SUCCESS CRITERION / The implementation is complete when the business can run an approved planning cycle and operations can support and recover it. Installation alone does not meet that criterion. |
| --- |

# 29. Manuals and knowledge-base reading map

Use the official manual catalog, then select the matching version and language.

IBM's requested PDF catalog names the following nine manuals. The catalog is the reliable starting point for downloads; individual PDF locations and access controls can change. Use its named download entries rather than a guessed PDF path. Refer to the linked online documentation when a download is unavailable.  [R06]

| Manual in the IBM catalog | Use it for | Related guide references |
| --- | --- | --- |
| Planning Analytics on the Cloud | Hosted onboarding and administration. | [R03], [R14], [R51] |
| Local Installation and Configuration | Architecture, prerequisites, installation, configuration and upgrade. | [R04], [R21]-[R30] |
| Planning Analytics New Features | Historical release-by-release changes. | [R05], [R69]-[R77] |
| Planning Analytics Workspace | Books, modeling, applications and plans. | [R06], [R80], [R82] |
| Planning Analytics as a Service | SaaS service usage and administration. | [R06], [R16], [R52] |
| Planning Analytics for Microsoft Excel | Excel installation, reporting and planning. | [R06], [R31]-[R33] |
| Planning Analytics Operations | Database operations and administration. | [R06], [R48] |
| Planning Analytics Reference | Parameters, functions and detailed technical lookup. | [R06], [R36]-[R41] |
| Spreadsheet Services / TM1 Web | Websheet use, installation and service configuration. | [R06], [R29], [R30], [R89] |

## Reference catalog conventions

The following catalog contains 90 distinct IBM URLs. Titles and URLs are clickable. Entries identify historical baselines, current releases, interactive tools and access restrictions. A link included for navigation is not represented as a fully reviewed manual. References were assembled on 8 October 2026; recheck versions and availability at implementation time.

| KNOWLEDGE-BASE MAINTENANCE / For a team knowledge store, retain the URL, title, offering, version, last review date and owner. Review after major upgrades. Never flatten preview, historical and production documents into an undifferentiated answer set. |
| --- |

# Reference catalog

R01-R09  |  Official IBM sources and navigation links

[R01] IBM Planning Analytics - product overview

https://www.ibm.com/products/planning-analytics

Capabilities, use cases, interfaces and integration overview.

[R02] Planning Analytics 2.0 documentation home

https://www.ibm.com/docs/en/planning-analytics/2.0.0?topic=SSD29G_2.0.0/main/welcome.htm

Original requested documentation baseline; select the version matching your deployment. Requested entry point; browser navigation required.

[R03] Planning Analytics on Cloud - administration manual

https://www.ibm.com/docs/en/SSD29G_2.0.0/com.ibm.swg.ba.cognos.tm1_cloud_mg.2.0.0.doc/pa_cloud.html

Requested hosted-service manual; supplement historical steps with current cloud guidance. Requested link; automated retrieval restricted.

[R04] Planning Analytics Local - installation and configuration

https://www.ibm.com/docs/en/SSD29G_2.0.0/com.ibm.swg.ba.cognos.tm1_inst.2.0.0.doc/pa_install.html

Architecture, data tier, Workspace, Excel, Spreadsheet Services and security.

[R05] Planning Analytics - new features manual, 2.0

https://www.ibm.com/docs/en/SSD29G_2.0.0/com.ibm.swg.ba.cognos.tm1_nfg.2.0.0.doc/pa_nfg.html

Historical component release notes; pair with current 2.1 and 3.1 sources. Requested link; automated retrieval restricted.

[R06] Planning Analytics manuals in PDF - official catalog

https://www.ibm.com/docs/en/SSD29G_2.0.0/main/pdf_link.html

Nine named manuals; use the catalog to obtain the edition and language required.

[R07] Software Product Compatibility Reports (SPCR)

https://www.ibm.com/software/reports/compatibility/clarity/index.html

Generate exact supported OS, software and prerequisite reports. Interactive browser required.

[R08] Planning Analytics supported languages - component index

https://www.ibm.com/docs/en/SSD29G_2.0.0/main/supported_languages.html

Entry point for Workspace, Excel, Local and Cloud language matrices.

[R09] GDPR readiness for Planning Analytics Local (PDF)

https://www.ibm.com/docs/en/SSD29G_2.0.0/gdpr/doc.pdf

Requested product privacy-readiness paper; read with your privacy and legal teams. Requested PDF; automated retrieval returned HTTP 403.

# Reference catalog - continued

R10-R18  |  Official IBM sources and navigation links

[R10] IBM Planning Analytics community

https://community.ibm.com/community/user/businessanalytics/communities/community-home?communitykey=8fde0600-e22b-4178-acf5-bf4eda43146b

Discussion, blogs, library and events; not a substitute for a support case.

[R11] Planning Analytics on Cloud Support Community

https://www.ibm.com/mysupport/s/topic/0TO500000002PWQGA2/planning-analytics-on-cloud?language=en_US&productId=01t50000004XdyhAAC

Requested product support destination. IBMid or support entitlement may be required.

[R12] Planning Analytics Local Support Community

https://www.ibm.com/mysupport/s/topic/0TO500000002PWWGA2/planning-analytics-local?language=en_US&productId=01t50000004XdynAAC

Requested Local support destination. IBMid or support entitlement may be required.

[R13] IBM Planning Analytics 101

https://www.ibm.com/community/101/ibm-planning-analytics/

Official knowledge hub and offering-specific support paths.

[R14] Planning Analytics on Cloud 101

https://www.ibm.com/community/101/ibm-planning-analytics/planning-analytics-on-cloud/

Cloud notices, connectivity changes, must-gathers and service operations.

[R15] Planning Analytics Local 101

https://www.ibm.com/community/101/ibm-planning-analytics/ibm-planning-analytics-local/

Local administration, technical diagnostics and support resources.

[R16] Planning Analytics as a Service 101

https://www.ibm.com/community/101/ibm-planning-analytics/planning-analytics-as-a-service/

SaaS support, engine, migration and ODBC connector must-gathers.

[R17] Planning Analytics Local 2.1.24 download announcement

https://www.ibm.com/support/pages/ibm-planning-analytics-local-2124-now-available-download-fix-central

25 September 2026 release; aligned Workspace, Excel and Spreadsheet Services guidance.

[R18] Planning Analytics Local Technical Preview 3.1.11

https://www.ibm.com/support/pages/ibm-planning-analytics-local-technical-preview-3111-available-download-fix-central

17 September 2026; explicitly without official product support; TM1 12.6.4 and PAW 3.1.11.

# Reference catalog - continued

R19-R27  |  Official IBM sources and navigation links

[R19] Planning Analytics 2.1 fix lists

https://www.ibm.com/support/pages/node/7145856

Version-specific resolved defects; use alongside new-feature and download notices.

[R20] Planning Analytics Local lifecycle

https://www.ibm.com/support/pages/planning-analytics-local-lifecycle

Lifecycle pointer; verify current terms and extensions rather than relying on old dates.

[R21] Install Planning Analytics Workspace Local, 2.1

https://www.ibm.com/docs/en/planning-analytics/2.1.0?topic=configuration-installing-planning-analytics-workspace-local

Windows and RHEL workflows, prerequisites, administration, backup and upgrade.

[R22] Planning Analytics Workspace Distributed, 2.1

https://www.ibm.com/docs/en/planning-analytics/2.1.0?topic=configuration-planning-analytics-workspace-distributed

OpenShift-based Workspace deployment; separate from the ordinary Local runtime.

[R23] Install the Data Tier for 2.0.9.21 and later

https://www.ibm.com/docs/en/planning-analytics/2.0.0?topic=local-installing-data-tier-planning-analytics-20921-later

TM1 Server, Admin Server, tools, samples and Administration agent packaging.

[R24] New TM1 Server installer in Planning Analytics Local 2.0.9.21

https://community.ibm.com/community/user/blogs/stuart-king1/2025/02/03/new-installation-program-for-tm1-server

IBM product-manager explanation of installer migration and Windows service registration.

[R25] Planning your installation

https://www.ibm.com/docs/en/planning-analytics/2.0.0?topic=configuration-planning-your-installation

Installation choices and prerequisites; select your target release.

[R26] Install Workspace Local on Linux

https://www.ibm.com/docs/ro/SSD29G_2.0.0/com.ibm.swg.ba.cognos.tm1_inst.2.0.0.doc/t_paw_install_on_linux_sc45_and_later.html

Version-dependent RHEL and container-runtime procedure; use language selector if required.

[R27] Upgrade Planning Analytics Local 2.1

https://www.ibm.com/docs/en/planning-analytics/2.1.0?topic=configuration-upgrading-planning-analytics-local-21

Release-specific upgrade sequence. Linked from IBM download notice; browser access may be required.

# Reference catalog - continued

R28-R36  |  Official IBM sources and navigation links

[R28] Deprecated features in Planning Analytics Local 2.1

https://www.ibm.com/docs/en/planning-analytics/2.1.0?topic=21-deprecated-features-in-planning-analytics-local

Review removed capabilities, components and platforms before migration. Linked from IBM download notice; browser access may be required.

[R29] Changes to TM1 Web deployment / Spreadsheet Services FAQ

https://www.ibm.com/support/pages/node/6223948

Separate installer, service and installation-directory implications.

[R30] Install Planning Analytics Spreadsheet Services, 2.1

https://www.ibm.com/docs/en/planning-analytics/2.1.0?topic=configuration-installing-planning-analytics-spreadsheet-services-tm1-web

TM1 Web / Spreadsheet Services installation. Linked from IBM release instructions.

[R31] Planning Analytics for Microsoft Excel conformance requirements

https://www.ibm.com/support/pages/ibm-planning-analytics-microsoft-excel-conformance-requirements

Validate Excel, server and Spreadsheet Services compatibility. IBM support reference; verify selected build.

[R32] Download and upgrade the single-XLL Excel add-in

https://www.ibm.com/docs/en/paww/2.0.0?topic=icpame-downloading-upgrading-planning-analytics-microsoft-excel-single-xll-add-in-versions-2065-later

IBM-linked single-XLL installation guidance for PAfE. Linked by IBM onboarding checklist.

[R33] Planning Analytics for Microsoft Excel - installation tasks

https://www.ibm.com/docs/en/planning-analytics/2.0.0?topic=excel-installation-tasks

Entry point to single .xll add-in setup.

[R34] Install and configure the Planning Analytics Administration agent

https://www.ibm.com/docs/en/planning-analytics/2.1.0?topic=mad-install-configure-planning-analytics-administration-agent-local-only

Local agent placement and configuration. Linked from IBM download instructions.

[R35] Monitor and administer Local databases with Planning Analytics Administration

https://www.ibm.com/docs/SSD29G_2.0.0/com.ibm.swg.ba.cognos.tm1_nfg.2.0.0.doc/c_paw_nf_paa_local.html

Agent functions, logs, alerts and database administration; historical feature introduction.

[R36] TM1 REST API documentation

https://www.ibm.com/docs/SSD29G_2.0.0/com.ibm.swg.ba.cognos.tm1_rest_api.2.0.0.doc/tm1_rest_api.html

REST concepts, configuration and API navigation. IBM Docs; browser access may be required.

# Reference catalog - continued

R37-R45  |  Official IBM sources and navigation links

[R37] TM1 REST API metadata reference

https://www.ibm.com/docs/en/planning-analytics/2.0.0?topic=api-metadata

Entity types, operations and configuration properties.

[R38] TM1 REST API installation and configuration

https://www.ibm.com/docs/en/planning-analytics/2.0.0?topic=api-installation-configuration

HTTPPortNumber, TLS and service metadata validation. IBM Docs; related localized topic reviewed.

[R39] TM1 REST API - cubes and native views

https://www.ibm.com/docs/SSD29G_2.0.0/com.ibm.swg.ba.cognos.tm1_rest_api.2.0.0.doc/t_tm1_rest_api_cubes_and_native_views.html

REST model-object access and cube/view operations.

[R40] TurboIntegrator - editing procedures

https://www.ibm.com/docs/SSD29G_2.0.0/com.ibm.swg.ba.cognos.tm1_turb.2.0.0.doc/t_tm1_turbo_editing_procedures.html

Prolog, Metadata, Data and Epilog roles.

[R41] FEEDERS rules function

https://www.ibm.com/docs/en/planning-analytics/2.0.0?topic=functions-feeders

Feeder section and sparse-consolidation rules.

[R42] Planning Analytics for Excel - sandboxes

https://www.ibm.com/docs/SSD29G_2.0.0/com.ibm.swg.ba.cognos.ug_cxr.2.0.0.doc/t_cxr_cubev_sandboxes.html

Private what-if analysis and deliberate commit to base data.

[R43] Securing dimensions and hierarchies

https://www.ibm.com/docs/SSD29G_2.0.0/com.ibm.swg.ba.cognos.tm1_dg_dvlpr.2.0.0.doc/t_tm1_dev_acc_securing_dimensions.html

Hierarchy security is independent of parent-dimension security in relevant releases.

[R44] TM1 security concepts

https://www.ibm.com/docs/en/planning-analytics/2.0.0?topic=concepts-security

Clients, groups and object-level authorization.

[R45] Allow processes to modify security data

https://www.ibm.com/docs/SSD29G_2.0.0/com.ibm.swg.ba.cognos.tm1_dg_dvlpr.2.0.0.doc/c_allowingprocessestomodifysecuritydata_n608df.html

Security Access capability and administrative separation for TI processes.

# Reference catalog - continued

R46-R54  |  Official IBM sources and navigation links

[R46] Planning Analytics on Cloud - subscriptions, roles and data security

https://community.ibm.com/community/user/blogs/paul-hart-prieto/2024/02/26/planning-analytics-on-cloud

IBM explanation of subscription, Workspace and database permission layers.

[R47] Troubleshooting TM1 data encryption with TM1Crypt

https://www.ibm.com/support/pages/troubleshooting-tm1-data-encryption-tm1crypt-tool

Test encryption, backup, recovery and key handling before production.

[R48] TM1 Operations, 2.1

https://www.ibm.com/docs/en/planning-analytics/2.1.0?topic=resources-tm1-operations

Online operations manual entry point.

[R49] Mandatory Workspace backup / restore for 2.0.100 and 2.1.7

https://www.ibm.com/support/pages/important-upgrade-requirement-planning-analytics-workspace-local-20100-and-217

Concrete example of an upgrade boundary requiring content backup and restore.

[R50] Workspace containers repeatedly enter Exit state

https://www.ibm.com/support/pages/node/6982083

Diagnostic commands and symptom record; full resolution may require sign-in.

[R51] Planning Analytics on Cloud getting-started checklist

https://community.ibm.com/community/user/blogs/yin-chu/2023/05/26/paoc-getting-started-checklist

Welcome, IBMid, Excel and support onboarding; older RDP / gateway advice is historical.

[R52] Planning Analytics as a Service getting-started checklist

https://community.ibm.com/community/user/blogs/yin-chu/2024/03/18/paaas-getting-started-checklist

Provisioning, environment creation, users, API access and data-connection planning.

[R53] Working with Planning Analytics as a Service Support

https://community.ibm.com/community/user/blogs/paul-hart-prieto/2024/07/08/ibm-planning-analytics-as-a-service-support

Offering-specific support and escalation guidance.

[R54] Working with Planning Analytics on Cloud Support

https://community.ibm.com/community/user/blogs/paul-hart-prieto/2024/05/01/ibm-paoc-support

Correct support entitlement and cloud incident handling.

# Reference catalog - continued

R55-R63  |  Official IBM sources and navigation links

[R55] Add and invite a cloud user

https://www.ibm.com/docs/en/paww/2.0.0?topic=cloud-add-invite-user-only

User invitation workflow. Linked by IBM onboarding checklist.

[R56] IBM SaaS Console - getting started

https://www.ibm.com/docs/en/saas-console?topic=getting-started-saas-console

Service provisioning and console administration. Linked by IBM onboarding checklist.

[R57] Noninteractive access in Planning Analytics as a Service

https://www.ibm.com/support/pages/how-do-i-create-noninteractive-account-planning-analytics-service

Use an appropriately authorized directory user and generated API key.

[R58] Manage Planning Analytics as a Service files with APIs

https://community.ibm.com/community/user/blogs/jessica-nicholls/2025/02/03/managing-paaas-with-apis

IBM worked example for API keys and environment-specific file operations.

[R59] Planning Analytics as a Service administrative ownership guidance

https://www.ibm.com/support/pages/node/7277204

Owner and administrator handover; assign a replacement before removing ownership.

[R60] Must-gather for Planning Analytics Satellite Connector

https://www.ibm.com/support/pages/must-gather-troubleshoot-planning-analytics-satellite-connector

Connector diagnostics, configuration and support evidence; redact keys.

[R61] Satellite Connector licensing for Planning Analytics

https://community.ibm.com/community/user/businessanalytics/blogs/sami-el-cheikh1/2024/08/07/satellite-connector-licensing-for-planning-analyti

IBM product guidance on connector entitlements and architecture; confirm current contract.

[R62] ODBCIS connection reset when listing database connections

https://www.ibm.com/support/pages/unable-select-database-connection-ti-process-error-failed-get-database-connections-odbcis-connection-reset

Firewall and external-path diagnostics for SaaS database connections.

[R63] ODBCIS 504 timeout on large queries

https://www.ibm.com/support/pages/odbcis-connector-returns-504-timeout-error-large-queries-exceeding-2-minutes

Load-balancer and WAF timeouts; test through the actual external route.

# Reference catalog - continued

R64-R72  |  Official IBM sources and navigation links

[R64] ODBCIS TI process cannot send HTTP POST

https://www.ibm.com/support/pages/ti-process-error-unable-open-data-source-failed-send-http-post-request

Incomplete root / intermediate certificate-chain troubleshooting.

[R65] Planning Analytics cloud service status

https://status.planning-analytics.cloud.ibm.com

Operational status and incident notifications. Live service; status changes continuously.

[R66] Planning Analytics on Cloud maintenance

https://www.ibm.com/docs/en/planning-analytics/2.0.0?topic=analytics-maintenance

Maintenance process; confirm dates against service notifications.

[R67] IBMid Enterprise Federation introduction

https://www.ibm.com/docs/en/ief?topic=welcome-introduction

Identity federation planning and enterprise identity integration.

[R68] What is my IBM Customer Number (ICN)?

https://www.ibm.com/support/pages/what-my-ibm-customer-number-icn

Support entitlement onboarding and customer-number lookup.

[R69] New features in Planning Analytics as a Service 3.1.11

https://www.ibm.com/support/pages/whats-coming-next-ibm-planning-analytics-service-3111

16 September 2026; reporting, data sources, AI provider options and database APIs.

[R70] New features in Planning Analytics as a Service 3.1.9

https://www.ibm.com/support/pages/node/7276340

June 2026; agent, plans, API, modeling and administration updates.

[R71] Extended Forecasting Engine introduction

https://community.ibm.com/community/user/blogs/svetlana-pestsova/2026/09/30/the-future-of-planning-is-here-ibm-planning-analytics-launches-the-extended-forecasting-engine

IBM introduction to Auto ARIMA, Holt-Winters, MSTL, BATS and XGBoost options.

[R72] Richer reports, more flexible agents - September 2026

https://community.ibm.com/community/user/blogs/sami-el-cheikh1/2026/09/25/richer-reports-more-flexible-agents-whats-new-in-i

Workspace agent integration update; distinguish available features from Excel roadmap.

# Reference catalog - continued

R73-R81  |  Official IBM sources and navigation links

[R73] Version-number change for Planning Analytics on Cloud

https://community.ibm.com/community/user/blogs/stuart-king1/2025/09/16/change-to-version-numbers-in-planning-analytics-on

Dedicated cloud moved Workspace / Excel numbering to 2.1 from October 2025.

[R74] Version-number change for Planning Analytics SaaS

https://community.ibm.com/community/user/blogs/stuart-king1/2025/09/17/change-to-version-numbers-in-planning-analytics-sa

AWS / Azure SaaS moved Workspace / Excel numbering to 3.1 from October 2025.

[R75] What is new in TM1 Database 12

https://www.ibm.com/docs/en/planning-analytics/3.1.0?topic=12-whats-new-in-tm1-database

Database-engine changes; separate from front-end release numbering.

[R76] What is new in Planning Analytics Workspace, 2.1

https://www.ibm.com/docs/en/planning-analytics/2.1.0?topic=features-whats-new-in-planning-analytics-workspace

Current-line Workspace release notes. Linked from IBM download notice.

[R77] What is new in Planning Analytics for Microsoft Excel, 3.1

https://www.ibm.com/docs/en/planning-analytics/3.1.0?topic=new-whats-in-planning-analytics-microsoft-excel

Release-specific Excel features. Linked from IBM release instructions.

[R78] Planning Analytics Workspace supported languages, 2.1

https://www.ibm.com/docs/en/planning-analytics/2.1.0?topic=workspace-supported-languages

Separate user-interface and documentation language support.

[R79] Planning Analytics for Excel supported languages

https://www.ibm.com/docs/SSD29G_2.0.0/com.ibm.swg.ba.cognos.ug_cxr.2.0.0.doc/c_pax_languages.html

Excel add-in language and translated-manual matrix.

[R80] Get started with Planning Analytics Workspace

https://www.ibm.com/docs/en/planning-analytics/2.1.0?topic=workspace-get-started-planning-analytics

Online user-manual entry point for Workspace.

[R81] What is TM1?

https://www.ibm.com/think/topics/tm1

Multidimensional in-memory engine, calculations, write-back, integration and security.

# Reference catalog - continued

R82-R90  |  Official IBM sources and navigation links

[R82] Planning Analytics Workspace capabilities

https://www.ibm.com/products/planning-analytics/workspace

Books, visualization, applications, plans and model creation.

[R83] Planning Analytics for Excel capabilities

https://www.ibm.com/products/planning-analytics/excel

Governed Excel-based planning, reporting and analysis.

[R84] Planning Analytics AI and Agent capabilities

https://www.ibm.com/products/planning-analytics/ai

Model-aware assistance, forecasting, agents and MCP integration.

[R85] Planning Analytics Connector for SAP

https://www.ibm.com/docs/en/planning-analytics/2.1.0?topic=analytics-planning-connector-sap

Official SAP connector manual. Linked from product page; automated retrieval restricted.

[R86] Planning Analytics AI forecasting

https://www.ibm.com/products/planning-analytics/ai-forecasting

Baseline, on-demand forecasting, spreading and statistical details.

[R87] Planning Analytics resources, demos and case studies

https://www.ibm.com/products/planning-analytics/resources

Business demonstrations, solution brief, trials and customer examples.

[R88] Planning Analytics pricing and deployment options

https://www.ibm.com/products/planning-analytics/pricing

Offering comparison and estimator; obtain a current entitlement-specific quote.

[R89] Excel Universal Reports and EvaluationService dependencies

https://www.ibm.com/support/pages/ibm-planning-analytics-v20-planning-analytics-microsoft-excel-release-100-now-available-download-planning-analytics-administration

Documents Spreadsheet Services and EvaluationService dependencies for Universal Reports.

[R90] Deprecation notices for Planning Analytics 2.0

https://www.ibm.com/support/pages/deprecation-notices-ibm-planning-analytics-20

Historical removals including Operations Console and PMHub; avoid obsolete runbooks.
