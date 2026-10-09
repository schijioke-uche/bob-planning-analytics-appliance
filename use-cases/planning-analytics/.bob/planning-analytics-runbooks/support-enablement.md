# Support and enablement

Source basis: user guide sections G26, G27, G28, G29. The workflow below is appliance-authored operational guidance, not verbatim IBM procedure. Resolve R references from the source guide and revalidate product/support facts.

## Workflow

1. Select offering-specific 101/support/manual resources, locale and entitlement.
2. Preserve guide R-reference qualifications and separate historical, preview and current documentation.
3. Assemble a minimal redacted incident record: impact, build matrix, time, reproduction, change history and relevant must-gather.
4. Create training routes for business users, modelers, administrators and integrators with toy models.
5. Never upload credentials, raw financial/employee data or unredacted connector configuration to forums/support.

## Evidence and exit gate
Deliver the requested result with source/version scope, validation evidence, remaining unknowns and the next authorized action. A proposed or offline-tested artifact is not a live deployment.

## Read selected sources
- G26: `.bob/planning-analytics-knowledgebase/guide/26-troubleshooting-by-failure-layer.md`
- G27: `.bob/planning-analytics-knowledgebase/guide/27-languages-community-and-support.md`
- G28: `.bob/planning-analytics-knowledgebase/guide/28-implementation-plan-and-acceptance-gates.md`
- G29: `.bob/planning-analytics-knowledgebase/guide/29-manuals-and-knowledge-base-reading-map.md`

## Always-active appliance controls
Read `AGENTS.md`, `.bob/PAA-DOMAIN-POLICY.md`, `.bob/PAA-SAFETY-POLICY.md`, and `.bob/BOB2-DOCUMENTATION-DISCOVERY-POLICY.md`.
Browse documentation, Search documentation/information and Knowledgebase retrieval remain permitted. Discover exact installed-tool library selectors before searching; reuse a validated current-session catalog. Never derive a library ID from a product name or an index name. Refresh once after a rejected selector and retry once only with a newly validated binding.
Use retrieved evidence in the running task context. Raw catalogs, metadata, snippets, scores, records and search/knowledgebase payloads must NOT appear on terminal/stdout/stderr or be reproduced in assistant messages. Never use echo/cat/tee or a subagent to bypass suppression. Show only truthful completion/failure statuses; retain a useful synthesized answer and citations. Successful forms are `Browse documentation libraries (completed)`, `Search <phrase searched> documentation (completed)`, and `Knowledgebase information retrieval (completed)`. Do not duplicate renderer statuses or alter ANSI colors, native cyan input/footer, icons, indentation or the red approval warning. See `.bob/BOB2-RETRIEVAL-DISPLAY-POLICY.md` and `.bob/BOB2-PRODUCTION-DISPLAY-PLAN.md`.
Design-only Markdown goes in `bob-planning-analytics-designs/`; implementation, tests and results go in `bob-planning-analytics-store/`. Do not touch sibling appliances. Generate and verify real files when requested. Execute externally only with explicit scope/authorization; never claim mock/offline evidence is a live product result.
