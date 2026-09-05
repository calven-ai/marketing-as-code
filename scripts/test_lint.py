#!/usr/bin/env python3
"""Tests for scripts/lint.py: one fixture repo per test, one test per check.

Run from the repo root:  python3 -m unittest scripts/test_lint.py
CI runs it before the lint itself, so a broken check never guards a repo.
"""

import json
import os
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


SKILL = ("---\nname: review\ndescription: Review a draft. Use when asked.\nlicense: MIT\nmetadata:\n  kind: workflow\n"
         "  area: core\n  needs: [seo-data]\n  writes: repo\n  runs: person\n---\n\n# Review\n")


def catalog_entry(**over):
    """A minimal, valid catalog vendor (DataForSEO, stdio, pinned); keyword arguments override fields."""
    vendor = {
        "id": "dataforseo", "name": "DataForSEO", "source": "dataforseo", "verified": "vendor", "checked": TODAY,
        "source_url": "https://example.com/dataforseo", "capabilities": ["keywords"], "writes": False,
        "write_tools": [], "read_only_switch": None, "caveats": [],
        "routes": {"mcp": [{"id": "local", "default": True, "server": "dataforseo", "transport": "stdio",
                            "command": "npx", "args": ["-y", "dataforseo-mcp-server@3.1.1"],
                            "env": {"DATAFORSEO_LOGIN": "${DATAFORSEO_LOGIN}",
                                    "DATAFORSEO_PASSWORD": "${DATAFORSEO_PASSWORD}"},
                            "auth": {"model": "env", "env": ["DATAFORSEO_LOGIN", "DATAFORSEO_PASSWORD"],
                                     "where": "the DataForSEO dashboard"},
                            "headless": True, "oauth_scopes": []}],
                   "cli": None, "script": None}}
    vendor.update(over)
    return vendor


def catalog_category(cid="seo-data", vendors=None, **over):
    data = {"id": cid, "title": cid, "for": "keywords and ranks", "data_domain": "data/seo",
            "manual": {"export": "export the CSV", "drop": "data/seo/snapshots/YYYY-MM-DD-<source>-<what>.csv"},
            "bridges": ["generic"], "vendors": [catalog_entry()] if vendors is None else vendors}
    data.update(over)
    return data


WIRED = {"wired": {"seo-data": {"vendor": "dataforseo", "variant": "local", "routes": ["mcp"],
                                "writes": "n/a", "since": "2026-08-31"}}, "custom_servers": {}}


def render_generated(root, rels=None):
    """Write every generated block the schema expects into the fixture's files (they must match to be clean)."""
    ctx = lint.Ctx(root=root, schema=SCHEMA)
    for rel, blocks in SCHEMA["generated"].items():
        if rel.startswith("_") or rel not in ctx.files or (rels and rel not in rels):
            continue
        for block in blocks:
            lint._write_block(ctx, rel, block)


