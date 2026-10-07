#!/usr/bin/env python3
"""Tests for the search scripts (scripts/_seo.py, seo_rank_track.py, seo_diff.py, page_join.py,
gsc_snapshot.py): SERP parsing, the scoreboard and findings, the crosswalk, the forecast, the page
join and the Search Console folding, all on fixtures. No network: a call that would leave the
machine fails the test.

Run from the repo root:  python3 -m unittest scripts/test_seo_scripts.py
"""

import contextlib
import datetime as dt
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _seo  # noqa: E402
import gsc_snapshot  # noqa: E402
import page_join  # noqa: E402
import seo_diff  # noqa: E402
import seo_rank_track  # noqa: E402

BRANDS = [{"brand": "Us", "kind": "self", "aliases": ["Us"], "domains": ["example.com"]},
          {"brand": "Rival", "kind": "competitor", "aliases": ["Rival"], "domains": ["rival.io"]}]

SERP = {"items": [
    {"type": "ai_overview", "references": [{"url": "https://example.com/guide/", "title": "Guide"},
                                           {"url": "https://rival.io/blog"}]},
    {"type": "organic", "rank_group": 1, "url": "https://rival.io/a", "title": "Rival"},
    {"type": "people_also_ask", "items": [{"title": "Is Rival worth it?"}]},
    {"type": "organic", "rank_group": 2, "url": "https://www.example.com/guide/", "title": "Ours"},
    {"type": "organic", "rank_group": 9, "url": "https://example.com/pricing"},
    {"type": "related_searches", "items": ["rival pricing", "rival vs us"]},
]}


def kw(kid, tier="1", track="category", page="/guide", prompts="", keyword=None):
    return {"id": kid, "keyword": keyword or f"kw {kid}", "track": track, "tier": tier,
            "intent": "commercial", "target_url": page, "aeo_prompts": prompts}


def serp_row(kid, rank="", url="", tier="1", track="category", page="/guide", aio_cited="no", ok="yes"):
    return {"keyword_id": kid, "keyword": f"kw {kid}", "track": track, "tier": tier, "target_url": page,
            "ok": ok, "rank": rank, "url": url, "aio": "yes", "aio_cited": aio_cited,
            "aio_cited_paths": url if aio_cited == "yes" else ""}


def no_network(*args, **kwargs):
    raise AssertionError("a test tried to reach the network")


