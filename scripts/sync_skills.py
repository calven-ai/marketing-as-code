#!/usr/bin/env python3
"""Keep .claude/skills/ symlinks pointing at the canonical .agents/skills/
definitions; --check reports drift without fixing it (used by CI).

Canonical skill definitions live in .agents/skills/<name>/ (the Agent Skills
open standard, auto-discovered by Cursor, Codex, and others). Claude Code
still reads .claude/skills/, so this script maintains one symlink per skill
(never a symlink of the whole directory: Claude Code writes housekeeping
files into .claude/skills/ that must not land in the canonical tree). On
filesystems without symlink support (e.g. Windows without developer mode) it
copies instead.

Usage, from the repo root:
    python3 scripts/sync_skills.py            # fix links
    python3 scripts/sync_skills.py --check    # report drift, exit 1 if any (CI)

Delete this script the day Claude Code reads .agents/skills/ natively.
"""

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANONICAL = ROOT / ".agents" / "skills"
SHIM = ROOT / ".claude" / "skills"


def canonical_skills():
    if not CANONICAL.is_dir():
        sys.exit(f"error: {CANONICAL} does not exist; run from a full checkout")
    return sorted(p.name for p in CANONICAL.iterdir()
                  if p.is_dir() and (p / "SKILL.md").is_file())


def desired_target(name):
    # Relative, so the repo can live anywhere.
    return Path("..") / ".." / ".agents" / "skills" / name


def current_state(name):
    """Return 'ok', 'missing', or a description of the drift."""
    link = SHIM / name
    if not link.exists() and not link.is_symlink():
        return "missing"
    if link.is_symlink():
        if link.readlink() == desired_target(name):
            return "ok"
        return f"symlink points at {link.readlink()}"
    if (link / "SKILL.md").is_file():
        # A copy (Windows fallback). Consider it ok only if identical.
        if (link / "SKILL.md").read_bytes() == (CANONICAL / name / "SKILL.md").read_bytes():
            return "ok"
        return "copy differs from canonical"
    return "not a symlink or skill copy"


def main(argv=None):
    check = "--check" in (sys.argv[1:] if argv is None else argv)
    names = canonical_skills()
    SHIM.mkdir(parents=True, exist_ok=True)

    drift = {n: s for n in names if (s := current_state(n)) != "ok"}
    # Anything in the shim that has no canonical counterpart (skip Claude
    # Code's own housekeeping entries such as .system).
    strays = [p.name for p in SHIM.iterdir()
              if not p.name.startswith(".") and p.name not in names]

    if check:
        for name, state in drift.items():
            print(f"drift: .claude/skills/{name}: {state}")
        for name in strays:
            print(f"stray: .claude/skills/{name} has no canonical skill")
        if drift or strays:
            print("run: python3 scripts/sync_skills.py")
            sys.exit(1)
        print(f"ok: {len(names)} skills in sync")
        return

    for name in drift:
        link = SHIM / name
        if link.is_symlink() or link.is_file():
            link.unlink()
        elif link.is_dir():
            shutil.rmtree(link)
        try:
            link.symlink_to(desired_target(name))
            print(f"linked .claude/skills/{name}")
        except OSError:
            shutil.copytree(CANONICAL / name, link)
            print(f"copied .claude/skills/{name} (symlinks unavailable)")
    for name in strays:
        print(f"warning: stray .claude/skills/{name} left in place "
              "(delete it if the skill was removed)")
    if not drift:
        print(f"ok: {len(names)} skills already in sync")


if __name__ == "__main__":
    main()