def make_repo(root):
    """The smallest tree that passes every check."""
    for rel in SCHEMA["required_files"]:
        write(root, rel, "# " + rel + "\n")
    for rel in SCHEMA["required_dirs"]:
        write(root, rel + "/.gitkeep")
    write(root, "content/_template/draft.md", draft("brief"))
    write(root, ".gitignore", ".env\n.env.*\n!.env.example\n")
    write(root, ".env.example", "DATAFORSEO_LOGIN=\nDATAFORSEO_PASSWORD=\n")
    server = {"command": "npx", "args": ["-y", "dataforseo-mcp-server@3.1.1"],
              "env": {"DATAFORSEO_LOGIN": "${DATAFORSEO_LOGIN}", "DATAFORSEO_PASSWORD": "${DATAFORSEO_PASSWORD}"}}
    write(root, ".mcp.json", json.dumps({"mcpServers": {"dataforseo": {"type": "stdio", **server}}}))
    write(root, ".cursor/mcp.json", json.dumps({"mcpServers": {"dataforseo": server}}).replace("${", "${env:"))
    write(root, ".claude/settings.json", json.dumps({"permissions": {
        "deny": list(SCHEMA["settings"]["required_deny"]), "disableBypassPermissionsMode": "disable"}}))
    write(root, "integrations/README.md", "# integrations\n")
    write(root, "integrations/catalog/README.md", "# catalog\n")
    write(root, "integrations/catalog/seo-data.json", json.dumps(catalog_category()))
    write(root, "integrations/wired.json", json.dumps(WIRED))
    write(root, "memory/decision-log.md", "# Decision log\n\nFormat.\n\n---\n")
    enums = SCHEMA["frontmatter"]["content/*/draft.md"]["enums"]
    write(root, "content/README.md", "# content\n\n" + "".join(f"  {k}: " + " | ".join(v) + "\n" for k, v in enums.items()))
    write(root, "docs/README.md", "# docs\n\n- [schema.json](schema.json)\n")
    write(root, "docs/schema.json", json.dumps(SCHEMA))
    write(root, ".agents/skills/review/SKILL.md", SKILL)
    for rel in SCHEMA["context_files"]:
        if "*" in rel:
            continue
        write(root, rel, FRONT.replace("source: repo", "document: x\nsource: repo") if rel.startswith("strategy") else FRONT)
    render_generated(root)
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

    def test_template_placeholder_past_brief_is_error(self):
        write(self.root, "content/2026-09-piece/brief.md", "# Brief\n")
        write(self.root, "content/2026-09-piece/draft.md",
              draft("in-review").replace("Body.", "[The draft. Written in the voice of brand/voice.md]"))
        self.assertTrue(self.findings("content-placeholder", lint.ERROR))
        write(self.root, "content/2026-09-piece/draft.md", draft("in-review").replace("# Title", "# [Title]"))
        self.assertTrue(self.findings("content-placeholder", lint.ERROR))
        write(self.root, "content/2026-09-piece/draft.md", draft("brief").replace("Body.", "[The draft. Text]"))
        self.assertFalse(self.findings("content-placeholder"))

    def test_bracketed_prose_only_warns(self):
        write(self.root, "content/2026-09-piece/brief.md", "# Brief\n")
        write(self.root, "content/2026-09-piece/draft.md", draft("in-review").replace("Body.", "Body. [Editor's note]"))
        self.assertEqual([lint.WARNING], [f.level for f in self.findings("content-placeholder")])

    def test_reference_links_and_colon_brackets_pass(self):
        write(self.root, "content/2026-09-piece/brief.md", "# Brief\n")
        write(self.root, "content/2026-09-piece/draft.md", draft("in-review").replace(
            "Body.", "See [The report][ref] and [Source: Gartner] and [Link](https://example.com).\n\n[ref]: https://example.com"))
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

    def test_status_state_is_case_insensitive(self):
        write(self.root, "projects/launch/brief.md", "# Launch\n")
        write(self.root, "projects/launch/status.md", "# Status\n\n## 2026-01-01\n\n- **State:** On track\n")
        self.assertFalse(self.findings("project-status"))

    def test_readme_state_drift(self):
        write(self.root, "projects/README.md", "# projects\n\nState: on track | done\n")
        self.assertTrue(self.findings("schema-prose", lint.WARNING))
        write(self.root, "projects/README.md", "# projects\n\nState: " + " | ".join(SCHEMA["project_status"]["states"]) + "\n")
        self.assertFalse(self.findings("schema-prose"))


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

    def test_inbox_readme_is_not_a_transcript(self):
        write(self.root, "memory/transcripts/inbox/README.md", "# Inbox\n\nDrop transcripts here.\n")
        self.assertFalse(self.findings("transcript-naming") + self.findings("frontmatter"))


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

    def test_folder_readmes_are_not_reports(self):
        write(self.root, "reports/qmr/README.md", "# qmr\n")
        write(self.root, "reports/recurring/seo/README.md", "# seo\n")
        self.assertFalse(self.findings("report-naming") + self.findings("report-data"))

    def test_qmr_status_vocabulary(self):
        write(self.root, "reports/qmr/2026-q3/report.md", "# QMR\n\n- **Status:** Final\n\n## Data used\n")
        self.assertFalse(self.findings("report-status"))
        write(self.root, "reports/qmr/2026-q3/report.md", "# QMR\n\n- **Status:** done\n\n## Data used\n")
        self.assertTrue(self.findings("report-status", lint.ERROR))

    def test_dashboard_with_example_numbers(self):
        write(self.root, "reports/_templates/dashboard.html", '<html data-example="replace"><title>[Dashboard title]</title>')
        write(self.root, "reports/qmr/2026-q3/dashboard.html", '<html data-example="replace"><title>Q3</title>')
        self.assertTrue(self.findings("report-example", lint.ERROR))
        write(self.root, "reports/qmr/2026-q3/dashboard.html", "<html><title>Q3</title>")
        self.assertFalse(self.findings("report-example"))


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
        write(self.root, "data/crm/snapshots/2026-01-01-hubspot-contacts.csv", "email\nana@gmail.com\n")
        self.assertTrue(self.findings("pii", lint.INFO))  # the template ships repo.private: true
        public = json.loads(json.dumps(SCHEMA))
        public["repo"]["private"] = False
        found = [f for f in lint.run_checks(lint.Ctx(root=self.root, schema=public)) if f.check == "pii"]
        self.assertEqual([lint.WARNING], [f.level for f in found])


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
        messages = [f.message for f in self.findings("skill", lint.ERROR)]
        self.assertTrue(any("`name:`" in m for m in messages))
        self.assertTrue(any("metadata" in m for m in messages))

    def test_skill_metadata_rules(self):
        def skill(meta):
            write(self.root, ".agents/skills/review/SKILL.md", f"---\nname: review\ndescription: x\nmetadata:\n{meta}---\n")
            return [f.message for f in self.findings("skill")]
        self.assertTrue(any("inline list" in m for m in skill("  kind: workflow\n  area: core\n  needs: DataForSEO MCP\n")))
        self.assertTrue(any("`nope`" in m for m in skill("  kind: workflow\n  area: core\n  needs: [nope]\n")))
        self.assertTrue(any("bridge" in m for m in skill("  kind: workflow\n  area: core\n  needs: [generic]\n")))
        self.assertTrue(any("`metadata.area`" in m for m in skill("  kind: workflow\n  needs: []\n")))
        self.assertTrue(any("`metadata.kind`" in m for m in skill("  kind: agent\n  area: core\n  needs: []\n")))
        self.assertTrue(any("cadence" in m for m in skill("  kind: role\n  area: core\n  needs: []\n")))
        self.assertTrue(any("never runs unattended" in m for m in
                            skill("  kind: workflow\n  area: core\n  needs: []\n  writes: external\n  runs: either\n")))
        self.assertTrue(any("typo" in m for m in skill("  kind: workflow\n  area: core\n  needs: []\n  cost: high\n")))
        self.assertEqual([], skill("  kind: role\n  area: seo\n  needs: [seo-data]\n  optional: [crm]\n  cadence: weekly\n"
                                   "  writes: repo\n  runs: either\n"))

    def test_paths_and_links(self):
        write(self.root, ".agents/skills/review/SKILL.md", SKILL +
              "Run `scripts/nope.py` and read `strategy/positioning.md`. See [x](../../../docs/nope.md).\n\n"
              "## Worked example\n\nEdit `projects/q4/status.md`.\n")
        paths = [f for f in self.findings("path")]
        self.assertEqual(1, len(paths))
        self.assertEqual(lint.ERROR, paths[0].level)
        self.assertTrue(self.findings("link", lint.ERROR))

    def test_generated_block_and_docs_index(self):
        write(self.root, "agents/README.md", "# Roster\n\n<!-- generated:skills-core -->\nstale\n<!-- /generated:skills-core -->\n")
        write(self.root, "docs/extra.md", "# Extra doc\n")
        found = self.findings("generated") + self.findings("docs-index")
        self.assertTrue(all(f.fixable for f in found))
        blocks = {m.group(1) for m in (__import__("re").search(r"`([a-z-]+)`", f.message) for f in found) if m}
        self.assertIn("skills-core", blocks)
        self.assertIn("skills-leadership", blocks)
        self.fix()
        self.assertFalse(self.findings("generated") + self.findings("docs-index"))
        self.assertIn("extra.md", (self.root / "docs/README.md").read_text())
        roster = (self.root / "agents/README.md").read_text()
        self.assertIn("| Skill | Kind | What it does | Needs |", roster)
        self.assertIn("[review](../.agents/skills/review/SKILL.md) | workflow | Review a draft | "
                      "[seo-data](../integrations/catalog/README.md#seo-data)", roster)

    def test_roster_area_block(self):
        write(self.root, ".agents/skills/pipeline-report/SKILL.md", SKILL.replace("name: review", "name: pipeline-report")
              .replace("area: core", "area: ops").replace("kind: workflow", "kind: role\n  cadence: weekly")
              .replace("needs: [seo-data]", "needs: [seo-data]\n  optional: [crm]"))
        block = lint.render_block(self.ctx(), "skills-ops")
        self.assertIn("| role (weekly) |", block)
        self.assertIn("(optional: [crm](../integrations/catalog/README.md#crm))", block)
        self.assertNotIn("[review]", block)
        with self.assertRaises(ValueError):
            lint.render_block(self.ctx(), "skills-nope")


