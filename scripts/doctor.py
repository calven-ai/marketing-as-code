#!/usr/bin/env python3
"""Health check for a marketing-as-code checkout.

Run from the repo root:  python3 scripts/doctor.py

Checks that the wiring agents depend on is intact, and reports which
templates are still unfilled (fine on day one; each unfilled template is a
question an agent will have to ask). Exit code 1 only on real breakage.
"""

import subprocess
import sys
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
    "strategy/positioning.md": "Template — unfilled",
    "strategy/messaging.md": "Template — unfilled",
    "strategy/icp-personas.md": "Template — unfilled",
    "brand/voice.md": "Template — unfilled",
    "data/ontology/metrics.md": "Template — unfilled",
    "data/ontology/funnel.md": "Template — unfilled",
    "data/ontology/events.md": "Template — unfilled",
    "integrations/tasks.md": "Fallback: in-repo checklists",
}


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
        print("info: .env present (gitignored — keep it that way)")
    else:
        print("info: no .env — fine unless you use key-based integrations "
              "(copy .env.example)")

    if unfilled:
        print(f"\nunfilled templates ({len(unfilled)}) — run /setup to fill them:")
        for rel in unfilled:
            print(f"  - {rel}")

    if problems:
        print(f"\nPROBLEMS ({len(problems)}):")
        for p in problems:
            print(f"  ✗ {p}")
        sys.exit(1)
    print("\nok: wiring intact")


if __name__ == "__main__":
    main()
