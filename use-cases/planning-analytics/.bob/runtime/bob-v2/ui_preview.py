#!/usr/bin/env python3
"""Local ANSI rendering diagnostic; no Bob/MCP/backend request. Not a live session."""
from __future__ import annotations
import json
import os
from pathlib import Path
import sys
from terminal_style import NativeCyanAccent, SgrState, accent_enabled
from production_display import RetrievalTextFilter
HERE = Path(__file__).resolve().parent
config = json.loads((HERE/'appliance.json').read_text())
enabled = accent_enabled(os.environ, sys.stdout.isatty())
print('PAA local presentation diagnostic (synthetic frame; no backend).')
if not enabled:
    print('Run in a color-capable terminal to display the ANSI preview.')
    sys.exit(0)
frame = ('\x1b[35m'+'\u2500'*84+'\x1b[39m\n'
         ' \x1b[35m\u276f\x1b[39m \u2588 Build Anything, @ for context, / for commands, $ for skills\n'
         '\x1b[35m'+'\u2500'*84+'\x1b[39m\n'
         ' \x1b[90m'+config['mode_names']['code']+' Mode \x1b[31m(auto-approve)\x1b[39m\n')
accent = NativeCyanAccent(config, True)
state = SgrState()
for line in frame.splitlines(keepends=True):
    sys.stdout.write(accent.apply(line, state))
    state.apply(line)
sys.stdout.write(accent.flush())
# Show exactly the three required statuses; the filter sees but hides demo bodies.
lines = ('\x1b[36mBrowse documentation libraries\x1b[90m (completed)\x1b[0m\n'
         '{"indices": [{"name": "synthetic_catalog", "description": "HIDDEN_DEMO_BODY"}]}\n'
         '\x1b[36mSearch Planning Analytics documentation\x1b[90m (completed)\x1b[0m\n'
         '{"results": [{"content": "HIDDEN_DEMO_BODY"}]}\n'
         '\x1b[36mKnowledgebase information retrieval\x1b[90m (completed)\x1b[0m\n'
         '{"documents": [{"content": "HIDDEN_DEMO_BODY"}]}\n')
filter_ = RetrievalTextFilter()
sys.stdout.write(filter_.feed(lines))
sys.stdout.write(filter_.finish())
sys.stdout.write('\x1b[0m')