class TestCatalog(LintCase):
    def put(self, cid="seo-data", **over):
        write(self.root, f"integrations/catalog/{cid}.json", json.dumps(catalog_category(cid, **over)))
        return [f for f in self.findings("catalog")]

    def test_fixture_catalog_is_clean(self):
        self.assertFalse(self.findings("catalog"))

    def test_invalid_json_and_unknown_category(self):
        write(self.root, "integrations/catalog/crm.json", "{not json")
        self.assertTrue(any("not valid JSON" in f.message for f in self.findings("catalog", lint.ERROR)))
        write(self.root, "integrations/catalog/crm.json", json.dumps(catalog_category("nope")))
        self.assertTrue(any("`id` must equal" in f.message for f in self.findings("catalog", lint.ERROR)))

    def test_manual_route_is_required(self):
        found = self.put(manual={})
        self.assertTrue(any("`manual`" in f.message for f in found))

    def test_unpinned_and_undeclared_placeholder_and_oauth_headless(self):
        loose = catalog_entry()
        loose["routes"]["mcp"][0]["args"] = ["-y", "dataforseo-mcp-server"]
        self.assertTrue(any("not pinned" in f.message for f in self.put(vendors=[loose])))
        undeclared = catalog_entry()
        undeclared["routes"]["mcp"][0]["auth"]["env"] = ["DATAFORSEO_LOGIN"]
        self.assertTrue(any("`auth.env`" in f.message for f in self.put(vendors=[undeclared])))
        oauth = catalog_entry()
        oauth["routes"]["mcp"][0].update({"transport": "http", "url": "https://mcp.example.com", "env": {},
                                          "auth": {"model": "oauth", "env": [], "where": "browser"}, "headless": True})
        self.assertTrue(any("cannot run headless" in f.message for f in self.put(vendors=[oauth])))

    def test_two_defaults_and_stale_check(self):
        two = catalog_entry()
        second = dict(two["routes"]["mcp"][0], id="remote")
        two["routes"]["mcp"].append(second)
        self.assertTrue(any("exactly one" in f.message for f in self.put(vendors=[two])))
        old = catalog_entry(checked="2020-01-01")
        found = self.put(vendors=[old])
        self.assertEqual([lint.WARNING], [f.level for f in found])
        self.assertIn("re-verify", found[0].message)

    def test_verified_enum_source_token_and_placeholder_url(self):
        self.assertTrue(any("`verified`" in f.message for f in self.put(vendors=[catalog_entry(verified="maybe")])))
        self.assertTrue(any("`source`" in f.message for f in self.put(vendors=[catalog_entry(source="data-for-seo")])))
        hosted = catalog_entry()
        hosted["routes"]["mcp"][0].update({"transport": "http", "url": "${DATAFORSEO_MCP_URL}", "env": {},
                                           "auth": {"model": "env", "env": ["DATAFORSEO_MCP_URL"], "where": "the account"}})
        self.assertFalse(self.put(vendors=[hosted]))
        hosted["routes"]["mcp"][0]["url"] = ""
        self.assertTrue(any("needs a `url`" in f.message for f in self.put(vendors=[hosted])))

    def test_missing_script_path(self):
        v = catalog_entry()
        v["routes"]["script"] = {"path": "scripts/nope.py", "env": [], "notes": ""}
        self.assertTrue(any("does not exist" in f.message for f in self.put(vendors=[v])))


