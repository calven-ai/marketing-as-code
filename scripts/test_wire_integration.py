#!/usr/bin/env python3
"""Tests for scripts/wire_integration.py: a temp checkout with a two-category
catalog per test, never the live catalog.

Run from the repo root:  python3 -m unittest scripts/test_wire_integration.py
"""

import contextlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import wire_integration as wi  # noqa: E402

SCRIPT = Path(__file__).resolve().parent / "wire_integration.py"

CRM = {
    "id": "crm", "title": "CRM", "for": "pipeline, contacts, deals",
    "data_domain": "data/crm",
    "manual": {"export": "CRM > Reports > export CSV", "drop": "data/crm/snapshots/YYYY-MM-DD-<source>-<what>.csv"},
    "bridges": ["generic"],
    "vendors": [
        {
            "id": "hubspot", "name": "HubSpot", "source": "hubspot", "verified": "vendor",
            "checked": "2026-09-04", "source_url": "https://developers.hubspot.com/mcp",
            "capabilities": ["contacts", "deals"],
            "writes": True, "write_tools": ["create_contact", "update_contact"],
            "read_only_switch": None, "caveats": ["OAuth only; cannot run headless"],
            "routes": {
                "mcp": [
                    {"id": "oauth", "default": True, "server": "hubspot", "transport": "http",
                     "url": "https://mcp.hubspot.com/anthropic",
                     "auth": {"model": "oauth", "env": [], "where": "browser grant"},
                     "headless": False, "oauth_scopes": ["crm.objects.contacts.read"]},
                    {"id": "token", "default": False, "server": "hubspot", "transport": "http",
                     "url": "https://mcp.hubspot.com/anthropic",
                     "headers": {"Authorization": "Bearer ${HUBSPOT_TOKEN}"},
                     "auth": {"model": "key", "env": ["HUBSPOT_TOKEN"], "where": "HubSpot > Settings > Private apps"},
                     "headless": True, "oauth_scopes": []},
                ],
                "cli": {"tool": "hubspot", "install": "HubSpot agent CLI", "notes": "headless snapshots"},
                "script": {"path": None, "notes": "copy scripts/seo_snapshot.py"},
            },
        },
        {
            "id": "shady", "name": "Shady CRM", "source": "shady", "verified": "unverified",
            "checked": "2026-09-04", "source_url": "https://example.com/shady",
            "writes": False, "write_tools": [], "read_only_switch": None,
            "routes": {"mcp": [{"id": "key", "default": True, "server": "shady", "transport": "http",
                                "url": "https://mcp.example.com/shady",
                                "auth": {"model": "key", "env": ["SHADY_KEY"], "where": "somewhere"},
                                "headless": True, "oauth_scopes": []}]},
        },
        {
            "id": "paper", "name": "Paper CRM", "source": "paper", "verified": "listing",
            "checked": "2026-09-04", "writes": False, "write_tools": [], "read_only_switch": None,
            "routes": {"cli": {"tool": "paper", "install": "brew install paper", "notes": ""}},
        },
    ],
}

ANALYTICS = {
    "id": "web-analytics", "title": "Web analytics", "data_domain": "data/analytics",
    "manual": {"export": "Analytics > Export", "drop": "data/analytics/snapshots/"},
    "bridges": [],
    "vendors": [{
        "id": "posthog", "name": "PostHog", "source": "posthog", "verified": "vendor",
        "checked": "2026-09-04", "source_url": "https://posthog.com/docs/model-context-protocol",
        "writes": True, "write_tools": [],
        "read_only_switch": {"kind": "env", "name": "READ_ONLY", "value": "true"},
        "routes": {
            "mcp": [{"id": "local", "default": True, "server": "posthog", "transport": "stdio",
                     "command": "npx", "args": ["-y", "posthog-mcp@1.0.0"],
                     "env": {"POSTHOG_API_KEY": "${POSTHOG_API_KEY}"},
                     "auth": {"model": "key", "env": ["POSTHOG_API_KEY"], "where": "PostHog > Settings > Personal API keys"},
                     "headless": True, "oauth_scopes": []}],
            "script": {"path": "scripts/posthog_snapshot.py", "notes": ""},
        },
    }],
}

