#!/usr/bin/env bash
set -euo pipefail
source "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/env.sh"
case "${1:-}" in
  object) exec 3lc service --host 127.0.0.1 --port 5015 --no-tui ;;
  compute) exec 3lc-compute --host 127.0.0.1 --port 5020 ;;
  *) echo "Usage: bash $0 object|compute (one terminal per service)"; exit 2 ;;
esac