class TestWired(LintCase):
    def test_fixture_is_bound(self):
        self.assertFalse(self.findings("wired"))

    def test_wired_server_missing_from_mcp_json(self):
        write(self.root, ".mcp.json", json.dumps({"mcpServers": {}}))
        write(self.root, ".cursor/mcp.json", json.dumps({"mcpServers": {}}))
        found = self.findings("wired", lint.ERROR)
        self.assertTrue(any("not in .mcp.json" in f.message for f in found))

    def test_unbound_server_warns_unless_custom(self):
        mcp = json.loads((self.root / ".mcp.json").read_text())
        mcp["mcpServers"]["other"] = {"type": "http", "url": "https://x.example.com"}
        write(self.root, ".mcp.json", json.dumps(mcp))
        cursor = json.loads((self.root / ".cursor/mcp.json").read_text())
        cursor["mcpServers"]["other"] = {"url": "https://x.example.com"}
        write(self.root, ".cursor/mcp.json", json.dumps(cursor))
        self.assertTrue(any("`other`" in f.message for f in self.findings("wired", lint.WARNING)))
        wired = json.loads(json.dumps(WIRED))
        wired["custom_servers"] = {"other": "the team's own server"}
        write(self.root, "integrations/wired.json", json.dumps(wired))
        self.assertFalse(self.findings("wired"))

    def test_denied_writes_need_rules_and_fix_adds_them(self):
        write(self.root, "integrations/catalog/crm.json", json.dumps(catalog_category(
            "crm", data_domain="data/crm", vendors=[catalog_entry(
                id="hubspot", name="HubSpot", source="hubspot", writes=True, write_tools=["create_contact"],
                routes={"mcp": [{"id": "oauth", "default": True, "server": "hubspot", "transport": "http",
                                 "url": "https://mcp.example.com", "headers": {},
                                 "auth": {"model": "oauth", "env": [], "where": "browser"},
                                 "headless": False, "oauth_scopes": []}], "cli": None, "script": None})])))
        wired = json.loads(json.dumps(WIRED))
        wired["wired"]["crm"] = {"vendor": "hubspot", "variant": "oauth", "routes": ["mcp"], "writes": "denied",
                                 "since": TODAY}
        write(self.root, "integrations/wired.json", json.dumps(wired))
        for rel in (".mcp.json", ".cursor/mcp.json"):
            data = json.loads((self.root / rel).read_text())
            data["mcpServers"]["hubspot"] = {"url": "https://mcp.example.com"}
            if rel == ".mcp.json":
                data["mcpServers"]["hubspot"]["type"] = "http"
            write(self.root, rel, json.dumps(data))
        write(self.root, ".agents/skills/review/SKILL.md", SKILL.replace("needs: [seo-data]", "needs: [seo-data, crm]"))
        render_generated(self.root)
        found = self.findings("wired", lint.ERROR)
        self.assertTrue(found and found[0].fixable and "mcp__hubspot__create_contact" in found[0].message)
        self.fix()
        self.assertFalse(self.findings("wired"))
        deny = json.loads((self.root / ".claude/settings.json").read_text())["permissions"]["deny"]
        self.assertIn("mcp__hubspot__create_contact", deny)

    def test_unknown_vendor_or_variant(self):
        wired = json.loads(json.dumps(WIRED))
        wired["wired"]["seo-data"]["variant"] = "remote"
        write(self.root, "integrations/wired.json", json.dumps(wired))
        self.assertTrue(any("variant" in f.message for f in self.findings("wired", lint.ERROR)))
        wired["wired"]["seo-data"].update({"vendor": "nope", "variant": "local"})
        write(self.root, "integrations/wired.json", json.dumps(wired))
        self.assertTrue(any("not in integrations/catalog" in f.message for f in self.findings("wired", lint.ERROR)))


