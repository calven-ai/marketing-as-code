#!/usr/bin/env python3
"""Tests for scripts/sync.py and scripts/propose.py: a real git repository per
test with a local bare "origin" that answers to a github.com URL, and a fake
`gh` on PATH that logs every call and answers from canned JSON.

Run from the repo root:  python3 -m unittest scripts/test_lifecycle.py
"""

import io
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _lifecycle  # noqa: E402
import doctor  # noqa: E402
import propose  # noqa: E402
import sync  # noqa: E402
from test_lint import SCHEMA, draft, make_repo, write  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
REPO_URL = "https://github.com/ana/repo.git"

FAKE_GH = r'''#!/bin/sh
printf '%s\n' "$*" >> "${GH_LOG:-/dev/null}"
state=open; head=""; prev=""
for a in "$@"; do
  [ "$prev" = "--state" ] && state="$a"
  [ "$prev" = "--head" ] && head="$(printf '%s' "$a" | tr '/' '_')"
  case "$a" in *review-requested*) state=review;; esac
  prev="$a"
done
case "$1 $2" in
  "auth status") [ -n "$GH_FAKE_LOGGED_OUT" ] && exit 1; exit 0;;
  "pr list")
    if [ -n "$head" ] && [ -f "$GH_FAKE_DIR/$state-$head.json" ]; then cat "$GH_FAKE_DIR/$state-$head.json"
    elif [ -z "$head" ] && [ -f "$GH_FAKE_DIR/$state.json" ]; then cat "$GH_FAKE_DIR/$state.json"
    else echo '[]'; fi;;
  "pr create") echo "https://github.com/ana/repo/pull/7";;
  "pr checks") exit 0;;
  "api user") echo '{"login":"ana","id":1}';;
  "api "*) echo '{}';;
esac
exit 0
'''


def sh(cwd, *args):
    return subprocess.run(["git", *args], cwd=str(cwd), capture_output=True, text=True)


def git(cwd, *args):
    proc = sh(cwd, *args)
    if proc.returncode != 0:
        raise AssertionError(f"git {' '.join(args)} failed: {proc.stderr}")
    return proc.stdout.strip()


