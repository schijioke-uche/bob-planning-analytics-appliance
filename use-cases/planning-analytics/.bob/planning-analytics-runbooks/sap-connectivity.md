# SAP and source-system connectivity

Source basis: user guide sections G17, G19, G07, G08. The workflow below is appliance-authored operational guidance, not verbatim IBM procedure. Resolve R references from the source guide and revalidate product/support facts.

## Workflow

1. Confirm SAP/source product, OData/ODBC surface, connector entitlement, direction and data owner.
2. Do not equate the Planning Analytics Connector for SAP with arbitrary TI ODBC.
3. Map measures, currencies, calendars, business keys and delta boundaries explicitly.
4. Validate source/network/identity from the actual connector path and reconcile an isolated pilot batch.
5. Bound retries and reruns, document sensitive data and protect connector secrets.

## Evidence and exit gate
Deliver the requested result with source/version scope, validation evidence, remaining unknowns and the next authorized action. A proposed or offline-tested artifact is not a live deployment.

## Read selected sources
- G17: `.bob/planning-analytics-knowledgebase/guide/17-turbointegrator-and-data-integration.md`
- G19: `.bob/planning-analytics-knowledgebase/guide/19-rest-apis-automation-and-sap.md`
- G07: `.bob/planning-analytics-knowledgebase/guide/7-on-cloud-connectivity-and-administration.md`
- G08: `.bob/planning-analytics-knowledgebase/guide/8-planning-analytics-as-a-service-onboarding.md`

## Always-active appliance controls
Read `AGENTS.md`, `.bob/PAA-DOMAIN-POLICY.md`, `.bob/PAA-SAFETY-POLICY.md`, and `.bob/BOB2-DOCUMENTATION-DISCOVERY-POLICY.md`.
Browse documentation, Search documentation/information and Knowledgebase retrieval remain permitted. Discover exact installed-tool library selectors before searching; reuse a validated current-session catalog. Never derive a library ID from a product name or an index name. Refresh once after a rejected selector and retry once only with a newly validated binding.
Use retrieved evidence in the running task context. Raw catalogs, metadata, snippets, scores, records and search/knowledgebase payloads must NOT appear on terminal/stdout/stderr or be reproduced in assistant messages. Never use echo/cat/tee or a subagent to bypass suppression. Show only truthful completion/failure statuses; retain a useful synthesized answer and citations. Successful forms are `Browse documentation libraries (completed)`, `Search <phrase searched> documentation (completed)`, and `Knowledgebase information retrieval (completed)`. Do not duplicate renderer statuses or alter ANSI colors, native cyan input/footer, icons, indentation or the red approval warning. See `.bob/BOB2-RETRIEVAL-DISPLAY-POLICY.md` and `.bob/BOB2-PRODUCTION-DISPLAY-PLAN.md`.
Design-only Markdown goes in `bob-planning-analytics-designs/`; implementation, tests and results go in `bob-planning-analytics-store/`. Do not touch sibling appliances. Generate and verify real files when requested. Execute externally only with explicit scope/authorization; never claim mock/offline evidence is a live product result.