class TestCoverage(LintCase):
    def test_unused_category_warns_and_missing_file_errors(self):
        write(self.root, "integrations/catalog/crm.json", json.dumps(catalog_category("crm", data_domain="data/crm", vendors=[])))
        found = self.findings("catalog-coverage")
        self.assertEqual([lint.WARNING], [f.level for f in found])
        self.assertEqual("integrations/catalog/crm.json", found[0].path)
        write(self.root, ".agents/skills/review/SKILL.md", SKILL.replace("needs: [seo-data]", "needs: [seo-data, crm, ads]"))
        found = self.findings("catalog-coverage")
        self.assertEqual([lint.ERROR], [f.level for f in found])
        self.assertIn("integrations/catalog/ads.json", found[0].message)


class TestRoleWorkflows(LintCase):
    def caller(self, skill):
        write(self.root, ".github/workflows/role-x.yml", f"on: schedule\njobs:\n  run:\n    uses: ./.github/workflows/role-run.yml\n    with:\n      skill: {skill}\n")
        write(self.root, "docs/operating-model.md", "# op\n\nrole-x.yml\n")
        return self.findings("role-workflow")

    def test_headless_role_passes_and_oauth_or_external_fails(self):
        write(self.root, ".agents/skills/brand-monitor/SKILL.md", SKILL.replace("name: review", "name: brand-monitor")
              .replace("kind: workflow", "kind: role\n  cadence: monthly").replace("runs: person", "runs: either"))
        self.assertFalse(self.caller("brand-monitor"))
        self.assertTrue(any("does not exist" in f.message for f in self.caller("nope")))
        write(self.root, ".agents/skills/publish/SKILL.md", SKILL.replace("name: review", "name: publish")
              .replace("writes: repo", "writes: external"))
        self.assertTrue(any("external systems" in f.message for f in self.caller("publish")))
        oauth = catalog_entry()
        oauth["routes"]["mcp"][0].update({"transport": "http", "url": "https://mcp.example.com", "env": {},
                                          "auth": {"model": "oauth", "env": [], "where": "browser"}, "headless": False})
        write(self.root, "integrations/catalog/seo-data.json", json.dumps(catalog_category(vendors=[oauth])))
        render_generated(self.root)
        self.assertTrue(any("key-based" in f.message for f in self.caller("brand-monitor")))


