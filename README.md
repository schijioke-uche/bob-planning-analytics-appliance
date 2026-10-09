# IBM Bob Planning Analytics Appliance (PAA)

**Appliance:** IBM Bob Planning Analytics Agent (PAA)  
**Author:** Dr. Jeffrey Chijioke-Uche, IBM Computer Scientist  
**Runtime:** Bob Shell 2.x  

---

## Overview

The **PAA appliance** is an IBM Bob–powered agent for IBM Planning Analytics and TM1. It provides domain-specific AI assistance for designing, modeling, integrating, and operating Planning Analytics environments across all supported deployment forms — Planning Analytics on Cloud (dedicated), Planning Analytics as a Service (SaaS/multitenant), Local (TM1 Server), Certified Containers, and IBM Software Hub on OpenShift.

### What PAA Does

- **Model** — TM1 dimensions, hierarchies, cubes, rules, feeders, MDX queries, and governed data model design → saved to `bob-planning-analytics-designs/`
- **Integrate** — TurboIntegrator (TI) processes, ODBC/REST/SAP source ingestion, chore scheduling, reconciliation → saved to `bob-planning-analytics-store/`
- **Deploy** — Local installation, Cloud/SaaS onboarding, Certified Containers, Software Hub on OpenShift, upgrade and migration
- **Operate** — Security and identity, Workspace/Excel, REST automation, performance diagnostics, backup/recovery, forecasting and AI governance

---

## Prerequisites

| Requirement | Notes |
|---|---|
| **Bob Shell 2.x CLI** | `bob` must be on your `PATH` — verify with `bob --version` |
| **Python 3.9+** | Required by `xLaunchpad.sh` and local utilities (`pa-tool.py`) |
| **Bash** | Version 4+ recommended |
| **Bob API Key** | Obtain from your IBM Bob account or team lead |
| **TM1/PA credentials (optional)** | Needed only when using the optional REST probe utility (`pa-tool.py rest-probe`) |

---

## Getting Started

### Step 1 — Clone / Open the Project

Open the `use-cases/planning-analytics/` directory in your terminal or IDE (e.g., VS Code with the IBM Bob extension).

```bash
cd use-cases/planning-analytics
```

### Step 2 — Configure Your Environment

Copy the provided example file to create your local `.env`:

```bash
cp .env.example .env
```

Then open `.env` and fill in your credentials. Minimum required values:

```bash
# Required: your IBM Bob API key
BOB_API_KEY="<your-api-key-here>"

# Bob instance classification (keep as-is unless directed otherwise)
BOB_INSTANCE_ID="IBM Internal"

# Optional: only needed for general-scope API keys (not inference-scope)
# BOB_TEAM_ID="<your-team-id>"

# Optional: TM1 service credentials for the REST probe utility only
# PA_TM1_AUTHORIZATION=   # complete Authorization header value — set via secret manager
# PA_TM1_USER=
# PA_TM1_PASSWORD=

# Optional: OpenShift / Software Hub context (container-platform mode)
# OPENSHIFT_API_URL=
# OPENSHIFT_CLUSTER_NAME=

# Optional: IBM Entitlement key for container registry pull
# IBM_ENTITLEMENT_KEY=
```

> **Security:** `.env` is listed in `.gitignore`. Never commit it. Never paste its contents into prompts, logs, or artifacts. Keep TM1/SaaS service credentials entirely separate from Bob authentication credentials.

### Step 3 — Authenticate

Run the authentication script to validate your API key against the Bob Shell 2.x backend:

```bash
bash bob-auth.sh
```

A successful run prints:

```
Bob Shell <version> Backend Authentication Validated Successfully!
```

If authentication fails, verify:
- `BOB_API_KEY` is set correctly in `.env`
- Network/TLS connectivity to `https://api.us-east.bob.ibm.com`
- If using a general-scope key, `BOB_TEAM_ID` must also be set in `.env`

---

