"""Shared helpers for the scripts in this folder. Standard library only.

Every script that needs a key or writes a snapshot uses these instead of
carrying its own copy, so a new connector (integrations/adding-an-integration.md)
copies the closest script and inherits the conventions:

    from _common import ENV_FILE, frontmatter, read_env_file, setting, snapshot_path

    key = setting("VENDOR_API_KEY")            # environment first, then .env
    path = snapshot_path("crm", "hubspot", "pipeline")
    # -> data/crm/snapshots/2026-09-03-hubspot-pipeline.csv
    fm = frontmatter(text)                     # {} without a block, None if unclosed

Scripts are the only code in this repo allowed to open .env, and they never
print what they find there.
"""

import os
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT / ".env"
DATA = ROOT / "data"


def read_env_file(path=ENV_FILE):
    """Minimal KEY=value parser. Ignores comments and blank lines."""
    values = {}
    path = Path(path)
    if not path.is_file():
        return values
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        values[key.strip()] = val.strip().strip('"').strip("'")
    return values


def setting(name, env_file=None):
    """The value of NAME: the environment wins, then the .env file, else "".

    A 1Password reference (op://...) is not a value: it resolves only when the
    command runs through `op run`, which scripts/with_env.sh does for you.
    """
    if env_file is None:
        env_file = read_env_file()
    value = os.environ.get(name) or env_file.get(name) or ""
    if value.startswith("op://"):
        sys.exit(f"{name} is a 1Password reference, not a value. Start the command through "
                 "`sh scripts/with_env.sh <command>` (or `op run`) so it resolves; docs/secrets.md.")
    return value


def snapshot_path(domain, source, what, ext="csv", day=None):
    """data/<domain>/snapshots/YYYY-MM-DD-<source>-<what>.<ext>, folder created.

    The naming is load-bearing (data/README.md): the date prefix sorts, so
    the last file in the folder is always the freshest.
    """
    day = day or date.today().isoformat()
    folder = DATA / domain / "snapshots"
    folder.mkdir(parents=True, exist_ok=True)
    return folder / f"{day}-{source}-{what}.{ext}"


FRONTMATTER_RE = re.compile(r"\A\ufeff?---\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.S)


def frontmatter(text):
    """The YAML frontmatter of a Markdown file as a dict.

    Deliberately small: `key: value` lines, one level of nesting for a key
    whose value is empty and whose next lines are indented (`metadata:`),
    `[a, b]` lists as Python lists, quotes stripped, `#` comments dropped.
    Returns {} when the file has no block and None when a block opens with
    `---` but never closes, so callers can tell "no frontmatter" from
    "broken frontmatter". Tolerates CRLF and a BOM.
    """
    if not text.lstrip("\ufeff").startswith("---"):
        return {}
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    out, parent = {}, None
    for raw in m.group(1).splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indented = raw.startswith((" ", "\t"))
        line = raw.strip()
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key, value = key.strip(), value.split(" #", 1)[0].strip()
        if value.startswith("[") and value.endswith("]"):
            value = [v.strip().strip("\"'") for v in value[1:-1].split(",") if v.strip()]
        elif len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        if indented and parent is not None:
            out[parent][key] = value
        else:
            if value == "":
                out[key] = {}
                parent = key
            else:
                out[key] = value
                parent = None
    # A key with an empty value and no nested lines is just an empty string.
    for key, value in list(out.items()):
        if value == {}:
            out[key] = ""
    return out