class TestThirdParty(LintCase):
    def test_reference_header_needs_registry_row_and_license(self):
        header = "<!-- source: https://github.com/x/y | license: MIT | fetched: 2026-09-04 -->\n\n# Notes\n"
        write(self.root, ".agents/skills/review/references/y.md", header)
        write(self.root, ".agents/skills/review/SKILL.md", SKILL.replace("license: MIT\n", ""))
        found = self.findings("third-party")
        self.assertEqual({lint.ERROR, lint.WARNING}, {f.level for f in found})
        write(self.root, "THIRD_PARTY.md", "# Third-party\n\n| `.agents/skills/review/references/y.md` | https://github.com/x/y | MIT |\n")
        write(self.root, ".agents/skills/review/SKILL.md", SKILL)
        self.assertFalse(self.findings("third-party"))
        write(self.root, ".agents/skills/review/references/own.md", "# Our own notes\n")
        self.assertFalse(self.findings("third-party"))


class TestMcpShape(LintCase):
    def test_unpinned_and_untyped_url_and_cursor_placeholder(self):
        write(self.root, ".mcp.json", json.dumps({"mcpServers": {
            "dataforseo": {"type": "stdio", "command": "npx", "args": ["-y", "dataforseo-mcp-server"]},
            "x": {"url": "https://x.example.com"}}}))
        write(self.root, ".cursor/mcp.json", json.dumps({"mcpServers": {
            "dataforseo": {"type": "stdio", "command": "npx", "args": ["-y", "dataforseo-mcp-server@1.0.0"]},
            "x": {"url": "https://x.example.com", "headers": {"Authorization": "Bearer ${X_KEY}"}}}}))
        messages = [f.message for f in self.findings("mcp")]
        self.assertTrue(any("pinned" in m for m in messages))
        self.assertTrue(any('"type": "http"' in m for m in messages))
        self.assertTrue(any("Cursor entries carry no" in m for m in messages))
        self.assertTrue(any("${env:VAR}" in m for m in messages))

    def test_secrets_doc_row(self):
        write(self.root, "docs/secrets.md", "# Secrets\n\n| `DATAFORSEO_LOGIN` |\n")
        found = self.findings("mcp-env", lint.WARNING)
        self.assertTrue(any(f.path == "docs/secrets.md" and "DATAFORSEO_PASSWORD" in f.message for f in found))