SCHEMA = {
    "mcp": {"files": [".mcp.json", ".cursor/mcp.json"], "placeholder": "\\$\\{(?:env:)?([A-Z][A-Z0-9_]*)\\}"},
    "catalog": {"dir": "integrations/catalog", "wired": "integrations/wired.json",
                "categories": ["crm", "web-analytics", "chat"]},
}

MCP = {"mcpServers": {"dataforseo": {"type": "stdio", "command": "npx", "args": ["-y", "dataforseo-mcp-server@3.1.1"],
                                     "env": {"DATAFORSEO_LOGIN": "${DATAFORSEO_LOGIN}"}}}}
SETTINGS = {"permissions": {"allow": ["Bash(python3 scripts/lint.py*)"], "deny": ["Read(./.env)", "Bash(env)"]}}


def write(root, rel, text):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def make_repo(root):
    write(root, "docs/schema.json", json.dumps(SCHEMA))
    write(root, "integrations/catalog/crm.json", json.dumps(CRM, indent=2))
    write(root, "integrations/catalog/web-analytics.json", json.dumps(ANALYTICS, indent=2))
    write(root, ".mcp.json", wi.dump_json(MCP))
    write(root, ".cursor/mcp.json", wi.dump_json(MCP).replace("${", "${env:").replace('"type": "stdio",\n', ""))
    write(root, ".env.example", "# DataForSEO\nDATAFORSEO_LOGIN=\nDATAFORSEO_PASSWORD=\n")
    write(root, ".claude/settings.json", wi.dump_json(SETTINGS))
    write(root, ".agents/skills/pipeline-review/SKILL.md",
          "---\nname: pipeline-review\ndescription: Review the pipeline.\nmetadata:\n  kind: workflow\n  needs: [crm]\n---\n\n# Pipeline\n")
    write(root, ".agents/skills/review/SKILL.md",
          "---\nname: review\ndescription: Review a draft.\nmetadata:\n  kind: workflow\n  needs: []\n---\n\n# Review\n")
    return root


class WireCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="mac-wire-"))
        self.root = make_repo(self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_cli(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = wi.main(["--root", str(self.root), *argv])
        return code, out.getvalue(), err.getvalue()

    def read(self, rel):
        return (self.root / rel).read_text(encoding="utf-8")

    def load(self, rel):
        return json.loads(self.read(rel))

    def snapshot(self):
        return {rel: self.read(rel) for rel in
                (".mcp.json", ".cursor/mcp.json", ".env.example", ".claude/settings.json")
                if (self.root / rel).is_file()}


class TestWireHttp(WireCase):
    def test_wires_default_variant_everywhere(self):
        code, out, err = self.run_cli("hubspot")
        self.assertEqual(0, code, err)
        mcp = self.load(".mcp.json")["mcpServers"]
        self.assertIn("dataforseo", mcp)
        self.assertEqual({"type": "http", "url": "https://mcp.hubspot.com/anthropic",
                          "oauth": {"scopes": ["crm.objects.contacts.read"]}}, mcp["hubspot"])
        self.assertEqual(["dataforseo", "hubspot"], list(mcp))
        cursor = self.load(".cursor/mcp.json")["mcpServers"]
        self.assertNotIn("type", cursor["hubspot"])
        self.assertEqual("https://mcp.hubspot.com/anthropic", cursor["hubspot"]["url"])
        deny = self.load(".claude/settings.json")["permissions"]["deny"]
        self.assertEqual(["Read(./.env)", "Bash(env)", "mcp__hubspot__create_contact", "mcp__hubspot__update_contact"], deny)
        wired = self.load("integrations/wired.json")
        self.assertEqual({"vendor": "hubspot", "variant": "oauth", "routes": ["mcp"], "writes": "denied",
                          "since": wi.dt.date.today().isoformat()}, wired["wired"]["crm"])
        self.assertEqual({}, wired["custom_servers"])
        # OAuth, no env vars: .env.example untouched.
        self.assertEqual("# DataForSEO\nDATAFORSEO_LOGIN=\nDATAFORSEO_PASSWORD=\n", self.read(".env.example"))
        self.assertIn("[mcp_servers.hubspot]", out)
        self.assertIn("| HubSpot | per person, OAuth |", out)
        self.assertIn("run: python3 scripts/lint.py --fix", out)
        self.assertTrue(self.read(".mcp.json").endswith("}\n"))

    def test_named_variant_with_bearer_header(self):
        code, out, err = self.run_cli("hubspot:token")
        self.assertEqual(0, code, err)
        mcp = self.load(".mcp.json")["mcpServers"]["hubspot"]
        self.assertEqual({"Authorization": "Bearer ${HUBSPOT_TOKEN}"}, mcp["headers"])
        self.assertNotIn("oauth", mcp)
        cursor = self.load(".cursor/mcp.json")["mcpServers"]["hubspot"]
        self.assertEqual({"Authorization": "Bearer ${env:HUBSPOT_TOKEN}"}, cursor["headers"])
        env = self.read(".env.example")
        self.assertIn("# HubSpot (crm): HubSpot > Settings > Private apps\nHUBSPOT_TOKEN=\n", env)
        self.assertEqual(1, env.count("HUBSPOT_TOKEN="))
        self.assertIn('bearer_token_env_var = "HUBSPOT_TOKEN"', out)
        self.assertIn("| `HUBSPOT_TOKEN` | per person |", out)
        self.assertEqual("token", self.load("integrations/wired.json")["wired"]["crm"]["variant"])

    def test_second_run_is_a_no_op(self):
        self.run_cli("hubspot:token")
        before = self.snapshot()
        wired_before = self.read("integrations/wired.json")
        code, out, err = self.run_cli("hubspot:token")
        self.assertEqual(0, code, err)
        self.assertIn("nothing to change", out)
        self.assertEqual(before, self.snapshot())
        self.assertEqual(wired_before, self.read("integrations/wired.json"))
        self.assertEqual(1, self.read(".env.example").count("HUBSPOT_TOKEN="))
        deny = self.load(".claude/settings.json")["permissions"]["deny"]
        self.assertEqual(len(deny), len(set(deny)))

    def test_allow_writes_skips_deny_and_records_allowed(self):
        code, out, err = self.run_cli("hubspot", "--allow-writes")
        self.assertEqual(0, code, err)
        deny = self.load(".claude/settings.json")["permissions"]["deny"]
        self.assertFalse([d for d in deny if d.startswith("mcp__")])
        self.assertEqual("allowed", self.load("integrations/wired.json")["wired"]["crm"]["writes"])
        self.assertIn("human gate", out)


class TestWireStdio(WireCase):
    def test_read_only_env_switch_and_whole_server_deny(self):
        code, out, err = self.run_cli("posthog")
        self.assertEqual(0, code, err)
        entry = self.load(".mcp.json")["mcpServers"]["posthog"]
        self.assertEqual({"type": "stdio", "command": "npx", "args": ["-y", "posthog-mcp@1.0.0"],
                          "env": {"POSTHOG_API_KEY": "${POSTHOG_API_KEY}", "READ_ONLY": "true"}}, entry)
        cursor = self.load(".cursor/mcp.json")["mcpServers"]["posthog"]
        self.assertEqual({"command": "npx", "args": ["-y", "posthog-mcp@1.0.0"],
                          "env": {"POSTHOG_API_KEY": "${env:POSTHOG_API_KEY}", "READ_ONLY": "true"}}, cursor)
        self.assertIn("# PostHog (web-analytics): PostHog > Settings > Personal API keys\nPOSTHOG_API_KEY=\n",
                      self.read(".env.example"))
        deny = self.load(".claude/settings.json")["permissions"]["deny"]
        self.assertIn("mcp__posthog", deny)
        self.assertIn("whole server", out)
        wired = self.load("integrations/wired.json")["wired"]["web-analytics"]
        self.assertEqual(["mcp", "script"], wired["routes"])
        self.assertEqual("denied", wired["writes"])
        self.assertIn('command = "npx"', out)
        self.assertIn('env = { POSTHOG_API_KEY = "", READ_ONLY = "true" }', out)

    def test_allow_writes_drops_the_switch(self):
        code, _out, err = self.run_cli("posthog", "--allow-writes")
        self.assertEqual(0, code, err)
        self.assertNotIn("READ_ONLY", self.load(".mcp.json")["mcpServers"]["posthog"]["env"])
        self.assertNotIn("mcp__posthog", self.load(".claude/settings.json")["permissions"]["deny"])

    def test_other_switch_kinds(self):
        entry = {"type": "http", "url": "https://x.example/mcp"}
        wi.apply_switch(entry, {"kind": "url", "name": "readonly", "value": "true"})
        self.assertEqual("https://x.example/mcp?readonly=true", entry["url"])
        wi.apply_switch(entry, {"kind": "url", "name": "readonly", "value": "true"})
        self.assertEqual("https://x.example/mcp?readonly=true", entry["url"])
        entry = {"type": "http", "url": "https://x.example/mcp"}
        wi.apply_switch(entry, {"kind": "url", "name": "path", "value": "readonly"})
        self.assertEqual("https://x.example/mcp/readonly", entry["url"])
        wi.apply_switch(entry, {"kind": "header", "name": "Close-Scope", "value": "mcp.read"})
        self.assertEqual({"Close-Scope": "mcp.read"}, entry["headers"])
        entry = {"type": "stdio", "command": "npx", "args": ["-y", "pkg"]}
        wi.apply_switch(entry, {"kind": "arg", "name": "--read-only", "value": None})
        wi.apply_switch(entry, {"kind": "arg", "name": "--read-only", "value": None})
        self.assertEqual(["-y", "pkg", "--read-only"], entry["args"])


class TestRefusals(WireCase):
    def test_unknown_vendor_and_variant(self):
        code, _out, err = self.run_cli("nothing")
        self.assertEqual(1, code)
        self.assertIn("unknown vendor", err)
        code, _out, err = self.run_cli("hubspot:nope")
        self.assertEqual(1, code)
        self.assertIn("no MCP variant", err)
        self.assertNotIn("hubspot", self.load(".mcp.json")["mcpServers"])

    def test_unverified_needs_force(self):
        code, _out, err = self.run_cli("shady")
        self.assertEqual(1, code)
        self.assertIn("unverified", err)
        self.assertNotIn("shady", self.load(".mcp.json")["mcpServers"])
        code, _out, err = self.run_cli("shady", "--force")
        self.assertEqual(0, code, err)
        self.assertIn("shady", self.load(".mcp.json")["mcpServers"])
        self.assertEqual("n/a", self.load("integrations/wired.json")["wired"]["crm"]["writes"])

    def test_no_mcp_route(self):
        code, _out, err = self.run_cli("paper")
        self.assertEqual(1, code)
        self.assertIn("no MCP route", err)
        self.assertIn("cli/script/manual", err)

    def test_server_bound_to_another_vendor(self):
        self.run_cli("hubspot")
        crm = json.loads(self.read("integrations/catalog/crm.json"))
        crm["vendors"][1]["routes"]["mcp"][0]["server"] = "hubspot"
        crm["vendors"][1]["verified"] = "vendor"
        write(self.root, "integrations/catalog/crm.json", json.dumps(crm))
        code, _out, err = self.run_cli("shady")
        self.assertEqual(1, code)
        self.assertIn("bound to hubspot", err)

    def test_category_narrows_and_unknown_category_refuses(self):
        code, _out, err = self.run_cli("hubspot", "--category", "web-analytics")
        self.assertEqual(1, code)
        self.assertIn("not listed under category", err)
        code, _out, err = self.run_cli("hubspot", "--category", "crm")
        self.assertEqual(0, code, err)


class TestDryRun(WireCase):
    def test_dry_run_writes_nothing(self):
        before = self.snapshot()
        code, out, err = self.run_cli("posthog", "--dry-run")
        self.assertEqual(0, code, err)
        self.assertEqual(before, self.snapshot())
        self.assertFalse((self.root / "integrations/wired.json").exists())
        self.assertIn("dry run", out)
        self.assertIn('"READ_ONLY": "true"', out)
        self.assertIn("${env:POSTHOG_API_KEY}", out)
        self.assertIn("POSTHOG_API_KEY=", out)

    def test_dry_run_unwire_writes_nothing(self):
        self.run_cli("posthog")
        before = self.snapshot()
        wired = self.read("integrations/wired.json")
        code, out, err = self.run_cli("--unwire", "posthog", "--dry-run")
        self.assertEqual(0, code, err)
        self.assertIn("dry run", out)
        self.assertEqual(before, self.snapshot())
        self.assertEqual(wired, self.read("integrations/wired.json"))


class TestUnwire(WireCase):
    def test_unwire_removes_servers_and_binding(self):
        self.run_cli("posthog")
        code, out, err = self.run_cli("--unwire", "posthog")
        self.assertEqual(0, code, err)
        self.assertNotIn("posthog", self.load(".mcp.json")["mcpServers"])
        self.assertNotIn("posthog", self.load(".cursor/mcp.json")["mcpServers"])
        self.assertIn("dataforseo", self.load(".mcp.json")["mcpServers"])
        self.assertNotIn("web-analytics", self.load("integrations/wired.json")["wired"])
        self.assertIn("POSTHOG_API_KEY=", self.read(".env.example"))
        self.assertIn("mcp__posthog", self.load(".claude/settings.json")["permissions"]["deny"])
        self.assertIn("left alone", out)

    def test_unwire_refuses_when_a_skill_needs_the_category(self):
        self.run_cli("hubspot")
        code, _out, err = self.run_cli("--unwire", "hubspot")
        self.assertEqual(1, code)
        self.assertIn("pipeline-review", err)
        self.assertIn("hubspot", self.load(".mcp.json")["mcpServers"])
        code, _out, err = self.run_cli("--unwire", "hubspot", "--force")
        self.assertEqual(0, code, err)
        self.assertNotIn("hubspot", self.load(".mcp.json")["mcpServers"])

    def test_unwire_unknown(self):
        code, _out, err = self.run_cli("--unwire", "posthog")
        self.assertEqual(1, code)
        self.assertIn("not wired", err)


class TestListings(WireCase):
    def test_list_and_category(self):
        self.run_cli("hubspot")
        code, out, err = self.run_cli("--list")
        self.assertEqual(0, code, err)
        self.assertIn("crm", out)
        self.assertIn("hubspot:oauth (mcp)", out)
        self.assertIn("posthog (mcp:stdio, vendor)", out)
        self.assertIn("paper (cli, listing)", out)
        self.assertIn("chat", out)
        self.assertIn("(no catalog file)", out)
        self.assertLess(out.index("crm"), out.index("web-analytics"))
        code, out, err = self.run_cli("--category", "crm")
        self.assertEqual(0, code, err)
        self.assertIn("mcp oauth (default)", out)
        self.assertIn("HUBSPOT_TOKEN", out)
        self.assertIn("write tools: create_contact", out)
        self.assertIn("cli hubspot", out)
        code, _out, err = self.run_cli("--category", "nope")
        self.assertEqual(1, code)

    def test_list_with_empty_or_broken_catalog(self):
        shutil.rmtree(self.root / "integrations" / "catalog")
        code, out, err = self.run_cli("--list")
        self.assertEqual(0, code, err)
        self.assertIn("catalog is empty", out)
        write(self.root, "integrations/catalog/crm.json", "{not json")
        code, out, err = self.run_cli("--list")
        self.assertEqual(0, code, err)
        self.assertIn("unreadable", out)

    def test_subset_stdout(self):
        self.run_cli("hubspot")
        code, out, err = self.run_cli("--subset", "hubspot", "--stdout")
        self.assertEqual(0, code, err)
        data = json.loads(out)
        self.assertEqual(["hubspot"], list(data["mcpServers"]))
        self.assertEqual("http", data["mcpServers"]["hubspot"]["type"])
        code, _out, err = self.run_cli("--subset", "hubspot,missing", "--stdout")
        self.assertEqual(1, code)
        self.assertIn("missing", err)


class TestCli(unittest.TestCase):
    def test_help_and_docstring(self):
        proc = subprocess.run([sys.executable, str(SCRIPT), "--help"], capture_output=True, text=True)
        self.assertEqual(0, proc.returncode, proc.stderr)
        self.assertIn("--unwire", proc.stdout)
        self.assertTrue(wi.__doc__.startswith("Wire a catalog vendor into this repo:"))


if __name__ == "__main__":
    unittest.main()
