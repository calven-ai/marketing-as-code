#!/usr/bin/env python3
"""Score the newest SERP snapshot (scripts/seo_rank_track.py) against the earlier ones: top 10,
top 30 and AI Overview citing us by tier (non-branded headline, the `brand` track apart), on
target, deltas, ranked findings, the forecast scored, Search Console striking distance and
candidates, and the crosswalk with data/seo/prompts.csv. Prints a summary or --json; exits 1
when a keyword names a retired or unknown prompt. No network.

    python3 scripts/seo_diff.py
    python3 scripts/seo_diff.py --json > /tmp/seo.json
    python3 scripts/seo_diff.py --snapshot data/seo/snapshots/2026-10-05-dataforseo-serp.csv

Findings (score; the first four always sort first):
  definition_change  the keyword set changed since the last run; deltas cover the overlap
  serp_errors        more than 10 % of SERP calls failed
  crosswalk_broken   a keyword's aeo_prompts names a retired or unknown prompt id
  forecast_miss      a range in the last forecast missed
  win / loss         a keyword entered or left the top 10 (by tier 3 / 2 / 1)
  aio_won / aio_lost an AI Overview started or stopped citing us (by tier)
  branded_gap        a `brand` track keyword where we are not first (3)
  not_indexed        a targeted page Search Console does not report as indexed (2)
  ctr_gap            a page with 20+ Search Console impressions and no click (2 targeted, else 1)
  ranked_not_cited   a top-10 page with AEO prompts that no AEO answer cites: AEO's (2)
  cited_not_ranked   a page AEO answers cite that no tracked keyword ranks in the top 30 (1)
  wrong_page         a keyword ranks with a page other than its target_url (1)
  rank_move          a rank moved 5 or more places inside the top 30 (1)

The forecast is the `- Forecast for YYYY-MM-DD: top10 3-6, top30 8-12, aio_cited 0-2` line in
memory/knowledge/seo-memory.md (non-branded counts), or --forecast "top10=3-6,top30=8-12".
"""
import argparse
import collections
import json
import re
import sys
from pathlib import Path

import _seo
import page_join
from _common import ROOT

MEMORY = ROOT / "memory" / "knowledge" / "seo-memory.md"
PRIORITY = ("definition_change", "serp_errors", "crosswalk_broken", "forecast_miss")
HISTORY = 8


def rank(r):
    return _seo.num(r.get("rank")) if _seo.flag(r.get("ok")) else None


def rates(rows):
    ok = [r for r in rows if _seo.flag(r.get("ok"))]
    ranks = [rank(r) for r in ok if rank(r)]
    return {"n": len(ok), "top10": sum(1 for x in ranks if x <= 10), "top30": len(ranks),
            "on_target": sum(1 for r in ok if rank(r) and r.get("target_url")
                             and _seo.path_of(r.get("url")) == _seo.path_of(r["target_url"])),
            "aio": sum(1 for r in ok if _seo.flag(r.get("aio"))),
            "aio_cited": sum(1 for r in ok if _seo.flag(r.get("aio_cited")))}


def scoreboard(rows):
    nb = [r for r in rows if not _seo.branded(r)]
    tiers = collections.defaultdict(list)
    tracks = collections.defaultdict(list)
    for r in nb:
        tiers[str(r.get("tier") or "?")].append(r)
        tracks[r.get("track") or "?"].append(r)
    brand = [r for r in rows if _seo.branded(r)]
    return {"non_branded": rates(nb),
            "by_tier": {t: rates(v) for t, v in sorted(tiers.items())},
            "by_track": {t: rates(v) for t, v in sorted(tracks.items())},
            "branded": {"n": len([r for r in brand if _seo.flag(r.get("ok"))]),
                        "first": sum(1 for r in brand if rank(r) == 1)}}


