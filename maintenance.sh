#!/usr/bin/env bash
set -Eeuo pipefail
# Complete release maintenance: no baseline receipt or content-hash admission.
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
export PYTHONDONTWRITEBYTECODE=1
umask 000
exec python3 "$ROOT/patches/PAA/install.py" --root "$ROOT" "$@"
