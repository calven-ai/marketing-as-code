#!/usr/bin/env python3
"""Ask answer engines every active prompt in data/seo/prompts.csv through DataForSEO and record who
they name and cite: data/seo/snapshots/YYYY-MM-DD-dataforseo-aeo-results.csv (one row per prompt
and engine) plus -aeo-answers.csv (the answer text and sources). Engines chatgpt, google_ai_mode
and claude by default, others with --engines; --estimate prints the cost, --dry-run lists the
calls, --max-usd refuses a dearer run, --redetect re-scores saved answers without spending.
Needs DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD (environment or .env). Standard library only.

    python3 scripts/aeo_track.py --estimate
    python3 scripts/aeo_track.py --category "[category]"     # the weekly collection
    python3 scripts/aeo_track.py --limit 2 --engines chatgpt --out /tmp/aeo   # smoke test
    python3 scripts/aeo_track.py --redetect                  # after a brands.csv change

Snapshots are immutable: a second run on the same day refuses. Brand detection reads prose only
(brands.csv aliases, word boundaries); prominence and accuracy are the brand-monitor skill's.
"""
import argparse
import datetime as dt
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import _aeo
from _common import ROOT, setting, snapshot_path

MAX_CHARS = 8000
# engine -> (label, DataForSEO endpoint, model sent, estimated USD per prompt, measured 2026-09-29).
# The default three are the cheap, distinct surfaces a buyer meets; the rest stay for --engines.
ENGINES = {
    "chatgpt": ("ChatGPT web UI, logged out", "ai_optimization/chat_gpt/llm_scraper/live/advanced",
                "chatgpt-web", 0.004),
    "google_ai_mode": ("Google AI Mode", "serp/google/ai_mode/live/advanced", "ai-mode", 0.004),
    "claude": ("Claude with web search", "ai_optimization/claude/llm_responses/live",
               "claude-haiku-4-5", 0.025),
    "perplexity": ("Perplexity", "ai_optimization/perplexity/llm_responses/live", "sonar", 0.007),
    "gemini": ("Gemini", "ai_optimization/gemini/llm_responses/live", "gemini-3.5-flash", 0.085),
    "google_aio": ("Google AI Overview", "serp/google/organic/live/advanced", "aio", 0.004),
}
DEFAULT_ENGINES = ["chatgpt", "google_ai_mode", "claude"]


def payload(engine, prompt, location=2840, language="en"):
    if engine in ("chatgpt", "google_ai_mode"):
        return [{"keyword": prompt, "location_code": location, "language_code": language}]
    if engine == "google_aio":
        return [{"keyword": prompt, "location_code": location, "language_code": language,
                 "depth": 10, "load_async_ai_overview": True}]
    return [{"user_prompt": prompt, "model_name": ENGINES[engine][2], "web_search": True}]


def _urls(refs):
    return [r["url"] for r in refs or [] if isinstance(r, dict) and r.get("url")]


def parse(engine, res):
    """One DataForSEO result as {text, sources, fan_out, model}."""
    text, sources, model = "", [], res.get("model") or res.get("model_name") or ENGINES[engine][2]
    if engine == "chatgpt":
        text = res.get("markdown") or ""
        sources = _urls(res.get("sources"))
        for item in res.get("items") or []:
            sources += _urls(item.get("sources"))
    elif engine in ("google_ai_mode", "google_aio"):
        for item in res.get("items") or []:
            if item.get("type") == "ai_overview":
                text += (item.get("markdown") or "") + "\n"
                sources += _urls(item.get("references"))
    else:
        for item in res.get("items") or []:
            if item.get("type") != "message":
                continue
            for section in item.get("sections") or []:
                if section.get("type") == "text":
                    text += section.get("text") or ""
                    sources += _urls(section.get("annotations"))
    return {"text": text.strip(), "sources": list(dict.fromkeys(sources)),
            "fan_out": res.get("fan_out_queries") or [], "model": model}