def crosswalk(keywords, prompts):
    """The keyword set against the AEO prompt set (data/seo/README.md, both tables)."""
    by_id = {p["id"]: p for p in prompts}
    live = {i for i, p in by_id.items() if p.get("status", "active") != "retired"}
    out = {"missing_prompts": [], "uncovered_pages": [], "unmapped_prompts": [],
           "tier_mismatch": [], "track_mismatch": []}
    named = set()
    for k in keywords:
        ids = _seo.split(k.get("aeo_prompts"))
        good = [by_id[i] for i in ids if i in live]
        named.update(p["id"] for p in good)
        for i in ids:
            if i not in live:
                out["missing_prompts"].append(f"{k['id']}:{i}" + (" (retired)" if i in by_id else ""))
        if good and all(str(p.get("tier")) != str(k.get("tier")) for p in good):
            out["tier_mismatch"].append(f"{k['id']} tier {k.get('tier')} vs "
                                        + ",".join(f"{p['id']}:{p.get('tier')}" for p in good))
        if good and all(p.get("track") != k.get("track") for p in good):
            out["track_mismatch"].append(f"{k['id']} {k.get('track')} vs "
                                         + ",".join(f"{p['id']}:{p.get('track')}" for p in good))
    targeted = {_seo.path_of(k.get("target_url")) for k in keywords} - {""}
    for p in prompts:
        if p["id"] not in live or str(p.get("tier")) not in ("1", "2") or p.get("intent") == "branded":
            continue
        page = _seo.path_of(p.get("target_page"))
        if page and page not in targeted and page not in out["uncovered_pages"]:
            out["uncovered_pages"].append(page)
        if p["id"] not in named:
            out["unmapped_prompts"].append(p["id"])
    return out


def read_forecast(text):
    """(for_date or None, {metric: (lo, hi)}) from a forecast line or flag value."""
    m = re.search(r"^\s*-?\s*Forecast(?: for (\d{4}-\d{2}-\d{2}))?:\s*(.+)$", text or "", re.M | re.I)
    if m:
        body, day = m.group(2), m.group(1)
    else:  # a --forecast value, never a stray line elsewhere in the memory file
        body, day = ("" if "\n" in (text or "") else text or ""), None
    ranges = {k: (int(lo), int(hi)) for k, lo, hi in
              re.findall(r"(top10|top30|aio_cited)\s*[= ]\s*(\d+)\s*-\s*(\d+)", body)}
    return day, ranges


def score_forecast(day, ranges, actual, current_day):
    if not ranges or (day and day > current_day):
        return None
    return {"for": day, "metrics": {k: {"range": [lo, hi], "actual": actual.get(k),
                                        "inside": lo <= (actual.get(k) or 0) <= hi}
                                    for k, (lo, hi) in ranges.items()}}


def search_console(gsc_pages, gsc_queries, tracked, targeted):
    """Striking distance, untracked candidates and the page findings from Search Console rows."""
    striking = [{"query": q["query"], "page": _seo.path_of(q.get("page")),
                 "impressions": _seo.num(q.get("impressions"), 0), "position": _seo.num(q.get("position")),
                 "tracked": q["query"].lower() in tracked}
                for q in gsc_queries
                if 8 <= (_seo.num(q.get("position")) or 0) <= 20 and (_seo.num(q.get("impressions"), 0) or 0) >= 20]
    striking.sort(key=lambda q: -q["impressions"])
    totals = collections.Counter()
    for q in gsc_queries:
        if q["query"].lower() not in tracked:
            totals[q["query"]] += _seo.num(q.get("impressions"), 0) or 0
    candidates = [{"query": q, "impressions": n} for q, n in totals.most_common(20) if n]
    findings = []
    for g in gsc_pages:
        p = _seo.path_of(g.get("page"))
        verdict = (g.get("index_verdict") or "").upper()
        if p in targeted and verdict and verdict != "PASS":
            findings.append({"kind": "not_indexed", "score": 2, "ref": p,
                             "detail": g.get("index_coverage") or verdict})
        imp, clicks = _seo.num(g.get("impressions"), 0) or 0, _seo.num(g.get("clicks"), 0) or 0
        if imp >= 20 and not clicks:
            findings.append({"kind": "ctr_gap", "score": 2 if p in targeted else 1, "ref": p,
                             "detail": f"{imp} impressions, 0 clicks, position {g.get('position')}"})
    return striking, candidates, findings


