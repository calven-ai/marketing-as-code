#!/usr/bin/env python3
"""Tests for scripts/sync_skills.py: a throwaway checkout per test. The script is
part of the gate's trust boundary (scripts/lint.py runs main's copy against a
proposal's worktree through --root), so its behaviour is pinned here.

Run from the repo root:  python3 -m unittest scripts/test_sync_skills.py
"""

import io
import os
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sync_skills  # noqa: E402


def make_checkout(root, names=("alpha", "beta")):
    for name in names:
        d = root / ".agents" / "skills" / name
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text(f"---\nname: {name}\ndescription: x\n---\n", encoding="utf-8")
    (root / ".agents" / "skills" / "_template").mkdir()  # no SKILL.md: not a skill
    return root


def run(*argv):
    out = io.StringIO()
    code = 0
    with redirect_stdout(out):
        try:
            sync_skills.main(list(argv))
        except SystemExit as err:
            code = err.code if isinstance(err.code, int) else 1
    return code, out.getvalue()


class SyncSkillsCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="mac-skills-"))
        self.root = make_checkout(self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_links_every_skill_relative_to_the_root_given(self):
        code, out = run("--root", str(self.root))
        self.assertEqual(0, code, out)
        for name in ("alpha", "beta"):
            link = self.root / ".claude" / "skills" / name
            self.assertTrue(link.is_symlink(), name)
            self.assertEqual(Path("../../.agents/skills") / name, link.readlink())
            self.assertTrue((link / "SKILL.md").is_file())
        self.assertFalse((self.root / ".claude" / "skills" / "_template").exists())
        self.assertEqual((0, "ok: 2 skills in sync\n"), run("--check", "--root", str(self.root)))

    def test_check_reports_drift_and_strays_without_touching_anything(self):
        run("--root", str(self.root))
        (self.root / ".claude" / "skills" / "alpha").unlink()
        stray = self.root / ".claude" / "skills" / "gone"
        stray.mkdir()
        code, out = run("--check", "--root", str(self.root))
        self.assertEqual(1, code)
        self.assertIn("drift: .claude/skills/alpha: missing", out)
        self.assertIn("stray: .claude/skills/gone", out)
        self.assertFalse((self.root / ".claude" / "skills" / "alpha").exists())
        self.assertTrue(stray.is_dir())

    def test_fix_relinks_and_leaves_strays_and_dotfiles_alone(self):
        run("--root", str(self.root))
        wrong = self.root / ".claude" / "skills" / "alpha"
        wrong.unlink()
        wrong.symlink_to(Path("..") / "elsewhere")
        (self.root / ".claude" / "skills" / ".system").mkdir()  # Claude Code's own housekeeping
        (self.root / ".claude" / "skills" / "gone").mkdir()
        code, out = run("--root", str(self.root))
        self.assertEqual(0, code)
        self.assertIn("linked .claude/skills/alpha", out)
        self.assertIn("warning: stray .claude/skills/gone", out)
        self.assertEqual(Path("../../.agents/skills/alpha"), wrong.readlink())
        self.assertTrue((self.root / ".claude" / "skills" / ".system").is_dir())
        self.assertTrue((self.root / ".claude" / "skills" / "gone").is_dir())

    def test_copies_when_symlinks_are_unavailable(self):
        with mock.patch.object(Path, "symlink_to", side_effect=OSError("no symlinks here")):
            code, out = run("--root", str(self.root))
        self.assertEqual(0, code)
        self.assertIn("copied .claude/skills/alpha (symlinks unavailable)", out)
        copy = self.root / ".claude" / "skills" / "alpha"
        self.assertTrue(copy.is_dir() and not copy.is_symlink())
        self.assertEqual((0, "ok: 2 skills in sync\n"), run("--check", "--root", str(self.root)))
        (self.root / ".agents" / "skills" / "alpha" / "SKILL.md").write_text("changed\n", encoding="utf-8")
        code, out = run("--check", "--root", str(self.root))
        self.assertEqual(1, code)
        self.assertIn("copy differs from canonical", out)

    def test_refuses_a_root_without_canonical_skills(self):
        code, out = run("--check", "--root", str(self.tmp / "nowhere"))
        self.assertNotEqual(0, code)

    def test_this_checkout_is_in_sync(self):
        """The template's own .claude/skills/ mirrors .agents/skills/ (the check enforces it)."""
        root = Path(__file__).resolve().parent.parent
        if not (root / ".claude" / "skills").is_dir():
            self.skipTest("no .claude/skills here")
        code, out = run("--check", "--root", str(root))
        self.assertEqual(0, code, out)


if __name__ == "__main__":
    unittest.main()
