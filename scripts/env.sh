#!/usr/bin/env bash
# Source this file; choose an absolute THREE_LC_ROOT before sourcing to reuse an installation.
three_lc_repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
export THREE_LC_ROOT="${THREE_LC_ROOT:-$three_lc_repo_dir/.local/three-lc}"
export VIRTUAL_ENV="$THREE_LC_ROOT/.venv"
export PATH="$VIRTUAL_ENV/bin:$PATH"
export TLC_DEFAULT_ROOT_DIR="$THREE_LC_ROOT/runtime"
export TLC_PROJECT_ROOT_URL="$THREE_LC_ROOT/projects"
export TLC_COMPUTE_MANAGED_PLUGINS_DIR="$THREE_LC_ROOT/managed-plugins"
export TLC_COMPUTE_HOST=127.0.0.1
export UV_CACHE_DIR="$THREE_LC_ROOT/cache/uv"
export UV_PYTHON_INSTALL_DIR="$THREE_LC_ROOT/runtime/python"
export PIP_CACHE_DIR="$THREE_LC_ROOT/cache/pip"
unset three_lc_repo_dir