## Launching with xLaunchpad

[`xLaunchpad.sh`](xLaunchpad.sh) is the official managed entry point for the PAA appliance. It automatically locates and delegates to the correct versioned launcher (`bob-planning-analytics-v<version>.sh`), loads the trusted project environment, and routes into the selected mode. The original ANSI color menu is presented on every interactive launch.

### Interactive Chat Session

```bash
bash xLaunchpad.sh
```

Starts an interactive Bob Shell 2.x session using the appliance default mode.

### Launch with a Specific Mode

Use `--mode` to target a PAA specialist mode directly:

```bash
bash xLaunchpad.sh --mode ask                  # Q&A, explanations, evidence review
bash xLaunchpad.sh --mode code                 # TI processes, rules, REST scripts, config files
bash xLaunchpad.sh --mode advance              # Enterprise architecture and migration design
bash xLaunchpad.sh --mode tm1-modeler          # TM1 dimensions, hierarchies, cubes, feeders, MDX
bash xLaunchpad.sh --mode ti-integration       # TI loads, ODBC/REST/SAP integration, chores
bash xLaunchpad.sh --mode cloud-saas           # Cloud / SaaS onboarding and administration
bash xLaunchpad.sh --mode local-platform       # Local TM1 install, ports, TLS, Admin Agent
bash xLaunchpad.sh --mode container-platform   # Certified Containers / Software Hub on OpenShift
bash xLaunchpad.sh --mode security-governance  # Security, identity, cell access, audit readiness
bash xLaunchpad.sh --mode operations-recovery  # Incident triage, backup/restore, upgrades, DR
bash xLaunchpad.sh --mode forecasting-ai       # Forecast engine selection, quality, AI governance
```

### One-Shot Task (Non-Interactive)

```bash
bash xLaunchpad.sh --mode tm1-modeler "Design a Revenue cube with Region and Product dimensions"
bash xLaunchpad.sh --mode ti-integration "Create a TI process to load actuals from a REST API source"
```

### Local Utility Commands (No Bob Required)

The `pa-tool.py` utility runs entirely offline:

```bash
TOOLS=.bob/planning-analytics-tools/pa-tool.py
python3 "$TOOLS" self-check
python3 "$TOOLS" scaffold finance-pilot --offering saas
python3 "$TOOLS" tm1-config-check .bob/planning-analytics-templates/tm1s.cfg.example
python3 "$TOOLS" reconcile \
  .bob/planning-analytics-templates/reconciliation-source.csv \
  .bob/planning-analytics-templates/reconciliation-target.csv \
  --keys Entity,Period --value Amount --tolerance 0.01
python3 "$TOOLS" forecast-evaluate .bob/planning-analytics-templates/forecast-evaluation.csv
```

---

## Available Modes

