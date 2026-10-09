#!/usr/bin/env bash
set -Eeuo pipefail
APP="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="$(cd -- "$APP/../.." && pwd -P)"
export PYTHONDONTWRITEBYTECODE=1
umask 000
exec python3 "$ROOT/patches/PAA/install.py" --root "$ROOT" "$@"
