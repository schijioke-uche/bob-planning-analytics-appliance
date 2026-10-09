---
name: configure-mcp
description: Use when the user wants to add, configure, or diagnose a Model Context Protocol server for Bob, including local and remote MCP configurations.
---

# Configure Mcp

Configure MCP
Use this skill to add a new MCP server or diagnose an existing one. Start by asking the
user which they need using ask_followup_question, then follow the appropriate path below.

Path A — Add a New MCP Server
A1 — Local or Remote?
Ask with ask_followup_question:

Local process: Bob spawns the server as a child process. Needs command + args.
Remote server: Bob connects to a running server over HTTP. Needs url (+ optional headers).
These are mutually exclusive — set command/args or url, not both. The transport is
inferred automatically — no need to set it yourself.

A2 — Gather Connection Details
Local: the executable ("npx", "uvx", "node", or an absolute path) and its arguments (e.g. ["-y", "@my-org/my-mcp-server"]).
Remote: the full URL, plus any auth headers.
Environment: any env vars the server needs (env). See the secrets warning in A4.
A3 — Verify System Dependencies (local servers only)
Before writing the config, confirm the required runtime is installed. Use execute_command to run
the appropriate check:

command value	Check to run
npx / npm / node	node --version
uvx / uv	uvx --version
python / python3	python3 --version
docker	docker --version, then docker info (daemon running?)
podman	podman --version, then podman info (service running?)
absolute path	ls <path> to confirm the binary exists
If the runtime is missing, provide the install URL and do not write the config until the user
confirms it is available or accepts the risk:

Runtime	Install URL
Node.js	https://nodejs.org
uv / uvx	https://docs.astral.sh/uv/getting-started/installation/
Python	https://www.python.org/downloads/
Docker	https://docs.docker.com/get-started/get-docker/
Podman	https://podman.io/docs/installation
A4 — Scope and Restrictions
Scope: Global (~/.bob/settings/mcp.json, all workspaces) or workspace (.bob/mcp.json, this project only)?
Mode restrictions (groups): omit for universal availability, or restrict the server's tools to specific modes (e.g. ["plan"]).
Auto-approval (alwaysAllow): an optional list of tool names that skip the confirmation prompt. Use sparingly — prefer explicit approval for anything destructive or network-writing.
A5 — Draft the Config Entry
Each server is one named object under the top-level mcpServers key:

Field	Notes
command	Local executable, e.g. "npx". (local only)
args	Array of arguments to the command. (local only)
url	Remote server URL — mutually exclusive with command. (remote only)
headers	HTTP headers for remote servers (e.g. auth tokens).
env	Env vars injected into a local server process.
disabled	true to keep the entry but not connect.
disabledTools	Array of tool names to suppress from this server.
alwaysAllow	Array of tool names to auto-approve.
timeout	Connection timeout (ms). Snapped to one of 5000, 10000, 30000, 60000, 120000, 300000, 600000, 1800000, 3600000; invalid values default to 60000.
groups	Restrict the server's tools to specific modes.
⚠️ Secrets in env/headers are written to disk verbatim. Bob does not expand
${VAR}-style references in mcp.json — whatever you write is stored literally and in
plaintext. Prefer servers that read their own credentials from the OS environment, a keychain, or a
.env file, and put only non-secret config here. If a secret must be passed inline, make sure the
user understands it persists in the file.

Example:

{
  "mcpServers": {
    "my-server-name": {
      "command": "npx",
      "args": ["-y", "@my-org/my-mcp-server"],
      "env": { "MY_API_KEY": "..." }
    }
  }
}

A6 — Write the File (read-then-merge)
Use read_file first; if the file exists, add your server to the existing mcpServers object
and write the whole file back with write_file. If it doesn't exist, create it with a
single-server mcpServers object. Never blind-overwrite — you would delete the user's other
servers.

Global:    ~/.bob/settings/mcp.json      (available in all workspaces)
Workspace: .bob/mcp.json        (overrides global for same-named servers)

Confirm with the user before writing, especially if env or headers contains a secret.

A7 — Confirm
The server connects immediately on save (hot-reload) when Bob has a workspace folder open. If Bob
is in an empty window, open a folder first with File > Open Folder before checking the MCP panel.
If it fails to connect, move to Path B to diagnose.

