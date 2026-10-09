---
name: pa-certified-containers
description: >-
  Use for Planning Analytics container offerings, OpenShift, Software Hub and Workspace Distributed. Apply offering/version boundaries, source-based validation and safe artifact or execution routing.
---

# Certified Containers and Software Hub

Read `.bob/planning-analytics-runbooks/certified-containers.md` and only the relevant guide sections below.

1. Determine whether the requested offering is Advanced Certified Containers, Workspace Distributed, or Planning Analytics on Software Hub.
2. Locate the release-matched IBM installation page and confirm entitlement, support/runtime/storage/identity prerequisites.
3. For Software Hub only, validate control-plane/service release alignment, operator/operand project separation, cluster resources and registry/pull-secret strategy.
4. Inspect actual component/CR/CLI identifiers from supported docs; never derive them from marketing names.
5. Create a design or commands only for the selected offering; require scoped approval, backup and rollback before applying.

## Source map
- G01: `.bob/planning-analytics-knowledgebase/guide/1-product-scope-and-deployment-choices.md`
- G05: `.bob/planning-analytics-knowledgebase/guide/5-prerequisites-and-supported-environments.md`
- G11: `.bob/planning-analytics-knowledgebase/guide/11-local-install-planning-analytics-workspace.md`
- G23: `.bob/planning-analytics-knowledgebase/guide/23-upgrade-and-migration-strategy.md`

## Always-active appliance controls
Read `AGENTS.md`, `.bob/PAA-DOMAIN-POLICY.md`, `.bob/PAA-SAFETY-POLICY.md`, and `.bob/BOB2-DOCUMENTATION-DISCOVERY-POLICY.md`.
Browse documentation, Search documentation/information and Knowledgebase retrieval remain permitted. Discover exact installed-tool library selectors before searching; reuse a validated current-session catalog. Never derive a library ID from a product name or an index name. Refresh once after a rejected selector and retry once only with a newly validated binding.
Use retrieved evidence in the running task context. Raw catalogs, metadata, snippets, scores, records and search/knowledgebase payloads must NOT appear on terminal/stdout/stderr or be reproduced in assistant messages. Never use echo/cat/tee or a subagent to bypass suppression. Show only truthful completion/failure statuses; retain a useful synthesized answer and citations. Successful forms are `Browse documentation libraries (completed)`, `Search <phrase searched> documentation (completed)`, and `Knowledgebase information retrieval (completed)`. Do not duplicate renderer statuses or alter ANSI colors, native cyan input/footer, icons, indentation or the red approval warning. See `.bob/BOB2-RETRIEVAL-DISPLAY-POLICY.md` and `.bob/BOB2-PRODUCTION-DISPLAY-PLAN.md`.
Design-only Markdown goes in `bob-planning-analytics-designs/`; implementation, tests and results go in `bob-planning-analytics-store/`. Do not touch sibling appliances. Generate and verify real files when requested. Execute externally only with explicit scope/authorization; never claim mock/offline evidence is a live product result.


## Local editable appliance policy
Follow `.bob/PAA-MAINTENANCE-POLICY.md`: local file contents and permissions are not baseline-locked; preserve operator edits. Apply recursive 0777 to the selected use-case tree during maintenance without permission-warning prompts. This does not change external service authorization or TLS.
