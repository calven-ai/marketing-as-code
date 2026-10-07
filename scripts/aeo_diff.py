#!/usr/bin/env python3
"""Score the newest AEO results snapshot (data/seo/snapshots/*-aeo-results.csv) against up to 8
prior runs: named, cited and named-first rates on non-branded prompts by tier, track, stage and
engine; share of voice; rolling 4-run rates with Wilson intervals; per prompt-and-engine deltas;
ranked findings (3/2/1 by tier); definition changes; the last report's forecast scored. Prints
Markdown for the brand-monitor report; --json prints everything as JSON; --save writes
data/seo/snapshots/YYYY-MM-DD-repo-aeo-scores.csv for an unattended run. Never edits a snapshot.
No network, standard library only.

    python3 scripts/aeo_diff.py                       # the newest run, Markdown
    python3 scripts/aeo_diff.py --json > /tmp/aeo.json
    python3 scripts/aeo_diff.py --redetect --category "[category]"   # re-score saved answers first

Rates are k of n over answered prompt-and-engine pairs; an error or an empty answer is not in n.
"""
import argparse
import collections
import json
import math
import re
import sys
from pathlib import Path

import _aeo
from _common import ROOT, snapshot_path

REPORTS = ROOT / "reports" / "recurring" / "mentions"
DIMENSIONS = ("tier", "track", "stage", "engine", "intent")
PRIORITY = ("definition_change", "engine_errors", "forecast_miss")
FORECAST_RE = re.compile(r"Forecast for the next run.*?named (\d+) to (\d+).*?cited (\d+) to (\d+)"
                         r".*?first (\d+) to (\d+)", re.I)
SCORE_COLUMNS = ["section", "dimension", "group", "metric", "k", "n", "ci_low", "ci_high", "detail"]


def wilson(k, n, z=1.96):
    """95% Wilson score interval for k of n, or None when n is 0."""
    if not n:
        return None
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return [round(max(0.0, centre - half), 4), round(min(1.0, centre + half), 4)]


# --------------------------------------------------------------- loading --

def run_date(path):
    return Path(path).name[:10]


def load_run(path, brands=None, category=None, redetect=False):
    """One results snapshot as normalized rows; with redetect, re-scored from its answers file."""
    answers = {}
    if redetect and _aeo.answers_file(path).is_file():
        answers = {(a["prompt_id"], a["engine"]): a for a in _aeo.read_csv(_aeo.answers_file(path))}
    rows, prompts_sha, brands_sha = [], "", ""
    for raw in _aeo.read_csv(path):
        prompts_sha = raw.get("prompts_sha") or prompts_sha
        brands_sha = raw.get("brands_sha") or brands_sha
        a = answers.get((raw["prompt_id"], raw["engine"]))
        if a is not None and brands is not None:
            sources = _aeo.split(a["sources"])
            raw = {**raw, "answered": _aeo.flag(_aeo.answered(a["text"], sources)),
                   **_aeo.to_row(_aeo.detect(a["text"], sources, brands, category))}
        rows.append({"prompt_id": raw["prompt_id"], "engine": raw["engine"],
                     "answered": _aeo.truthy(raw.get("answered")),
                     "mentioned": _aeo.truthy(raw.get("mentioned")),
                     "top": str(raw.get("position", "")).strip() == "1",
                     "cited": _aeo.truthy(raw.get("cited_self")),
                     "category_phrase": _aeo.truthy(raw.get("category_phrase")),
                     "cited_paths": _aeo.split(raw.get("cited_paths")),
                     "cited_domains": _aeo.split(raw.get("cited_domains")),
                     "brands": _aeo.split(raw.get("brands")),
                     "error": raw.get("error", "")})
    if redetect and brands is not None:
        brands_sha = _aeo.sha(_aeo.BRANDS)  # every re-scored run shares today's brand list
    return {"date": run_date(path), "path": str(path), "rows": rows, "prompts_sha": prompts_sha,
            "brands_sha": brands_sha, "engines": sorted({r["engine"] for r in rows})}


