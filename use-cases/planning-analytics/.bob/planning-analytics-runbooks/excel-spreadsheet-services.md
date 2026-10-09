# Excel and Spreadsheet Services

Source basis: user guide sections G13, G14, G18, G26. The workflow below is appliance-authored operational guidance, not verbatim IBM procedure. Resolve R references from the source guide and revalidate product/support facts.

## Workflow

1. Inventory Office channel/version/bitness, XLL, Workspace, TM1 and Spreadsheet Services builds.
2. Verify exact conformance and the installation instructions; use managed signing/trust, not globally weakened Office security.
3. Check EvaluationService where Universal Reports/TM1SET or distributed topology requires it.
4. Test read, refresh, authorized write-back, reopen/reconnect and use by a second entitled user.
5. Isolate workbook/report/service/model failures; preserve workbooks and PAfE rollback media.

## Evidence and exit gate
Deliver the requested result with source/version scope, validation evidence, remaining unknowns and the next authorized action. A proposed or offline-tested artifact is not a live deployment.

## Read selected sources
- G13: `.bob/planning-analytics-knowledgebase/guide/13-planning-analytics-for-microsoft-excel.md`
- G14: `.bob/planning-analytics-knowledgebase/guide/14-spreadsheet-services-and-cognos-integration.md`
- G18: `.bob/planning-analytics-knowledgebase/guide/18-books-plans-scenarios-and-excel-reporting.md`
- G26: `.bob/planning-analytics-knowledgebase/guide/26-troubleshooting-by-failure-layer.md`

## Always-active appliance controls
Read `AGENTS.md`, `.bob/PAA-DOMAIN-POLICY.md`, `.bob/PAA-SAFETY-POLICY.md`, and `.bob/BOB2-DOCUMENTATION-DISCOVERY-POLICY.md`.
Browse documentation, Search documentation/information and Knowledgebase retrieval remain permitted. Discover exact installed-tool library selectors before searching; reuse a validated current-session catalog. Never derive a library ID from a product name or an index name. Refresh once after a rejected selector and retry once only with a newly validated binding.
Use retrieved evidence in the running task context. Raw catalogs, metadata, snippets, scores, records and search/knowledgebase payloads must NOT appear on terminal/stdout/stderr or be reproduced in assistant messages. Never use echo/cat/tee or a subagent to bypass suppression. Show only truthful completion/failure statuses; retain a useful synthesized answer and citations. Successful forms are `Browse documentation libraries (completed)`, `Search <phrase searched> documentation (completed)`, and `Knowledgebase information retrieval (completed)`. Do not duplicate renderer statuses or alter ANSI colors, native cyan input/footer, icons, indentation or the red approval warning. See `.bob/BOB2-RETRIEVAL-DISPLAY-POLICY.md` and `.bob/BOB2-PRODUCTION-DISPLAY-PLAN.md`.
Design-only Markdown goes in `bob-planning-analytics-designs/`; implementation, tests and results go in `bob-planning-analytics-store/`. Do not touch sibling appliances. Generate and verify real files when requested. Execute externally only with explicit scope/authorization; never claim mock/offline evidence is a live product result.