| Mode slug | Name | Use for |
|---|---|---|
| `ask` | IBM Bob Planning Analytics Ask Appliance | Questions, explanations, evidence review, and explicitly requested saved answers |
| `code` | IBM Bob Planning Analytics Code Appliance | TI processes, rules, REST automation, tests, and implementation from an approved design |
| `advance` | IBM Bob Planning Analytics Advance Appliance | Enterprise architecture, offering/version BOM, topology, migration, RPO/RTO, and acceptance gates |
| `plan` | IBM Bob Planning Analytics Plan Appliance | Phased implementation plans, estimates, and task breakdowns |
| `orchestrator` | IBM Bob Planning Analytics Orchestrator Appliance | Multi-stage requests spanning model, platform, integration, security, and business owners |
| `wxo-agent-architect` | IBM Bob Planning Analytics WXO Agent Architect Appliance | watsonx Orchestrate integrations, ADK/MCP agent design, and external workflow orchestration |
| `general-ask` | IBM Bob Planning Analytics General Ask Appliance | Supporting identity, REST, network, Excel, or operating-system questions |
| `general-code` | IBM Bob Planning Analytics General Code Appliance | Supporting Bash, PowerShell, Python, TypeScript, and REST adapter artifacts |
| `general-advance` | IBM Bob Planning Analytics General Advance Appliance | Architecture involving data platforms, identity, finance governance, or hybrid integrations |
| `drawio` | IBM Bob Planning Analytics Draw.io Appliance | Explicit diagram or visual architecture requests (source-to-TI-to-cube, identity, network flows) |
| `graphql-dev` | IBM Bob Planning Analytics GraphQL Development Appliance | GraphQL facade or API gateway integration over Planning Analytics REST services |
| `tm1-modeler` | IBM Bob Planning Analytics TM1 Modeler Appliance | Data-model correctness, dimensions, consolidations, sparse calculations, and model reviews |
| `ti-integration` | IBM Bob Planning Analytics TI Integration Appliance | Source ingestion, metadata updates, TI failures, reconciliation, and chore scheduling |
| `workspace-excel` | IBM Bob Planning Analytics Workspace and Excel Appliance | Workspace books/plans, PAfE reports, XLL rollout, and Spreadsheet Services |
| `cloud-saas` | IBM Bob Planning Analytics Cloud and SaaS Appliance | Managed-service identity, environment creation, connector/API, and cloud operations |
| `local-platform` | IBM Bob Planning Analytics Local Platform Appliance | Local install, supported OS/runtime, ports, TLS, and Administration Agent |
| `container-platform` | IBM Bob Planning Analytics Container Platform Appliance | OpenShift/container deployments, Certified Containers, and Software Hub installation |
| `security-governance` | IBM Bob Planning Analytics Security and Governance Appliance | Security architecture, entitlement, group/hierarchy/cell access, and audit readiness |
| `operations-recovery` | IBM Bob Planning Analytics Operations and Recovery Appliance | Incident triage, performance baselines, upgrades, backup/restore, and disaster recovery |
| `forecasting-ai` | IBM Bob Planning Analytics Forecasting and AI Appliance | Forecast engine/method selection, quality measurement, and AI agent/provider governance |

In the IBM Bob IDE extension, select the matching project custom mode from the mode selector.

---

## Deployment Offering Reference

PAA keeps the following Planning Analytics deployment targets **distinct**. Always identify the exact target before generating configuration, credentials, or installation guidance:

| Offering | Description |
|---|---|
| **Planning Analytics on Cloud (Dedicated)** | IBM-managed, single-tenant hosted service |
| **Planning Analytics as a Service (SaaS)** | Multitenant managed service; API key auth |
| **Planning Analytics Local** | Self-installed TM1 Server on supported OS |
| **Certified Containers** | Container images for OpenShift deployment |
| **IBM Software Hub (OpenShift)** | Operator-managed deployment via IBM Cloud Pak for Data / Software Hub |

---

## Project Structure

```
use-cases/planning-analytics/
├── .env.example                          # Template — copy to .env and fill in credentials
├── .env                                  # Your local credentials (git-ignored)
├── xLaunchpad.sh                         # Managed entry point — always use this to launch
├── bob-auth.sh                           # API key authentication validator
├── bob-planning-analytics-v<x.y.z>.sh   # Versioned launcher (selected automatically by xLaunchpad)
├── tls-control.sh                        # TLS/CA configuration
├── paa-self-check.sh                     # Local appliance self-check (no Bob required)
├── maintenance.sh                        # Normalize permissions on use-case tree
├── bob-planning-analytics-designs/       # Design artifacts (architecture, models, runbooks)
├── bob-planning-analytics-store/         # Implementation artifacts (TI, rules, scripts, results)
├── AGENTS.md                             # Appliance context for the Bob agent
└── .bob/
    ├── custom_modes.yaml                 # 20 project custom modes
    ├── settings.json                     # Bob IDE settings and hooks
    ├── planning-analytics-tools/         # pa-tool.py — local utilities (self-check, scaffold, probe)
    ├── planning-analytics-runbooks/      # Domain runbooks (TM1 modeling, TI, backup, migration…)
    ├── planning-analytics-templates/     # Starter templates (tm1s.cfg, TI contracts, forecast CSV…)
    ├── planning-analytics-knowledgebase/ # Comprehensive PA guide and indexed reference catalog
    ├── skills/                           # 32 PAA-focused Bob skills
    └── rules-<slug>/                     # Per-mode rules loaded automatically
```