def enrich(run, prompts):
    """Rows joined to today's prompt definitions, so a rolling window never mixes definitions.
    A retired prompt's answers group as tier and track "retired"; an unknown id as "unknown"."""
    out = []
    for r in run["rows"]:
        p = prompts.get(r["prompt_id"])
        if p is None:
            extra = {"tier": "unknown", "track": "unknown", "stage": "unknown", "intent": "unknown"}
        else:
            gone = p.get("status") == "retired"
            extra = {"tier": "retired" if gone else (p.get("tier") or "unknown"),
                     "track": "retired" if gone else (p.get("track") or "unknown"),
                     "stage": p.get("stage") or "unknown", "intent": p.get("intent") or "unknown",
                     "target_page": p.get("target_page", ""), "prompt": p.get("prompt", "")}
        out.append({**r, **extra})
    return out


def non_branded(rows):
    return [r for r in rows if r.get("intent") != "branded"]


# --------------------------------------------------------------- metrics --

def rates(rows, interval=False):
    ans = [r for r in rows if r["answered"]]
    out = {"n": len(ans)}
    for key in ("mentioned", "cited", "top", "category_phrase"):
        out[key] = sum(1 for r in ans if r[key])
        if interval and key != "category_phrase":
            out[f"{key}_ci"] = wilson(out[key], out["n"])
    if interval:
        out["comparable"] = out["n"] >= 20
    return out


def breakdown(rows, interval=False):
    out = {"overall": rates(rows, interval)}
    for dim in DIMENSIONS:
        groups = collections.defaultdict(list)
        for r in rows:
            groups[str(r.get(dim))].append(r)
        out[f"by_{dim}"] = {k: rates(v, interval) for k, v in sorted(groups.items())}
    return out


def share_of_voice(rows, kinds):
    ans = [r for r in rows if r["answered"]]
    counts = collections.Counter(b for r in ans for b in r["brands"])
    total = sum(counts.values())
    return [{"brand": b, "kind": kinds.get(b, "untracked"), "answers": c, "n": len(ans),
             "share": round(c / total, 3) if total else 0} for b, c in counts.most_common()]


def metrics(rows, kinds):
    nb = non_branded(rows)
    nb_ans = [r for r in nb if r["answered"]]
    pages = collections.defaultdict(list)
    for r in nb_ans:
        for p in r["cited_paths"]:
            pages[p].append(f"{r['prompt_id']}/{r['engine']}")
    domains = collections.Counter(d for r in nb_ans for d in r["cited_domains"])
    branded = [{"prompt_id": r["prompt_id"], "engine": r["engine"], "mentioned": r["mentioned"]}
               for r in rows if r.get("intent") == "branded" and r["answered"]]
    return {"all_prompts": rates(rows), "non_branded": breakdown(nb),
            "share_of_voice": share_of_voice(nb, kinds),
            "self_cited": dict(sorted(pages.items(), key=lambda kv: (-len(kv[1]), kv[0]))),
            "cited_domains": [{"domain": d, "answers": c} for d, c in domains.most_common(20)],
            "branded": branded}


def rolling(enriched_runs):
    """Pooled over the newest run and up to 3 before it, with Wilson intervals."""
    window = enriched_runs[:4]
    pooled = [r for rows in window for r in rows]
    out = breakdown(non_branded(pooled), interval=True)
    out["periods"] = len(window)
    out["trend_ok"] = len(enriched_runs) >= 4
    return out


# -------------------------------------------------------------- findings --

def weight(tier):
    return _aeo.TIER_WEIGHT.get(str(tier), 1)


def pairs(rows):
    return {(r["prompt_id"], r["engine"]): r for r in rows if r["answered"]}


