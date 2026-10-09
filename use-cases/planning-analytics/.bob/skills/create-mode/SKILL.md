---
name: create-mode
description: Use when the user wants to create or update a Bob custom mode; gathers persona, permissions, scope, slug, YAML entry, and validation requirements.
---

# Create Mode

Step 1 — Gather Requirements
Use the ask_followup_question tool before writing anything:

Purpose & persona: What is this mode for? What role/behavior should it embody? (This becomes roleDefinition — the primary differentiator. Push for a focused, specific persona, not a generic one.)
Tool access: What should it be allowed to do — read files, edit files, run commands, use the browser, use MCP servers? (This maps to groups.)
Scope: Global (available in every workspace) or workspace (only this project)?
Display details: A human-readable name for the picker, and optionally whenToUse (tooltip) and a short description.
Step 2 — Choose and Validate the Slug
The slug is the mode's unique identifier. It must match:

^[a-zA-Z0-9-]+$        (letters, digits, and dashes only — no underscores, no spaces)

⚠️ Keep slugs unique — avoid reusing one. A duplicate slug within the same file fails schema
validation and the entire file is dropped (no modes load from it). Reusing a slug that already
exists in another scope is also best avoided — one entry will silently shadow the other. Before
writing, read the target file (Step 4) and confirm the slug isn't already taken.

Step 3 — Draft the YAML Entry
Each mode is one object under the top-level customModes array. Fields:

Field	Required	Notes
slug	✅	Unique id, regex above.
name	✅	Display name shown in the mode picker.
roleDefinition	✅	Core system prompt / persona. Where most design effort goes.
whenToUse	No	Tooltip in the mode picker.
description	No	Short description.
customInstructions	No	Appended to the system prompt after roleDefinition.
groups	No	Tool permission groups (see below). List explicitly — omitting groups gives the mode none of the grouped tools (it can't read, edit, run commands, etc.), not full access.
allowedSubagents	No	Trap: if set, restricts sub-agent spawning to only the named presets. Omit unless you specifically need that restriction.
Tool permission groups
The supported group values are:

Group	Allows
read	File reading and symbol lookup
edit	File writing and modification
execute	Shell command execution
mcp	MCP server tools
skill	use_skill tool (load skill instructions)
todo	update_todo_list tool
subagent	spawn_subagent tool
mode	switch_mode tool
A group can carry a fileRegex restriction (tuple form):

groups:
  - read
  - - edit
    - fileRegex: ".*\\.md$"   # this mode may only edit markdown files

⚠️ Use only the exact group names above. Group names are free-form strings to the schema, so an
unrecognized value (e.g. command instead of execute, or write, shell, run) is
not a validation error — the file loads fine, but that line matches no tool and silently grants
nothing. The result is a mode quietly missing a capability you thought you granted, with no error
anywhere. Double-check each group against the table; the most common slip is command for shell
access, which must be execute.

⚠️ Two validations beyond the slug rule will drop the whole file if violated: duplicate group
names are rejected, and any fileRegex must compile as a valid regular expression.

Example entry:

customModes:
  - slug: docs-writer
    name: Docs Writer
    roleDefinition: >-
      You are a technical writer who produces clear, concise documentation.
      You favor examples over prose and never edit source code.
    whenToUse: Use when writing or revising documentation.
    groups:
      - read
      - - edit
        - fileRegex: ".*\\.(md|mdx)$"

⚠️ Use plain ASCII. The loader strips problematic unicode (curly quotes " " ' ', em/en
dashes, non-breaking spaces) — copy-pasting YAML from a rich editor often introduces these. Type
straight quotes and hyphens.

Step 4 — Write the File (read-then-append)
The file's top-level key is customModes (an array). Use read_file first; if the file exists,
append your new entry to the existing customModes array and write the whole thing back with
write_file. If it doesn't exist, create it with a single-entry customModes array.

Global:    ~/.bob/settings/custom_modes.yaml   (available in all workspaces)
Workspace: .bob/custom_modes.yaml              (only when this workspace is open)

⚠️ The two scopes are not symmetric. Global modes live under a settings/ sub-directory
(~/.bob/settings/custom_modes.yaml), but workspace modes do not (.bob/custom_modes.yaml,
no settings/). Writing a global mode to ~/.bob/custom_modes.yaml puts it in a directory
nothing watches, so it silently never loads. Use the exact paths above.

Never overwrite an existing file blind — you would delete the user's other modes.

Step 5 — Confirm
Tell the user the mode appears in the mode picker immediately (hot-reload, no restart). If it
doesn't appear, the file likely failed validation and was dropped — re-check the slug regex,
slug uniqueness, group names, and any fileRegex.

Reminders
Always ask questions using the ask_followup_question tool.
Read the target file and confirm slug uniqueness before writing.
Prefer workspace scope (.bob/custom_modes.yaml) unless the user wants the mode everywhere.
Never include information without evidence.


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

<!-- PAA-EXTENSION-CONTRACT-BEGIN -->
## Planning Analytics registry integration
For a new native mode, use a unique lowercase hyphenated slug and a display name `IBM Bob Planning Analytics <Role> Appliance`. Retain `ask`, `code` and `advance`. Create its `.bob/rules-<slug>/` binding and reference the PAA domain/safety, documentation-discovery and retrieval-display policies. Update `.bob/runtime/bob-v2/appliance.json` `mode_slugs`, `mode_names`, and `rule_sources` together; this keeps the doctor and cyan footer registry synchronized. Do not rewrite the inherited Python runtime or recolor the entire terminal. Validate YAML and run `paa-self-check.sh` and a selected-mode CLI check before claiming readiness.
A new user mode is an editable project change: preserve its diff and keep the runtime mode/rule mapping coherent. Do not add baseline hash admission or forge historical receipts. Do not alter sibling file contents.
<!-- PAA-EXTENSION-CONTRACT-END -->


## Local editable appliance policy
Follow `.bob/PAA-MAINTENANCE-POLICY.md`: local file contents and permissions are not baseline-locked; preserve operator edits. Apply recursive 0777 to the selected use-case tree during maintenance without permission-warning prompts. This does not change external service authorization or TLS.