class LifecycleCase(unittest.TestCase):
    """work/ is the marketer's clone, other/ a teammate's (or the gate's), origin.git the bare repository."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="mac-life-"))
        origin = self.tmp / "origin.git"
        cfg = self.tmp / "gitconfig"
        cfg.write_text("[user]\n\tname = Ana\n\temail = ana@example.com\n[init]\n\tdefaultBranch = main\n"
                       f"[url \"{origin}\"]\n\tinsteadOf = {REPO_URL}\n", encoding="utf-8")
        fake = self.tmp / "bin" / "gh"
        fake.parent.mkdir()
        fake.write_text(FAKE_GH, encoding="utf-8")
        fake.chmod(fake.stat().st_mode | stat.S_IXUSR)
        (self.tmp / "gh").mkdir()
        self.env = mock.patch.dict(os.environ, {
            "GIT_CONFIG_GLOBAL": str(cfg), "GIT_CONFIG_NOSYSTEM": "1", "HOME": str(self.tmp),
            "GIT_TERMINAL_PROMPT": "0", "GH_EXE": str(fake), "GH_LOG": str(self.tmp / "gh.log"),
            "GH_FAKE_DIR": str(self.tmp / "gh"), "GH_FAKE_LOGGED_OUT": ""})
        self.env.start()
        subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(origin)], check=True)
        self.work = self.tmp / "work"
        subprocess.run(["git", "clone", "-q", REPO_URL, str(self.work)], check=True, capture_output=True)
        make_repo(self.work)
        write(self.work, "scripts/hooks/pre-push", (ROOT / "scripts" / "hooks" / "pre-push").read_text(encoding="utf-8"))
        (self.work / "scripts" / "hooks" / "pre-push").chmod(0o755)
        write(self.work, "scripts/lint.py", "import sys\nsys.exit(0)\n")  # the hook's lint, a stand-in
        write(self.work, ".github/PULL_REQUEST_TEMPLATE.md", (ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md").read_text())
        git(self.work, "add", "-A")
        git(self.work, "commit", "-q", "-m", "Start")
        git(self.work, "push", "-q", "-u", "origin", "main")
        self.other = self.tmp / "other"
        subprocess.run(["git", "clone", "-q", REPO_URL, str(self.other)], check=True, capture_output=True)

    def tearDown(self):
        self.env.stop()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def gh_log(self):
        path = self.tmp / "gh.log"
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def fake_prs(self, name, prs):
        (self.tmp / "gh" / f"{name}.json").write_text(json.dumps(prs), encoding="utf-8")

    def run_script(self, module, *args):
        out = io.StringIO()
        with redirect_stdout(out):
            code = module.main([*args, "--root", str(self.work), "--json"])
        return code, json.loads(out.getvalue())

    def propose(self, *args, title="A change"):
        return self.run_script(propose, "--title", title, *args)

    def sync(self, *args):
        return self.run_script(sync, *args)

    def other_pushes(self, rel, text, branch="main", message="Teammate"):
        git(self.other, "fetch", "-q", "origin")
        git(self.other, "switch", "-q", "-C", branch, f"origin/{branch}")
        write(self.other, rel, text)
        git(self.other, "add", "-A")
        git(self.other, "commit", "-q", "-m", message)
        git(self.other, "push", "-q", "origin", branch)

    def branch(self):
        return git(self.work, "branch", "--show-current")

    def origin_rev(self, ref):
        return sh(self.tmp / "origin.git", "rev-parse", ref).stdout.strip()


class TestPropose(LifecycleCase):
    def test_from_main_edits_become_a_proposal(self):
        before = self.origin_rev("main")
        write(self.work, "content/2026-09-post/draft.md", draft())
        code, out = self.propose(title="Post: the September piece")
        self.assertEqual(0, code, out)
        self.assertTrue(self.branch().startswith("proposal/"), self.branch())
        self.assertIn("september-piece", self.branch())
        self.assertEqual(before, self.origin_rev("main"))  # the approved copy on GitHub is untouched
        self.assertEqual(git(self.work, "rev-parse", "HEAD"), self.origin_rev(self.branch()))
        self.assertIn(f"pr create -R ana/repo --base main --head {self.branch()} --title Post: the September piece",
                      self.gh_log())
        self.assertEqual("https://github.com/ana/repo/pull/7", out["url"])
        self.assertEqual("needs-review", out["kind"])
        self.assertIn("needs review from a teammate", out["outcome"])  # the template ships review.self_merge: false
        self.assertEqual(["content/2026-09-post/draft.md"], out["files"])
        self.assertEqual("Post: the September piece", git(self.work, "log", "-1", "--format=%s"))

    def test_nothing_changed(self):
        code, out = self.propose()
        self.assertEqual(0, code)
        self.assertIn(propose.NOTHING, out["lines"])
        self.assertEqual("main", self.branch())

    def test_problem_blocks_with_nothing_saved(self):
        write(self.work, "content/2026-09-bad/draft.md", draft("bogus"))
        code, out = self.propose()
        self.assertEqual(1, code)
        self.assertTrue(any("problems to fix" in line for line in out["lines"]), out["lines"])
        self.assertIn("Nothing was sent. Fix these (ask me), then propose again.", out["lines"])
        self.assertEqual("main", self.branch())
        self.assertEqual("Start", git(self.work, "log", "-1", "--format=%s"))
        self.assertNotIn("pr create", self.gh_log())

    def test_fixable_problem_is_fixed_and_committed(self):
        settings = json.loads((self.work / ".claude" / "settings.json").read_text())
        settings["permissions"]["deny"].remove("Read(./.env)")
        write(self.work, ".claude/settings.json", json.dumps(settings))
        code, out = self.propose()
        self.assertEqual(0, code, out)
        self.assertIn("Fixed 1 small things on the way.", out["lines"])
        self.assertIn("Read(./.env)", (self.work / ".claude" / "settings.json").read_text())
        self.assertEqual("", git(self.work, "status", "--porcelain"))

    def test_bookkeeping_outcome(self):
        write(self.work, "data/seo/snapshots/2026-09-04-dataforseo-rankings.csv", "keyword,rank\nx,1\n")
        code, out = self.propose(title="Rankings snapshot")
        self.assertEqual(0, code, out)
        self.assertEqual("bookkeeping", out["kind"])
        self.assertIn("merges itself", out["outcome"])

    def test_existing_proposal_is_updated_not_recreated(self):
        write(self.work, "memory/knowledge/topic.md", "# Topic\n")
        self.propose(title="Topic")
        branch = self.branch()
        self.fake_prs(f"open-{branch.replace('/', '_')}", [{"number": 7, "title": "Topic", "url": "https://github.com/ana/repo/pull/7",
                                                            "headRefName": branch}])
        write(self.work, "memory/knowledge/topic.md", "# Topic\n\nMore.\n")
        code, out = self.propose(title="Topic, more")
        self.assertEqual(0, code, out)
        self.assertIn("Updated your proposal: https://github.com/ana/repo/pull/7", out["lines"])
        self.assertEqual(1, self.gh_log().count("pr create"))

    def test_tidy_commit_on_github_is_brought_in_before_pushing(self):
        write(self.work, "memory/knowledge/a.md", "# A\n")
        self.propose(title="A")
        branch = self.branch()
        self.other_pushes("memory/knowledge/tidy.md", "# Tidy\n", branch=branch, message="Tidy: apply the safe fixes")
        write(self.work, "memory/knowledge/b.md", "# B\n")
        code, out = self.propose(title="B")
        self.assertEqual(0, code, out)
        self.assertEqual(git(self.work, "rev-parse", "HEAD"), self.origin_rev(branch))
        self.assertTrue((self.work / "memory" / "knowledge" / "tidy.md").is_file())

    def test_without_gh_the_link_opens_the_proposal_in_the_browser(self):
        os.environ["GH_EXE"] = str(self.tmp / "no-such-gh")
        write(self.work, "memory/knowledge/a.md", "# A\n")
        code, out = self.propose(title="A note")
        self.assertEqual(0, code, out)
        self.assertEqual(self.origin_rev(self.branch()), git(self.work, "rev-parse", "HEAD"))  # pushed anyway
        self.assertTrue(out["url"].startswith(f"https://github.com/ana/repo/compare/main...{self.branch()}?quick_pull=1&title=A%20note"))
        self.assertTrue(any("Create pull request" in line for line in out["lines"]))
        self.assertEqual("", self.gh_log())

    def test_not_connected(self):
        alone = self.tmp / "alone"
        subprocess.run(["git", "init", "-q", str(alone)], check=True)
        out = io.StringIO()
        with redirect_stdout(out):
            code = propose.main(["--title", "x", "--root", str(alone), "--json"])
        self.assertEqual(1, code)
        self.assertIn(_lifecycle.NOT_CONNECTED, json.loads(out.getvalue())["lines"])

    def test_landed_branch_is_refused(self):
        git(self.work, "switch", "-q", "-c", "proposal/old")
        self.fake_prs("merged-proposal_old", [{"number": 3, "title": "Old", "url": "u", "headRefName": "proposal/old"}])
        write(self.work, "memory/knowledge/a.md", "# A\n")
        code, out = self.propose()
        self.assertEqual(1, code)
        self.assertIn(propose.LANDED, out["lines"])

    def test_check_changes_nothing(self):
        write(self.work, "memory/knowledge/a.md", "# A\n")
        code, out = self.run_script(propose, "--check")
        self.assertEqual(0, code)
        self.assertEqual(["memory/knowledge/a.md"], out["files"])
        self.assertEqual("main", self.branch())
        self.assertEqual("Start", git(self.work, "log", "-1", "--format=%s"))
        self.assertIn("No problems in the files.", out["lines"])

    def test_missing_identity(self):
        (self.tmp / "gitconfig").write_text(f"[url \"{self.tmp / 'origin.git'}\"]\n\tinsteadOf = {REPO_URL}\n")
        write(self.work, "memory/knowledge/a.md", "# A\n")
        code, out = self.propose()
        self.assertEqual(1, code)
        self.assertIn(propose.NO_IDENTITY, out["lines"])

    def test_hook_refuses_a_push_to_the_approved_copy(self):
        self.sync()  # turns the hook on
        write(self.work, "memory/knowledge/a.md", "# A\n")
        git(self.work, "add", "-A")
        git(self.work, "commit", "-q", "-m", "Straight to main")
        proc = sh(self.work, "push", "origin", "main")
        self.assertNotEqual(0, proc.returncode)
        self.assertIn("refusing to push straight to main", proc.stderr)


class TestSync(LifecycleCase):
    def test_brings_the_approved_copy_forward(self):
        self.other_pushes("memory/knowledge/new.md", "# New\n")
        code, out = self.sync()
        self.assertEqual(0, code, out)
        self.assertTrue(any(line.startswith("Brought in 1 changes from the approved copy") for line in out["lines"]), out["lines"])
        self.assertEqual(git(self.work, "rev-parse", "HEAD"), self.origin_rev("main"))
        self.assertIn("You are on: the approved copy.", out["lines"])
        self.assertIn("No open proposals of yours.", out["lines"])
        self.assertEqual("scripts/hooks", git(self.work, "config", "core.hooksPath"))

    def test_up_to_date(self):
        code, out = self.sync()
        self.assertIn("The approved copy is up to date.", out["lines"])

    def test_branch_behind_its_pushed_copy_and_behind_main(self):
        write(self.work, "memory/knowledge/a.md", "# A\n")
        self.propose(title="A")
        branch = self.branch()
        self.other_pushes("memory/knowledge/tidy.md", "# Tidy\n", branch=branch, message="Tidy")
        self.other_pushes("memory/knowledge/landed.md", "# Landed\n")
        code, out = self.sync()
        self.assertEqual(0, code, out)
        self.assertIn("The check tidied your proposal; brought that in.", out["lines"])
        self.assertIn("Brought the approved copy into your proposal.", out["lines"])
        self.assertTrue((self.work / "memory" / "knowledge" / "landed.md").is_file())
        self.assertEqual("", git(self.work, "status", "--porcelain"))

    def test_conflict_is_named_and_undone(self):
        write(self.work, "memory/knowledge/shared.md", "# Shared\n\nmine\n")
        self.propose(title="Mine")
        self.other_pushes("memory/knowledge/shared.md", "# Shared\n\ntheirs\n")
        code, out = self.sync()
        self.assertEqual(0, code, out)
        self.assertTrue(any("changed the same lines in memory/knowledge/shared.md" in line for line in out["lines"]), out["lines"])
        self.assertFalse((self.work / ".git" / "MERGE_HEAD").exists())
        self.assertEqual("", git(self.work, "status", "--porcelain"))
        code, out = self.sync("--keep-conflicts")
        self.assertTrue((self.work / ".git" / "MERGE_HEAD").exists())
        self.assertIn("<<<<<<<", (self.work / "memory" / "knowledge" / "shared.md").read_text())

    def test_unsaved_edits_skip_the_merge(self):
        write(self.work, "memory/knowledge/a.md", "# A\n")
        self.propose(title="A")
        self.other_pushes("memory/knowledge/landed.md", "# Landed\n")
        write(self.work, "memory/knowledge/a.md", "# A\n\nedited\n")
        code, out = self.sync()
        self.assertTrue(any(line.startswith("You have unsaved edits to memory/knowledge/a.md") for line in out["lines"]), out["lines"])
        self.assertFalse((self.work / "memory" / "knowledge" / "landed.md").exists())

    def test_landed_branch_removed_gone_branch_kept(self):
        git(self.work, "branch", "done")
        git(self.work, "branch", "gone")
        self.fake_prs("merged-done", [{"number": 9, "title": "Done", "url": "u", "headRefName": "done"}])
        code, out = self.sync()
        self.assertIn("Proposal #9 landed; removed its branch.", out["lines"])
        branches = git(self.work, "branch", "--format=%(refname:short)").split()
        self.assertNotIn("done", branches)
        self.assertIn("gone", branches)

    def test_status_shows_proposals_in_plain_words(self):
        self.fake_prs("open", [
            {"number": 1, "title": "Checking", "url": "u1", "headRefName": "a", "labels": [],
             "statusCheckRollup": [{"name": "doctor", "status": "IN_PROGRESS", "conclusion": ""}], "reviewDecision": ""},
            {"number": 2, "title": "Red", "url": "u2", "headRefName": "b", "labels": [],
             "statusCheckRollup": [{"name": "doctor", "status": "COMPLETED", "conclusion": "FAILURE"}], "reviewDecision": ""},
            {"number": 3, "title": "Green", "url": "u3", "headRefName": "c", "labels": [{"name": "needs-review"}],
             "statusCheckRollup": [{"name": "doctor", "status": "COMPLETED", "conclusion": "SUCCESS"},
                                   {"name": "review-gate", "status": "COMPLETED", "conclusion": "SUCCESS"}], "reviewDecision": ""}])
        code, out = self.sync("--status")
        text = "\n".join(out["lines"])
        self.assertIn("#1 Checking: checking.", text)
        self.assertIn("#2 Red: problems: see the health check comment on the proposal.", text)
        self.assertIn("#3 Green: ready for you to merge.", text)
        self.assertTrue(any(line.startswith("doctor:") for line in out["lines"]))

    def test_status_when_logged_out(self):
        os.environ["GH_FAKE_LOGGED_OUT"] = "1"
        code, out = self.sync("--status")
        self.assertEqual(0, code)
        self.assertIn(_lifecycle.NO_GH, out["lines"])

    def test_dry_run_changes_nothing(self):
        self.other_pushes("memory/knowledge/new.md", "# New\n")
        code, out = self.sync("--dry-run")
        self.assertIn("Would bring in 1 changes from the approved copy.", out["lines"])
        self.assertNotEqual(git(self.work, "rev-parse", "HEAD"), self.origin_rev("main"))


class TestDoctorMachine(LifecycleCase):
    def test_fix_sets_hook_and_identity_from_github(self):
        (self.tmp / "gitconfig").write_text(f"[url \"{self.tmp / 'origin.git'}\"]\n\tinsteadOf = {REPO_URL}\n")
        notes, fixed = doctor.local_setup(self.work, fix=True)
        self.assertEqual([], notes)
        self.assertEqual(3, len(fixed), fixed)  # name and email, the hook, the credential helper
        self.assertEqual("ana", git(self.work, "config", "user.name"))
        self.assertEqual("1+ana@users.noreply.github.com", git(self.work, "config", "user.email"))
        self.assertEqual("scripts/hooks", git(self.work, "config", "core.hooksPath"))
        self.assertIn("auth setup-git", self.gh_log())

    def test_without_fix_it_only_reports(self):
        notes, fixed = doctor.local_setup(self.work, fix=False)
        self.assertEqual([], fixed)
        self.assertTrue(any("pre-push hook is off" in n for n in notes), notes)
        self.assertEqual("", sh(self.work, "config", "core.hooksPath").stdout.strip())

    def test_no_gh_and_logged_out(self):
        os.environ["GH_EXE"] = str(self.tmp / "no-such-gh")
        notes, _ = doctor.local_setup(self.work)
        self.assertIn(doctor.NO_GH, notes)
        os.environ["GH_EXE"] = str(self.tmp / "bin" / "gh")
        os.environ["GH_FAKE_LOGGED_OUT"] = "1"
        notes, _ = doctor.local_setup(self.work)
        self.assertIn(doctor.NOT_LOGGED_IN, notes)


class TestPureParts(unittest.TestCase):
    def test_describe(self):
        gate = {"name": "review-gate", "conclusion": "ACTION_REQUIRED"}
        self.assertEqual("waiting for a teammate to read it",
                         _lifecycle.describe({"statusCheckRollup": [gate], "labels": []}, self_merge=False))
        self.assertEqual("ready for you to merge",
                         _lifecycle.describe({"statusCheckRollup": [gate], "labels": []}, self_merge=True))
        self.assertEqual("bookkeeping, merges itself once the check is green",
                         _lifecycle.describe({"statusCheckRollup": [], "labels": [{"name": "bookkeeping"}]}, False))

    def test_outcome(self):
        self.assertIn("merges itself", _lifecycle.outcome("bookkeeping", False, [], "u"))
        self.assertIn("You are the reviewer", _lifecycle.outcome("needs-review", True, [], "u"))
        self.assertEqual("This needs review from @ben. Link: u.", _lifecycle.outcome("needs-review", False, ["@ben"], "u"))
        self.assertEqual("This needs review from a teammate. Link: u.", _lifecycle.outcome("needs-review", False, [], "u"))

    def test_body_and_commit_message(self):
        co = _lifecycle.Checkout(ROOT)
        body = propose.build_body(co, "Sharper claim.\n\nThe old one hedged.")
        self.assertIn("## What this changes\n\nSharper claim.", body)
        self.assertIn("## Why\n\nThe old one hedged.", body)
        self.assertIn("## Review checklist", body)
        self.assertNotIn("<!--", body)
        self.assertEqual("Title\n\nSharper claim.\n\nThe old one hedged.\n", propose.commit_message("Title", body))
        own = propose.build_body(co, "## What this changes\n\nX\n\n## Why\n\nY")
        self.assertTrue(own.startswith("## What this changes\n\nX"))
        self.assertIn("## Review checklist", own)

    def test_push_failure_messages(self):
        self.assertEqual(propose.SECRET, propose.push_failure("remote: error: GH013: Repository rule violations"))
        self.assertEqual(propose.AUTH, propose.push_failure("fatal: Authentication failed for 'https://github.com/x'"))
        self.assertIsNone(propose.push_failure("! [rejected] main -> main (non-fast-forward)"))
        self.assertIn("refusing", propose.push_failure("pre-push: refusing to push straight to main.\nerror: failed"))

    def test_origin_repo_parsing(self):
        import _common
        for url in ("git@github.com:ana/repo.git", "https://github.com/ana/repo.git", "https://github.com/ana/repo",
                    "ssh://git@github.com/ana/repo.git", "https://github.com/ana/repo/"):
            self.assertEqual(("ana", "repo"), _common.ORIGIN_RE.search(url).groups(), url)
        self.assertIsNone(_common.ORIGIN_RE.search("https://gitlab.com/ana/repo.git"))


if __name__ == "__main__":
    unittest.main()