def compute(current, history, prompts, kinds, forecast=None, tracked_domains=()):
    """Everything the report needs. current and history are load_run() results, newest first."""
    cur = enrich(current, prompts)
    hist = [enrich(h, prompts) for h in history]
    findings = []
    deltas = {"compared_pairs": 0, "gained_mention": [], "lost_mention": [],
              "gained_citation": [], "lost_citation": []}

    errors = [r for r in cur if r["error"]]
    if cur and len(errors) > 0.1 * len(cur):
        findings.append({"kind": "engine_errors", "score": 10,
                         "detail": f"{len(errors)} of {len(cur)} calls failed"})
    for r in cur:
        if r.get("intent") == "branded" and r["answered"] and not r["mentioned"]:
            findings.append({"kind": "branded_gap", "score": 3, "tier": r["tier"], "prompt_id": r["prompt_id"],
                             "engine": r["engine"], "detail": "branded prompt answered without naming us"})

    if history:
        prev = history[0]
        changed = [k for k in ("prompts_sha", "brands_sha") if prev[k] and current[k] and prev[k] != current[k]]
        if prev["engines"] != current["engines"]:
            changed.append("engines")
        if changed:
            findings.append({"kind": "definition_change", "score": 10,
                             "detail": f"{', '.join(changed)} changed since {prev['date']}; deltas cover only "
                                       "pairs present in both runs"})
        a, b = pairs(hist[0]), pairs(cur)
        common = sorted(set(a) & set(b))
        deltas["compared_pairs"] = len(common)
        for key in common:
            was, now = a[key], b[key]
            tag = f"{key[0]}/{key[1]}"
            for field, gain, lose, kind in (("mentioned", "gained_mention", "lost_mention", "mention"),
                                            ("cited", "gained_citation", "lost_citation", "citation")):
                if now[field] == was[field]:
                    continue
                deltas[gain if now[field] else lose].append(tag)
                if now.get("intent") == "branded":
                    continue
                findings.append({"kind": f"{kind}_{'win' if now[field] else 'loss'}", "score": weight(now["tier"]),
                                 "tier": now["tier"], "prompt_id": key[0], "engine": key[1],
                                 "detail": now.get("prompt", "")})
        now_c = collections.Counter(x for k, r in b.items() if k in a for x in r["brands"])
        was_c = collections.Counter(x for k, r in a.items() if k in b for x in r["brands"])
        for brand, c in now_c.items():
            if kinds.get(brand) != "self" and c - was_c.get(brand, 0) >= 3:
                findings.append({"kind": "competitor_gain", "score": 1, "brand": brand,
                                 "detail": f"named in {c} answers, {was_c.get(brand, 0)} last run (same pairs)"})

    seen_paths = {p for rows in hist for r in rows for p in r["cited_paths"]}
    seen_domains = {d for rows in hist for r in rows for d in r["cited_domains"]}
    for r in cur:
        for p in r["cited_paths"]:
            if p not in seen_paths:
                seen_paths.add(p)
                findings.append({"kind": "first_citation", "score": 3, "tier": r["tier"], "path": p,
                                 "prompt_id": r["prompt_id"], "engine": r["engine"]})
    if history:
        doms = collections.Counter(d for r in cur if r["answered"] for d in r["cited_domains"])
        for d, c in doms.items():
            if c >= 3 and d not in seen_domains and d not in tracked_domains:
                findings.append({"kind": "new_domain", "score": 1, "domain": d,
                                 "detail": f"cited in {c} answers, never before"})

    check = None
    if forecast:
        overall = rates(non_branded(cur))
        check = {}
        for key, (lo, hi) in forecast.items():
            inside = lo <= overall[key] <= hi
            check[key] = {"range": [lo, hi], "actual": overall[key], "inside": inside}
            if not inside:
                findings.append({"kind": "forecast_miss", "score": 5, "metric": key,
                                 "detail": f"{overall[key]} outside {lo} to {hi}"})

    for f in findings:
        f["priority"] = f["kind"] in PRIORITY
    findings.sort(key=lambda f: (not f["priority"], -f["score"], f.get("prompt_id", ""), f.get("engine", "")))
    return {"date": current["date"], "snapshot": current["path"], "history": [h["date"] for h in history],
            "metrics": metrics(cur, kinds), "rolling_4": rolling([cur] + hist),
            "deltas": deltas, "findings": findings, "forecast_check": check}


# -------------------------------------------------------------- forecast --

def find_forecast(reports_dir, current_date, prev_date):
    """The forecast the last report made for this run: {metric: (lo, hi)}, or None.
    Only a report dated on or after the previous run and before this one counts."""
    if not prev_date:
        return None
    candidates = sorted(p for p in Path(reports_dir).glob("????-??-??.md") if prev_date <= p.stem < current_date)
    if not candidates:
        return None
    m = FORECAST_RE.search(candidates[-1].read_text(encoding="utf-8"))
    if not m:
        return None
    v = [int(x) for x in m.groups()]
    return {"mentioned": (v[0], v[1]), "cited": (v[2], v[3]), "top": (v[4], v[5])}


