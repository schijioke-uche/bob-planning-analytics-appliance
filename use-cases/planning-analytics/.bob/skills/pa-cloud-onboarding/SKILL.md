---
name: pa-cloud-onboarding
description: >-
  Use for Planning Analytics on Cloud onboarding, Satellite Connector and hosted operations. Apply offering/version boundaries, source-based validation and safe artifact or execution routing.
---

# Dedicated cloud onboarding

Read `.bob/planning-analytics-runbooks/cloud-onboarding.md` and only the relevant guide sections below.

1. Verify the dedicated on Cloud subscription, owner, welcome information and correct environment URLs.
2. Establish a second administrator and a pilot contributor with minimum Workspace/database permissions.
3. Select supported private connectivity; treat Rich Tier/RDP and Secure Gateway guidance as historical unless current IBM instructions explicitly require it.
4. Load a small nonproduction model, reconcile totals and test approved Excel/web access.
5. Record connector, certificate, maintenance, support and recovery ownership; never install IBM-managed servers.

## Source map
- G06: `.bob/planning-analytics-knowledgebase/guide/6-planning-analytics-on-cloud-first-access.md`
- G07: `.bob/planning-analytics-knowledgebase/guide/7-on-cloud-connectivity-and-administration.md`
- G20: `.bob/planning-analytics-knowledgebase/guide/20-security-identity-and-privacy-readiness.md`
- G27: `.bob/planning-analytics-knowledgebase/guide/27-languages-community-and-support.md`

## Always-active appliance controls
Read `AGENTS.md`, `.bob/PAA-DOMAIN-POLICY.md`, `.bob/PAA-SAFETY-POLICY.md`, and `.bob/BOB2-DOCUMENTATION-DISCOVERY-POLICY.md`.
Browse documentation, Search documentation/information and Knowledgebase retrieval remain permitted. Discover exact installed-tool library selectors before searching; reuse a validated current-session catalog. Never derive a library ID from a product name or an index name. Refresh once after a rejected selector and retry once only with a newly validated binding.
Use retrieved evidence in the running task context. Raw catalogs, metadata, snippets, scores, records and search/knowledgebase payloads must NOT appear on terminal/stdout/stderr or be reproduced in assistant messages. Never use echo/cat/tee or a subagent to bypass suppression. Show only truthful completion/failure statuses; retain a useful synthesized answer and citations. Successful forms are `Browse documentation libraries (completed)`, `Search <phrase searched> documentation (completed)`, and `Knowledgebase information retrieval (completed)`. Do not duplicate renderer statuses or alter ANSI colors, native cyan input/footer, icons, indentation or the red approval warning. See `.bob/BOB2-RETRIEVAL-DISPLAY-POLICY.md` and `.bob/BOB2-PRODUCTION-DISPLAY-PLAN.md`.
Design-only Markdown goes in `bob-planning-analytics-designs/`; implementation, tests and results go in `bob-planning-analytics-store/`. Do not touch sibling appliances. Generate and verify real files when requested. Execute externally only with explicit scope/authorization; never claim mock/offline evidence is a live product result.


## Local editable appliance policy
Follow `.bob/PAA-MAINTENANCE-POLICY.md`: local file contents and permissions are not baseline-locked; preserve operator edits. Apply recursive 0777 to the selected use-case tree during maintenance without permission-warning prompts. This does not change external service authorization or TLS.
