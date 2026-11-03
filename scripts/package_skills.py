#!/usr/bin/env python3
"""Zip each product marketing skill for upload to the Claude app (Customize > Skills).

The Claude app takes one ZIP per skill, with the skill's folder as the only
top-level entry. This script writes one such ZIP per folder in
plugins/product-marketing/skills/. The release workflow (skills-release.yml)
attaches the output to each GitHub release; dist/ is never committed.

Usage, from the repo root:
    python3 scripts/package_skills.py                 # writes dist/claude-app/
    python3 scripts/package_skills.py --out some/dir  # elsewhere
"""

import argparse
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "plugins" / "product-marketing" / "skills"
# A fixed timestamp keeps the ZIPs byte-identical across runs.
STAMP = (2026, 1, 1, 0, 0, 0)


def skill_dirs(skills):
    return sorted(d for d in skills.iterdir() if (d / "SKILL.md").is_file())


def add_tree(zf, folder, prefix):
    for path in sorted(folder.rglob("*")):
        if path.is_file() and not path.name.startswith("."):
            info = zipfile.ZipInfo(f"{prefix}/{path.relative_to(folder).as_posix()}", STAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, path.read_bytes())


def package(skills, out):
    out.mkdir(parents=True, exist_ok=True)
    dirs = skill_dirs(skills)
    for d in dirs:
        with zipfile.ZipFile(out / f"{d.name}.zip", "w") as zf:
            add_tree(zf, d, d.name)
    return [d.name for d in dirs]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--skills", type=Path, default=SKILLS)
    ap.add_argument("--out", type=Path, default=ROOT / "dist" / "claude-app")
    args = ap.parse_args(argv)
    names = package(args.skills, args.out)
    if not names:
        print(f"no skills found in {args.skills}", file=sys.stderr)
        return 1
    print(f"{len(names)} skills zipped into {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
