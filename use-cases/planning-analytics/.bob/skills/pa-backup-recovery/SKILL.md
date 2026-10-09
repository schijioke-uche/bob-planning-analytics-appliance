---
name: pa-backup-recovery
description: >-
  Use for TM1/Workspace backups, encrypted recovery, restore tests and disaster recovery. Apply offering/version boundaries, source-based validation and safe artifact or execution routing.
---

# Backup and recovery

Read `.bob/planning-analytics-runbooks/backup-recovery.md` and only the relevant guide sections below.

1. Define RPO/RTO, scope/owner and the actual offering-specific backup contract.
2. Protect TM1 data/metadata/security, Workspace content, Spreadsheet Services config, integrations, identities and required keys.
3. Use an application-consistent supported backup method; do not treat arbitrary hot-file copying as a complete backup.
4. Restore to an isolated compatible target and reconcile totals, permissions, books, Excel, TI and schedules.
5. Measure recovery and record gaps; preserve pre-upgrade recovery sets and never claim backup success proves restore success.

## Source map
- G21: `.bob/planning-analytics-knowledgebase/guide/21-backup-restore-and-disaster-recovery.md`
- G20: `.bob/planning-analytics-knowledgebase/guide/20-security-identity-and-privacy-readiness.md`
- G23: `.bob/planning-analytics-knowledgebase/guide/23-upgrade-and-migration-strategy.md`

## Always-active appliance controls
Read `AGENTS.md`, `.bob/PAA-DOMAIN-POLICY.md`, `.bob/PAA-SAFETY-POLICY.md`, and `.bob/BOB2-DOCUMENTATION-DISCOVERY-POLICY.md`.
Browse documentation, Search documentation/information and Knowledgebase retrieval remain permitted. Discover exact installed-tool library selectors before searching; reuse a validated current-session catalog. Never derive a library ID from a product name or an index name. Refresh once after a rejected selector and retry once only with a newly validated binding.
Use retrieved evidence in the running task context. Raw catalogs, metadata, snippets, scores, records and search/knowledgebase payloads must NOT appear on terminal/stdout/stderr or be reproduced in assistant messages. Never use echo/cat/tee or a subagent to bypass suppression. Show only truthful completion/failure statuses; retain a useful synthesized answer and citations. Successful forms are `Browse documentation libraries (completed)`, `Search <phrase searched> documentation (completed)`, and `Knowledgebase information retrieval (completed)`. Do not duplicate renderer statuses or alter ANSI colors, native cyan input/footer, icons, indentation or the red approval warning. See `.bob/BOB2-RETRIEVAL-DISPLAY-POLICY.md` and `.bob/BOB2-PRODUCTION-DISPLAY-PLAN.md`.
Design-only Markdown goes in `bob-planning-analytics-designs/`; implementation, tests and results go in `bob-planning-analytics-store/`. Do not touch sibling appliances. Generate and verify real files when requested. Execute externally only with explicit scope/authorization; never claim mock/offline evidence is a live product result.


## Local editable appliance policy
Follow `.bob/PAA-MAINTENANCE-POLICY.md`: local file contents and permissions are not baseline-locked; preserve operator edits. Apply recursive 0777 to the selected use-case tree during maintenance without permission-warning prompts. This does not change external service authorization or TLS.
