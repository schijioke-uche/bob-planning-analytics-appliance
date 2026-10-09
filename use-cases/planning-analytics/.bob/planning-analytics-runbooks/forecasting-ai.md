# Forecasting and AI governance

Source basis: user guide sections G24, G25, G15. The workflow below is appliance-authored operational guidance, not verbatim IBM procedure. Resolve R references from the source guide and revalidate product/support facts.

## Workflow

1. Define time grain, history, exclusions, missing/zero policies, holdout periods and business use.
2. Check which forecast engine/method/provider is actually available and entitled for the selected offering/build.
3. Compare baseline and candidate on untouched holdouts using MAE/RMSE/bias and justified percentage metrics; pa-tool.py forecast-evaluate does scoring only.
4. Review anomalies, uncertainty, leakage and overrides; do not promote a forecast directly to approved targets.
5. Separate AI explanation, orchestration and material write-back with named approval, least privilege and retention controls.

## Evidence and exit gate
Deliver the requested result with source/version scope, validation evidence, remaining unknowns and the next authorized action. A proposed or offline-tested artifact is not a live deployment.

## Read selected sources
- G24: `.bob/planning-analytics-knowledgebase/guide/24-new-features-what-to-evaluate-now.md`
- G25: `.bob/planning-analytics-knowledgebase/guide/25-forecasting-and-ai-governance.md`
- G15: `.bob/planning-analytics-knowledgebase/guide/15-model-design-dimensions-cubes-and-drivers.md`

## Always-active appliance controls
Read `AGENTS.md`, `.bob/PAA-DOMAIN-POLICY.md`, `.bob/PAA-SAFETY-POLICY.md`, and `.bob/BOB2-DOCUMENTATION-DISCOVERY-POLICY.md`.
Browse documentation, Search documentation/information and Knowledgebase retrieval remain permitted. Discover exact installed-tool library selectors before searching; reuse a validated current-session catalog. Never derive a library ID from a product name or an index name. Refresh once after a rejected selector and retry once only with a newly validated binding.
Use retrieved evidence in the running task context. Raw catalogs, metadata, snippets, scores, records and search/knowledgebase payloads must NOT appear on terminal/stdout/stderr or be reproduced in assistant messages. Never use echo/cat/tee or a subagent to bypass suppression. Show only truthful completion/failure statuses; retain a useful synthesized answer and citations. Successful forms are `Browse documentation libraries (completed)`, `Search <phrase searched> documentation (completed)`, and `Knowledgebase information retrieval (completed)`. Do not duplicate renderer statuses or alter ANSI colors, native cyan input/footer, icons, indentation or the red approval warning. See `.bob/BOB2-RETRIEVAL-DISPLAY-POLICY.md` and `.bob/BOB2-PRODUCTION-DISPLAY-PLAN.md`.
Design-only Markdown goes in `bob-planning-analytics-designs/`; implementation, tests and results go in `bob-planning-analytics-store/`. Do not touch sibling appliances. Generate and verify real files when requested. Execute externally only with explicit scope/authorization; never claim mock/offline evidence is a live product result.