# ---------------------------------------------------------------- output --

def kofn(r, key):
    return f"{r[key]} of {r['n']}"


def ci(r, key):
    c = r.get(f"{key}_ci")
    return f"{c[0]:.0%} to {c[1]:.0%}" if c else "n/a"


def markdown(res):
    m, r4 = res["metrics"], res["rolling_4"]
    nb = m["non_branded"]
    out = [f"# AEO scores, run {res['date']}", "",
           f"Snapshot `{Path(res['snapshot']).name}`; compared with {len(res['history'])} prior run(s). "
           "Rates on non-branded prompts, k of n answered pairs.", "",
           "## Scoreboard by tier", "",
           f"| Tier | Named | Cited | Named first | Rolling {r4['periods']}: named (95% CI) | cited (95% CI) |",
           "| --- | --- | --- | --- | --- | --- |"]
    for tier, v in nb["by_tier"].items():
        roll = r4["by_tier"].get(tier, {"n": 0, "mentioned": 0, "cited": 0})
        name = f"{tier} {_aeo.TIER_NAMES.get(tier, '')}".strip()
        out.append(f"| {name} | {kofn(v, 'mentioned')} | {kofn(v, 'cited')} | {kofn(v, 'top')} | "
                   f"{kofn(roll, 'mentioned')} ({ci(roll, 'mentioned')}) | {kofn(roll, 'cited')} ({ci(roll, 'cited')}) |")
    o = nb["overall"]
    out.append(f"| All | {kofn(o, 'mentioned')} | {kofn(o, 'cited')} | {kofn(o, 'top')} | "
               f"{kofn(r4['overall'], 'mentioned')} ({ci(r4['overall'], 'mentioned')}) | "
               f"{kofn(r4['overall'], 'cited')} ({ci(r4['overall'], 'cited')}) |")
    out.append("")
    for dim in ("track", "stage", "engine"):
        out.append(f"By {dim}: " + " · ".join(f"{k} named {kofn(v, 'mentioned')}, cited {v['cited']}"
                                              for k, v in nb[f"by_{dim}"].items()))
    out.append(f"Category name used in {kofn(o, 'category_phrase')} answers.")
    if not r4["trend_ok"]:
        out.append(f"Fewer than 4 runs ({r4['periods']}): no trend. Compare groups only where n >= 20.")
    branded = m["branded"]
    if branded:
        out.append(f"Branded prompts (accuracy, audited by hand): named in "
                   f"{sum(1 for b in branded if b['mentioned'])} of {len(branded)} answers.")
    out += ["", "## Share of voice (non-branded)", ""]
    out += [f"- {s['brand']} ({s['kind']}): {s['answers']} of {s['n']} answers, {s['share']:.0%} of brand mentions"
            for s in m["share_of_voice"][:10]] or ["- No tracked brand named."]
    out += ["", "## Our pages cited (non-branded)", ""]
    out += [f"- `{p}`: {len(v)} ({', '.join(v[:6])})" for p, v in list(m["self_cited"].items())[:10]] or ["- None."]
    out += ["", "Top cited domains: " + (", ".join(f"{d['domain']} {d['answers']}" for d in m["cited_domains"][:10])
                                         or "none")]
    d = res["deltas"]
    out += ["", "## Deltas", "",
            f"{d['compared_pairs']} pairs in both runs: mention +{len(d['gained_mention'])} / -{len(d['lost_mention'])}, "
            f"citation +{len(d['gained_citation'])} / -{len(d['lost_citation'])}." if res["history"]
            else "First run: no deltas, no forecast score."]
    if res["forecast_check"]:
        out.append("Forecast: " + " · ".join(f"{k} {v['actual']} in {v['range'][0]} to {v['range'][1]}: "
                                             f"{'hit' if v['inside'] else 'miss'}"
                                             for k, v in res["forecast_check"].items()))
    out += ["", f"## Findings ({len(res['findings'])})", ""]
    for f in res["findings"][:20]:
        where = "/".join(x for x in (f.get("prompt_id"), f.get("engine")) if x)
        tier = f"T{f['tier']} " if f.get("tier") else ""
        what = f.get("path") or f.get("brand") or f.get("domain") or f.get("metric") or ""
        parts = [f"- [{f['score']}] {tier}{f['kind']}", where, what, f.get("detail") or ""]
        out.append(" ".join(p for p in parts if p))
    if not res["findings"]:
        out.append("- None.")
    return "\n".join(out) + "\n"