### Artifact Routing

| What you create | Where it goes |
|---|---|
| Architecture diagrams, data model designs, migration plans, runbooks, acceptance docs | `bob-planning-analytics-designs/` |
| TI processes, TM1 rules, REST scripts, reconciliation results, test fixtures, scaffolds | `bob-planning-analytics-store/` |

---

## Available Skills

The appliance ships the following PAA-focused skills, loaded automatically when relevant:

| Skill | Purpose |
|---|---|
| `bob-planning-analytics` | Core PAA domain policy, offering distinctions, artifact routing |
| `pa-tm1-modeling` | Dimensions, hierarchies, cubes, sparse calculations, model governance |
| `pa-tm1-rules-feeders` | TM1 rules syntax, feeder correctness, consolidation logic |
| `pa-tm1-mdx` | MDX query construction and validation |
| `pa-ti-integration` | TurboIntegrator loads, ODBC/REST/SAP, chores, reconciliation |
| `pa-rest-automation` | Planning Analytics REST API automation |
| `pa-security-identity` | Identity, least privilege, group/cell access, audit |
| `pa-cloud-onboarding` | Cloud / SaaS onboarding and environment setup |
| `pa-local-install` | Local TM1 Server installation and configuration |
| `pa-migration-upgrade` | Upgrade paths, migration sequences, cutover planning |
| `pa-backup-recovery` | Backup strategy, restore validation, DR procedures |
| `pa-performance-diagnostics` | Performance baselines, diagnostics, capacity |
| `pa-forecasting-ai` | Forecast engines, quality metrics, AI governance |
| `pa-excel-spreadsheet-services` | PAfE, XLL, Spreadsheet Services, websheets |
| `pa-workspace-books-plans` | Workspace book/plan authoring and diagnostics |
| `pa-business-planning` | Business planning workflows and governance |
| `pa-sap-connectivity` | SAP HANA and BW connectivity patterns |
| `pa-saas-onboarding` | SaaS multitenant onboarding |
| `pa-certified-containers` | Certified Containers deployment guidance |
| `pa-admin-agent` | Administration Agent configuration |
| `pa-support-enablement` | Support engagement and mustgather |
| `pa-deployment-selector` | Deployment target selection guidance |
| `planning-analytics-knowledgebase` | Indexed PA guide and reference catalog |
| `create-plan` | Structured planning artifact generation |
| `create-skill` | Authoring new Bob skills |
| `create-mode` | Authoring new Bob custom modes |
| `configure-mcp` | Configuring MCP integrations |
| `build-mcp-server` | Building custom MCP servers |
| `mcp-tool-guard` | MCP tool safety guidance |
| `xlsx-insights` | Office spreadsheet analysis |
| `git-version-control` | Git workflow assistance |

---

## TLS / Enterprise CA

If your environment uses a custom enterprise certificate authority, set the path in `.env` before authenticating:

```bash
BOB_NODE_EXTRA_CA_CERTS="/path/to/your/enterprise-ca.pem"
```

TLS verification is **always enabled** in this appliance. `NODE_TLS_REJECT_UNAUTHORIZED` is explicitly cleared by `tls-control.sh` on every launch.

---

## Quick-Start Summary

```bash
# 1. Copy and configure credentials
cp .env.example .env
#    → edit .env: set BOB_API_KEY (and BOB_TEAM_ID if needed)

# 2. Authenticate
bash bob-auth.sh

# 3. Launch
bash xLaunchpad.sh
```
