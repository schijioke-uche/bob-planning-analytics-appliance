---
name: xlsx-insights
description: Use when the user asks for analysis, extraction, or insights from an Excel .xlsx workbook using workbook sampling, JSON dump, and a focused extraction script.
---

# Xlsx Insights

Content
XLSX Insights
Use this skill when the user asks for analysis, extraction, or insights from an Excel (.xlsx)
workbook. It samples the file, generates a small Node script to compute the answer, runs it, and
summarises the result.

Step 1 — Sample the Workbook
Call read_xlsx with just path to get the workbook's structure without flooding context:

read_xlsx({ path: "<workspace-relative-path>.xlsx" })

Read the tool result carefully:

Sheet names and total row counts per sheet (hidden sheets are included in the list — note them)
Headers and inferred column types for the active sheet
First ~50 sample rows
If detectedHeaderRow is present, the real headers may be on a different row — retry with header_row: <detectedHeaderRow> before proceeding. This is especially common when merged cells span the first few rows (e.g. a merged title band above the real column headers).
If sampleWarning is present, act on it before proceeding.
If formulaErrors is present, report the broken cells to the user before proceeding. A value of "#UNCALCULATED" means the formula was never computed (workbook was not saved after edits); all other values (e.g. "#DIV/0!", "#REF!", "#N/A") are live Excel formula errors. Ask the user whether to skip those cells, treat them as null, or fix the source workbook first.
If a column type is "string" but sample values look like numbers, the cells were formatted as Text in Excel. Your script must coerce them: Number(row[idx["Price"]]) || 0.
Step 2 — Confirm Intent
If the user's request is unambiguous given the schema, proceed directly to Step 3.

If the request is ambiguous (e.g. multiple sheets that could match, column names that are unclear,
or an aggregation that could be interpreted several ways), ask one focused question using
ask_followup_question before continuing. Do not ask multiple questions at once.

Step 3 — Dump the Workbook to JSON
Call read_xlsx with dump: true. Do not pass header_row — the dump auto-detects
the real header row independently for each sheet:

read_xlsx({ path: "<path>.xlsx", dump: true })

Read the manifest path from the tool result — it will look like:
.bob/tmp/xlsx-dumps/<stem>-<hash>/manifest.json

The manifest lists each sheet with its JSON file path, row count, and correct headers
(auto-detected per sheet, so a workbook where different sheets have headers on different rows
is handled automatically). The dump is content-addressed: calling again with the same file
reuses the existing dump without re-reading the workbook.

Step 4 — Write an Extraction Script
Use write_file to create a Node script inside the dump directory, alongside the data it reads:

.bob/tmp/xlsx-dumps/<stem>-<hash>/<slug>.mjs

Where <slug> is a short kebab-case description of what the script does (e.g.
revenue-by-region.mjs, overdue-invoices.mjs). Do not use a timestamp as the filename.

Keeping the script beside its data makes it self-contained and easy to re-run or hand off.

Critical rules for the script:

Use Node stdlib only — fs.readFileSync + JSON.parse. Do not import "exceljs" or any other npm package. The JSON dump was already produced by


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