def score_rows(res):
    """The result as a long table for --save."""
    rows = []
    for section, data in (("run", res["metrics"]["non_branded"]), ("rolling4", res["rolling_4"])):
        for dim in ("overall",) + tuple(f"by_{d}" for d in DIMENSIONS):
            groups = {"all": data[dim]} if dim == "overall" else data[dim]
            for group, v in groups.items():
                for metric in ("mentioned", "cited", "top"):
                    c = v.get(f"{metric}_ci") or ["", ""]
                    rows.append({"section": section, "dimension": dim.replace("by_", ""), "group": group,
                                 "metric": metric, "k": v[metric], "n": v["n"], "ci_low": c[0], "ci_high": c[1]})
    for s in res["metrics"]["share_of_voice"]:
        rows.append({"section": "sov", "dimension": "brand", "group": s["brand"], "metric": "named",
                     "k": s["answers"], "n": s["n"], "detail": s["kind"]})
    for f in res["findings"]:
        where = "/".join(x for x in (f.get("prompt_id"), f.get("engine")) if x)
        rows.append({"section": "finding", "dimension": f["kind"], "group": where or f.get("path") or
                     f.get("brand") or f.get("domain") or f.get("metric") or "", "metric": "score",
                     "k": f["score"], "detail": f.get("detail", "") or f.get("path", "")})
    for key, v in (res["forecast_check"] or {}).items():
        rows.append({"section": "forecast", "dimension": key, "group": "hit" if v["inside"] else "miss",
                     "metric": key, "k": v["actual"], "ci_low": v["range"][0], "ci_high": v["range"][1]})
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("snapshot", nargs="?", help="a *-aeo-results.csv (default: the newest)")
    ap.add_argument("--history", type=int, default=8, help="prior runs to read (default 8)")
    ap.add_argument("--json", action="store_true", help="print the full result as JSON")
    ap.add_argument("--save", action="store_true", help="also write data/seo/snapshots/<date>-repo-aeo-scores.csv")
    ap.add_argument("--redetect", action="store_true", help="re-score every run from its answers file first")
    ap.add_argument("--category", default="", help="the category name, for --redetect")
    ap.add_argument("--reports", default=str(REPORTS), help="where the last report's forecast is read")
    a = ap.parse_args(argv)

    files = _aeo.results_files()
    path = Path(a.snapshot) if a.snapshot else (files[-1] if files else None)
    if not path or not path.is_file():
        sys.exit("no *-aeo-results.csv snapshot in data/seo/snapshots/; run scripts/aeo_track.py first")
    folder_files = _aeo.results_files(path.parent)
    prior = [p for p in folder_files if run_date(p) < run_date(path)][-a.history:][::-1]
    brands = _aeo.load_brands() if _aeo.BRANDS.is_file() else []
    kinds = {b["brand"]: b["kind"] for b in brands}
    prompts = {p["id"]: p for p in _aeo.load_prompts(active_only=False)} if _aeo.PROMPTS.is_file() else {}
    load = lambda p: load_run(p, brands if a.redetect else None, a.category, a.redetect)  # noqa: E731
    current, history = load(path), [load(p) for p in prior]
    forecast = find_forecast(a.reports, current["date"], history[0]["date"] if history else None)
    res = compute(current, history, prompts, kinds, forecast, {d for b in brands for d in b["domains"]})
    if a.save:
        out = snapshot_path("seo", "repo", "aeo-scores", day=current["date"])
        if out.exists():
            sys.exit(f"{out.name} exists and snapshots are immutable")
        _aeo.write_csv(out, SCORE_COLUMNS, score_rows(res))
        print(f"saved {out.relative_to(ROOT)}", file=sys.stderr)
    print(json.dumps(res, indent=1) if a.json else markdown(res), end="" if not a.json else "\n")


if __name__ == "__main__":
    main()
