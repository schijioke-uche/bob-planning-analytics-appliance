# TurboIntegrator implementation contract

Prolog: validate parameters/source/permissions, initialize bounded context and confirm approved target slice.
Metadata: create/update only approved members and mappings; define handling of unknown elements.
Data: validate values, apply explicit replace/increment semantics and count accepted/rejected rows.
Epilog: report actual completion and reconciliation; verify exact failure semantics rather than assuming this phase always runs.

Before implementation, specify zero/missing behavior, duplicate handling, transaction/rollback constraints, logging redaction, source checkpoints and rerun idempotence. Do not execute a process or enable a chore until authorized. Source basis: Guide G17 and R40.