def ask(engine, prompt, brands, caller, category=None, location=2840, language="en", retry=True):
    """One prompt on one engine: (result row, answer row or None). Never raises on an API error."""
    row = {"prompt_id": prompt["id"], "engine": engine, "model": ENGINES[engine][2],
           "answered": "false", "cost_usd": 0, "error": ""}
    try:
        body = caller(ENGINES[engine][1], payload(engine, prompt["prompt"], location, language))
    except SystemExit as err:  # seo_snapshot.call exits on HTTP errors; keep the run going
        row["error"] = str(err)[:200]
        return row, None
    task = (body.get("tasks") or [{}])[0]
    row["cost_usd"] = round(body.get("cost") or task.get("cost") or 0, 6)
    if task.get("status_code") != 20000 or not task.get("result"):
        row["error"] = f"{task.get('status_code')} {task.get('status_message')}"[:200]
        return row, None
    p = parse(engine, task["result"][0])
    ok = _aeo.answered(p["text"], p["sources"])
    if not ok and retry and engine == "chatgpt":
        # The web UI sometimes returns only a preamble: one retry, both costs counted.
        again, answer = ask(engine, prompt, brands, caller, category, location, language, retry=False)
        again["cost_usd"] = round(float(again["cost_usd"]) + row["cost_usd"], 6)
        return again, answer
    row.update(model=p["model"], answered=_aeo.flag(ok), answer_chars=len(p["text"]),
               **_aeo.to_row(_aeo.detect(p["text"], p["sources"], brands, category)))
    answer = {"prompt_id": prompt["id"], "engine": engine, "text": p["text"][:MAX_CHARS],
              "sources": "|".join(u.replace("|", "%7C") for u in p["sources"][:40]),
              "fan_out": "|".join(q.replace("|", " ") for q in p["fan_out"][:20])}
    return row, answer


def collect(prompts, engines, brands, caller, category=None, workers=6, location=2840, language="en"):
    jobs = [(e, p) for p in prompts for e in engines]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(lambda j: ask(j[0], j[1], brands, caller, category, location, language), jobs))


def estimate(n_prompts, engines):
    return round(n_prompts * sum(ENGINES[e][3] for e in engines), 2)


