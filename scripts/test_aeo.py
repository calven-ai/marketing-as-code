#!/usr/bin/env python3
"""Tests for the AEO tracker: brand detection on prose (scripts/_aeo.py), parsing and collection
with a fake DataForSEO caller (scripts/aeo_track.py), and the scoring (scripts/aeo_diff.py) over
fixture snapshots in a temp folder. No network, no key.

Run from the repo root:  python3 -m unittest scripts/test_aeo.py
"""

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _aeo  # noqa: E402
import aeo_diff  # noqa: E402
import aeo_track  # noqa: E402

BRANDS_CSV = """brand,kind,aliases,domains
Acme,self,Acme|Acme.io,acme.io
Rival,competitor,Rival|RivalHQ,rival.example
Other,competitor,Other Co,other.example
"""
PROMPTS_CSV = """id,prompt,track,stage,intent,tier,persona,target_page,source,status,added_on,retired_on,rationale
P001,best tools for x,category,consideration,direct,1,lead,/pricing,research,active,2026-10-01,,r
P002,how do teams solve y,category,awareness,indirect,2,lead,/guides/y,research,active,2026-10-01,,r
P003,what is acme,brand,decision,branded,1,lead,/,research,active,2026-10-01,,r
P004,old wording,craft,awareness,indirect,3,lead,,research,retired,2026-10-01,2026-10-05,r
"""
LONG = " filler" * 100


class Fixture(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "brands.csv").write_text(BRANDS_CSV)
        (self.tmp / "prompts.csv").write_text(PROMPTS_CSV)
        self.brands = _aeo.load_brands(self.tmp / "brands.csv")
        self.prompts = {p["id"]: p for p in _aeo.load_prompts(self.tmp / "prompts.csv", active_only=False)}
        self.kinds = {b["brand"]: b["kind"] for b in self.brands}

    def write_run(self, day, rows, prompts_sha="a", brands_sha="b", answers=None):
        path = self.tmp / f"{day}-dataforseo-aeo-results.csv"
        full = []
        for r in rows:
            base = {c: "" for c in _aeo.RESULT_COLUMNS}
            base.update(answered="true", mentioned="false", cited_self="false", category_phrase="false",
                        prompts_sha=prompts_sha, brands_sha=brands_sha, model="m", cost_usd="0.004")
            base.update(r)
            full.append(base)
        _aeo.write_csv(path, _aeo.RESULT_COLUMNS, full)
        if answers is not None:
            _aeo.write_csv(_aeo.answers_file(path), _aeo.ANSWER_COLUMNS, answers)
        return path


def row(pid, engine="chatgpt", named=False, paths="", brands="", domains="", position=""):
    return {"prompt_id": pid, "engine": engine, "mentioned": _aeo.flag(named), "cited_paths": paths,
            "cited_self": _aeo.flag(bool(paths)), "brands": brands, "cited_domains": domains,
            "position": position or ("1" if named else "")}


class TestDetect(Fixture):
    def test_order_position_and_citation(self):
        d = _aeo.detect("Try Rival first, or Acme for small teams." + LONG,
                        ["https://www.acme.io/pricing/", "https://rival.example/x"], self.brands)
        self.assertEqual(d["brands"], ["Rival", "Acme"])
        self.assertEqual(d["position"], 2)
        self.assertTrue(d["mentioned"] and d["cited_self"])
        self.assertEqual(d["cited_paths"], ["/pricing"])
        self.assertEqual(d["cited_domains"], ["acme.io", "rival.example"])

    def test_word_boundaries(self):
        d = _aeo.detect("Acmeology and rivalry are not brands", [], self.brands)
        self.assertEqual(d["brands"], [])

    def test_links_and_labels_are_not_mentions(self):
        d = _aeo.detect("Rival is solid ([acme.io](https://acme.io/?utm_source=x)) [rival.example +2]",
                        ["https://acme.io/"], self.brands)
        self.assertEqual(d["brands"], ["Rival"])
        self.assertFalse(d["mentioned"])
        self.assertTrue(d["cited_self"])

    def test_link_text_is_prose(self):
        self.assertTrue(_aeo.detect("Use [Acme](https://acme.io/) today", [], self.brands)["mentioned"])

    def test_category_phrase(self):
        self.assertTrue(_aeo.detect("The best marketing platforms are", [], self.brands,
                                    "marketing platform")["category_phrase"])
        self.assertFalse(_aeo.detect("The best marketing platforms are", [], self.brands)["category_phrase"])

    def test_preamble_is_unanswered(self):
        self.assertFalse(_aeo.answered("I'll search for options.", []))
        self.assertTrue(_aeo.answered("Rival.", ["https://rival.example/"]))
        self.assertTrue(_aeo.answered("x" * 600, []))