def compute(current, history=(), keywords=(), prompts=None, gsc_pages=(), gsc_queries=(),
            aeo=(), forecast_text="", current_day=""):
    """Everything the seo-analyst reads, from snapshot rows. history: earlier runs, newest first."""
    prev = history[0] if history else None
    findings = []
    board = scoreboard(current)
    errors = [r for r in current if not _seo.flag(r.get("ok"))]
    if current and len(errors) > 0.1 * len(current):
        findings.append({"kind": "serp_errors", "score": 10,
                         "detail": f"{len(errors)} of {len(current)} SERP calls failed"})
    cw = crosswalk(keywords, prompts) if prompts is not None else None
    if cw and cw["missing_prompts"]:
        findings.append({"kind": "crosswalk_broken", "score": 10,
                         "detail": "aeo_prompts names " + ", ".join(cw["missing_prompts"])})
    for r in current:
        rk = rank(r)
        if _seo.branded(r) and _seo.flag(r.get("ok")) and rk != 1:
            findings.append({"kind": "branded_gap", "score": 3, "ref": r["keyword_id"], "tier": r.get("tier"),
                             "detail": f"{r['keyword']}: rank {rk or '>30'}"})
        if rk and r.get("target_url") and _seo.path_of(r.get("url")) != _seo.path_of(r["target_url"]):
            findings.append({"kind": "wrong_page", "score": 1, "ref": r["keyword_id"], "tier": r.get("tier"),
                             "detail": f"{r['keyword']}: rank {rk} with {r['url']}, target {r['target_url']}"})
    deltas = {"compared": 0, "gained_top10": [], "lost_top10": [], "aio_won": [], "aio_lost": [], "moves": []}
    if prev is not None:
        was = {r["keyword_id"]: r for r in prev}
        if set(was) != {r["keyword_id"] for r in current}:
            findings.append({"kind": "definition_change", "score": 10,
                             "detail": "keyword ids differ from the last run; deltas cover keywords in both"})
        for r in current:
            w = was.get(r["keyword_id"])
            if not (w and _seo.flag(w.get("ok")) and _seo.flag(r.get("ok"))):
                continue
            deltas["compared"] += 1
            kid, a, b = r["keyword_id"], rank(w) or 99, rank(r) or 99
            show = (lambda x: x if x < 99 else ">30")
            base = {"ref": kid, "tier": r.get("tier"), "score": _seo.weight(r.get("tier"))}
            if b <= 10 < a:
                deltas["gained_top10"].append(kid)
                findings.append({"kind": "win", **base, "detail": f"{r['keyword']}: {show(a)} -> {b}"})
            elif a <= 10 < b:
                deltas["lost_top10"].append(kid)
                findings.append({"kind": "loss", **base, "detail": f"{r['keyword']}: {a} -> {show(b)}"})
            elif a <= 30 and b <= 30 and abs(a - b) >= 5:
                deltas["moves"].append({"keyword_id": kid, "from": a, "to": b})
                findings.append({"kind": "rank_move", **base, "score": 1, "detail": f"{r['keyword']}: {a} -> {b}"})
            if _seo.flag(r.get("aio_cited")) != _seo.flag(w.get("aio_cited")):
                kind = "aio_won" if _seo.flag(r.get("aio_cited")) else "aio_lost"
                deltas[kind].append(kid)
                findings.append({"kind": kind, **base, "detail": f"{r['keyword']}: "
                                 + (r.get("aio_cited_paths") or w.get("aio_cited_paths") or "")})
    targeted = {_seo.path_of(k.get("target_url")) for k in keywords} | \
               {_seo.path_of(p.get("target_page")) for p in prompts or [] if p.get("status", "active") != "retired"}
    targeted.discard("")
    tracked = {(k.get("keyword") or "").lower() for k in keywords}
    striking, candidates, gsc_findings = search_console(gsc_pages, gsc_queries, tracked, targeted)
    findings += gsc_findings
    if aeo:
        joined = page_join.join(current, keywords, aeo, prompts or [])
        for p, e in joined.items():
            if e["top10"] and e["aeo_prompts"] and not e["aeo_cited"]:
                findings.append({"kind": "ranked_not_cited", "score": 2, "ref": p, "owner": "aeo",
                                 "detail": f"top 10 for {', '.join(e['top10'])}; prompts "
                                           f"{', '.join(e['aeo_prompts'])} never cite it"})
            if e["aeo_cited"] and not e["best_rank"] and e["keywords"]:
                findings.append({"kind": "cited_not_ranked", "score": 1, "ref": p,
                                 "detail": f"cited in {e['aeo_cited']} AEO answers; no tracked keyword ranks it"})
    day, ranges = read_forecast(forecast_text)
    actual = board["non_branded"]
    fc = score_forecast(day, ranges, actual, current_day)
    for k, v in (fc or {}).get("metrics", {}).items():
        if not v["inside"]:
            findings.append({"kind": "forecast_miss", "score": 5, "ref": k,
                             "detail": f"{v['actual']} outside {v['range'][0]}-{v['range'][1]}"})
    findings.sort(key=lambda f: (f["kind"] not in PRIORITY, -f["score"], str(f.get("ref", ""))))
    series = [{k: rates([r for r in run if not _seo.branded(r)])[k] for k in ("n", "top10", "top30", "aio_cited")}
              for run in list(reversed(list(history))) + [current]]
    return {"scoreboard": board, "deltas": deltas, "findings": findings, "crosswalk": cw,
            "forecast_check": fc, "striking_distance": striking, "candidates": candidates,
            "history": series, "trend_ok": len(series) >= 4}