Notes for power users
Server name is the deduplication key: a same-named server at workspace scope overrides global. Use this intentionally for per-project credential overrides.
Nested monorepos: a deeper .bob/mcp.json overrides a shallower one within the same workspace (depth via calculateConfigDepth()).
Path B — Diagnose an Existing MCP Server
Work through each phase in order. Stop and report findings as soon as you identify the root cause.

B1 — Read the Config
Use read_file to load the relevant mcp.json (ask the user which scope if unclear):

Workspace: .bob/mcp.json
Global:    ~/.bob/settings/mcp.json

If the file doesn't exist, report that and stop — there is nothing to diagnose.

B2 — Validate the Config Schema
For every server entry under mcpServers, check:

Transport exclusivity — command/args and url are mutually exclusive. Both set = invalid.
Transport completeness — local servers must have command; remote servers must have url.
disabled flag — if true, the server will never connect. Confirm whether that is intentional.
groups — must match known Bob permission groups: read, edit, execute, mcp, skill, todo, subagent, mode. Anything else silently grants nothing.
Duplicate server names — the same key twice in mcpServers is invalid JSON; the whole file fails to parse.
JSON validity — malformed JSON causes the entire file to be ignored (no servers load).
Report every issue found before continuing.

B3 — Check System Dependencies
For each local server (has command), run the version check using execute_command:

command value	Runtime	Check command
npx / npm / node	Node.js	node --version
uvx / uv	uv	uvx --version
python / python3	Python	python3 --version
docker	Docker	docker --version, then docker info
podman	Podman	podman --version, then podman info
absolute path	—	ls <path>
A non-zero exit or "command not found" means the runtime is missing — report it with the install URL
from the table in A3.

Also inspect the env block for each server. Flag any value that is clearly a placeholder
(e.g. "...", "<YOUR_KEY>", "TODO", empty string) — these will cause auth failures at
connect time.

B4 — Summarize and Recommend
Present findings as a clear list:

✅ Items that look correct
❌ Issues found (config errors, missing runtimes, placeholders)
⚠️ Warnings (off-spec values, unusual settings)
For each ❌, provide a concrete fix — either the corrected JSON or the install command.

If everything checks out but the server still does not connect, advise the user to:

Confirm Bob has a workspace folder open; MCP servers do not connect in an empty window.
Check Bob's MCP panel for the live error message from the server process.
Test the command manually in a terminal (e.g. npx -y @my-org/my-server) to see raw output.
Confirm required env vars are set and not expired.
Reminders
Always ask questions using the ask_followup_question tool.
Run one execute_command per dependency check — do not batch unrelated checks.
Read the target file and merge — never overwrite existing servers.
Confirm before writing secrets to disk.
Never modify mcp.json unless the user explicitly asks for a fix (Path B).
Never include information without evidence.

<!-- BEGIN IBM BOB MCP TOOL GUARD POLICY v${BOB_VERSION}.S3 -->
## MCP Tool Guard Policy

When the user asks to create, build, configure, diagnose, or explain an MCP server, do not call `search_docs`, `show_sections`, or any documentation-search helper first. Those helpers are not required for MCP server work and may fail when a page parameter is missing.

Use the local workspace skills and files instead:

1. Prefer `.bob/skills/build-mcp-server/SKILL.md` for custom MCP server design, scaffolding, implementation, registration, and verification.
2. Prefer `.bob/skills/configure-mcp/SKILL.md` for Bob MCP configuration, `.bob/mcp.json`, `~/.bob/settings/mcp.json`, local STDIO servers, remote HTTP/SSE servers, runtime checks, and diagnostics.
3. Ask only the minimum clarifying questions needed for transport, language/runtime, API/authentication needs, and workspace/global scope.
4. If documentation is needed, use local skill instructions first and ask the user for a specific external document or page before using any documentation-search tool.
5. Never fail a user-facing MCP workflow because `search_docs` or `show_sections` is unavailable or returned an argument error.

This guard applies to all appliance modes. It supplements, and does not replace, appliance-specific domain policies.
<!-- END IBM BOB MCP TOOL GUARD POLICY v${BOB_VERSION}.S3 -->


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