def body(result, status=20000, cost=0.004):
    return {"status_code": 20000, "cost": cost,
            "tasks": [{"status_code": status, "status_message": "Ok", "result": [result] if result else None}]}


class TestTrack(Fixture):
    def test_parse_each_shape(self):
        p = aeo_track.parse("chatgpt", {"markdown": "Acme", "sources": [{"url": "https://acme.io/a"}],
                                        "items": [{"sources": [{"url": "https://acme.io/a"}, {"url": "https://b.example"}]}]})
        self.assertEqual(p["sources"], ["https://acme.io/a", "https://b.example"])
        p = aeo_track.parse("google_ai_mode", {"items": [{"type": "ai_overview", "markdown": "Rival",
                                                          "references": [{"url": "https://rival.example"}]}]})
        self.assertEqual((p["text"], p["sources"]), ("Rival", ["https://rival.example"]))
        p = aeo_track.parse("claude", {"model_name": "claude-haiku-4-5", "items": [{"type": "message", "sections": [
            {"type": "text", "text": "Use Acme.", "annotations": [{"url": "https://acme.io/"}]}]}]})
        self.assertEqual((p["text"], p["model"]), ("Use Acme.", "claude-haiku-4-5"))

    def test_payload_shapes(self):
        self.assertIn("keyword", aeo_track.payload("chatgpt", "q")[0])
        self.assertEqual(aeo_track.payload("claude", "q")[0]["model_name"], "claude-haiku-4-5")
        self.assertTrue(aeo_track.payload("claude", "q")[0]["web_search"])

    def test_collect_with_fake_caller(self):
        calls = []

        def caller(endpoint, payload):
            calls.append(endpoint)
            if "claude" in endpoint:
                return body(None, status=40501)
            if "chat_gpt" in endpoint:
                return body({"markdown": "Rival and Acme." + LONG, "sources": [{"url": "https://acme.io/p"}]})
            raise SystemExit("DataForSEO returned HTTP 500")

        prompts = list(_aeo.load_prompts(self.tmp / "prompts.csv"))[:1]
        done = aeo_track.collect(prompts, ["chatgpt", "claude", "google_ai_mode"], self.brands, caller, workers=1)
        rows = {r["engine"]: r for r, _ in done}
        self.assertEqual(rows["chatgpt"]["mentioned"], "true")
        self.assertEqual(rows["chatgpt"]["position"], 2)
        self.assertEqual(rows["chatgpt"]["cited_paths"], "/p")
        self.assertTrue(rows["claude"]["error"].startswith("40501"))
        self.assertIn("HTTP 500", rows["google_ai_mode"]["error"])
        self.assertEqual(sum(1 for _, a in done if a), 1)
        self.assertEqual(len(calls), 3)

    def test_chatgpt_preamble_retries_once_and_sums_cost(self):
        replies = iter([body({"markdown": "I'll search."}), body({"markdown": "Acme." + LONG})])
        r, a = aeo_track.ask("chatgpt", {"id": "P001", "prompt": "q"}, self.brands, lambda e, p: next(replies))
        self.assertEqual((r["answered"], r["mentioned"]), ("true", "true"))
        self.assertAlmostEqual(r["cost_usd"], 0.008)

    def test_estimate(self):
        self.assertEqual(aeo_track.estimate(100, ["chatgpt", "google_ai_mode", "claude"]), 3.3)

    def test_redetect_reports_changes_without_writing(self):
        path = self.write_run("2026-10-05", [row("P001", brands="Rival")],
                              answers=[{"prompt_id": "P001", "engine": "chatgpt",
                                        "text": "Rival or Acme." + LONG, "sources": "", "fan_out": ""}])
        before = path.read_text()
        changes = aeo_track.redetect(path, self.brands)
        self.assertIn(("P001", "chatgpt", "mentioned", "false", "true"), changes)
        self.assertEqual(path.read_text(), before)

    def test_dry_run_spends_nothing(self):
        with mock.patch.object(_aeo, "PROMPTS", self.tmp / "prompts.csv"), \
                mock.patch.object(_aeo, "BRANDS", self.tmp / "brands.csv"), \
                mock.patch("aeo_track.setting", side_effect=AssertionError("no key read on a dry run")):
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                aeo_track.main(["--dry-run"])
        self.assertIn("= 9 calls", out.getvalue())

    def test_max_usd_refuses(self):
        with mock.patch.object(_aeo, "PROMPTS", self.tmp / "prompts.csv"), \
                mock.patch.object(_aeo, "BRANDS", self.tmp / "brands.csv"), \
                contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as ctx:
                aeo_track.main(["--max-usd", "0.01"])
        self.assertIn("over --max-usd", str(ctx.exception))


