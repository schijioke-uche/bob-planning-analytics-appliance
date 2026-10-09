# PAA-3.0.0 controls

Use `bash patch-PAA-3.sh --apply` (default), `--check`, `--status`, or explicit
`--rollback`. `--root` accepts the existing repository root; `--use-case-dir`
selects use-cases/use-case. This full release needs no earlier PAA patch.

Local bytes and existing modes are not compared to a baseline. Existing files,
including .env and .env.example, are preserved. Mode 0777 is applied recursively
to all real files/directories in the selected tree. No permission warnings or
confirmation prompts are emitted. Missing payload files are added without
replacing existing files. Archive path/type/CRC validation applies only to the
payload being extracted, not to the operator's edited project.

The new root maintenance.sh invokes this engine once and never runs earlier
installer code. An old repository's user-authored maintenance.sh is not silently
modified by copying these controls alone; use the new full package's entrypoint.
