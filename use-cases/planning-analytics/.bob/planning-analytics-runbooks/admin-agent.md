# Local Administration agent

Source basis: user guide sections G03, G12, G22. The workflow below is appliance-authored operational guidance, not verbatim IBM procedure. Resolve R references from the source guide and revalidate product/support facts.

## Workflow

1. Distinguish Local Administration agent from AI Agent and from this PAA project abbreviation.
2. Locate the required agent on each relevant TM1 host and verify build compatibility.
3. Check management endpoints, credentials/API-key configuration where applicable, TLS and firewall reachability.
4. Test status/log/alert visibility and an approved nonproduction management action.
5. Record ownership and upgrade/restart procedure; browser login alone is not agent-readiness evidence.

## Evidence and exit gate
Deliver the requested result with source/version scope, validation evidence, remaining unknowns and the next authorized action. A proposed or offline-tested artifact is not a live deployment.

## Read selected sources
- G03: `.bob/planning-analytics-knowledgebase/guide/3-architecture-and-component-responsibilities.md`
- G12: `.bob/planning-analytics-knowledgebase/guide/12-workspace-configuration-and-administration-agent.md`
- G22: `.bob/planning-analytics-knowledgebase/guide/22-operations-capacity-and-performance.md`

## Always-active appliance controls
Read `AGENTS.md`, `.bob/PAA-DOMAIN-POLICY.md`, `.bob/PAA-SAFETY-POLICY.md`, and `.bob/BOB2-DOCUMENTATION-DISCOVERY-POLICY.md`.
Browse documentation, Search documentation/information and Knowledgebase retrieval remain permitted. Discover exact installed-tool library selectors before searching; reuse a validated current-session catalog. Never derive a library ID from a product name or an index name. Refresh once after a rejected selector and retry once only with a newly validated binding.
Use retrieved evidence in the running task context. Raw catalogs, metadata, snippets, scores, records and search/knowledgebase payloads must NOT appear on terminal/stdout/stderr or be reproduced in assistant messages. Never use echo/cat/tee or a subagent to bypass suppression. Show only truthful completion/failure statuses; retain a useful synthesized answer and citations. Successful forms are `Browse documentation libraries (completed)`, `Search <phrase searched> documentation (completed)`, and `Knowledgebase information retrieval (completed)`. Do not duplicate renderer statuses or alter ANSI colors, native cyan input/footer, icons, indentation or the red approval warning. See `.bob/BOB2-RETRIEVAL-DISPLAY-POLICY.md` and `.bob/BOB2-PRODUCTION-DISPLAY-PLAN.md`.
Design-only Markdown goes in `bob-planning-analytics-designs/`; implementation, tests and results go in `bob-planning-analytics-store/`. Do not touch sibling appliances. Generate and verify real files when requested. Execute externally only with explicit scope/authorization; never claim mock/offline evidence is a live product result.
