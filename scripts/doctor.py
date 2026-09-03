#!/usr/bin/env python3
"""Health check for a marketing-as-code checkout.

Run from the repo root:  python3 scripts/doctor.py

Checks that the wiring agents depend on is intact, reports which templates
are still unfilled (fine on day one; each unfilled template is a question an
agent will have to ask), and lists context files whose `last_reviewed` date
is missing or older than STALE_AFTER_DAYS (informational; the alternative to
reviewing them by hand is a context layer, see
integrations/context-layer.md). Exit code 1 only on real breakage.
"""

import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED = [
    "AGENTS.md",
    ".env.example",
    "integrations/tasks.md",
    "memory/decision-log.md",
    "data/ontology/metrics.md",
    "reports/_templates/dashboard.html",
    "reports/_templates/qmr/data-checklist.md",
]

TEMPLATES = {  # file -> marker meaning "still unfilled"
    "strategy/positioning.md": "Template: unfilled",
    "strategy/messaging.md": "Template: unfilled",
    "strategy/icp.md": "Template: unfilled",
    "strategy/personas.md": "Template: unfilled",
    "strategy/product-brief.md": "Template: unfilled",
    "brand/voice.md": "Template: unfilled",
    "brand/visual-identity.md": "Template: unfilled",
    "data/ontology/metrics.md": "Template: unfilled",
    "data/ontology/funnel.md": "Template: unfilled",
    "data/ontology/events.md": "Template: unfilled",
    "data/ontology/naming.md": "Template: unfilled",
    "integrations/tasks.md": "Fallback: in-repo checklists",
}

CONTEXT_FILES = [  # carry `source` and `last_reviewed` frontmatter
    "strategy/positioning.md",
    "strategy/messaging.md",
    "strategy/icp.md",
    "strategy/personas.md",
    "strategy/product-brief.md",
    "brand/voice.md",
    "brand/visual-identity.md",
]
STALE_AFTER_DAYS = 90


def frontmatter(text):
    """Return the YAML frontmatter as a flat dict (simple key: value lines)."""
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            out[key.strip()] = value.split("#", 1)[0].strip()
    return out


def context_freshness(unfilled):
    """Classify context files: served, stale, unreviewed. Never a problem."""
    served, stale, unreviewed = [], [], []
    today = date.today()
    for rel in CONTEXT_FILES:
        path = ROOT / rel
        if not path.is_file() or rel in unfilled:
            continue  # missing is REQUIRED's job; unfilled is reported above
        fm = frontmatter(path.read_text(encoding="utf-8"))
        if fm.get("source") == "context-layer":
            served.append(rel)
            continue
        raw = fm.get("last_reviewed", "")
        try:
            reviewed = date.fromisoformat(raw)
        except ValueError:
            unreviewed.append(rel)
            continue
        age = (today - reviewed).days
        if age > STALE_AFTER_DAYS:
            stale.append((rel, age))
    return served, stale, unreviewed


def main():
    problems = []

    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            problems.append(f"missing required file: {rel}")

    sync = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "sync_skills.py"), "--check"],
        capture_output=True, text=True)
    if sync.returncode != 0:
        problems.append("skill links out of sync:\n  "
                        + sync.stdout.strip().replace("\n", "\n  "))

    unfilled = [rel for rel, marker in TEMPLATES.items()
                if (ROOT / rel).is_file()
                and marker in (ROOT / rel).read_text(encoding="utf-8")]

    if (ROOT / ".env").is_file():
        print("info: .env present (gitignored; keep it that way)")
    else:
        print("info: no .env; fine unless you use key-based integrations "
              "(copy .env.example)")

    if unfilled:
        print(f"\nunfilled templates ({len(unfilled)}), run /setup to fill them:")
        for rel in unfilled:
            print(f"  - {rel}")

    served, stale, unreviewed = context_freshness(unfilled)
    if served:
        print(f"\ncontext served by a context layer ({len(served)}), files are fallbacks:")
        for rel in served:
            print(f"  - {rel}")
    if stale:
        print(f"\nstale context ({len(stale)}), not reviewed in "
              f"{STALE_AFTER_DAYS}+ days:")
        for rel, age in stale:
            print(f"  - {rel} ({age} days)")
    if unreviewed:
        print(f"\nunreviewed context ({len(unreviewed)}), filled but no "
              "last_reviewed date:")
        for rel in unreviewed:
            print(f"  - {rel}")
    if stale or unreviewed:
        print("  review them with the team and set last_reviewed, or connect a "
              "context layer: integrations/context-layer.md")

    if problems:
        print(f"\nPROBLEMS ({len(problems)}):")
        for p in problems:
            print(f"  ✗ {p}")
        sys.exit(1)
    print("\nok: wiring intact")


if __name__ == "__main__":
    main()
