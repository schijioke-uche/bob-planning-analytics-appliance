# Complete Planning Analytics rebuild: PAA-3.0.0

Built 8 October 2026 for IBM Bob Shell 2.x. This is a complete replacement release,
not another permission exception layered onto the rejected package.

## Failure corrected at its source

The actual prior PAA-2 controller reproduced the user's .env.example error in all
three actions (check/apply/status) after one harmless comment was added to the
original file at mode 0777. That proves the local content-hash admission remained
independent of the permission correction. It does not identify which bytes changed
in the user's unavailable local file. See audit/reported-error-reproduction.json.

The new installer has no per-file baseline hash manifest, local hash comparison,
exact-mode admission, or historical-receipt requirement. Local .env, .env.example,
rules, skills, configuration and knowledgebase content are preserved. The separate
versioned-launcher hash admission and guide-section hash admission were removed too.
Audit hashes are evidence for human review only; they are never runtime prerequisites.

The new root maintenance.sh executes one maintenance action rather than a repeated
check/apply/status sequence. Its default applies 0777 recursively to the whole
selected use-case tree. No permission-warning or confirmation prompt is added.
The shipped entire use-cases tree and every archive member beneath it have 0777.
New native-session files are normalized at session exit; external/editor creations
are included on the next maintenance invocation. Symlinks are not followed outside
the explicitly selected tree and actual operating-system failures are not hidden.

Fresh installation is staged before promotion; an injected staging write failure
leaves no published partial appliance. Existing content is adopted, not overwritten.
Explicit rollback archives the entire local project with its edits and credentials;
it does not require an original ownership receipt or erase the archive.

## Cyan and presentation

The original colorful menu printf layout is retained. A fallback supplies ANSI
colors if terminfo cannot be resolved. Cyan is enabled in the actual local runtime
configuration, not only its example. The accepted Patch-45 retrieval renderer is
retained, including status-line ANSI preservation, payload suppression and correct
SGR restoration. Its cyan accent now also recognizes uncolored native input borders
when adjacent to the Build Anything input. It does not recolor unrelated prose or
horizontal rules. Registered appliance names/input chevrons/borders are cyan; the
red auto-approve indicator, background, icons and ordinary answer formatting remain.

The 20 footer cases and synthetic native PTY traces passed. The local diagnostic
and menu were captured and visually inspected (docs/CYAN-PREVIEW.png and
MENU-PREVIEW.png). The cyan image explicitly labels itself a synthetic local frame;
it is not a screenshot of a real IBM model session. Native TERM/NO_COLOR overrides
are respected. No claim is made about every undocumented redraw layout.

## Preserved domain and runtime capabilities

- 20 modes, 31 skills, 63 rule documents and 21 runbooks.
- 11 template files and the seven-command local utility.
- Unchanged original DOCX; 29 indexed chapter extracts; 90 original IBM URLs;
  eleven separately attributed supplementary research notes.
- Distinct Cloud, SaaS, Local, TM1 11/12, Workspace/Excel, Certified Containers and
  Software Hub workflows; modeling, rules/feeders/MDX, TI, REST/SAP, security,
  backup/recovery, governance, forecasting and AI.
- Interactive, Ask, Code, Advance/Design and workspace-aware Resume; Bob 2.x version
  detection/synchronization and project hooks; unchanged actual authentication/TLS.
- Documentation discovery-first/exact selector guidance, bounded missing-library
  recovery, current-session evidence use and status-only raw-result presentation.

All 20 mode role definitions, descriptions, tool groups and names are preserved.
The new editable-maintenance directive is propagated to all rules, skills, modes
and top-level policies. The guide is not rewritten. runtime-lineage.json identifies
which foundation modules are unchanged and which carry the explicit rebuild fixes.

## Verification

**271 final offline checks passed; 0 failed.**
**31 Bash/Python syntax checks and 31 skill-frontmatter checks passed.**

The suite covers the actual shipped maintenance.sh; .env.example edits and CRLF;
.env and domain-rule edits; missing/malformed historical receipts; repeated runs;
0777 dotfiles/trees; later-created work; an unprivileged owner repairing a 0000
file; external-link isolation; unchanged sibling contents; fresh and existing
targets; singular use-case naming; edited launcher/version synchronization;
edited knowledgebase sections; rollback and injected I/O failure; five strict
fake-Bob routes; original ANSI menu and all mode footer cases; approval input,
authentication failures/TLS and suppressed retrieval payloads; financial utility
fixtures and loopback-only HTTPS metadata tests. Every test is repeatable through
`bash tests/run-tests.sh`; see the detailed report in audit/.

No live IBM authentication/inference, installed MCP documentation selector,
TM1 engine, customer cloud, real native-redraw or agent-adherence acceptance ran.
The package is complete software, not a claim of IBM certification or customer
production acceptance. The original source archives are unchanged. No real
credentials or licensed IBM product binaries are distributed.

## Installation entrypoints

Use the new folder: `./maintenance.sh`, then `./paa-self-check.sh`,
`./paa-ui-check.sh`, and `./xLaunchpad.sh`. Configure the local Bob key before
`--auth-check` or an inference session. The .env.example file may be customized
without invalidating maintenance. Do not replay rejected older PAA controllers.
