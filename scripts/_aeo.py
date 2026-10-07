"""Shared pieces of the AEO tracker (scripts/aeo_track.py and scripts/aeo_diff.py): the prompt set,
the brand list, brand detection on answer prose, and the snapshot files. Standard library only.

Detection is deterministic and reads prose only: links, bare URLs and domain-shaped citation
labels are stripped first, so `[example.com](https://example.com)` is a citation, never a
mention. Prominence and accuracy are the agent's judgment, not this module's.
"""

import csv
import hashlib
import re
from pathlib import Path
from urllib.parse import urlparse

from _common import DATA

SEO = DATA / "seo"
PROMPTS = SEO / "prompts.csv"
BRANDS = SEO / "brands.csv"
SNAPSHOTS = SEO / "snapshots"

RESULT_COLUMNS = ["prompt_id", "engine", "model", "answered", "mentioned", "position", "cited_self",
                  "cited_paths", "cited_domains", "brands", "category_phrase", "answer_chars",
                  "cost_usd", "error", "prompts_sha", "brands_sha"]
ANSWER_COLUMNS = ["prompt_id", "engine", "text", "sources", "fan_out"]
TIER_WEIGHT = {"1": 3, "2": 2, "3": 1}
TIER_NAMES = {"1": "Buy", "2": "Problem", "3": "Authority"}

URL_RE = re.compile(r"\]\([^)]*\)|https?://\S+|www\.\S+")
LABEL_RE = re.compile(r"\[[\w.-]+\.[a-z]{2,}(?:\s*\+\d+)?\]", re.I)
# Shorter than this with no sources is a preamble ("I'll search for that") or an empty shell:
# left out of n, never counted as "not named".
MIN_ANSWER_CHARS = 500


def sha(path):
    """First 12 hex characters of the file's SHA-256, or "" when it does not exist."""
    path = Path(path)
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12] if path.is_file() else ""


def split(value):
    """A `|`-separated cell as a list, empty parts dropped."""
    return [v.strip() for v in (value or "").split("|") if v.strip()]


def read_csv(path):
    with Path(path).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_csv(path, columns, rows):
    with Path(path).open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def load_prompts(path=None, active_only=True):
    rows = read_csv(path or PROMPTS)
    return [r for r in rows if r.get("status", "active") == "active"] if active_only else rows


def load_brands(path=None):
    """brands.csv as dicts with a compiled word-boundary pattern over the aliases."""
    brands = []
    for r in read_csv(path or BRANDS):
        aliases = split(r.get("aliases")) or [r["brand"]]
        pattern = r"(?<![\w.-])(" + "|".join(re.escape(a) for a in aliases) + r")(?![\w-])"
        brands.append({"brand": r["brand"], "kind": r.get("kind", ""),
                       "domains": [d.lower() for d in split(r.get("domains"))],
                       "re": re.compile(pattern, re.I)})
    return brands


def self_brand(brands):
    return next((b for b in brands if b["kind"] == "self"), None)


def domain(url):
    host = (urlparse(url).hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def on_domains(url, domains):
    d = domain(url)
    return any(d == x or d.endswith("." + x) for x in domains)


def prose(text):
    """The answer with links, bare URLs and domain-shaped citation labels removed."""
    return LABEL_RE.sub(" ", URL_RE.sub("] ", text or ""))


def answered(text, sources):
    body = prose(text).strip()
    return bool(body) and (len(body) >= MIN_ANSWER_CHARS or bool(sources))


def category_re(category):
    """The team's one category name as a pattern (plural tolerated), or None."""
    category = (category or "").strip()
    return re.compile(r"\b" + re.escape(category) + r"s?\b", re.I) if category else None


def detect(text, sources, brands, category=None):
    """Who an answer names, in what order, and what it cites.

    `position` is our rank among the tracked brands by first occurrence in the prose (1 = named
    first), "" when we are not named.
    """
    body = prose(text)
    firsts = sorted((m.start(), b["brand"]) for b in brands for m in [b["re"].search(body)] if m)
    named = [name for _, name in firsts]
    me = self_brand(brands)
    me_name = me["brand"] if me else None
    cited_domains = []
    for u in sources:
        d = domain(u)
        if d and d not in cited_domains:
            cited_domains.append(d)
    self_paths = sorted({urlparse(u).path.rstrip("/") or "/" for u in sources
                         if me and on_domains(u, me["domains"])})
    pattern = category_re(category)
    return {"mentioned": me_name in named,
            "position": named.index(me_name) + 1 if me_name in named else "",
            "brands": named, "cited_self": bool(self_paths), "cited_paths": self_paths,
            "cited_domains": cited_domains,
            "category_phrase": bool(pattern and pattern.search(body))}


def flag(value):
    return "true" if value else "false"


def truthy(value):
    return str(value).strip().lower() in ("true", "1", "yes")


def to_row(d):
    """A detect() result as snapshot cells."""
    return {"mentioned": flag(d["mentioned"]), "position": d["position"],
            "cited_self": flag(d["cited_self"]), "cited_paths": "|".join(d["cited_paths"]),
            "cited_domains": "|".join(d["cited_domains"]), "brands": "|".join(d["brands"]),
            "category_phrase": flag(d["category_phrase"])}


def results_files(folder=None):
    """Every results snapshot, oldest first: the DataForSEO collector's and any manual drop."""
    return sorted(Path(folder or SNAPSHOTS).glob("????-??-??-*-aeo-results.csv"))


def answers_file(results_path):
    path = Path(results_path)
    return path.with_name(path.name.replace("-aeo-results.csv", "-aeo-answers.csv"))
