#!/usr/bin/env python3
"""Tests for scripts/lint.py: one fixture repo per test, one test per check.

Run from the repo root:  python3 -m unittest scripts/test_lint.py
CI runs it before the lint itself, so a broken check never guards a repo.
"""

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lint  # noqa: E402
import review_gate  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = json.loads((ROOT / "docs" / "schema.json").read_text(encoding="utf-8"))

TODAY = __import__("datetime").date.today().isoformat()
FRONT = f"---\nsource: repo\nlast_reviewed: {TODAY}\nowner: Ana\n---\n\n# Doc\n\nText.\n"


def write(root, rel, text=""):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(text, bytes):
        path.write_bytes(text)
    else:
        path.write_text(text, encoding="utf-8")
    return path


def make_repo(root):
    """The smallest tree that passes every check."""
    for rel in SCHEMA["required_files"]:
        write(root, rel, "# " + rel + "\n")
    for rel in SCHEMA["required_dirs"]:
        write(root, rel + "/.gitkeep")
    write(root, "content/_template/draft.md", draft("brief"))
    write(root, ".gitignore", ".env\n.env.*\n!.env.example\n")
    write(root, ".env.example", "DATAFORSEO_LOGIN=\nDATAFORSEO_PASSWORD=\n")
    mcp = {"mcpServers": {"dataforseo": {"command": "npx", "env": {"DATAFORSEO_LOGIN": "${DATAFORSEO_LOGIN}"}}}}
    write(root, ".mcp.json", json.dumps(mcp))
    write(root, ".cursor/mcp.json", json.dumps(mcp).replace("${", "${env:"))
    write(root, ".claude/settings.json", json.dumps({"permissions": {
        "deny": list(SCHEMA["settings"]["required_deny"]), "disableBypassPermissionsMode": "disable"}}))
    write(root, "integrations/README.md", "# integrations\n\n`DATAFORSEO_LOGIN`, `DATAFORSEO_PASSWORD`\n")
    write(root, "memory/decision-log.md", "# Decision log\n\nFormat.\n\n---\n")
    write(root, "content/README.md", "# content\n\n  status: idea | brief | draft | in-review | published | evergreen\n"
          "  channel: blog | email | linkedin | webinar | ad | case-study | other\n")
    write(root, "docs/README.md", "# docs\n\n- [schema.json](schema.json)\n")
    write(root, "docs/schema.json", json.dumps(SCHEMA))
    write(root, ".agents/skills/review/SKILL.md",
          "---\nname: review\ndescription: Review a draft. Use when asked.\nmetadata:\n  kind: workflow\n  needs: nothing\n---\n\n# Review\n")
    for rel in SCHEMA["context_files"]:
        write(root, rel, FRONT.replace("source: repo", "document: x\nsource: repo") if rel.startswith("strategy") else FRONT)
    return root


def draft(status="draft", extra=""):
    return (f"---\nproject: \"\"\nstatus: {status}\nchannel: blog\nowner: Ana\npublished: \"\"\npublished_url: \"\"\n"
            f"{extra}---\n\n# Title\n\nBody.\n")


class LintCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="mac-lint-"))
        self.root = make_repo(self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def ctx(self):
        return lint.Ctx(root=self.root, schema=SCHEMA)

    def findings(self, check=None, level=None):
        ctx = self.ctx()
        out = lint.run_checks(ctx)
        if check:
            out = [f for f in out if f.check == check]
        if level:
            out = [f for f in out if f.level == level]
        return out

    def assertClean(self):
        bad = [f for f in self.findings() if f.level != lint.INFO]
        self.assertEqual([], [(f.path, f.message) for f in bad])

    def fix(self):
        ctx = self.ctx()
        lint.apply_fixes(ctx, lint.run_checks(ctx))


class TestFixture(LintCase):
    def test_fixture_is_clean(self):
        self.assertClean()


class TestFrontmatter(LintCase):
    def test_unclosed_block_is_an_error(self):
        write(self.root, "content/2026-09-piece/draft.md", "---\nstatus: draft\nno end")
        self.assertTrue(self.findings("frontmatter-syntax", lint.ERROR))

    def test_crlf_is_a_fixable_warning(self):
        write(self.root, "content/2026-09-piece/brief.md", "# Brief\r\n")
        write(self.root, "content/2026-09-piece/draft.md", draft().replace("\n", "\r\n"))
        found = self.findings("frontmatter-syntax", lint.WARNING)
        self.assertTrue(found and all(f.fixable for f in found))
        self.fix()
        self.assertFalse(self.findings("frontmatter-syntax"))

    def test_enum_and_date_and_unknown_key(self):
        write(self.root, "content/2026-09-piece/brief.md", "# Brief\n")
        write(self.root, "content/2026-09-piece/draft.md", draft("ready", "typo_key: 1\n").replace('published: ""', "published: soon"))
        messages = [f.message for f in self.findings("frontmatter")]
        self.assertTrue(any("not one of" in m for m in messages))
        self.assertTrue(any("YYYY-MM-DD" in m for m in messages))
        self.assertTrue(any("typo_key" in m for m in messages))

    def test_missing_key_with_default_is_fixable(self):
        write(self.root, "content/2026-09-piece/brief.md", "# Brief\n")
        write(self.root, "content/2026-09-piece/draft.md", draft().replace('published_url: ""\n', ""))
        found = self.findings("frontmatter", lint.ERROR)
        self.assertTrue(found and found[0].fixable)
        self.fix()
        self.assertFalse(self.findings("frontmatter"))

    def test_strategy_needs_document_key(self):
        write(self.root, "strategy/personas.md", FRONT)
        self.assertTrue(any("document" in f.message for f in self.findings("frontmatter", lint.ERROR)))


class TestContent(LintCase):
    def test_published_needs_date_and_url(self):
        write(self.root, "content/2026-09-piece/brief.md", "# Brief\n")
        write(self.root, "content/2026-09-piece/draft.md", draft("published"))
        levels = {f.level for f in self.findings("content-published")}
        self.assertEqual({lint.ERROR, lint.WARNING}, levels)

    def test_placeholder_past_brief(self):
        write(self.root, "content/2026-09-piece/brief.md", "# Brief\n")
        write(self.root, "content/2026-09-piece/draft.md", draft("in-review").replace("Body.", "[The draft goes here]"))
        self.assertTrue(self.findings("content-placeholder", lint.ERROR))
        write(self.root, "content/2026-09-piece/draft.md", draft("brief").replace("Body.", "[The draft goes here]"))
        self.assertFalse(self.findings("content-placeholder"))

    def test_project_must_exist(self):
        write(self.root, "content/2026-09-piece/brief.md", "# Brief\n")
        write(self.root, "content/2026-09-piece/draft.md", draft().replace('project: ""', "project: projects/nope"))
        self.assertTrue(self.findings("content-project", lint.ERROR))

    def test_folder_naming_and_brief(self):
        write(self.root, "content/My Post/draft.md", draft())
        checks = {f.check for f in self.findings()}
        self.assertIn("content-naming", checks)
        self.assertIn("content-brief", checks)

    def test_readme_enum_drift(self):
        write(self.root, "content/README.md", "# content\n\n  status: idea | brief\n")
        self.assertTrue(self.findings("schema-prose", lint.WARNING))


class TestContext(LintCase):
    def test_stale_and_unreviewed(self):
        write(self.root, "brand/voice.md", FRONT.replace(TODAY, "2020-01-01"))
        write(self.root, "brand/visual-identity.md", FRONT.replace(f"last_reviewed: {TODAY}", "last_reviewed:"))
        self.assertEqual(2, len(self.findings("context-stale")))

    def test_unfilled_and_served_are_quiet(self):
        write(self.root, "brand/voice.md", FRONT.replace(f"last_reviewed: {TODAY}", "last_reviewed:") + "\nTemplate: unfilled\n")
        write(self.root, "brand/visual-identity.md", FRONT.replace("source: repo", "source: context-layer").replace("2026-01-01", "2020-01-01"))
        self.assertFalse(self.findings("context-stale"))
        self.assertTrue(self.findings("template", lint.INFO))


class TestProjects(LintCase):
    def test_brief_required_and_no_content_inside(self):
        write(self.root, "projects/launch/status.md", "# Status\n")
        write(self.root, "projects/launch/draft.md", "x")
        checks = {f.check for f in self.findings(level=lint.ERROR)}
        self.assertIn("project-brief", checks)
        self.assertIn("project-contents", checks)

    def test_status_state_and_order_fix(self):
        write(self.root, "projects/launch/brief.md", "# Launch\n")
        write(self.root, "projects/launch/status.md",
              "# Status\n\n## 2026-01-01\n\n- **State:** on track\n- Old.\n\n## 2026-02-01\n\n- **State:** sideways\n- New.\n")
        found = self.findings("project-status")
        self.assertTrue(any(f.level == lint.ERROR for f in found))
        self.assertTrue(any(f.fixable for f in found))
        self.fix()
        text = (self.root / "projects/launch/status.md").read_text()
        self.assertLess(text.index("2026-02-01"), text.index("2026-01-01"))


class TestDecisionLog(LintCase):
    def test_format_and_order(self):
        write(self.root, "memory/decision-log.md",
              "# Log\n\n---\n\n## 2026-01-01: Old\n\n- **Decided by:** A\n- **Source:** x\n- **Context:** y\n- **Follow-ups:** none\n\n"
              "## 2026-02-01: New\n\n- **Decided by:** A\n- **Context:** y\n\n## bad heading\n")
        found = self.findings("decision-log")
        self.assertTrue(any("bullets" in f.message for f in found))
        self.assertTrue(any("heading" in f.message for f in found))
        self.assertTrue(any(f.fixable for f in found))


class TestTranscripts(LintCase):
    def test_rename_from_frontmatter(self):
        write(self.root, "memory/transcripts/inbox/Weekly Sync.md",
              "---\ntitle: Weekly sync\ndate: 2026-09-03\nsource: manual\n---\n\n# Weekly sync\n")
        found = self.findings("transcript-naming")
        self.assertTrue(found and found[0].fixable)
        self.fix()
        self.assertTrue((self.root / "memory/transcripts/inbox/2026-09-03-weekly-sync.md").exists())

    def test_connector_needs_id(self):
        write(self.root, "memory/transcripts/inbox/2026-09-03-sync.md",
              "---\ntitle: Sync\ndate: 2026-09-03\nsource: granola\n---\n")
        self.assertTrue(self.findings("transcript-contract", lint.ERROR))


class TestData(LintCase):
    def test_snapshot_naming_and_columns(self):
        write(self.root, "data/seo/snapshots/rankings.csv", "a,b\n1,2\n")
        write(self.root, "data/seo/snapshots/2026-01-01-dataforseo-volume.csv", "a,b\n1,2\n")
        write(self.root, "data/seo/snapshots/2026-02-01-dataforseo-volume.csv", "a,c\n1,2\n")
        self.assertTrue(self.findings("snapshot-naming", lint.ERROR))
        self.assertTrue(self.findings("snapshot-columns", lint.WARNING))

    def test_canonical_header_and_ragged_rows(self):
        write(self.root, "data/seo/keywords.csv", "keyword,volume\nx,1,2\n")
        messages = [f.message for f in self.findings("csv", lint.ERROR)]
        self.assertTrue(any("header must be" in m for m in messages))
        self.assertTrue(any("columns" in m for m in messages))


class TestReports(LintCase):
    def test_data_used(self):
        write(self.root, "reports/recurring/seo/2026-09-01.md", "# R\n\n## Answer\n")
        write(self.root, "reports/adhoc/2026-09-01-why/report.md",
              "# R\n\n## Data used\n\n- `data/seo/snapshots/2026-01-01-x-y.csv`\n")
        messages = [f.message for f in self.findings("report-data")]
        self.assertTrue(any("Data used" in m for m in messages))
        self.assertTrue(any("does not exist" in m for m in messages))


class TestRepoHygiene(LintCase):
    def test_binaries(self):
        write(self.root, "content/2026-09-x/hero.png", b"\x89PNG\0\0")
        write(self.root, "playgrounds/demo/shot.png", b"\x89PNG\0\0")
        write(self.root, "brand/logos/logo.png", b"\x89PNG\0\0")
        levels = {f.path: f.level for f in self.findings("binary")}
        self.assertEqual(lint.ERROR, levels["content/2026-09-x/hero.png"])
        self.assertEqual(lint.WARNING, levels["playgrounds/demo/shot.png"])
        self.assertNotIn("brand/logos/logo.png", levels)

    def test_filename_with_space(self):
        write(self.root, "memory/knowledge/my notes.md", "# N\n")
        found = self.findings("filename")
        self.assertTrue(found and found[0].fixable)

    def test_required_dir_is_fixable(self):
        shutil.rmtree(self.root / "reports/qmr")
        found = self.findings("required", lint.ERROR)
        self.assertTrue(found and found[0].fixable)
        self.fix()
        self.assertTrue((self.root / "reports/qmr/.gitkeep").exists())

    def test_env_tracked_and_gitignore(self):
        write(self.root, ".env", "KEY=1\n")
        write(self.root, ".gitignore", "node_modules\n")
        self.assertEqual(2, len(self.findings("env-tracked", lint.ERROR)))

    def test_secret_shapes(self):
        write(self.root, "memory/knowledge/notes.md", "token " + "xoxb-" + "1234567890-abcdefghijklmnop\n")
        write(self.root, "docs/secrets.md", "Keys look like `sk-ant-` and go in .env.\n")
        paths = {f.path for f in self.findings("secret", lint.ERROR)}
        self.assertEqual({"memory/knowledge/notes.md"}, paths)

    def test_pii_level_follows_privacy(self):
        write(self.root, "data/accounts/snapshots/2026-01-01-apify-people.csv", "name,email\nA,a@corp.io\n")
        self.assertTrue(self.findings("pii", lint.WARNING))
        private = dict(SCHEMA, repo={"private": True})
        ctx = lint.Ctx(root=self.root, schema=private)
        self.assertTrue([f for f in lint.check_pii(ctx) if f.level == lint.INFO])


class TestConfigs(LintCase):
    def test_mcp_servers_and_env(self):
        write(self.root, ".cursor/mcp.json", json.dumps({"mcpServers": {"other": {"url": "x"}}}))
        write(self.root, ".mcp.json", json.dumps({"mcpServers": {"dataforseo": {"env": {"K": "${NEW_KEY}"}}}}))
        messages = [f.message for f in self.findings("mcp") + self.findings("mcp-env")]
        self.assertTrue(any("server lists differ" in m for m in messages))
        self.assertTrue(any("NEW_KEY" in m for m in messages))

    def test_mcp_value_instead_of_placeholder(self):
        write(self.root, ".mcp.json", json.dumps({"mcpServers": {"dataforseo": {"headers": {"Authorization": "Bearer abcdefghijklmnop"}}}}))
        self.assertTrue(any("credential" in f.message for f in self.findings("mcp", lint.ERROR)))

    def test_settings_deny(self):
        write(self.root, ".claude/settings.json", json.dumps({"permissions": {"deny": []}}))
        self.assertTrue(self.findings("settings", lint.ERROR))

    def test_settings_one_missing_rule_is_fixable(self):
        deny = [d for d in SCHEMA["settings"]["required_deny"] if d != "Bash(env)"]
        write(self.root, ".claude/settings.json", json.dumps({"permissions": {"deny": deny, "allow": ["Bash(ls)"]}}))
        found = self.findings("settings", lint.ERROR)
        self.assertTrue(found and all(f.fixable for f in found))
        self.assertTrue(any("Bash(env)" in f.message for f in found))
        self.assertTrue(any("disableBypassPermissionsMode" in f.message for f in found))
        self.fix()
        self.assertFalse(self.findings("settings"))
        data = json.loads((self.root / ".claude/settings.json").read_text())
        self.assertEqual(["Bash(ls)"], data["permissions"]["allow"])
        self.assertEqual("disable", data["permissions"]["disableBypassPermissionsMode"])


class TestSkillsAndDocs(LintCase):
    def test_skill_name_and_metadata(self):
        write(self.root, ".agents/skills/review/SKILL.md", "---\nname: reviewer\ndescription: x\n---\n")
        found = self.findings("skill")
        self.assertTrue(any(f.level == lint.ERROR for f in found))
        self.assertTrue(any(f.level == lint.WARNING for f in found))

    def test_paths_and_links(self):
        write(self.root, ".agents/skills/review/SKILL.md",
              "---\nname: review\ndescription: x\nmetadata:\n  kind: workflow\n  needs: nothing\n---\n\n"
              "Run `scripts/nope.py` and read `strategy/positioning.md`. See [x](../../../docs/nope.md).\n\n"
              "## Worked example\n\nEdit `projects/q4/status.md`.\n")
        paths = [f for f in self.findings("path")]
        self.assertEqual(1, len(paths))
        self.assertEqual(lint.ERROR, paths[0].level)
        self.assertTrue(self.findings("link", lint.ERROR))

    def test_generated_block_and_docs_index(self):
        write(self.root, "agents/README.md", "# Roster\n\n<!-- generated:skills-roles -->\nstale\n<!-- /generated:skills-roles -->\n")
        write(self.root, "docs/extra.md", "# Extra doc\n")
        found = self.findings("generated") + self.findings("docs-index")
        self.assertEqual(3, len([f for f in found if f.fixable]))  # two blocks, one index entry
        self.fix()
        self.assertFalse(self.findings("generated") + self.findings("docs-index"))
        self.assertIn("extra.md", (self.root / "docs/README.md").read_text())
        self.assertIn("| Agent | What it does | Needs |", (self.root / "agents/README.md").read_text())


class TestClassify(unittest.TestCase):
    def test_bookkeeping_globs(self):
        globs = SCHEMA["bookkeeping"]["globs"]
        for path in ["projects/launch/status.md", "projects/q4/webinar/status.md", "memory/decision-log.md",
                     "data/seo/snapshots/2026-01-01-x-y.csv", "memory/transcripts/inbox/2026-01-01-a.md",
                     "reports/recurring/seo/2026-01-01.md"]:
            self.assertTrue(any(lint.match_glob(path, g) for g in globs), path)
        for path in ["projects/launch/brief.md", "strategy/positioning.md", "content/2026-09-x/draft.md",
                     "reports/adhoc/2026-01-01-q/report.md", ".agents/skills/review/SKILL.md"]:
            self.assertFalse(any(lint.match_glob(path, g) for g in globs), path)

    def test_classify_paths(self):
        cp = lint.classify_paths
        self.assertEqual("needs-review", cp(SCHEMA, []))
        self.assertEqual("bookkeeping", cp(SCHEMA, ["memory/decision-log.md", "data/seo/snapshots/2026-01-01-x-y.csv"]))
        self.assertEqual("needs-review", cp(SCHEMA, ["memory/decision-log.md", "strategy/positioning.md"]))
        for machinery in ["docs/schema.json", "scripts/review_gate.py", ".github/workflows/gate.yml",
                          ".claude/settings.json", ".mcp.json", ".cursor/mcp.json", "AGENTS.md", ".gitignore",
                          ".agents/skills/review/SKILL.md", "integrations/README.md"]:
            self.assertEqual("needs-review", cp(SCHEMA, ["memory/decision-log.md", machinery]), machinery)

    def test_schema_cannot_widen_bookkeeping(self):
        """A proposal that edits the schema to call itself bookkeeping is still needs-review."""
        widened = json.loads(json.dumps(SCHEMA))
        widened["bookkeeping"]["globs"] = ["**"]
        widened["bookkeeping"]["never"] = []
        self.assertEqual("needs-review", lint.classify_paths(widened, ["docs/schema.json"]))
        self.assertEqual("needs-review", lint.classify_paths(widened, ["scripts/lint.py", "memory/decision-log.md"]))
        self.assertEqual("bookkeeping", lint.classify_paths(widened, ["strategy/positioning.md"]))  # globs still apply below the constant

    def test_match_glob(self):
        self.assertTrue(lint.match_glob("a/b/c.md", "a/**"))
        self.assertTrue(lint.match_glob("a/c.md", "a/*"))
        self.assertFalse(lint.match_glob("a/b/c.md", "a/*"))
        self.assertTrue(lint.match_glob("memory/transcripts/inbox/x.md", "memory/transcripts/**"))


if __name__ == "__main__":
    unittest.main()


class TestReviewGate(unittest.TestCase):
    def test_needs_review_verdict(self):
        v = review_gate.needs_review_verdict
        team = {"review": {"self_merge": False}}
        solo = {"review": {"self_merge": True}}
        self.assertEqual("success", v(team, "ana", ["ben"], [])[0])
        self.assertEqual("action_required", v(team, "ana", [], [])[0])
        self.assertIn("@ben", v(team, "ana", [], ["@ben"])[1])
        self.assertEqual("success", v(solo, "ana", [], [])[0])
        self.assertEqual("action_required", v({}, "ana", [], [])[0])  # absent means a team
        self.assertTrue(review_gate.self_merge_allowed(SCHEMA) in (True, False))
