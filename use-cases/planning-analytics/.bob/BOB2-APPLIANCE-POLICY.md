# IBM Bob Planning Analytics Appliance - runtime integration

PAA-3.0.0 is derived from the verified Software Hub appliance after Patches 41-45. The original BOB2-45 runtime, production filter and cyan/ANSI module are reused byte-for-byte, along with benchmark-derived authentication and TLS. This is a new appliance identity, not SWA with renamed deployment instructions.

`xLaunchpad.sh` loads trusted `.env` once and chooses the versioned Planning Analytics launcher; runtime.py validates Bob 2.x capabilities and mode bindings. Settings hooks, AGENTS.md, the PAA policies, mode rules, relevant skills and planning-analytics-tools provide context. Code routes remain `bob chat --mode` and `bob run --mode --workspace ... --trust --accept-license <prompt>` with a positional request and boolean accept-license. No obsolete top-level chat-mode flags.

Native chat/resume retain the PTY and Patch-45 styling. One-shot output uses the inherited structured renderer, not a complete recreation of native pretty output. Authentication performs the real isolated benchmark probe, which may incur a small backend request; preview and doctor do not run inference. Auto-approval defaults match the benchmark, but is not permission for destructive work and is not a sandbox. Set BOB2_CHAT_AUTO_APPROVE=0 for interactive approvals.

Patch controls live at repository `patches/PAA/`; the appliance lives at `use-cases/planning-analytics/`. Runtime provenance is `.bob/PAA-UPSTREAM-LINEAGE.json`; this release does not forge SWA's patch receipts/backups or allow old SWA patch scripts to run against PAA. Historical seven-appliance --all controllers remain seven-appliance controllers.

Read `.bob/PAA-DOMAIN-POLICY.md` and `.bob/PAA-SAFETY-POLICY.md` before implementation. The supplied guide supplements project intelligence; it does not replace current IBM compatibility/entitlement authority.

## Always-active appliance controls
Read `AGENTS.md`, `.bob/PAA-DOMAIN-POLICY.md`, `.bob/PAA-SAFETY-POLICY.md`, and `.bob/BOB2-DOCUMENTATION-DISCOVERY-POLICY.md`.
Browse documentation, Search documentation/information and Knowledgebase retrieval remain permitted. Discover exact installed-tool library selectors before searching; reuse a validated current-session catalog. Never derive a library ID from a product name or an index name. Refresh once after a rejected selector and retry once only with a newly validated binding.
Use retrieved evidence in the running task context. Raw catalogs, metadata, snippets, scores, records and search/knowledgebase payloads must NOT appear on terminal/stdout/stderr or be reproduced in assistant messages. Never use echo/cat/tee or a subagent to bypass suppression. Show only truthful completion/failure statuses; retain a useful synthesized answer and citations. Successful forms are `Browse documentation libraries (completed)`, `Search <phrase searched> documentation (completed)`, and `Knowledgebase information retrieval (completed)`. Do not duplicate renderer statuses or alter ANSI colors, native cyan input/footer, icons, indentation or the red approval warning. See `.bob/BOB2-RETRIEVAL-DISPLAY-POLICY.md` and `.bob/BOB2-PRODUCTION-DISPLAY-PLAN.md`.
Design-only Markdown goes in `bob-planning-analytics-designs/`; implementation, tests and results go in `bob-planning-analytics-store/`. Do not touch sibling appliances. Generate and verify real files when requested. Execute externally only with explicit scope/authorization; never claim mock/offline evidence is a live product result.


## Local editable appliance policy
Follow `.bob/PAA-MAINTENANCE-POLICY.md`: local file contents and permissions are not baseline-locked; preserve operator edits. Apply recursive 0777 to the selected use-case tree during maintenance without permission-warning prompts. This does not change external service authorization or TLS.