class TestCompetitive(LintCase):
    def test_battlecards_carry_frontmatter_and_age(self):
        write(self.root, "strategy/competitive/README.md", "# competitive\n")
        write(self.root, "strategy/competitive/_battlecard-template.md", "# [Competitor]\n")
        self.assertClean()
        write(self.root, "strategy/competitive/acme.md", "# Acme\n")
        self.assertTrue(self.findings("frontmatter", lint.ERROR))
        write(self.root, "strategy/competitive/acme.md", "---\nlast_reviewed: 2020-01-01\nowner: Ana\n---\n\n# Acme\n")
        self.assertFalse(self.findings("frontmatter"))
        self.assertTrue(self.findings("context-stale", lint.WARNING))


class TestAdoption(LintCase):
    def test_clean_fixture_has_no_residue(self):
        self.assertFalse(self.findings("adoption"))

    def test_each_marker_is_reported(self):
        write(self.root, ".github/CODEOWNERS", "strategy/ @owner-placeholder\n")
        write(self.root, "SECURITY.md", "# Security\n\nhttps://github.com/calven-ai/marketing-as-code/security\n")
        write(self.root, "CODE_OF_CONDUCT.md", "# Conduct\n\noss@calven.ai\n")
        write(self.root, "memory/decision-log.md", "# Log\n\n---\n\n## 2026-09-01: x\n\n- **Decided by:** Ana (repository maintainer)\n"
              "- **Source:** a\n- **Context:** b\n- **Follow-ups:** none\n")
        write(self.root, "data/seo/keywords.csv", "keyword,intent,target_url,difficulty,volume,current_rank,last_checked,notes\n"
              "x,commercial,/x,1,1,1,2026-01-01,example row: replace me\n")
        found = self.findings("adoption")
        self.assertEqual(5, len(found))
        self.assertTrue(all(f.level == lint.INFO and "make-it-yours" in f.message for f in found))

    def test_example_company_is_flagged_once_templates_are_filled(self):
        write(self.root, "examples/beacon/strategy/positioning.md", "# Beacon\n")
        self.assertTrue(any(f.path == "examples" for f in self.findings("adoption")))
        for rel in SCHEMA["templates"]:
            if not rel.startswith("_"):
                write(self.root, rel, "# t\n\n> **" + SCHEMA["templates"][rel] + ".**\n")
        self.assertFalse(any(f.path == "examples" for f in self.findings("adoption")))

    def test_public_repo_with_personal_data(self):
        write(self.root, "data/accounts/target-accounts.csv", "company,domain,tier,owner,status,notes\nAcme,acme.com,1,,prospect,\n")
        self.assertFalse(self.findings("adoption"))  # ships private: true
        public = json.loads(json.dumps(SCHEMA))
        public["repo"]["private"] = False
        found = [f for f in lint.run_checks(lint.Ctx(root=self.root, schema=public)) if f.check == "adoption"]
        self.assertTrue(any("repo.private" in f.message for f in found))


