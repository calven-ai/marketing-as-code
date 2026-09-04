#!/usr/bin/env python3
"""Hand a role run the keys its MCP servers need, and nothing else: reads the run's MCP
config (the --subset output of scripts/wire_integration.py), finds every ${VAR}
placeholder in it, takes each value from the ALL_SECRETS JSON that
.github/workflows/role-run.yml passes in, masks it in the log, and appends
VAR=value to the file GITHUB_ENV names. A placeholder with no secret behind it is
reported by name so the run fails early. Never prints a value, never reads .env.

    python3 scripts/role_env.py .role-run/mcp.json
"""

import json
import os
import re
import sys

PLACEHOLDER = re.compile(r"\$\{([A-Z][A-Z0-9_]*)\}")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        sys.exit("usage: python3 scripts/role_env.py <mcp.json>")
    try:
        text = open(argv[0], encoding="utf-8").read()
        json.loads(text)
    except (OSError, json.JSONDecodeError) as err:
        sys.exit(f"{argv[0]}: {err}")
    wanted = sorted(set(PLACEHOLDER.findall(text)))
    try:
        secrets = json.loads(os.environ.get("ALL_SECRETS") or "{}")
    except json.JSONDecodeError:
        sys.exit("ALL_SECRETS is not JSON; the workflow passes toJSON(secrets)")
    env_file = os.environ.get("GITHUB_ENV")
    missing = [v for v in wanted if not secrets.get(v)]
    if missing:
        sys.exit("not set in the automation environment: " + ", ".join(missing)
                 + " (docs/secrets.md); the role cannot run unattended without them")
    if env_file:
        with open(env_file, "a", encoding="utf-8") as fh:
            for var in wanted:
                value = str(secrets[var])
                print(f"::add-mask::{value}")
                fh.write(f"{var}={value}\n")
    print("exported: " + (", ".join(wanted) or "nothing; the run needs no keys"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
