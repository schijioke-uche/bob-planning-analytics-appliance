---
name: create-skill
description: Use when the user wants to create or refine a reusable Bob custom skill; validates scope, name, frontmatter, supporting files, and workspace/global placement.
---

# Create Skill

Step 0 — Decide Whether a Skill Is the Right Fit
Before gathering requirements, apply judgment — a good skill is small, focused, and reusable, and
not every request should become one. Evaluate these, and push back on the user where they don't hold:

Is a skill even the right tool? Skills are for recurring, procedural workflows that benefit from self-activation. A one-off task, or something the model already handles well unprompted, does not need a skill. If a mode (persona + tool permissions) or just a well-worded prompt fits better, say so.
Is it one focused capability? Each skill should do one thing well. If the request spans several distinct workflows, propose splitting it into smaller skills that compose, rather than one sprawling skill.
Is it the right size? A skill that balloons into hundreds of lines of branching instructions is a sign the scope is wrong. Keep the body tight and procedural; move bulky reference material into supporting files (see Step 4 notes) instead of inlining everything.
Raise these concerns with the user now — do not silently scaffold an over-scoped or unnecessary skill.

Step 1 — Gather Requirements
Use the ask_followup_question tool to understand the skill before writing anything:

What should the skill do? What task or workflow does it guide the model through?
When should it activate? What user phrasing or situation should trigger it? (This becomes the description — the single most important field.)
Scope: Global (available in every workspace) or workspace (only this project)?
Invocation: By default a skill is both a /<skill-name> command and auto-invoked by Bob whenever its description matches — this is almost always what you want, so it needs no config. The only choice worth raising: should it instead run only when the user explicitly types /<skill-name> (no auto-invocation)? That maps to the "Allow Bob to use this skill" toggle (metadata.disable-model-invocation, see Step 3).
If the answers reveal the skill is really several workflows, return to Step 0 and propose splitting
it before continuing.

Step 2 — Choose and Validate the Name
The canonical name comes from the directory that contains SKILL.md, and the directory name
must match:

^[a-z0-9]+(-[a-z0-9]+)*$        (lowercase, digits, single dashes between words)   max 64 chars

⚠️ Validation is silent. An invalid name (uppercase, underscores, spaces, leading/trailing or
doubled dashes) causes the skill to be skipped with no error. Confirm the final name with the
user before writing.

Step 3 — Draft the Frontmatter and Body
A normal skill needs only two frontmatter fields: name and description. That's it — keep it
simple.

---
name: security-review
description: Use when the user wants to review a PR for security issues — walks through auth, input validation, and secrets handling.
---

# Security Review

Follow these steps to review the pull request...

name — match the directory name. (It's technically inferred from the directory, but writing it explicitly is the convention.)
description — the trigger. This is what drives auto-activation, so write it with concrete trigger phrases ("Use when the user wants to…"), not vague intent. If omitted, the first body line is used as a fallback, but an explicit description is much better.
The body is the procedural content the model follows when the skill activates. Write it like the
create-plan skill: clear, step-numbered, and naming the actual Bob tools to use
(ask_followup_question, write_file, etc.).

Optional: advanced metadata fields
Most skills need none of these — the default (both a / command and auto-invoked by Bob) is
usually right. Add a metadata: block only to change that:

Field	Default	Notes
metadata.disable-model-invocation	false	true ⇒ Bob will not auto-invoke it; it runs only when the user types /<skill-name>. This is the "Allow Bob to use this skill" toggle in settings.
metadata.argument-hint	—	Autocomplete hint shown after /skill-name, e.g. "[issue-number]".
metadata.user-invocable	true	Advanced: false ⇒ agent-only (no / command), but Bob can still auto-invoke it. Rarely wanted for user skills; this is how built-ins like create-plan work.
Step 4 — Decide Whether Supporting Scripts Are Needed
Before writing any files, evaluate whether the skill's workflow involves steps that are better
handled by a script than by Bob reasoning through them freeform each time.

Reach for a supporting script when the skill needs to:

Fetch or transform data from an external source (APIs, databases, files)
Parse structured output into a consistent format (JSON, CSV, XML)
Run a sequence of shell commands and return a single clean result
Generate boilerplate or scaffolding from a template
Perform any logic where free-form model reasoning would produce inconsistent results
Keep it in prose instructions when:

The steps are simple, linear, and tool-call based
The output is open-ended (summaries, explanations, plans)
There is no external data to fetch or process
If a script is warranted, write it alongside SKILL.md in the same skill directory. The
SKILL.md body should then instruct Bob to run the script using execute_command and act on its
output, rather than trying to replicate the logic in natural language.

A script can be in any language the user's system supports — shell, Python, Node.js, etc. Keep it
focused: one script, one responsibility. If the skill needs multiple distinct data-gathering steps,
prefer multiple small scripts over one large one.

Example layout:

.bob/skills/my-skill/
  SKILL.md          ← procedural instructions that call the script
  fetch-data.sh     ← does the programmatic work, prints structured output

Step 5 — Write the Files
Place SKILL.md in a directory named exactly after the skill. Use the write_file tool. Write
any supporting scripts to the same directory in the same step.

Always default to the .bob folder. It's the canonical Bob location and makes onboarding
straightforward for new users:

Global:    ~/.bob/skills/<skill-name>/SKILL.md
Workspace: .bob/skills/<skill-name>/SKILL.md

Only use .agents or .claude instead if the user's workspace clearly shows they are already
working in that ecosystem (e.g. an existing .agents/ or .claude/ directory with content).
Never mention or suggest these alternatives unprompted — the goal is a smooth first-run experience,
not a folder-choice decision for someone just getting started.

If the user does use an alternative root, the precedence order is .bob > .agents > .claude, and the
same sub-path applies: <root>/skills/<skill-name>/SKILL.md.

Step 6 — Confirm
Tell the user the skill will be available in the next task — start a new conversation to use it.
If it does not appear, the most likely cause is an invalid name (Step 2); re-check the name against
the regex.

Notes for power users
First-wins deduplication by name: workspace > global > builtin. A workspace skill silently overrides a global one with the same name.
Grouped skills: a skill may live one level deeper inside a "group" folder (skills/<group>/<skill-name>/SKILL.md). The name still comes from the immediate parent directory, not the group folder. Useful for organizing many related skills.
Supporting files: any file placed alongside SKILL.md is available to the skill at activation time — scripts, static reference data, templates, etc.
Reminders
Always ask questions using the ask_followup_question tool.
Confirm the final name and scope with the user before writing.
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
## Planning Analytics skill integration
Create one lowercase-hyphenated skill directory under `.bob/skills/`, with valid name/description frontmatter and explicit trigger conditions. Add the PAA artifact paths, offering/version discipline, authorization boundary and links to the domain/safety and all three BOB2 discovery/retrieval/display policies. Browse/Search/Knowledgebase operations stay permitted; raw output remains prohibited and the cyan/native styling must not be rewritten. Add a concise README/index entry and test any executable helper against synthetic fixtures before declaring it usable. Treat a new skill as a versioned extension, not as retroactively covered by the original baseline's manifest.
<!-- PAA-EXTENSION-CONTRACT-END -->


## Local editable appliance policy
Follow `.bob/PAA-MAINTENANCE-POLICY.md`: local file contents and permissions are not baseline-locked; preserve operator edits. Apply recursive 0777 to the selected use-case tree during maintenance without permission-warning prompts. This does not change external service authorization or TLS.
