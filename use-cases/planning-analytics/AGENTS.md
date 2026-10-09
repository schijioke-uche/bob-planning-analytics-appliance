# IBM Bob Planning Analytics Appliance (PAA)

This is the eighth domain appliance, dedicated to IBM Planning Analytics and TM1. Do not identify as Software Hub or the quantum benchmark. Runtime inheritance is Patches 41-45; domain release is PAA-3.0.0. Read `.bob/PAA-DOMAIN-POLICY.md`, `.bob/PAA-SAFETY-POLICY.md`, `.bob/BOB2-APPLIANCE-POLICY.md`, global/mode rules and relevant skills together.

## Entry points and relationships
`xLaunchpad.sh` -> managed `bob-planning-analytics-v<installed-version>.sh` -> `.bob/runtime/bob-v2/runtime.py` -> selected custom mode. `.bob/settings.json` invokes the context hook. Bob authenticates through the original benchmark-derived bob-auth.sh and tls-control.sh. Menu actions: interactive code, question ask, implementation code, advanced design advance, workspace-scoped resume. Optional specialist modes are selected in native Bob or with a local BOB2_*_MODE override.

## Knowledge and implementation
The supplied comprehensive guide is included unchanged, plus 29 indexed section extracts and its 90 original reference entries in `.bob/planning-analytics-knowledgebase/`. Consult its relevant sections for Planning Analytics work and preserve its source/version qualifications. Supplemental IBM research is separate. Use `.bob/skills/README-custom-skills.md`, `.bob/planning-analytics-runbooks/`, `.bob/planning-analytics-tools/` and `.bob/planning-analytics-templates/` for bounded workflows. No IBM product server, license, entitlement, credentials or authenticated tenant is bundled.

## Offering discipline
Resolve dedicated Cloud versus SaaS versus Local versus Certified Containers versus Software Hub. Keep TM1 11/12, Workspace, Excel, Spreadsheet Services, Local Administration agent and AI Agent distinct. Do not invent an MCP library name from this appliance name. No one-size-fits-all installation or support claim.

## Installation and changes
The new appliance belongs at `use-cases/planning-analytics/`; new patch controls belong at `patches/PAA/`. Existing seven-appliance scripts stay unchanged and do not automatically include PAA. Do not apply historical SWA patches to PAA. Preserve all sibling appliances and user data.

## Always-active appliance controls
Read `AGENTS.md`, `.bob/PAA-DOMAIN-POLICY.md`, `.bob/PAA-SAFETY-POLICY.md`, and `.bob/BOB2-DOCUMENTATION-DISCOVERY-POLICY.md`.
Browse documentation, Search documentation/information and Knowledgebase retrieval remain permitted. Discover exact installed-tool library selectors before searching; reuse a validated current-session catalog. Never derive a library ID from a product name or an index name. Refresh once after a rejected selector and retry once only with a newly validated binding.
Use retrieved evidence in the running task context. Raw catalogs, metadata, snippets, scores, records and search/knowledgebase payloads must NOT appear on terminal/stdout/stderr or be reproduced in assistant messages. Never use echo/cat/tee or a subagent to bypass suppression. Show only truthful completion/failure statuses; retain a useful synthesized answer and citations. Successful forms are `Browse documentation libraries (completed)`, `Search <phrase searched> documentation (completed)`, and `Knowledgebase information retrieval (completed)`. Do not duplicate renderer statuses or alter ANSI colors, native cyan input/footer, icons, indentation or the red approval warning. See `.bob/BOB2-RETRIEVAL-DISPLAY-POLICY.md` and `.bob/BOB2-PRODUCTION-DISPLAY-PLAN.md`.
Design-only Markdown goes in `bob-planning-analytics-designs/`; implementation, tests and results go in `bob-planning-analytics-store/`. Do not touch sibling appliances. Generate and verify real files when requested. Execute externally only with explicit scope/authorization; never claim mock/offline evidence is a live product result.


## Local editable appliance policy
Follow `.bob/PAA-MAINTENANCE-POLICY.md`: local file contents and permissions are not baseline-locked; preserve operator edits. Apply recursive 0777 to the selected use-case tree during maintenance without permission-warning prompts. This does not change external service authorization or TLS.
