# Local installation

Source basis: user guide sections G05, G09, G10, G11, G12, G14. The workflow below is appliance-authored operational guidance, not verbatim IBM procedure. Resolve R references from the source guide and revalidate product/support facts.

## Workflow

1. Capture exact component versions, SPCR, host/runtime, approved media, service identities and backup state.
2. Plan data/log/backup locations outside installation media and separate native/REST/Admin Server flows.
3. Follow release-specific installers and service registration; distinguish the 2.0.9.21 installer boundary and technical-preview TM1 12 packaging.
4. Configure Workspace/Spreadsheet Services/Administration agent independently with trusted endpoints.
5. Verify ordinary-user login, REST metadata, model totals, restart recovery and a usable restore before schedules.

## Evidence and exit gate
Deliver the requested result with source/version scope, validation evidence, remaining unknowns and the next authorized action. A proposed or offline-tested artifact is not a live deployment.

## Read selected sources
- G05: `.bob/planning-analytics-knowledgebase/guide/5-prerequisites-and-supported-environments.md`
- G09: `.bob/planning-analytics-knowledgebase/guide/9-local-install-and-register-the-tm1-data-tier.md`
- G10: `.bob/planning-analytics-knowledgebase/guide/10-local-database-configuration-and-connectivity.md`
- G11: `.bob/planning-analytics-knowledgebase/guide/11-local-install-planning-analytics-workspace.md`
- G12: `.bob/planning-analytics-knowledgebase/guide/12-workspace-configuration-and-administration-agent.md`
- G14: `.bob/planning-analytics-knowledgebase/guide/14-spreadsheet-services-and-cognos-integration.md`

## Always-active appliance controls
Read `AGENTS.md`, `.bob/PAA-DOMAIN-POLICY.md`, `.bob/PAA-SAFETY-POLICY.md`, and `.bob/BOB2-DOCUMENTATION-DISCOVERY-POLICY.md`.
Browse documentation, Search documentation/information and Knowledgebase retrieval remain permitted. Discover exact installed-tool library selectors before searching; reuse a validated current-session catalog. Never derive a library ID from a product name or an index name. Refresh once after a rejected selector and retry once only with a newly validated binding.
Use retrieved evidence in the running task context. Raw catalogs, metadata, snippets, scores, records and search/knowledgebase payloads must NOT appear on terminal/stdout/stderr or be reproduced in assistant messages. Never use echo/cat/tee or a subagent to bypass suppression. Show only truthful completion/failure statuses; retain a useful synthesized answer and citations. Successful forms are `Browse documentation libraries (completed)`, `Search <phrase searched> documentation (completed)`, and `Knowledgebase information retrieval (completed)`. Do not duplicate renderer statuses or alter ANSI colors, native cyan input/footer, icons, indentation or the red approval warning. See `.bob/BOB2-RETRIEVAL-DISPLAY-POLICY.md` and `.bob/BOB2-PRODUCTION-DISPLAY-PLAN.md`.
Design-only Markdown goes in `bob-planning-analytics-designs/`; implementation, tests and results go in `bob-planning-analytics-store/`. Do not touch sibling appliances. Generate and verify real files when requested. Execute externally only with explicit scope/authorization; never claim mock/offline evidence is a live product result.
