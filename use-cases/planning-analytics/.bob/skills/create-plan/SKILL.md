---
name: create-plan
description: Use when the user wants a structured implementation plan before code changes; gathers requirements, researches the codebase, writes a plan file, validates it, and guides subtask execution.
---

# Create Plan

Step 1 — Gather Requirements
Ask the user clarifying questions to fully understand the task:

What is the goal and expected outcome?
Are there constraints, preferences, or non-goals?
Which parts of the codebase are likely involved?
Any related issues or requirement documents?
Do not proceed until you have enough context to scope the work, be critical of vague intent or requirements.

Step 2 — Code Search via Sub-Agent
Spawn a spawn_subagent of type "explore" to research the codebase. The sub-agent should:

Locate relevant files, symbols, and patterns related to the task
Identify existing utilities or abstractions that should be reused
Identify existing design patterns
Surface any constraints or conventions (e.g. patterns in similar files)
Use the sub-agent's findings to ground your plan in the actual code.

Step 3 — Clarify Design Intention
Based on the requirements and code research:

Always confirm your understanding of the intended design with the user
Raise any open questions or trade-offs that need a decision
Adjust scope if the code research revealed complexity or simplifications
Do not begin writing the plan document until design intent is confirmed.

Step 4 — Write the Plan File
Write a structured plan to a markdown file (e.g. {short-plan-name}-plan.md). The plan must NOT go into low-level code detail — focus on what needs to happen and why.

The plan file must include:

Top-Level Overview
A concise summary of the goal, scope, and approach.

Sub-Tasks
Break the work into sub-tasks. Each sub-task must have:

Intent — what this sub-task achieves and why
Expected Outcomes — observable results when this sub-task is complete
Todo List — ordered, specific steps to achieve the outcome
Relevant Context — pointers to relevant files, symbols, or patterns
Status — [ ] pending (updated to [x] done after completion)
Design each sub-task to be processed independently, one at a time, so changes stay focused and reviewable.

Step 5 — Plan Validation
Before moving to implementation, ensure that the user has fully read the plan. Always ask the user targeted questions to verify the plan is correct and complete:

Does this plan capture the full scope of the task?
Are the sub-task boundaries and ordering correct?
Is any context missing that would be needed during implementation?
Use Mermaid diagrams in chat responses where they clarify architecture or workflow, but do not place Mermaid diagrams directly in the plan file. Avoid double quotes and parentheses inside square brackets in Mermaid syntax.

Refine the plan file based on the user's answers.

Step 6 — Implementation
Only after the user confirms the plan, recommend implementation by calling the switch_mode tool to agent.

When explaining how to implement the plan in agent mode:

Using the start_subtask tool, create a new task for each subtask in the <plan-file>.
In the prompt for the subtask make sure it reads the plan-file to gain the full context around the task.
After each sub task is complete update the task status in the <plan-file>
Add any context needed for the next subtask in the <plan-file>
Wait for the user to check and ok the changes before moving on to the next subtask.
Reminders
Ask questions always using the "ask_followup_question" tool
Never include information without evidence
Don't include time estimates


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
