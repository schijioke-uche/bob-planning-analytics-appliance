---
name: pa-saas-onboarding
description: >-
  Use for Planning Analytics as a Service on AWS/Azure, tenant environments, API keys and SaaS connectivity. Apply offering/version boundaries, source-based validation and safe artifact or execution routing.
---

# SaaS onboarding

Read `.bob/planning-analytics-runbooks/saas-onboarding.md` and only the relevant guide sections below.

1. Confirm SaaS tenant, region, quota, identity domain and TM1 generation.
2. Use the service console for environments/databases; invite appropriate directory users and assign least privilege.
3. Use the installed service API-key workflow; do not manufacture legacy noninteractive Local accounts.
4. Validate SaaS ODBC/private source connectivity from its actual execution path and run a bounded, reconciled pilot load.
5. Test administrator handover, contributor access, Excel and API lifecycle without exposing credentials.

## Source map
- G08: `.bob/planning-analytics-knowledgebase/guide/8-planning-analytics-as-a-service-onboarding.md`
- G17: `.bob/planning-analytics-knowledgebase/guide/17-turbointegrator-and-data-integration.md`
- G19: `.bob/planning-analytics-knowledgebase/guide/19-rest-apis-automation-and-sap.md`
- G20: `.bob/planning-analytics-knowledgebase/guide/20-security-identity-and-privacy-readiness.md`

## Always-active appliance controls
Read `AGENTS.md`, `.bob/PAA-DOMAIN-POLICY.md`, `.bob/PAA-SAFETY-POLICY.md`, and `.bob/BOB2-DOCUMENTATION-DISCOVERY-POLICY.md`.
Browse documentation, Search documentation/information and Knowledgebase retrieval remain permitted. Discover exact installed-tool library selectors before searching; reuse a validated current-session catalog. Never derive a library ID from a product name or an index name. Refresh once after a rejected selector and retry once only with a newly validated binding.
Use retrieved evidence in the running task context. Raw catalogs, metadata, snippets, scores, records and search/knowledgebase payloads must NOT appear on terminal/stdout/stderr or be reproduced in assistant messages. Never use echo/cat/tee or a subagent to bypass suppression. Show only truthful completion/failure statuses; retain a useful synthesized answer and citations. Successful forms are `Browse documentation libraries (completed)`, `Search <phrase searched> documentation (completed)`, and `Knowledgebase information retrieval (completed)`. Do not duplicate renderer statuses or alter ANSI colors, native cyan input/footer, icons, indentation or the red approval warning. See `.bob/BOB2-RETRIEVAL-DISPLAY-POLICY.md` and `.bob/BOB2-PRODUCTION-DISPLAY-PLAN.md`.
Design-only Markdown goes in `bob-planning-analytics-designs/`; implementation, tests and results go in `bob-planning-analytics-store/`. Do not touch sibling appliances. Generate and verify real files when requested. Execute externally only with explicit scope/authorization; never claim mock/offline evidence is a live product result.


## Local editable appliance policy
Follow `.bob/PAA-MAINTENANCE-POLICY.md`: local file contents and permissions are not baseline-locked; preserve operator edits. Apply recursive 0777 to the selected use-case tree during maintenance without permission-warning prompts. This does not change external service authorization or TLS.