class Helpers(unittest.TestCase):
    def test_path_of(self):
        cases = {"https://www.example.com/guide/": "/guide", "/guide/": "/guide", "https://example.com": "/",
                 "example.com/a?b=1": "/a", "(not set)": "", "": "", "/": "/"}
        for raw, want in cases.items():
            self.assertEqual(want, _seo.path_of(raw), raw)

    def test_market_never_defaults(self):
        with tempfile.TemporaryDirectory() as tmp:
            metrics = Path(tmp) / "metrics.md"
            metrics.write_text("| Search location | [e.g. United States] | |\n| Search language | [en] | |\n")
            with self.assertRaises(SystemExit):
                _seo.market(metrics=metrics)
            self.assertEqual({"location_code": 2826, "language_code": "en"},
                             _seo.market("2826", "en", metrics=metrics))
            metrics.write_text("| Search location | Germany | x |\n| Search language | de | x |\n")
            self.assertEqual({"location_name": "Germany", "language_code": "de"}, _seo.market(metrics=metrics))

    def test_prompts_without_ids_skip_the_crosswalk(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "prompts.csv"
            p.write_text("prompt,persona\nx,y\n")
            self.assertIsNone(_seo.prompts(p))


class RankTrack(unittest.TestCase):
    def test_parse_serp(self):
        row, results = seo_rank_track.parse_serp(SERP, ["example.com"], BRANDS)
        self.assertEqual((2, "/guide"), (row["rank"], row["url"]))
        self.assertEqual("/guide|/pricing", row["our_urls"])
        self.assertEqual(("yes", "yes", "/guide"), (row["aio"], row["aio_cited"], row["aio_cited_paths"]))
        self.assertEqual("Rival", row["top10_brands"])
        self.assertEqual("rival.io|example.com", row["top10_domains"])
        self.assertEqual(1, row["paa"])
        kinds = [r["kind"] for r in results]
        self.assertEqual(3, kinds.count("organic"))
        self.assertEqual(["paa", "related", "related"], kinds[-3:])
        self.assertEqual("Rival", results[0]["brand"])

    def test_not_ranked(self):
        row, _ = seo_rank_track.parse_serp({"items": [{"type": "organic", "rank_group": 1,
                                                       "url": "https://rival.io/"}]}, ["example.com"], BRANDS)
        self.assertEqual(("", "no", "no"), (row["rank"], row["aio"], row["aio_cited"]))

    def test_transient_error_retries_once_and_counts_both_costs(self):
        bad = {"cost": 0.01, "tasks": [{"status_code": 40101, "status_message": "Internal SE Server Error"}]}
        with mock.patch("seo_snapshot.call", side_effect=[bad, bad]) as call:
            row, results, cost = seo_rank_track.fetch({"keyword": "x"}, {"language_code": "en"}, ["example.com"], [])
        self.assertEqual(2, call.call_count)
        self.assertEqual("no", row["ok"])
        self.assertAlmostEqual(0.02, cost)

    def _run(self, *argv, rows=None):
        rows = rows or [kw("K001"), kw("K002")]
        out = io.StringIO()
        with mock.patch("_seo.keywords", return_value=rows), mock.patch("_seo.brands", return_value=BRANDS), \
                mock.patch("seo_snapshot.call", side_effect=no_network), contextlib.redirect_stdout(out):
            code = seo_rank_track.main(["--location", "Germany", "--language", "de", *argv])
        return code, out.getvalue()

    def test_dry_run_spends_nothing(self):
        code, out = self._run("--dry-run")
        self.assertEqual(0, code)
        self.assertIn("Germany / de", out)
        self.assertIn("est $0.02", out)

    def test_cost_guard_refuses_before_any_call(self):
        with self.assertRaises(SystemExit) as ctx:
            self._run("--max-usd", "0.01", rows=[kw(f"K{i:03}") for i in range(10)])
        self.assertIn("exceeds --max-usd", str(ctx.exception))


class Diff(unittest.TestCase):
    KWS = [kw("K1"), kw("K2", tier="3", page="/y"), kw("K3", track="brand", page="/")]

    def test_scoreboard_and_findings(self):
        prev = [serp_row("K1", 14, "/guide"), serp_row("K2", 3, "/y", tier="3"),
                serp_row("K3", 1, "/", track="brand", page="/")]
        cur = [serp_row("K1", 6, "/guide", aio_cited="yes"), serp_row("K2", "", tier="3"),
               serp_row("K3", 2, "/pricing", track="brand", page="/")]
        res = seo_diff.compute(cur, [prev], self.KWS)
        board = res["scoreboard"]
        self.assertEqual((2, 1, 1), (board["non_branded"]["n"], board["non_branded"]["top10"],
                                     board["non_branded"]["on_target"]))
        self.assertEqual({"n": 1, "first": 0}, board["branded"])
        kinds = {(f["kind"], f.get("ref")) for f in res["findings"]}
        for want in [("win", "K1"), ("loss", "K2"), ("branded_gap", "K3"), ("wrong_page", "K3"), ("aio_won", "K1")]:
            self.assertIn(want, kinds)
        win = next(f for f in res["findings"] if f["kind"] == "win")
        loss = next(f for f in res["findings"] if f["kind"] == "loss")
        self.assertEqual((3, 1), (win["score"], loss["score"]))  # tier 1 against tier 3
        self.assertFalse(res["trend_ok"])

    def test_small_moves_are_not_findings(self):
        res = seo_diff.compute([serp_row("K1", 16, "/guide")], [[serp_row("K1", 13, "/guide")]], self.KWS[:1])
        self.assertFalse([f for f in res["findings"] if f["kind"] == "rank_move"])
        res = seo_diff.compute([serp_row("K1", 20, "/guide")], [[serp_row("K1", 13, "/guide")]], self.KWS[:1])
        self.assertTrue([f for f in res["findings"] if f["kind"] == "rank_move"])

    def test_definition_change_sorts_first(self):
        res = seo_diff.compute([serp_row("K1"), serp_row("K9")], [[serp_row("K1")]], self.KWS)
        self.assertEqual("definition_change", res["findings"][0]["kind"])

    def test_crosswalk(self):
        prompts = [{"id": "P1", "tier": "1", "track": "category", "intent": "direct", "target_page": "/a",
                    "status": "active"},
                   {"id": "P2", "tier": "2", "track": "category", "intent": "indirect", "target_page": "/b",
                    "status": "active"},
                   {"id": "P3", "tier": "1", "track": "category", "intent": "direct", "target_page": "/a",
                    "status": "retired"}]
        keywords = [kw("K1", tier="3", page="/a", prompts="P1|P3|P9")]
        cw = seo_diff.crosswalk(keywords, prompts)
        self.assertEqual(["K1:P3 (retired)", "K1:P9"], cw["missing_prompts"])
        self.assertEqual(["/b"], cw["uncovered_pages"])
        self.assertEqual(["P2"], cw["unmapped_prompts"])
        self.assertEqual(1, len(cw["tier_mismatch"]))
        res = seo_diff.compute([serp_row("K1")], [], keywords, prompts)
        self.assertEqual("crosswalk_broken", res["findings"][0]["kind"])

    def test_forecast(self):
        text = "# memory\n\n- Forecast for 2026-10-05: top10 2-4, top30 0-1\n"
        res = seo_diff.compute([serp_row("K1", 5, "/guide")], [], self.KWS[:1], forecast_text=text,
                               current_day="2026-10-05")
        fc = res["forecast_check"]["metrics"]
        self.assertFalse(fc["top10"]["inside"])
        self.assertTrue(fc["top30"]["inside"])
        self.assertIn("forecast_miss", [f["kind"] for f in res["findings"]])
        not_due = seo_diff.compute([serp_row("K1")], [], self.KWS[:1], forecast_text=text, current_day="2026-10-01")
        self.assertIsNone(not_due["forecast_check"])
        self.assertEqual((None, {}), seo_diff.read_forecast("# memory\n- Forecast for [YYYY-MM-DD]: top10 [lo]-[hi]\n"))

    def test_search_console_findings(self):
        pages = [{"page": "/guide", "clicks": "0", "impressions": "40", "position": "11.2",
                  "index_verdict": "PASS"},
                 {"page": "/y", "clicks": "0", "impressions": "3", "index_verdict": "NEUTRAL",
                  "index_coverage": "Discovered - currently not indexed"}]
        queries = [{"query": "kw K1", "page": "/guide", "impressions": "30", "position": "12"},
                   {"query": "new idea", "page": "/guide", "impressions": "25", "position": "9"},
                   {"query": "far away", "page": "/guide", "impressions": "90", "position": "35"}]
        res = seo_diff.compute([serp_row("K1", 12, "/guide")], [], self.KWS[:2], gsc_pages=pages, gsc_queries=queries)
        kinds = {(f["kind"], f.get("ref")) for f in res["findings"]}
        self.assertIn(("ctr_gap", "/guide"), kinds)
        self.assertIn(("not_indexed", "/y"), kinds)
        self.assertEqual(["kw K1", "new idea"], [q["query"] for q in res["striking_distance"]])
        self.assertEqual([True, False], [q["tracked"] for q in res["striking_distance"]])
        self.assertEqual(["far away", "new idea"], [c["query"] for c in res["candidates"]])

    def test_aeo_hand_offs(self):
        prompts = [{"id": "P1", "tier": "1", "track": "category", "intent": "direct", "target_page": "/guide"},
                   {"id": "P2", "tier": "2", "track": "category", "intent": "indirect", "target_page": "/y"}]
        aeo = [{"prompt_id": "P2", "engine": "chatgpt", "answered": "yes", "cited_self": "yes", "cited_paths": "/y"}]
        res = seo_diff.compute([serp_row("K1", 4, "/guide"), serp_row("K2", "", tier="3", page="/y")], [],
                               self.KWS[:2], prompts, aeo=aeo)
        kinds = {(f["kind"], f.get("ref")) for f in res["findings"]}
        self.assertIn(("ranked_not_cited", "/guide"), kinds)
        self.assertIn(("cited_not_ranked", "/y"), kinds)


class PageJoin(unittest.TestCase):
    def test_join_by_path(self):
        serp = [serp_row("K1", 4, "/guide", aio_cited="yes"), serp_row("K2", 15, "/guide/", page="/y")]
        prompts = [{"id": "P1", "target_page": "/guide", "intent": "direct"},
                   {"id": "P2", "target_page": "/guide", "intent": "branded"},
                   {"id": "P3", "target_page": "/old", "intent": "direct", "status": "retired"}]
        aeo = [{"prompt_id": "P1", "answered": "yes", "cited_self": "yes", "cited_paths": "https://example.com/guide/"},
               {"prompt_id": "P2", "answered": "yes", "cited_self": "yes", "cited_paths": "/guide"},
               {"prompt_id": "P1", "answered": "yes", "cited_self": "no", "cited_paths": ""}]
        gsc = [{"page": "/guide", "clicks": "3", "impressions": "120", "ctr": "0.025", "position": "7.5",
                "index_verdict": "PASS"}]
        web = [{"landing_page": "https://example.com/guide", "sessions": "40", "engaged_sessions": "20",
                "conversions": "2"}, {"landing_page": "/guide/", "sessions": "10", "engaged_sessions": "5",
                                      "conversions": "0"}, {"landing_page": "(not set)", "sessions": "9"}]
        joined = page_join.join(serp, [kw("K1"), kw("K2", page="/y")], aeo, prompts, gsc, web)
        e = joined["/guide"]
        self.assertEqual((["K1"], ["K1", "K2"], 4, ["K1"], ["K1"]),
                         (e["keywords"], e["ranks_with"], e["best_rank"], e["top10"], e["aio_cited"]))
        self.assertEqual((["P1", "P2"], 1), (e["aeo_prompts"], e["aeo_cited"]))  # branded answers never count
        self.assertEqual((3, 120, "PASS", 50, 2), (e["gsc_clicks"], e["gsc_impressions"], e["index"],
                                                   e["sessions"], e["conversions"]))
        self.assertNotIn("/old", joined)
        self.assertEqual(["K2"], joined["/y"]["keywords"])
        self.assertEqual("K1|K2", page_join.flat("/guide", e)["ranks_with"])

    def test_missing_sources_are_fine(self):
        self.assertEqual({"/guide": ["K1"]}, {p: e["keywords"] for p, e in page_join.join(keywords=[kw("K1")]).items()})


class SearchConsole(unittest.TestCase):
    S, E = dt.date(2026, 9, 1), dt.date(2026, 9, 28)

    def test_page_rows_fold_paths_and_weight_position(self):
        cur = [{"keys": ["https://example.com/a/"], "clicks": 1, "impressions": 10, "position": 4.0},
               {"keys": ["https://www.example.com/a"], "clicks": 1, "impressions": 30, "position": 8.0}]
        prev = [{"keys": ["https://example.com/a"], "clicks": 0, "impressions": 5, "position": 20.0}]
        index = {"/a": {"index_verdict": "PASS"}, "/b": {"index_verdict": "NEUTRAL"}}
        rows = {r["page"]: r for r in gsc_snapshot.page_rows(cur, prev, index, self.S, self.E)}
        a = rows["/a"]
        self.assertEqual((2, 40, 7.0, 0.05, 5, "PASS"),
                         (a["clicks"], a["impressions"], a["position"], a["ctr"], a["prev_impressions"], a["index_verdict"]))
        self.assertEqual((0, "NEUTRAL"), (rows["/b"]["impressions"], rows["/b"]["index_verdict"]))

    def test_query_rows_and_origin(self):
        rows = gsc_snapshot.query_rows([{"keys": ["q", "https://example.com/a/"], "clicks": 0,
                                         "impressions": 3, "ctr": 0, "position": 12.34}], self.S, self.E)
        self.assertEqual(("q", "/a", 12.3, "2026-09-28"), (rows[0]["query"], rows[0]["page"],
                                                           rows[0]["position"], rows[0]["date_to"]))
        self.assertEqual("https://example.com", gsc_snapshot.origin("sc-domain:example.com"))
        self.assertEqual("https://www.example.com", gsc_snapshot.origin("https://www.example.com/"))

    def test_dry_run_and_missing_keys_call_nothing(self):
        with mock.patch("gsc_snapshot.post", side_effect=no_network), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, gsc_snapshot.main(["--dry-run", "--end", "2026-09-28"]))
            with mock.patch("gsc_snapshot.setting", return_value=""), self.assertRaises(SystemExit) as ctx:
                gsc_snapshot.main(["--end", "2026-09-28"])
        self.assertIn("GSC_CLIENT_ID", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
