---
name: mcp-tool-guard
description: Use when the user asks to create, build, configure, diagnose, explain, or troubleshoot an MCP server or Bob MCP configuration, especially when documentation-search tools such as search_docs or show_sections are unavailable or failing.
---

# MCP Tool Guard

Follow this workflow for MCP server and Bob MCP configuration requests.

## 1. Do not start with documentation-search tools

Do not call `search_docs`, `show_sections`, or similar documentation-section helpers as the first step. They are not required for MCP work and can fail when a page parameter is unavailable.

## 2. Route to the correct local skill

Use local workspace skill instructions first:

- Use `.bob/skills/build-mcp-server/SKILL.md` when the user wants to design, scaffold, implement, register, or verify a custom MCP server.
- Use `.bob/skills/configure-mcp/SKILL.md` when the user wants to add, update, restrict, or diagnose Bob MCP configuration.

## 3. Ask targeted questions only when required

Collect only the missing facts needed to proceed:

- Local STDIO server or remote HTTP/SSE server.
- Preferred language/runtime, usually Node.js/TypeScript unless the user specifies otherwise.
- External API or service integration.
- Authentication model and whether secrets must be written to disk.
- Workspace or global Bob configuration scope.

## 4. Continue without search_docs/show_sections

If `search_docs` or `show_sections` is unavailable, missing, or returns an argument error, ignore that failure and continue using the local skill instructions and the user's requirements.

## 5. Preserve appliance policy

Keep the appliance-specific domain rules authoritative. MCP guidance supplements the appliance; it does not override QCA, TIA, SWA, WMA, or QVC design/store routing and safety policies.


<!-- BOB2-41-CONTEXT:BEGIN -->
## Bob Shell 2.x appliance integration
Read `AGENTS.md` and `.bob/BOB2-APPLIANCE-POLICY.md` together with this file. Use the current mode's `.bob/rules-<slug>/`, relevant project skills, and domain tools. Preserve the domain-specific behavior above and the appliance's design/store separation. Historical patches/backups are not active instructions. Use the versioned launcher through `xLaunchpad.sh`; do not reconstruct legacy Bob 1.x CLI commands.
<!-- BOB2-41-CONTEXT:END -->

## Planning Analytics appliance integration
Read `.bob/PAA-DOMAIN-POLICY.md` and `.bob/PAA-SAFETY-POLICY.md`. Keep this shared capability available for Planning Analytics. Use native tools only when installed; do not invent tool availability. Design Markdown: `bob-planning-analytics-designs/`; implementation: `bob-planning-analytics-store/`. Existing source procedures are guidance, not permission for external writes. Do not print retrieved payloads.

<!-- BOB2-45-DISCOVERY-DISPLAY:BEGIN -->
## Discover first; use evidence internally; preserve production presentation
Read `.bob/BOB2-DOCUMENTATION-DISCOVERY-POLICY.md`,
`.bob/BOB2-RETRIEVAL-DISPLAY-POLICY.md` and
`.bob/BOB2-PRODUCTION-DISPLAY-PLAN.md` in every mode, skill and subtask.
Browse documentation libraries, Search documentation/information, and Knowledgebase
retrieval remain PERMITTED when needed. Do not disable tools/MCP or change source
precedence, authorization, local-skill-first, artifact-routing or safety policies.
BEFORE searching, inspect the actual tool schema and discover its libraries unless
a validated catalog for that tool is already held in this running session. Use
only an exact tool-supported selector. Never derive it from a product/mode name or
assume a catalog index name is a library argument. No guessed slug conversion.
On a nonexistent-library error, invalidate that binding, refresh discovery once,
and retry once only with a newly validated selector; never repeat the rejected ID
or loop. Verify product/version relevance. Use an alternate authorized source or
report an unresolved source when no valid binding exists; never fabricate evidence.
Hold catalogs, resolved bindings and retrieval results in the running Bob task
context and use the evidence for the requested answer/design/code/verification.
Raw retrieval payload display is strictly PROHIBITED on terminal/stdout/stderr or
in assistant text: no indices, descriptions, metadata, scores, snippets, pages,
query/result dumps or knowledgebase records. Do not bypass via echo/cat/tee/logs
or another tool/subagent. Do not clear or modify evidence before the agent uses it.
After actual success show only the corresponding status:
`Browse documentation libraries (completed)`;
`Search <phrase searched> documentation (completed)`;
`Knowledgebase information retrieval (completed)`.
Use the actual concise non-secret searched phrase. Preserve original ANSI colors,
icons, indentation, input UI, warning colors and answer formatting. Do not output
literal ANSI instructions, rebuild Bob's footer, or duplicate renderer statuses.
Failures/cancellations remain truthful; give a synthesized sourced answer and keep
approvals/non-retrieval work visible. No extra raw-result cache/log is needed.
Normal Bob context/history limits apply. Mode names/slugs and tool permissions
remain those in `.bob/BOB2-MODE-MAP.json` and the current mode registry.
<!-- BOB2-45-DISCOVERY-DISPLAY:END -->


## Local editable appliance policy
Follow `.bob/PAA-MAINTENANCE-POLICY.md`: local file contents and permissions are not baseline-locked; preserve operator edits. Apply recursive 0777 to the selected use-case tree during maintenance without permission-warning prompts. This does not change external service authorization or TLS.
