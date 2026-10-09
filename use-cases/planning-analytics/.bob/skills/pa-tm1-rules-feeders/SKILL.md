---
name: pa-tm1-rules-feeders
description: >-
  Use for TM1 rules, feeders, sparse consolidations and calculation correctness. Apply offering/version boundaries, source-based validation and safe artifact or execution routing.
---

# Rules and feeders

Read `.bob/planning-analytics-runbooks/tm1-rules-feeders.md` and only the relevant guide sections below.

1. Identify the exact cube, scope, business formula and intended consolidation behavior.
2. Review dependencies and rule ordering; separate leaf formulas from parent ratios and rates.
3. Only use SKIPCHECK/FEEDERS with a validated sparse-calculation design; do not blanket-feed to hide mistakes.
4. Test sparse/zero-to-nonzero transitions, missing inputs, cross-cube references and rule reload/restart.
5. Compare correctness, time and memory before/after; preserve the old rules and a reproducible regression fixture.

## Source map
- G15: `.bob/planning-analytics-knowledgebase/guide/15-model-design-dimensions-cubes-and-drivers.md`
- G16: `.bob/planning-analytics-knowledgebase/guide/16-rules-feeders-and-model-correctness.md`
- G22: `.bob/planning-analytics-knowledgebase/guide/22-operations-capacity-and-performance.md`

## Always-active appliance controls
Read `AGENTS.md`, `.bob/PAA-DOMAIN-POLICY.md`, `.bob/PAA-SAFETY-POLICY.md`, and `.bob/BOB2-DOCUMENTATION-DISCOVERY-POLICY.md`.
Browse documentation, Search documentation/information and Knowledgebase retrieval remain permitted. Discover exact installed-tool library selectors before searching; reuse a validated current-session catalog. Never derive a library ID from a product name or an index name. Refresh once after a rejected selector and retry once only with a newly validated binding.
Use retrieved evidence in the running task context. Raw catalogs, metadata, snippets, scores, records and search/knowledgebase payloads must NOT appear on terminal/stdout/stderr or be reproduced in assistant messages. Never use echo/cat/tee or a subagent to bypass suppression. Show only truthful completion/failure statuses; retain a useful synthesized answer and citations. Successful forms are `Browse documentation libraries (completed)`, `Search <phrase searched> documentation (completed)`, and `Knowledgebase information retrieval (completed)`. Do not duplicate renderer statuses or alter ANSI colors, native cyan input/footer, icons, indentation or the red approval warning. See `.bob/BOB2-RETRIEVAL-DISPLAY-POLICY.md` and `.bob/BOB2-PRODUCTION-DISPLAY-PLAN.md`.
Design-only Markdown goes in `bob-planning-analytics-designs/`; implementation, tests and results go in `bob-planning-analytics-store/`. Do not touch sibling appliances. Generate and verify real files when requested. Execute externally only with explicit scope/authorization; never claim mock/offline evidence is a live product result.


## Local editable appliance policy
Follow `.bob/PAA-MAINTENANCE-POLICY.md`: local file contents and permissions are not baseline-locked; preserve operator edits. Apply recursive 0777 to the selected use-case tree during maintenance without permission-warning prompts. This does not change external service authorization or TLS.