class TestScriptsIndex(LintCase):
    def test_scripts_block_lists_shell_hooks_and_tests(self):
        write(self.root, "scripts/doctor.py", '"""Health check.\n\nMore."""\n')
        write(self.root, "scripts/test_lint.py", '"""Tests for lint."""\n')
        write(self.root, "scripts/with_env.sh", "#!/bin/sh\n# Start a command\n# with .env loaded.\n#\n# Usage.\n")
        write(self.root, "scripts/hooks/pre-push", "#!/bin/sh\n# Refuses a push to main.\n\nexit 0\n")
        block = lint.render_block(self.ctx(), "scripts")
        self.assertIn("| [doctor.py](doctor.py) | Health check. |", block)
        self.assertIn("| [test_lint.py](test_lint.py) | Tests for lint. |", block)
        self.assertIn("| [with_env.sh](with_env.sh) | Start a command with .env loaded. |", block)
        self.assertIn("| [hooks/pre-push](hooks/pre-push) | Refuses a push to main. |", block)


class TestExample(LintCase):
    """examples/beacon/ mirrors the real tree; overlaid on the fixture it must pass every check."""

    def test_beacon_passes_every_check(self):
        src = ROOT / "examples" / "beacon"
        if not src.is_dir():
            self.skipTest("no examples/beacon in this checkout")
        overlaid = []
        for path in src.rglob("*"):
            if path.is_file():
                rel = path.relative_to(src).as_posix()
                write(self.root, rel, path.read_bytes())
                overlaid.append(rel)
        self.assertGreater(len(overlaid), 20)
        found = [f for f in self.findings() if f.level != lint.INFO and f.check != "context-stale"]
        self.assertEqual([], [(f.path, f.message) for f in found])
        self.assertEqual([], [f.path for f in self.findings("template") if f.path in overlaid])
        self.assertTrue(any(f.path.startswith("reports/qmr/") for f in self.findings("report-example")) is False)


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

    def test_repository_variable_overrides_the_file(self):
        team = {"review": {"self_merge": False}}
        os.environ["REVIEW_SELF_MERGE"] = "true"
        try:
            self.assertTrue(review_gate.self_merge_allowed(team))
            self.assertEqual("success", review_gate.needs_review_verdict(team, "ana", [], [])[0])
        finally:
            os.environ.pop("REVIEW_SELF_MERGE", None)
        self.assertFalse(review_gate.self_merge_allowed(team))
    def test_rule_changing_proposals_are_not_tidied(self):
        self.assertTrue(review_gate.tidy_allowed(["memory/decision-log.md", "projects/x/status.md"]))
        self.assertFalse(review_gate.tidy_allowed(["scripts/lint.py", "scripts/README.md"]))
        self.assertFalse(review_gate.tidy_allowed(["docs/schema.json"]))


if __name__ == "__main__":
    unittest.main()
