# Upgrade and migration

Source basis: user guide sections G02, G23, G21, G13. The workflow below is appliance-authored operational guidance, not verbatim IBM procedure. Resolve R references from the source guide and revalidate product/support facts.

## Workflow

1. Inventory source/target offering, TM1 generation, component builds, custom integrations and deprecated dependencies.
2. Verify every required transition, support/conformance report and matching release notes, including preview restrictions.
3. Rehearse with isolated representative models and retain rollback media, config, identities, key recovery and Workspace content.
4. Test rule totals, security, TI reruns, API, Excel/websheets, workflows and concurrent load.
5. Perform approved cutover with load freeze and reconciliation; do not retire the old environment until sign-off.

## Evidence and exit gate
Deliver the requested result with source/version scope, validation evidence, remaining unknowns and the next authorized action. A proposed or offline-tested artifact is not a live deployment.

## Read selected sources
- G02: `.bob/planning-analytics-knowledgebase/guide/2-versions-release-lines-and-evidence.md`
- G23: `.bob/planning-analytics-knowledgebase/guide/23-upgrade-and-migration-strategy.md`
- G21: `.bob/planning-analytics-knowledgebase/guide/21-backup-restore-and-disaster-recovery.md`
- G13: `.bob/planning-analytics-knowledgebase/guide/13-planning-analytics-for-microsoft-excel.md`

## Always-active appliance controls
Read `AGENTS.md`, `.bob/PAA-DOMAIN-POLICY.md`, `.bob/PAA-SAFETY-POLICY.md`, and `.bob/BOB2-DOCUMENTATION-DISCOVERY-POLICY.md`.
Browse documentation, Search documentation/information and Knowledgebase retrieval remain permitted. Discover exact installed-tool library selectors before searching; reuse a validated current-session catalog. Never derive a library ID from a product name or an index name. Refresh once after a rejected selector and retry once only with a newly validated binding.
Use retrieved evidence in the running task context. Raw catalogs, metadata, snippets, scores, records and search/knowledgebase payloads must NOT appear on terminal/stdout/stderr or be reproduced in assistant messages. Never use echo/cat/tee or a subagent to bypass suppression. Show only truthful completion/failure statuses; retain a useful synthesized answer and citations. Successful forms are `Browse documentation libraries (completed)`, `Search <phrase searched> documentation (completed)`, and `Knowledgebase information retrieval (completed)`. Do not duplicate renderer statuses or alter ANSI colors, native cyan input/footer, icons, indentation or the red approval warning. See `.bob/BOB2-RETRIEVAL-DISPLAY-POLICY.md` and `.bob/BOB2-PRODUCTION-DISPLAY-PLAN.md`.
Design-only Markdown goes in `bob-planning-analytics-designs/`; implementation, tests and results go in `bob-planning-analytics-store/`. Do not touch sibling appliances. Generate and verify real files when requested. Execute externally only with explicit scope/authorization; never claim mock/offline evidence is a live product result.
