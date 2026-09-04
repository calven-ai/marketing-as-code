#!/usr/bin/env python3
"""Health check for a marketing-as-code checkout: runs every check in
scripts/lint.py against docs/schema.json, then reports unfilled templates,
context files past their review date, whether an .env exists, and whether
this machine is ready to propose (git, your name, the pre-push hook, the
GitHub CLI and its login). --fix applies the safe fixes first, turns the
hook on and sets your name from your GitHub login; --strict fails on
warnings too (CI on main); --brief prints three lines for the session-start
hook; --github checks the repository settings through gh. Exit 1 only on
real breakage.

Run from the repo root:  python3 scripts/doctor.py

When it is red, fix what it names or ask your agent for /doctor. The
findings are the same ones CI posts on every proposal (check.yml), so a
green doctor here means a green check there.
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lint  # noqa: E402
from _common import find_gh, gh_ready, origin_repo, run  # noqa: E402

ROOT = lint.ROOT


def github_settings():
    """Warnings about repo settings scripts/github_setup.sh would apply. Needs gh."""
    out = []
    name = origin_repo(ROOT)  # this checkout's own repository, never a fork's parent
    repo = _api(f"repos/{name}") if name and find_gh() else None
    if not repo:
        return ["gh is not available or not logged in; skipped the GitHub settings check"]
    if not repo.get("allow_squash_merge") or repo.get("allow_merge_commit") or repo.get("allow_rebase_merge"):
        out.append("merge method is not squash-only (proposals should land as one commit)")
    if not repo.get("delete_branch_on_merge"):
        out.append("branches are not deleted on merge (old proposals will pile up)")
    if not repo.get("allow_auto_merge"):
        out.append("auto-merge is off (a person cannot click 'merge when ready' on a checking proposal)")
    rules = _api(f"repos/{name}/rulesets") or []
    if "main" not in [r.get("name") for r in rules]:
        out.append("no ruleset named 'main' (nothing stops a push to the approved copy)")
    out += environment_settings(name)
    if out:
        out.append("run: scripts/github_setup.sh (docs/github-settings.md explains each setting and the plan it needs)")
    return out + review_policy(name, repo)


def review_policy(name, repo):
    """docs/schema.json's repo.private and review.self_merge against what GitHub says (docs/make-it-yours.md)."""
    out = []
    schema = json.loads((ROOT / "docs" / "schema.json").read_text(encoding="utf-8"))
    declared = bool((schema.get("repo") or {}).get("private"))
    if repo.get("private") is not None and bool(repo.get("private")) != declared:
        actual = "private" if repo.get("private") else "public"
        out.append(f"docs/schema.json says repo.private is {str(declared).lower()} but the repository is {actual}; "
                   "set repo.private to match (/setup asks)")
    variable = _api(f"repos/{name}/actions/variables/REVIEW_SELF_MERGE") or {}
    self_merge = bool((schema.get("review") or {}).get("self_merge")) or \
        str(variable.get("value", "")).strip().lower() == "true"
    people = _api(f"repos/{name}/collaborators")
    if self_merge and isinstance(people, list) and len(people) > 1:
        out.append(f"self-merge is on but {len(people)} people can push; set review.self_merge to false in "
                   "docs/schema.json (or remove the REVIEW_SELF_MERGE variable) so someone other than the author "
                   "approves (docs/workflow.md)")
    return out


def _api(path):
    proc = run([find_gh() or "gh", "api", path], cwd=ROOT, check=False)
    if proc.returncode != 0:
        return None
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return None


def environment_settings(repo):
    """The `automation` environment holds the bot keys and only main may use it; the workflow
    token is read-only by default and cannot approve proposals (docs/secrets.md)."""
    out = []
    env = _api(f"repos/{repo}/environments/automation")
    if env is None:
        out.append("no environment named 'automation' (the bot keys for unattended runs have nowhere safe to live)")
    else:
        policy = env.get("deployment_branch_policy") or {}
        branches = _api(f"repos/{repo}/environments/automation/deployment-branch-policies") or {}
        names = [b.get("name") for b in branches.get("branch_policies", [])]
        if not policy.get("custom_branch_policies") or names != ["main"]:
            out.append("environment 'automation' is not restricted to main (a workflow on any branch could read the bot keys)")
    perms = _api(f"repos/{repo}/actions/permissions/workflow")
    if perms is not None:
        if perms.get("default_workflow_permissions") != "read":
            out.append("the workflow token defaults to write (each job should ask for what it needs)")
        if perms.get("can_approve_pull_request_reviews"):
            out.append("GitHub Actions may approve pull requests (an agent in Actions could approve its own proposal)")
    return out


NO_GH = "GitHub CLI is not installed. Download it from cli.github.com, then say /doctor again."
NOT_LOGGED_IN = "Not logged in to GitHub. Run: gh auth login --web (it opens your browser and shows a code)."