def summary(res, names):
    b = res["scoreboard"]
    o = b["non_branded"]
    lines = [f"SERP {names['serp']} vs {names['previous'] or 'nothing (first run: no deltas)'}",
             f"non-branded: top 10 {o['top10']} of {o['n']}, top 30 {o['top30']}, on target {o['on_target']}, "
             f"AI Overview shown {o['aio']}, citing us {o['aio_cited']}"]
    for t, v in b["by_tier"].items():
        lines.append(f"  tier {t} {_seo.TIERS.get(t, '?')}: top 10 {v['top10']} of {v['n']} · top 30 {v['top30']}"
                     f" · AI Overview cites us {v['aio_cited']} of {v['aio']}")
    lines.append(f"branded: first on {b['branded']['first']} of {b['branded']['n']}")
    hist = " → ".join(f"{h['top10']}/{h['n']}" for h in res["history"])
    lines.append(f"top-10 series: {hist}" + ("" if res["trend_ok"] else " (fewer than 4 runs: no trend)"))
    cw = res["crosswalk"]
    lines.append("crosswalk: " + (" · ".join(f"{k} {len(v)}" for k, v in cw.items()) if cw
                                  else "skipped (data/seo/prompts.csv has no id column)"))
    fc = res["forecast_check"]
    if fc:
        lines.append("forecast: " + " · ".join(f"{k} {v['actual']} in {v['range'][0]}-{v['range'][1]}: "
                                               + ("inside" if v["inside"] else "MISS") for k, v in fc["metrics"].items()))
    lines.append(f"search console: {names['gsc_pages'] or 'none'}; striking distance {len(res['striking_distance'])}, "
                 f"untracked queries {len(res['candidates'])}")
    lines.append(f"findings: {len(res['findings'])}")
    for f in res["findings"][:15]:
        lines.append(f"  - {f['kind']} {f.get('ref', '')} {f['detail']}".rstrip())
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--snapshot", help="the SERP snapshot to score (default: the newest)")
    ap.add_argument("--forecast", help='e.g. "top10=3-6,top30=8-12,aio_cited=0-2" (else the memory file)')
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    runs = _seo.snapshots("serp")
    current = Path(a.snapshot) if a.snapshot else (runs[-1] if runs else None)
    if not current or not current.is_file():
        sys.exit("No SERP snapshot in data/seo/snapshots/; run scripts/seo_rank_track.py first.")
    day = current.name[:10]
    earlier = [p for p in runs if p.name[:10] < day][-HISTORY:]
    history = [_seo.read_csv(p) for p in reversed(earlier)]
    gsc_pages = _seo.latest("gsc-pages", on_or_before=day)
    gsc_queries = _seo.latest("gsc-queries", on_or_before=day)
    aeo = _seo.latest("aeo-results", on_or_before=day)
    forecast = a.forecast or (MEMORY.read_text(encoding="utf-8") if MEMORY.is_file() else "")
    res = compute(_seo.read_csv(current), history, _seo.keywords(), _seo.prompts(),
                  _seo.read_csv(gsc_pages) if gsc_pages else [], _seo.read_csv(gsc_queries) if gsc_queries else [],
                  _seo.read_csv(aeo) if aeo else [], forecast, day)
    names = {"serp": current.name, "previous": earlier[-1].name if earlier else None,
             "gsc_pages": gsc_pages.name if gsc_pages else None, "aeo": aeo.name if aeo else None}
    print(json.dumps({"sources": names, **res}, indent=2) if a.json else summary(res, names))
    return 1 if res["crosswalk"] and res["crosswalk"]["missing_prompts"] else 0


if __name__ == "__main__":
    sys.exit(main())
