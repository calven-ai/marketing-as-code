#!/usr/bin/env python3
"""Tests for scripts/package_skills.py: one ZIP per skill, folder at the top.

Run from the repo root:  python3 -m unittest scripts/test_package_skills.py
"""

import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import package_skills  # noqa: E402


class TestPackage(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="mac-pkg-"))
        skills = self.tmp / "skills"
        (skills / "battlecard" / "references").mkdir(parents=True)
        (skills / "battlecard" / "SKILL.md").write_text("---\nname: battlecard\n---\n")
        (skills / "battlecard" / "references" / "card.md").write_text("# Card\n")
        (skills / "notes").mkdir()  # no SKILL.md: not a skill
        self.skills, self.out = skills, self.tmp / "out"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_one_zip_per_skill_with_the_folder_on_top(self):
        self.assertEqual(["battlecard"], package_skills.package(self.skills, self.out))
        with zipfile.ZipFile(self.out / "battlecard.zip") as zf:
            self.assertEqual(["battlecard/SKILL.md", "battlecard/references/card.md"], sorted(zf.namelist()))

    def test_output_is_reproducible(self):
        package_skills.package(self.skills, self.out)
        first = (self.out / "battlecard.zip").read_bytes()
        package_skills.package(self.skills, self.out)
        self.assertEqual(first, (self.out / "battlecard.zip").read_bytes())


if __name__ == "__main__":
    unittest.main()