class TestDiff(Fixture):
    def score(self, current, *history, forecast=None):
        load = aeo_diff.load_run
        return aeo_diff.compute(load(current), [load(h) for h in history], self.prompts, self.kinds, forecast)

    def test_wins_losses_by_tier_and_branded_gap(self):
        prev = self.write_run("2026-09-28", [row("P001"), row("P002", paths="/guides/y"), row("P003", named=True)])
        cur = self.write_run("2026-10-05", [row("P001", named=True), row("P002"), row("P003")])
        res = self.score(cur, prev)
        found = {(f["kind"], f.get("prompt_id"), f["score"]) for f in res["findings"]}
        self.assertIn(("mention_win", "P001", 3), found)
        self.assertIn(("citation_loss", "P002", 2), found)
        self.assertIn(("branded_gap", "P003", 3), found)
        self.assertNotIn("mention_loss", {f["kind"] for f in res["findings"]})  # branded never a loss
        self.assertEqual(res["deltas"]["gained_mention"], ["P001/chatgpt"])

    def test_definition_change_first(self):
        prev = self.write_run("2026-09-28", [row("P001")], prompts_sha="a")
        cur = self.write_run("2026-10-05", [row("P001"), row("P001", engine="claude")], prompts_sha="z")
        res = self.score(cur, prev)
        self.assertEqual(res["findings"][0]["kind"], "definition_change")
        self.assertIn("engines", res["findings"][0]["detail"])
        self.assertEqual(res["deltas"]["compared_pairs"], 1)

    def test_non_branded_headline_and_share_of_voice(self):
        cur = self.write_run("2026-10-05", [row("P001", brands="Rival", paths="/guides/z"),
                                            row("P003", named=True, brands="Acme", paths="/")])
        m = self.score(cur)["metrics"]
        nb = m["non_branded"]["overall"]
        self.assertEqual((nb["n"], nb["mentioned"], nb["cited"]), (1, 0, 1))
        self.assertEqual(m["share_of_voice"][0]["brand"], "Rival")
        self.assertEqual(list(m["self_cited"]), ["/guides/z"])
        self.assertEqual(m["branded"], [{"prompt_id": "P003", "engine": "chatgpt", "mentioned": True}])

    def test_unanswered_is_not_in_n(self):
        cur = self.write_run("2026-10-05", [row("P001", named=True), {**row("P002"), "answered": "false",
                                                                     "error": "500"}])
        self.assertEqual(self.score(cur)["metrics"]["non_branded"]["overall"]["n"], 1)

    def test_rolling_pools_four_runs_with_wilson(self):
        days = ["2026-09-14", "2026-09-21", "2026-09-28", "2026-10-05", "2026-10-12"]
        paths = [self.write_run(d, [row("P001", named=(i % 2 == 0))]) for i, d in enumerate(days)]
        res = self.score(paths[-1], *reversed(paths[:-1]))
        r4 = res["rolling_4"]
        self.assertEqual((r4["periods"], r4["overall"]["n"], r4["overall"]["mentioned"]), (4, 4, 2))
        self.assertTrue(r4["trend_ok"])
        self.assertFalse(r4["overall"]["comparable"])
        self.assertEqual(r4["overall"]["mentioned_ci"], aeo_diff.wilson(2, 4))

    def test_retired_prompt_groups_as_retired(self):
        cur = self.write_run("2026-10-05", [row("P004", paths="/x"), row("P999")])
        tiers = self.score(cur)["metrics"]["non_branded"]["by_tier"]
        self.assertEqual(set(tiers), {"retired", "unknown"})

    def test_first_citation_once(self):
        prev = self.write_run("2026-09-28", [row("P001", paths="/pricing")])
        cur = self.write_run("2026-10-05", [row("P001", paths="/pricing|/platform")])
        firsts = [f["path"] for f in self.score(cur, prev)["findings"] if f["kind"] == "first_citation"]
        self.assertEqual(firsts, ["/platform"])

    def test_forecast_read_and_scored(self):
        reports = self.tmp / "reports"
        reports.mkdir()
        (reports / "2026-09-28.md").write_text(
            "**Forecast for the next run** (80%): named 2 to 4 · cited 0 to 1 · named first 0 to 1\n")
        fc = aeo_diff.find_forecast(reports, "2026-10-05", "2026-09-28")
        self.assertEqual(fc, {"mentioned": (2, 4), "cited": (0, 1), "top": (0, 1)})
        self.assertIsNone(aeo_diff.find_forecast(reports, "2026-10-05", "2026-09-29"))
        prev = self.write_run("2026-09-28", [row("P001")])
        cur = self.write_run("2026-10-05", [row("P001", named=True)])
        res = self.score(cur, prev, forecast=fc)
        self.assertFalse(res["forecast_check"]["mentioned"]["inside"])
        self.assertEqual(res["findings"][0]["kind"], "forecast_miss")

    def test_redetect_rescoring_on_load(self):
        path = self.write_run("2026-10-05", [row("P001")],
                              answers=[{"prompt_id": "P001", "engine": "chatgpt", "text": "Acme." + LONG,
                                        "sources": "", "fan_out": ""}])
        with mock.patch.object(_aeo, "BRANDS", self.tmp / "brands.csv"):
            run = aeo_diff.load_run(path, self.brands, redetect=True)
        self.assertTrue(run["rows"][0]["mentioned"])
        self.assertFalse(aeo_diff.load_run(path)["rows"][0]["mentioned"])

    def test_markdown_and_score_rows(self):
        prev = self.write_run("2026-09-28", [row("P001"), row("P002")])
        cur = self.write_run("2026-10-05", [row("P001", named=True, brands="Acme|Rival"), row("P002")])
        res = self.score(cur, prev)
        text = aeo_diff.markdown(res)
        self.assertIn("| 1 Buy | 1 of 1 |", text)
        self.assertIn("mention_win P001/chatgpt", text)
        rows = aeo_diff.score_rows(res)
        self.assertTrue(any(r["section"] == "rolling4" and r["dimension"] == "tier" for r in rows))
        self.assertTrue(any(r["section"] == "finding" for r in rows))

    def test_first_run_says_so(self):
        cur = self.write_run("2026-10-05", [row("P001")])
        self.assertIn("First run", aeo_diff.markdown(self.score(cur)))


if __name__ == "__main__":
    unittest.main()
