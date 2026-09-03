"""Shared helpers for the scripts in this folder. Standard library only.

Every script that needs a key or writes a snapshot uses these instead of
carrying its own copy, so a new connector (integrations/adding-an-integration.md)
copies the closest script and inherits the conventions:

    from _common import ENV_FILE, read_env_file, setting, snapshot_path

    key = setting("VENDOR_API_KEY")            # environment first, then .env
    path = snapshot_path("crm", "hubspot", "pipeline")
    # -> data/crm/snapshots/2026-09-03-hubspot-pipeline.csv

Scripts are the only code in this repo allowed to open .env, and they never
print what they find there.
"""

import os
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
    """The value of NAME: the environment wins, then the .env file, else ""."""
    if env_file is None:
        env_file = read_env_file()
    return os.environ.get(name) or env_file.get(name) or ""


def snapshot_path(domain, source, what, ext="csv", day=None):
    """data/<domain>/snapshots/YYYY-MM-DD-<source>-<what>.<ext>, folder created.

    The naming is load-bearing (data/README.md): the date prefix sorts, so
    the last file in the folder is always the freshest.
    """
    day = day or date.today().isoformat()
    folder = DATA / domain / "snapshots"
    folder.mkdir(parents=True, exist_ok=True)
    return folder / f"{day}-{source}-{what}.{ext}"
