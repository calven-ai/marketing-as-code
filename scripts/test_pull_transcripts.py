#!/usr/bin/env python3
"""Tests for the parts of scripts/pull_transcripts.py that turn API output into
filenames: what the provider sends is data, and none of it may choose a path
outside memory/transcripts/inbox/. No network.

Run from the repo root:  python3 -m unittest scripts/test_pull_transcripts.py
"""

import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pull_transcripts as pt  # noqa: E402

TODAY = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class TestDateOf(unittest.TestCase):
    def test_iso_timestamps(self):
        self.assertEqual("2026-09-06", pt.date_of({"created_at": "2026-09-06T14:03:00Z"}))
        self.assertEqual("2026-09-06", pt.date_of({"created_at": "2026-09-06T14:03:00+02:00"}))
        self.assertEqual("2026-09-06", pt.date_of({"created_at": "2026-09-06"}))

    def test_anything_else_is_today(self):
        for raw in ("../../../x", "2026/09/06", "yesterday", "", None, 42, "2026-09-06/../.."):
            got = pt.date_of({"created_at": raw})
            self.assertTrue(TODAY.match(got), (raw, got))
            self.assertNotIn("/", got)


class TestSlugify(unittest.TestCase):
    def test_only_lowercase_ascii_and_hyphens(self):
        self.assertEqual("weekly-sync-q3", pt.slugify("Weekly sync / Q3!"))
        self.assertEqual("meeting", pt.slugify("../../"))
        self.assertEqual("meeting", pt.slugify(""))
        self.assertLessEqual(len(pt.slugify("x" * 200)), 50)


class TestInboxPath(unittest.TestCase):
    def test_stays_inside_the_inbox(self):
        p = pt.inbox_path("2026-09-06-weekly-sync.md")
        self.assertEqual(pt.INBOX.resolve(), p.parent)

    def test_refuses_anything_that_escapes(self):
        for bad in ("../x.md", "sub/x.md", "..", "/etc/passwd", "a\\b.md"):
            with self.assertRaises(SystemExit, msg=bad):
                pt.inbox_path(bad)


if __name__ == "__main__":
    unittest.main()
