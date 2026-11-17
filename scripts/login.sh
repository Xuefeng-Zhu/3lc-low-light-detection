#!/usr/bin/env bash
set -euo pipefail
source "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/env.sh"
umask 077
mkdir -p "$TLC_DEFAULT_ROOT_DIR"
chmod 700 "$TLC_DEFAULT_ROOT_DIR"
echo 'Copy your 3LC API key from https://account.3lc.ai/api-key.'
echo 'Paste it only into the official CLI hidden prompt; do not put it in shell history.'
exec 3lc login