def redetect(results_path, brands, category=None):
    """Re-score one saved run from its answers file: (prompt_id, engine, field, old, new) per change.
    Writes nothing; aeo_diff.py --redetect applies the same re-scoring when it scores."""
    answers = {(a["prompt_id"], a["engine"]): a for a in _aeo.read_csv(_aeo.answers_file(results_path))}
    changes = []
    for row in _aeo.read_csv(results_path):
        a = answers.get((row["prompt_id"], row["engine"]))
        if not a:
            continue
        sources = _aeo.split(a["sources"])
        new = {"answered": _aeo.flag(_aeo.answered(a["text"], sources)),
               **_aeo.to_row(_aeo.detect(a["text"], sources, brands, category))}
        for field, value in new.items():
            if str(row.get(field, "")) != str(value):
                changes.append((row["prompt_id"], row["engine"], field, row.get(field, ""), value))
    return changes


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--engines", default=",".join(DEFAULT_ENGINES),
                    help=f"comma-separated, from {', '.join(ENGINES)}")
    ap.add_argument("--category", default="", help="the team's one category name, matched in prose")
    ap.add_argument("--limit", type=int, help="only the first N active prompts (smoke test; use --out)")
    ap.add_argument("--max-usd", type=float, default=5.0, help="refuse a run estimated above this")
    ap.add_argument("--estimate", action="store_true", help="print the cost estimate and stop")
    ap.add_argument("--dry-run", action="store_true", help="list every call and stop, no API call")
    ap.add_argument("--redetect", nargs="?", const="latest", metavar="RESULTS_CSV",
                    help="re-score a saved run (default the newest) from its answers; no calls, no writes")
    ap.add_argument("--location", type=int, default=2840, help="DataForSEO location code (2840 = US)")
    ap.add_argument("--language", default="en")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--out", help="write into this folder instead of data/seo/snapshots (smoke tests)")
    a = ap.parse_args(argv)

    brands = _aeo.load_brands()
    if a.redetect:
        files = _aeo.results_files()
        path = Path(a.redetect) if a.redetect != "latest" else (files[-1] if files else None)
        if not path or not path.is_file():
            sys.exit("no results snapshot to re-score")
        changes = redetect(path, brands, a.category)
        for pid, engine, field, old, new in changes:
            print(f"{pid}/{engine} {field}: {old or '(empty)'} -> {new or '(empty)'}")
        print(f"{len(changes)} change(s) in {path.name}; the snapshot is unchanged, "
              "aeo_diff.py --redetect scores with them")
        return

    engines = [e.strip() for e in a.engines.split(",") if e.strip()]
    unknown = [e for e in engines if e not in ENGINES]
    if unknown:
        sys.exit(f"unknown engine(s) {unknown}; known: {', '.join(ENGINES)}")
    if not _aeo.self_brand(brands):
        sys.exit("data/seo/brands.csv has no row with kind self; add ours first")
    prompts = _aeo.load_prompts()[: a.limit] if a.limit else _aeo.load_prompts()
    if not prompts:
        sys.exit("data/seo/prompts.csv has no active prompts")
    est = estimate(len(prompts), engines)
    print(f"{len(prompts)} prompts x {len(engines)} engines ({', '.join(engines)}) = "
          f"{len(prompts) * len(engines)} calls, estimated ${est}")
    if a.dry_run:
        for p in prompts:
            for e in engines:
                print(f"  {p['id']} {e:15} {ENGINES[e][1]}  {p['prompt']}")
    if a.estimate or a.dry_run:
        return
    if est > a.max_usd:
        sys.exit(f"estimated ${est} is over --max-usd {a.max_usd}; trim the set or raise the cap")
    if not setting("DATAFORSEO_LOGIN") or not setting("DATAFORSEO_PASSWORD"):
        sys.exit("DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD are not set. See integrations/README.md.")

    today = dt.date.today().isoformat()
    if a.out:
        Path(a.out).mkdir(parents=True, exist_ok=True)
        results_path = Path(a.out) / f"{today}-dataforseo-aeo-results.csv"
    else:
        results_path = snapshot_path("seo", "dataforseo", "aeo-results", day=today)
    if results_path.exists():
        sys.exit(f"{results_path.name} exists and snapshots are immutable; run again tomorrow or use --out")

    from seo_snapshot import call  # the shared DataForSEO call; imported late so tests need no key
    done = collect(prompts, engines, brands, call, a.category, a.workers, a.location, a.language)
    rows = [r for r, _ in done]
    if all(r["error"] for r in rows):
        sys.exit("every call failed; nothing written. First error: " + rows[0]["error"])
    stamp = {"prompts_sha": _aeo.sha(_aeo.PROMPTS), "brands_sha": _aeo.sha(_aeo.BRANDS)}
    for r in rows:
        r.update(stamp)
    _aeo.write_csv(results_path, _aeo.RESULT_COLUMNS, rows)
    _aeo.write_csv(_aeo.answers_file(results_path), _aeo.ANSWER_COLUMNS, [x for _, x in done if x])
    n = sum(1 for r in rows if r["answered"] == "true")
    named = sum(1 for r in rows if r.get("mentioned") == "true")
    cost = round(sum(float(r["cost_usd"] or 0) for r in rows), 4)
    errors = sum(1 for r in rows if r["error"])
    where = results_path.relative_to(ROOT) if results_path.is_relative_to(ROOT) else results_path
    print(f"saved {where}: named in {named} of {n} answered, {errors} errors, ${cost} billed")


if __name__ == "__main__":
    main()
