#!/usr/bin/env python3
"""Tests for scripts/web_snapshot.py: the queries it builds, the CSVs it writes
from fixture rows, and the one channel expression it shares with the
web-analyst's PostHog reference. No network.

Run from the repo root:  python3 -m unittest scripts/test_web_snapshot.py
"""

import csv
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import web_snapshot as ws  # noqa: E402

REFERENCE = ws.ROOT / ".agents" / "skills" / "web-analyst" / "references" / "posthog.md"
END = "2026-09-27"


def build(**kw):
    args = dict(end=END, domain="example.com", cta_events=["cta_clicked"],
                conversion_events=["signup_completed"])
    args.update(kw)
    return ws.build_queries(**args)


def squash(text):
    return re.sub(r"\s+", " ", text).strip()


class TestQueries(unittest.TestCase):
    def test_every_query_is_filled_bounded_and_windowed(self):
        queries = build()
        self.assertEqual(set(queries), set(ws.COLUMNS))
        for what, sql in queries.items():
            self.assertNotIn("{{", sql, what)
            self.assertRegex(sql, r"LIMIT \d+\s*$", what)
            self.assertIn("toDateTime('2026-09-27')", sql, what)
            self.assertIn("INTERVAL 27 DAY", sql, what)  # the 28-day session window

    def test_aliases_match_the_csv_columns(self):
        for what, sql in ws.QUERIES.items():
            outer = sql.split("FROM", 1)[0] if what != "tracking-quality" else sql.split("FROM (", 1)[0]
            aliases = re.findall(r"\bAS (\w+)", outer)
            plain = [c for c in ws.COLUMNS[what] if c not in aliases]
            for col in plain:  # a bare column (channel, source) is selected by name
                self.assertRegex(outer, rf"\b{col}\b", f"{what}: {col}")

    def test_session_entry_scope_only(self):
        # The model reads the session's entry source, never the per-event referrer.
        for what, sql in build().items():
            self.assertNotIn("properties.$referring_domain", sql, what)

    def test_channel_order(self):
        order = re.findall(r"'(Direct|Paid|Newsletter|Email|AI Assistant|Organic Search|Social|Referral)'",
                           ws.CHANNEL_HOGQL)
        self.assertEqual(["Direct", "Paid", "Newsletter", "Email", "AI Assistant", "Organic Search",
                          "Social", "Referral", "Direct"], order)

    def test_domain_lands_as_self_referral(self):
        sql = build(domain="shop.example.org")["traffic-by-source"]
        self.assertIn("= 'shop.example.org'", sql)
        self.assertIn("'.shop.example.org'", sql)

    def test_events_and_decision_path_land(self):
        sql = build(cta_events=["cta_clicked", "pricing_cta_clicked"], conversion_events=["demo_requested"],
                    decision_path="/plans")["site-funnel"]
        self.assertIn("IN ('cta_clicked', 'pricing_cta_clicked')", sql)
        self.assertIn("IN ('demo_requested')", sql)
        self.assertIn("properties.$pathname = '/plans'", sql)

    def test_refuses_what_would_break_out_of_sql(self):
        for bad in ({"domain": "example.com' OR 1=1 --"}, {"domain": "https://example.com"},
                    {"domain": ""}, {"cta_events": ["x'); DROP"]}, {"conversion_events": []},
                    {"decision_path": "pricing"}, {"decision_path": "/p'"}):
            with self.assertRaises(SystemExit, msg=bad):
                build(**bad)

    def test_no_company_domains_in_the_lists(self):
        text = ws.CHANNEL_HOGQL + ws.SESSIONS_HOGQL + ws.ENGINE_REFERRERS
        self.assertNotIn("example.com", text)


class TestReferenceMatches(unittest.TestCase):
    def blocks(self):
        text = REFERENCE.read_text(encoding="utf-8")
        return [squash(b) for b in re.findall(r"```sql\n(.*?)```", text, re.S)]

    def test_channel_expression_is_the_scripts(self):
        want = squash(ws.CHANNEL_HOGQL.replace("{{domain}}", "example.com")
                      .replace("{{engine_sources}}", ws.quoted(ws.ENGINE_SOURCES))
                      .replace("{{engine_referrers}}", ws.ENGINE_REFERRERS))
        self.assertIn(want, self.blocks(), "references/posthog.md must carry the script's channel expression")

    def test_source_expression_is_the_scripts(self):
        want = squash(ws.SOURCE_HOGQL.replace("{{domain}}", "example.com"))
        self.assertIn(want, self.blocks())


