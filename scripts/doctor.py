#!/usr/bin/env python3
"""Health check for a marketing-as-code checkout: runs every check in
scripts/lint.py against docs/schema.json, then reports unfilled templates,
context files past their review date, and whether an .env exists. --fix
applies the safe fixes first; --strict fails on warnings too (CI on main);
--brief prints three lines for the session-start hook; --github checks the
repository settings through gh. Exit 1 only on real breakage.

Run from the repo root:  python3 scripts/doctor.py

When it is red, fix what it names or ask your agent for /doctor. The
findings are the same ones CI posts on every proposal (check.yml), so a
green doctor here means a green check there.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lint  # noqa: E402

ROOT = lint.ROOT


def github_settings():
    """Warnings about repo settings scripts/github_setup.sh would apply. Needs gh."""
    out = []
    try:
        view = subprocess.run(["gh", "repo", "view", "--json",
                               "squashMergeAllowed,mergeCommitAllowed,rebaseMergeAllowed,deleteBranchOnMerge,"
                               "autoMergeAllowed,isPrivate,nameWithOwner"],
                              capture_output=True, text=True, check=True, cwd=str(ROOT))
        repo = json.loads(view.stdout)
    except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
        return ["gh is not available or not logged in; skipped the GitHub settings check"]
    if not repo.get("squashMergeAllowed") or repo.get("mergeCommitAllowed") or repo.get("rebaseMergeAllowed"):
        out.append("merge method is not squash-only (proposals should land as one commit)")
    if not repo.get("deleteBranchOnMerge"):
        out.append("branches are not deleted on merge (old proposals will pile up)")
    if not repo.get("autoMergeAllowed"):
        out.append("auto-merge is off (bookkeeping proposals wait for the checks, then merge themselves)")
    try:
        rules = subprocess.run(["gh", "api", f"repos/{repo['nameWithOwner']}/rulesets"],
                               capture_output=True, text=True, check=True, cwd=str(ROOT))
        names = [r.get("name") for r in json.loads(rules.stdout)]
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        names = []
    if "main" not in names:
        out.append("no ruleset named 'main' (nothing stops a push to the approved copy)")
    if out:
        out.append("run: scripts/github_setup.sh (docs/github-settings.md explains each setting and the plan it needs)")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Health check for this checkout.")
    ap.add_argument("--fix", action="store_true", help="apply the safe fixes first")
    ap.add_argument("--strict", action="store_true", help="warnings fail too")
    ap.add_argument("--format", choices=["text", "github"], default="text")
    ap.add_argument("--brief", action="store_true", help="three lines: problems, stale, unfilled")
    ap.add_argument("--github", action="store_true", help="also check the GitHub repository settings")
    args = ap.parse_args(argv)

    ctx = lint.Ctx()
    findings = lint.run_checks(ctx)
    fixed = []
    if args.fix:
        fixed = lint.apply_fixes(ctx, findings)
        findings = lint.run_checks(ctx)

    errors = [f for f in findings if f.level == lint.ERROR]
    warnings = [f for f in findings if f.level == lint.WARNING]
    unfilled = [f.path for f in findings if f.check == "template"]
    stale = [f.path for f in warnings if f.check == "context-stale"]
    served = [rel for rel in ctx.schema["context_files"]
              if ctx.exists(rel) and (ctx.fm(rel) or {}).get("source") == "context-layer"]

    if args.brief:
        print(f"doctor: {len(errors)} problems, {len(warnings)} warnings"
              + ("; run python3 scripts/doctor.py" if errors or warnings else ""))
        print(f"stale context: {', '.join(stale) if stale else 'none'}")
        print(f"unfilled templates: {len(unfilled)}" + (" (run /setup)" if unfilled else ""))
        return 1 if errors else 0

    if fixed:
        print(f"fixed {len(fixed)}:")
        for f in fixed:
            print(f"  {f.path}: {f.message}")
        print()

    if (ROOT / ".env").is_file():
        print("info: .env present (gitignored; keep it that way)")
    else:
        print("info: no .env; fine unless you use key-based integrations (copy .env.example)")

    if unfilled:
        print(f"\nunfilled templates ({len(unfilled)}), run /setup to fill them:")
        for rel in unfilled:
            print(f"  - {rel}")
    if served:
        print(f"\ncontext served by a context layer ({len(served)}), files are fallbacks:")
        for rel in served:
            print(f"  - {rel}")

    visible = [f for f in findings if f.level != lint.INFO]
    if args.format == "github":
        if visible:
            print(lint.format_github(visible))
    else:
        if warnings:
            print(f"\nWARNINGS ({len(warnings)}):")
            print(lint.format_text(warnings))
        if errors:
            print(f"\nPROBLEMS ({len(errors)}):")
            print(lint.format_text(errors))
            fixable = sum(1 for f in errors if f.fixable)
            if fixable:
                print(f"\n{fixable} of these are auto-fixable: python3 scripts/doctor.py --fix")
            print("or ask your agent for /doctor")

    if args.github:
        notes = github_settings()
        if notes:
            print("\nGitHub settings:")
            for n in notes:
                print(f"  - {n}")

    if errors or (args.strict and warnings):
        return 1
    print("\nok: wiring intact" + (f", {len(warnings)} warnings" if warnings else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
