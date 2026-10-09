#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
for TREE in use-cases use-case; do
  if [[ -f "$ROOT/$TREE/planning-analytics/xLaunchpad.sh" ]]; then
    exec bash "$ROOT/$TREE/planning-analytics/xLaunchpad.sh" "$@"
  fi
done
printf '%s\n' 'PAA launchpad not found. Run bash maintenance.sh first.' >&2
exit 2