def local_setup(root=ROOT, fix=False):
    """'Your machine' notes: what stops /propose from working here, and what --fix set right.
    Returns (notes, fixed). Never asks for or prints a key."""
    notes, fixed = [], []
    if shutil.which("git") is None:
        notes.append("git is not installed. On a Mac run `xcode-select --install`; on Windows install Git for "
                     "Windows; on Linux use your package manager (docs/troubleshooting.md).")
        return notes, fixed
    if not (Path(root) / ".git").exists():
        notes.append("this folder is not a copy of the repository yet; clone it with GitHub Desktop (docs/new-to-github.md)")
    elif not origin_repo(root):
        notes.append("this copy is not connected to a repository on GitHub (docs/new-to-github.md)")
    exe = find_gh()
    logged_in = bool(exe) and gh_ready(root)
    name = run(["git", "config", "user.name"], cwd=root, check=False).stdout.strip()
    email = run(["git", "config", "user.email"], cwd=root, check=False).stdout.strip()
    if not (name and email):
        user = None
        if fix and logged_in:
            try:
                user = json.loads(run([exe, "api", "user"], cwd=root, check=False).stdout or "{}")
            except json.JSONDecodeError:
                user = None
        if user and user.get("login"):
            login = user["login"]
            run(["git", "config", "--global", "user.name", name or login], cwd=root, check=False)
            run(["git", "config", "--global", "user.email", email or f"{user.get('id', 0)}+{login}@users.noreply.github.com"],
                cwd=root, check=False)
            fixed.append("set your name and email for commits from your GitHub login")
        else:
            notes.append("Git does not know your name yet. Log in to GitHub (below) and run `python3 scripts/doctor.py "
                         "--fix`, or set it once: git config --global user.name \"Your Name\" and user.email")
    hooks = run(["git", "config", "core.hooksPath"], cwd=root, check=False).stdout.strip()
    if hooks != "scripts/hooks" and (Path(root) / "scripts" / "hooks").is_dir():
        if fix:
            run(["git", "config", "core.hooksPath", "scripts/hooks"], cwd=root, check=False)
            fixed.append("turned on the safety check that runs before anything leaves this computer")
        else:
            notes.append("the pre-push hook is off in this clone; turn it on once: git config core.hooksPath scripts/hooks")
    if not exe:
        notes.append(NO_GH)
    elif not logged_in:
        notes.append(NOT_LOGGED_IN)
    else:
        helpers = run(["git", "config", "--get-all", "credential.helper"], cwd=root, check=False).stdout
        if not any(k in helpers for k in ("gh", "osxkeychain", "manager", "store", "cache")):
            if fix:
                run([exe, "auth", "setup-git"], cwd=root, check=False)
                fixed.append("let git use your GitHub login when pushing")
            else:
                notes.append("git may ask for a password when pushing; run once: gh auth setup-git")
    if sys.version_info < (3, 9):
        notes.append(f"Python {sys.version_info.major}.{sys.version_info.minor} is old; the scripts need 3.9 or newer")
    return notes, fixed


def brief(ctx, findings=None):
    """The three lines the session-start hook and /sync print: problems, stale context, unfilled templates.
    A fourth line, only while the template's residue is still here (docs/make-it-yours.md)."""
    findings = lint.run_checks(ctx) if findings is None else findings
    errors = [f for f in findings if f.level == lint.ERROR]
    warnings = [f for f in findings if f.level == lint.WARNING]
    unfilled = [f.path for f in findings if f.check == "template"]
    stale = [f.path for f in warnings if f.check == "context-stale"]
    adoption = [f for f in findings if f.check == "adoption"]
    lines = [f"doctor: {len(errors)} problems, {len(warnings)} warnings"
             + ("; run python3 scripts/doctor.py" if errors or warnings else ""),
             f"stale context: {', '.join(stale) if stale else 'none'}",
             f"unfilled templates: {len(unfilled)}" + (" (run /setup)" if unfilled else "")]
    if adoption:
        lines.append(f"make it yours: {len(adoption)} items left (docs/make-it-yours.md)")
    return lines


def adoption_lines(findings):
    """The Make it yours items, without the prefix and pointer every finding carries."""
    out = []
    for f in findings:
        if f.check != "adoption":
            continue
        text = f.message
        for cut in ("make it yours: ", " (docs/make-it-yours.md)"):
            text = text.replace(cut, "")
        out.append(text)
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
        print("\n".join(brief(ctx, findings)))
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
    if shutil.which("npx") is None:
        print("info: Node.js is not installed; only the DataForSEO server in .mcp.json needs it (integrations/README.md)")
    notes, done = local_setup(ROOT, fix=args.fix)
    for line in done:
        print(f"fixed: {line}")
    if notes:
        print("\nYour machine:")
        for n in notes:
            print(f"  - {n}")
    else:
        print("info: your machine is ready to propose")

    if unfilled:
        print(f"\nunfilled templates ({len(unfilled)}), run /setup to fill them:")
        for rel in unfilled:
            print(f"  - {rel}")
    if served:
        print(f"\ncontext served by a context layer ({len(served)}), files are fallbacks:")
        for rel in served:
            print(f"  - {rel}")
    residue = adoption_lines(findings)
    if residue:
        print(f"\nMake it yours ({len(residue)} left), docs/make-it-yours.md:")
        for line in residue:
            print(f"  - {line}")

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