class TestWrite(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.folder = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_rows_and_posthog_shape_write_the_same_csv(self):
        cols = ws.COLUMNS["site-funnel"]
        values = [300, 249, 4, 47, 150, 44, 9, 3, 399]
        a = ws.write_snapshot("site-funnel", [dict(zip(cols, values))], END, "2026-09-28", self.folder)
        rows = ws.normalise({"columns": cols, "results": [values]})
        b = ws.write_snapshot("site-funnel", rows, END, "2026-09-29", self.folder)
        self.assertEqual(a.read_text(), b.read_text())
        with a.open() as fh:
            got = list(csv.reader(fh))
        self.assertEqual(["date_from", "date_to", *cols], got[0])
        self.assertEqual(["2026-09-21", "2026-09-27", *map(str, values)], got[1])
        self.assertEqual("2026-09-28-posthog-site-funnel.csv", a.name)

    def test_nulls_are_empty_and_extra_columns_dropped(self):
        row = {c: None for c in ws.COLUMNS["tracking-quality"]}
        row["unexpected"] = "x"
        path = ws.write_snapshot("tracking-quality", [row], END, "2026-09-28", self.folder)
        line = path.read_text().splitlines()[1]
        self.assertEqual("2026-09-21,2026-09-27" + "," * len(ws.COLUMNS["tracking-quality"]), line)

    def test_never_overwrites(self):
        ws.write_snapshot("conversions", [], END, "2026-09-28", self.folder)
        with self.assertRaises(SystemExit):
            ws.write_snapshot("conversions", [], END, "2026-09-28", self.folder)

    def test_refuses_rows_missing_a_column(self):
        with self.assertRaises(SystemExit):
            ws.write_snapshot("conversions", [{"event": "cta_clicked"}], END, "2026-09-28", self.folder)

    def test_from_results_writes_each_named_snapshot(self):
        results = {"site-funnel": [dict(zip(ws.COLUMNS["site-funnel"], range(9)))],
                   "conversions": {"columns": ws.COLUMNS["conversions"], "results": []}}
        src = self.folder / "rows.json"
        src.write_text(json.dumps(results))
        with mock.patch.object(ws, "SNAPSHOTS", self.folder), mock.patch.object(ws, "ROOT", self.folder), \
             mock.patch("builtins.print"):
            ws.main(["--domain", "example.com", "--end", END, "--from-results", str(src)])
        names = sorted(p.name for p in self.folder.glob("*-posthog-*.csv"))
        self.assertEqual(2, len(names))
        self.assertTrue(any(n.endswith("-posthog-site-funnel.csv") for n in names))


class TestNoNetwork(unittest.TestCase):
    def run_main(self, *args):
        with mock.patch("urllib.request.urlopen", side_effect=AssertionError("network")), \
             mock.patch("builtins.print") as out:
            ws.main(["--domain", "example.com", "--end", END, *args])
        return "\n".join(" ".join(map(str, c.args)) for c in out.call_args_list)

    def test_print_sql_and_dry_run_never_call_out(self):
        self.assertIn("LIMIT", self.run_main("--print-sql"))
        with mock.patch.object(ws, "setting", return_value="phx_secret_value"):
            text = self.run_main("--dry-run")
        self.assertIn("7 queries", text)
        self.assertNotIn("phx_secret_value", text)

    def test_missing_key_exits_without_calling_out(self):
        with mock.patch.object(ws, "setting", return_value=""), \
             mock.patch("urllib.request.urlopen", side_effect=AssertionError("network")):
            with self.assertRaises(SystemExit):
                ws.main(["--domain", "example.com", "--end", END])

    def test_incomplete_day_refused(self):
        today = ws.dt.datetime.now(ws.dt.timezone.utc).date().isoformat()
        with self.assertRaises(SystemExit):
            ws.main(["--domain", "example.com", "--end", today, "--print-sql"])


if __name__ == "__main__":
    unittest.main()
