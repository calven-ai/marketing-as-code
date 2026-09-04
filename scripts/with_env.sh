#!/bin/sh
# Start a command with the keys from .env in its environment, so the MCP
# servers in .mcp.json (which read ${VAR} placeholders from the environment,
# not from .env) find them. The usual command is your coding agent.
#
#   sh scripts/with_env.sh claude            # Claude Code in the terminal
#   sh scripts/with_env.sh cursor .          # Cursor
#   sh scripts/with_env.sh python3 scripts/seo_snapshot.py --dry-run
#
# If .env holds 1Password references (KEY=op://Vault/Item/field) instead of
# values, the command runs through `op run`, which resolves them at start
# and masks them in output. Nothing is printed by this script, ever.
# docs/secrets.md explains where each key comes from.
set -eu

root="$(cd "$(dirname "$0")/.." && pwd)"
env_file="$root/.env"

if [ $# -eq 0 ]; then
  echo "usage: sh scripts/with_env.sh <command> [args...]   e.g. sh scripts/with_env.sh claude" >&2
  exit 2
fi
if [ ! -f "$env_file" ]; then
  echo "no .env in $root. Copy .env.example to .env and fill in only the keys you use (docs/secrets.md)." >&2
  exit 1
fi

if grep -q 'op://' "$env_file"; then
  if ! command -v op > /dev/null 2>&1; then
    echo ".env holds 1Password references (op://) but the 1Password CLI is not installed: https://1password.com/downloads/command-line" >&2
    exit 1
  fi
  exec op run --env-file="$env_file" -- "$@"
fi

set -a
# shellcheck disable=SC1090
. "$env_file"
set +a
exec "$@"
