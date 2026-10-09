# Local maintenance policy - PAA-3.0.0

Local appliance files are operator-editable. Never require a historical installer
receipt, a baseline SHA-256 match, or exact mode bits before maintenance, install,
status, or launch. Preserve existing `.env`, `.env.example`, configuration, rules,
skills, knowledgebase edits and generated work. Do not reset files to shipped bytes.

The selected repository `use-cases/` (or explicit `use-case/`) tree uses 0777 for
all real files and directories, including hidden entries. `maintenance.sh` applies
that policy recursively, with no permission warnings or confirmation prompts.
Do not follow symlinks to chmod outside the selected tree. Do not change ownership,
service-side access, TLS verification, or the seven siblings' file contents.
Runtime-created appliance files are normalized on session exit; maintenance covers
files created independently by editors or other applications.

The release's `audit/` inventory is for review only. It is not an installation or
runtime admission check. Missing/old patch receipts do not block execution.
Real missing executables, invalid runtime JSON, unavailable credentials, and OS
I/O errors still describe genuine failures; do not hide them or label them success.
