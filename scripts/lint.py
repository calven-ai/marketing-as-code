#!/usr/bin/env python3
"""Deterministic checks for everything docs/schema.json says is valid:
frontmatter, naming, file placement, CSV headers, links, secrets, the
generated README tables. --fix applies the safe fixes; --strict, --format
github, --json, --file and --classify serve CI, hooks and skills.

Run from the repo root:
    python3 scripts/lint.py                 # findings, exit 1 on any error
    python3 scripts/lint.py --fix           # apply the safe fixes, then re-check
    python3 scripts/lint.py --strict        # warnings fail too (CI on main)
    python3 scripts/lint.py --format github # ::error/::warning annotations
    python3 scripts/lint.py --json          # findings as JSON, for skills
    python3 scripts/lint.py --file PATH     # file-level checks for one file (hooks)
    python3 scripts/lint.py --classify BASE # bookkeeping | needs-review, then the paths

Three levels. error: blocks a proposal (broken frontmatter, a misplaced
file, a committed key). warning: annotated, never blocks unless --strict
(stale context, a naming slip). info: doctor prose only (unfilled
templates). Every check is one function in CHECKS, named after what it
checks, so a missing check is one function away. Anything a person has to
judge (voice, contradictions, cascades) is not here; that is the audit
skill's job. Standard library only.
"""

import argparse
import csv
import fnmatch
import io
import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import frontmatter  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "docs" / "schema.json"

ERROR, WARNING, INFO = "error", "warning", "info"
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv"}
TEXT_EXT = {".md", ".txt", ".csv", ".json", ".yml", ".yaml", ".py", ".sh", ".html",
            ".svg", ".toml", ".env", ".example", ".gitignore", ".gitkeep", ""}


class Finding:
    __slots__ = ("level", "path", "line", "check", "message", "fix")

    def __init__(self, level, path, message, check="", line=0, fix=None):
        self.level, self.path, self.message = level, path, message
        self.check, self.line, self.fix = check, line, fix

    @property
    def fixable(self):
        return self.fix is not None

    def as_dict(self):
        return {"level": self.level, "path": self.path, "line": self.line,
                "check": self.check, "message": self.message, "fixable": self.fixable}


class Ctx:
    """What every check reads: the schema, the tracked files, cached text."""

    def __init__(self, root=ROOT, schema=None, files=None):
        self.root = Path(root)
        self.schema = schema or json.loads((self.root / "docs" / "schema.json").read_text(encoding="utf-8"))
        self.files = files if files is not None else tracked_files(self.root)
        self._text = {}

    def path(self, rel):
        return self.root / rel

    def exists(self, rel):
        return (self.root / rel).exists()

    def text(self, rel):
        if rel not in self._text:
            try:  # bytes first, so CRLF survives for the check that reports it
                self._text[rel] = (self.root / rel).read_bytes().decode("utf-8", "replace")
            except (OSError, UnicodeError):
                self._text[rel] = ""
        return self._text[rel]

    def fm(self, rel):
        return frontmatter(self.text(rel))

    def glob(self, pattern):
        return [f for f in self.files if match_glob(f, pattern)]

    def forget(self, rel):
        self._text.pop(rel, None)


def tracked_files(root):
    """Paths git tracks (plus staged), else everything under root."""
    try:
        out = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "--cached", "--others",
                              "--exclude-standard"], capture_output=True, check=True).stdout
        files = {f for f in out.decode("utf-8", "replace").split("\0") if f}  # a set: a conflicted file lists thrice
        return sorted(f for f in files if (root / f).is_file() or (root / f).is_symlink())
    except (subprocess.CalledProcessError, FileNotFoundError):
        files = []
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for name in filenames:
                files.append(str(Path(dirpath, name).relative_to(root).as_posix()))
        return sorted(files)


def match_glob(path, pattern):
    """fnmatch where * stops at / and ** crosses folders."""
    regex = "".join(
        ".*" if tok == "**" else "[^/]*" if tok == "*" else re.escape(tok)
        for tok in re.split(r"(\*\*|\*)", pattern) if tok)
    regex = regex.replace(".*/", "(?:.*/)?")
    return re.fullmatch(regex, path) is not None


def is_iso_date(value):
    try:
        date.fromisoformat(value)
        return True
    except (TypeError, ValueError):
        return False


def line_of(text, needle):
    for i, line in enumerate(text.splitlines(), 1):
        if needle in line:
            return i
    return 0


# ---------------------------------------------------------------- checks --

def check_frontmatter_syntax(ctx):
    """Every Markdown frontmatter block closes; no CRLF or BOM."""
    out = []
    for rel in ctx.files:
        if not rel.endswith(".md"):
            continue
        raw = ctx.text(rel)
        if raw.startswith("﻿"):
            out.append(Finding(WARNING, rel, "file starts with a BOM", "frontmatter-syntax",
                               fix=lambda r=rel: _rewrite(ctx, r, lambda t: t.lstrip("﻿"))))
        if "\r\n" in raw:
            out.append(Finding(WARNING, rel, "Windows line endings (CRLF); the repo is LF",
                               "frontmatter-syntax",
                               fix=lambda r=rel: _rewrite(ctx, r, lambda t: t.replace("\r\n", "\n"))))
        if ctx.fm(rel) is None:
            out.append(Finding(ERROR, rel, "frontmatter opens with --- but never closes",
                               "frontmatter-syntax", line=1))
    return out


def _rewrite(ctx, rel, transform):
    path = ctx.path(rel)
    text = transform(path.read_bytes().decode("utf-8", "replace"))
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    ctx.forget(rel)


def check_frontmatter_schema(ctx):
    """Required keys, enums, ISO dates and known keys per docs/schema.json."""
    out = []
    for pattern, rule in ctx.schema["frontmatter"].items():
        if pattern.startswith("_"):
            continue
        for rel in ctx.glob(pattern):
            if rel in rule.get("except", []):
                continue
            fm = ctx.fm(rel)
            if fm is None:
                continue  # frontmatter-syntax reports it
            if not fm:
                out.append(Finding(ERROR, rel, "missing frontmatter block", "frontmatter", line=1))
                continue
            known = set(rule["required"]) | set(rule.get("optional", []))
            for key in rule["required"]:
                if key not in fm:
                    default = rule.get("defaults", {}).get(key)
                    fix = None
                    if default is not None:
                        fix = (lambda r=rel, k=key, d=default: _add_frontmatter_key(ctx, r, k, d))
                    out.append(Finding(ERROR, rel, f"frontmatter is missing `{key}`", "frontmatter",
                                       line=1, fix=fix))
            for key in fm:
                if key not in known and not any(fnmatch.fnmatch(key, k) for k in known if "*" in k):
                    out.append(Finding(WARNING, rel, f"unknown frontmatter key `{key}` (typo?)",
                                       "frontmatter", line=line_of(ctx.text(rel), f"{key}:")))
            for key, allowed in rule.get("enums", {}).items():
                value = fm.get(key)
                if value not in (None, "") and value not in allowed:
                    out.append(Finding(ERROR, rel,
                                       f"`{key}: {value}` is not one of {', '.join(allowed)}",
                                       "frontmatter", line=line_of(ctx.text(rel), f"{key}:")))
            for key in rule.get("dates", []):
                value = fm.get(key)
                if value not in (None, "") and not is_iso_date(str(value)):
                    out.append(Finding(ERROR, rel, f"`{key}: {value}` is not a YYYY-MM-DD date",
                                       "frontmatter", line=line_of(ctx.text(rel), f"{key}:")))
    return out


def _add_frontmatter_key(ctx, rel, key, default):
    def transform(text):
        head, sep, rest = text.partition("\n---")
        return f"{head}\n{key}: {json.dumps(default) if default else ''}".rstrip() + sep + rest
    _rewrite(ctx, rel, transform)


def check_content(ctx):
    """Content pieces: folder name, brief present, status-dependent fields, project link."""
    out = []
    naming = re.compile(ctx.schema["naming"]["content_folder"])
    placeholder = re.compile(r"\[[A-Z][^\]\n:]{0,80}\](?![\(\[:])")
    template_marks = ctx.schema.get("content", {}).get("template_placeholders", [])
    folders = sorted({f.split("/")[1] for f in ctx.files
                      if f.startswith("content/") and f.count("/") >= 2 and not f.startswith("content/_")})
    for folder in folders:
        base = f"content/{folder}"
        if not naming.match(folder):
            out.append(Finding(WARNING, base, "content folder should be named YYYY-MM-<kebab-title> "
                               "(content/README.md)", "content-naming"))
        if f"{base}/brief.md" not in ctx.files:
            out.append(Finding(WARNING, base, "no brief.md; every piece starts from a brief",
                               "content-brief"))
        draft = f"{base}/draft.md"
        if draft not in ctx.files:
            continue
        fm = ctx.fm(draft) or {}
        status = fm.get("status", "")
        text = ctx.text(draft)
        if status in ("published", "evergreen"):
            if not is_iso_date(str(fm.get("published", ""))):
                out.append(Finding(ERROR, draft, f"status is {status} but `published:` has no date",
                                   "content-published", line=line_of(text, "published:")))
            if not fm.get("published_url"):
                out.append(Finding(WARNING, draft, "published but `published_url` is empty",
                                   "content-published", line=line_of(text, "published_url:")))
        if status not in ("", "idea", "brief"):
            if "Template: unfilled" in text:
                out.append(Finding(ERROR, draft, "still carries the 'Template: unfilled' marker",
                                   "content-placeholder", line=line_of(text, "Template: unfilled")))
            body = text.split("\n---", 2)[-1]
            left = next((m for m in template_marks if m in body), None)
            if left:
                out.append(Finding(ERROR, draft, f"the template's placeholder is still in a {status} piece: {left}",
                                   "content-placeholder", line=line_of(text, left)))
            else:
                hit = placeholder.search(body)
                if hit:
                    out.append(Finding(WARNING, draft, f"looks like a placeholder in a {status} piece: "
                                       f"{hit.group(0)}; if it is prose, ignore this",
                                       "content-placeholder", line=line_of(text, hit.group(0))))
        project = str(fm.get("project", "") or "")
        if project:
            if project.startswith("projects/_archive/"):
                out.append(Finding(WARNING, draft, f"project `{project}` is archived", "content-project",
                                   line=line_of(text, "project:")))
            elif not (ctx.path(project) / "brief.md").is_file() and not (ctx.path(project) / "campaign.md").is_file():
                out.append(Finding(ERROR, draft, f"`project: {project}` is not a project folder with a brief",
                                   "content-project", line=line_of(text, "project:")))
    return out


def check_content_readme_enums(ctx):
    """content/README.md states the same status and channel values as the schema."""
    out = []
    rel = "content/README.md"
    if rel not in ctx.files:
        return out
    text = ctx.text(rel)
    enums = ctx.schema["frontmatter"]["content/*/draft.md"]["enums"]
    for key, values in enums.items():
        expected = f"{key}: " + " | ".join(values)
        if expected not in text:
            out.append(Finding(WARNING, rel, f"README lists different `{key}` values than docs/schema.json "
                               f"(expected `{expected}`)", "schema-prose", line=line_of(text, f"{key}:")))
    return out


def check_projects_readme_enums(ctx):
    """projects/README.md states the same State values as the schema."""
    rel = "projects/README.md"
    if rel not in ctx.files:
        return []
    text = ctx.text(rel)
    expected = "State: " + " | ".join(ctx.schema["project_status"]["states"])
    if expected not in text:
        return [Finding(WARNING, rel, f"README lists different `State` values than docs/schema.json "
                        f"(expected `{expected}`)", "schema-prose", line=line_of(text, "State:"))]
    return []


def check_context_freshness(ctx):
    """Context files reviewed within stale_after_days; served files are fine."""
    out = []
    today = date.today()
    limit = ctx.schema["stale_after_days"]
    for rel in ctx.schema["context_files"]:
        if rel not in ctx.files:
            continue
        text = ctx.text(rel)
        marker = ctx.schema["templates"].get(rel)
        if marker and marker in text:
            continue
        fm = ctx.fm(rel) or {}
        if fm.get("source") == "context-layer":
            continue
        raw = str(fm.get("last_reviewed", "") or "")
        if not is_iso_date(raw):
            out.append(Finding(WARNING, rel, "filled but has no `last_reviewed` date; review it with the "
                               "team and set the date, or connect a context layer (integrations/context-layer.md)",
                               "context-stale", line=line_of(text, "last_reviewed:")))
            continue
        age = (today - date.fromisoformat(raw)).days
        if age > limit:
            out.append(Finding(WARNING, rel, f"not reviewed in {age} days (limit {limit}); review it or "
                               "connect a context layer", "context-stale", line=line_of(text, "last_reviewed:")))
    return out


def check_projects(ctx):
    """Project folders: a brief, a well-formed status.md, no content or data inside."""
    out = []
    states = ctx.schema["project_status"]["states"]
    forbidden = ctx.schema["project_status"]["forbidden_files"]
    heading = re.compile(ctx.schema["naming"]["status_heading"])
    dirs = sorted({str(Path(f).parent.as_posix()) for f in ctx.files
                   if f.startswith("projects/") and not f.startswith(("projects/_", "projects/README"))})
    for d in dirs:
        parent = str(Path(d).parent.as_posix())
        has_brief = ctx.exists(f"{d}/brief.md") or ctx.exists(f"{d}/campaign.md")
        if not has_brief and parent == "projects":
            out.append(Finding(ERROR, d, "project folder without brief.md or campaign.md (projects/README.md)",
                               "project-brief"))
        for rel in ctx.files:
            if str(Path(rel).parent.as_posix()) == d:
                name = Path(rel).name
                if any(fnmatch.fnmatch(name, pat) for pat in forbidden):
                    out.append(Finding(ERROR, rel, "content and data do not live in project folders; "
                                       "move it to content/ or data/ and link it from the brief (git mv)",
                                       "project-contents"))
        status = f"{d}/status.md"
        if status in ctx.files:
            text = ctx.text(status)
            dates = []
            for i, line in enumerate(text.splitlines(), 1):
                m = heading.match(line)
                if m:
                    dates.append((m.group(1), i))
                sm = re.match(r"- \*\*State:\*\* (.+)$", line.strip())
                if sm and sm.group(1).strip().strip("[]").lower() not in states and not sm.group(1).startswith("["):
                    out.append(Finding(ERROR, status, f"State `{sm.group(1).strip()}` is not one of "
                                       f"{', '.join(states)}", "project-status", line=i))
            if dates != sorted(dates, key=lambda x: x[0], reverse=True):
                out.append(Finding(WARNING, status, "status entries are not newest-first", "project-status",
                                   line=dates[0][1] if dates else 0,
                                   fix=lambda r=status: _reorder_dated_sections(ctx, r, heading)))
    return out


def _reorder_dated_sections(ctx, rel, heading):
    """Sort `## YYYY-MM-DD...` sections newest first; everything before the first one stays."""
    def transform(text):
        lines = text.splitlines(keepends=True)
        first = next((i for i, l in enumerate(lines) if heading.match(l.rstrip("\n"))), None)
        if first is None:
            return text
        head, rest = lines[:first], lines[first:]
        sections, current = [], []
        for line in rest:
            if heading.match(line.rstrip("\n")) and current:
                sections.append(current)
                current = []
            current.append(line)
        if current:
            sections.append(current)
        sections.sort(key=lambda s: heading.match(s[0].rstrip("\n")).group(1), reverse=True)
        body = "".join("".join(s).rstrip("\n") + "\n\n" for s in sections)
        return "".join(head) + body.rstrip("\n") + "\n"
    _rewrite(ctx, rel, transform)


def check_decision_log(ctx):
    """Entries follow the format at the top of the file, newest first."""
    out = []
    rel = "memory/decision-log.md"
    if rel not in ctx.files:
        return out
    text = ctx.text(rel)
    heading = re.compile(ctx.schema["naming"]["decision_heading"])
    bullets = ctx.schema["decision_log"]["bullets"]
    lines = text.splitlines()
    try:
        start = lines.index("---") + 1
    except ValueError:
        return [Finding(ERROR, rel, "no `---` separator; entries go below it", "decision-log")]
    entries, i = [], start
    while i < len(lines):
        line = lines[i]
        if line.startswith("## "):
            m = heading.match(line)
            if not m:
                out.append(Finding(ERROR, rel, "entry heading must be `## YYYY-MM-DD: sentence`",
                                   "decision-log", line=i + 1))
            else:
                entries.append((m.group(1), i + 1))
            block, j = [], i + 1
            while j < len(lines) and not lines[j].startswith("## "):
                block.append(lines[j])
                j += 1
            labels = [re.match(r"- \*\*([^:*]+):\*\*", b).group(1) for b in block
                      if re.match(r"- \*\*([^:*]+):\*\*", b)]
            if labels != bullets:
                out.append(Finding(ERROR, rel, "entry bullets must be exactly, in order: "
                                   + ", ".join(bullets), "decision-log", line=i + 1))
            i = j
        else:
            if line.strip() and not line.startswith("<!--"):
                out.append(Finding(WARNING, rel, "text outside an entry below the separator",
                                   "decision-log", line=i + 1))
            i += 1
    if entries != sorted(entries, key=lambda e: e[0], reverse=True):
        out.append(Finding(WARNING, rel, "entries are not newest-first", "decision-log",
                           line=entries[0][1],
                           fix=lambda: _reorder_dated_sections(ctx, rel, re.compile(r"^## (\d{4}-\d{2}-\d{2}):"))))
    return out


def check_transcripts(ctx):
    """Transcript files follow the inbox contract (memory/transcripts/README.md)."""
    out = []
    naming = re.compile(ctx.schema["naming"]["transcript"])
    for rel in ctx.files:
        if not rel.startswith(("memory/transcripts/inbox/", "memory/transcripts/processed/")):
            continue
        name = Path(rel).name
        if name in (".gitkeep", "README.md"):
            continue
        m = naming.match(name)
        fm = ctx.fm(rel) if rel.endswith(".md") else {}
        fm = fm or {}
        if not m:
            fix = None
            if is_iso_date(str(fm.get("date", ""))) and fm.get("title"):
                new = f"{fm['date']}-{slug(str(fm['title']))}{Path(rel).suffix}"
                fix = lambda r=rel, n=new: _rename(ctx, r, n)
            out.append(Finding(WARNING, rel, "transcript should be named YYYY-MM-DD-<slug>.md",
                               "transcript-naming", fix=fix))
        elif fm.get("date") and str(fm["date"]) != m.group(1):
            out.append(Finding(WARNING, rel, f"filename date {m.group(1)} differs from `date: {fm['date']}`",
                               "transcript-naming"))
        source = str(fm.get("source", "") or "")
        if rel.endswith(".md") and source and source != "manual" and f"{source}_id" not in fm:
            out.append(Finding(ERROR, rel, f"a `{source}` transcript needs `{source}_id` so re-runs can dedupe",
                               "transcript-contract", line=line_of(ctx.text(rel), "source:")))
    return out


def slug(text):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", text.lower())).strip("-")[:60]


def _rename(ctx, rel, new_name):
    src = ctx.path(rel)
    dst = src.with_name(new_name)
    if dst.exists():
        return
    try:
        subprocess.run(["git", "-C", str(ctx.root), "mv", rel, str(dst.relative_to(ctx.root))],
                       check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        src.rename(dst)
    ctx.files = sorted(f for f in ctx.files if f != rel) + [str(dst.relative_to(ctx.root).as_posix())]


def check_snapshots(ctx):
    """Snapshots are dated CSVs; the same <source>-<what> keeps its columns."""
    out = []
    naming = re.compile(ctx.schema["naming"]["snapshot"])
    headers = {}
    for rel in ctx.files:
        if not match_glob(rel, "data/*/snapshots/*") or rel.endswith(".gitkeep"):
            continue
        name = Path(rel).name
        m = naming.match(name)
        if not m:
            out.append(Finding(ERROR, rel, "snapshot must be named YYYY-MM-DD-<source>-<what>.csv (data/README.md)",
                               "snapshot-naming"))
            continue
        key = (Path(rel).parent.as_posix(), m.group(2), m.group(3))
        header = _csv_header(ctx.text(rel))
        if header is not None:
            headers.setdefault(key, []).append((rel, header))
    for key, items in headers.items():
        first = items[0][1]
        for rel, header in items[1:]:
            if header != first:
                out.append(Finding(WARNING, rel, f"columns differ from {items[0][0]}; keep columns stable per "
                                   "<source>-<what> so snapshots diff (data/README.md)", "snapshot-columns"))
    return out


def _csv_header(text):
    try:
        return next(csv.reader(io.StringIO(text)))
    except (StopIteration, csv.Error):
        return None


def check_csv(ctx):
    """Canonical tables keep their exact header; every CSV parses with uniform columns."""
    out = []
    canonical = ctx.schema["csv"]["canonical"]
    for rel in ctx.files:
        if not rel.endswith(".csv") or rel.startswith("playgrounds/"):
            continue
        text = ctx.text(rel)
        rows = list(csv.reader(io.StringIO(text)))
        if not rows:
            out.append(Finding(ERROR, rel, "empty CSV; a table needs a header row", "csv"))
            continue
        if rel in canonical and rows[0] != canonical[rel]:
            out.append(Finding(ERROR, rel, "header must be exactly: " + ",".join(canonical[rel]), "csv", line=1))
        width = len(rows[0])
        for i, row in enumerate(rows[1:], 2):
            if row and len(row) != width:
                out.append(Finding(ERROR, rel, f"row has {len(row)} columns, header has {width}", "csv", line=i))
                break
    return out


def check_reports(ctx):
    """Reports are dated, list the data they used, and that data exists."""
    out = []
    n = ctx.schema["naming"]
    for rel in ctx.files:
        if not rel.startswith("reports/") or rel.startswith("reports/_templates/") or rel.endswith(".gitkeep"):
            continue
        parts = rel.split("/")
        if len(parts) < 3 or parts[-1] == "README.md":
            continue
        kind, name = parts[1], parts[-1]
        if kind == "recurring" and len(parts) == 4 and not re.match(n["report_recurring"], name):
            out.append(Finding(WARNING, rel, "recurring reports are named YYYY-MM-DD.md (reports/README.md)",
                               "report-naming"))
        elif kind == "adhoc" and not re.match(n["report_adhoc"], parts[2]):
            out.append(Finding(WARNING, rel, "ad hoc reports live in adhoc/YYYY-MM-DD-<question>/", "report-naming"))
        elif kind == "qmr" and not re.match(n["report_qmr"], parts[2]):
            out.append(Finding(WARNING, rel, "QMRs live in qmr/<year>-q<n>/", "report-naming"))
        if rel.endswith(".md"):
            text = ctx.text(rel)
            qmr_states = ctx.schema.get("reports", {}).get("qmr_states", [])
            sm = re.search(r"^- \*\*Status:\*\* (.+)$", text, re.M) if kind == "qmr" and name == "report.md" else None
            if sm and qmr_states:
                value = sm.group(1).strip()
                if not value.startswith("[") and value.strip("[]").lower() not in qmr_states:
                    out.append(Finding(ERROR, rel, f"Status `{value}` is not one of {', '.join(qmr_states)} "
                                       "(reports/README.md)", "report-status", line=line_of(text, sm.group(0))))
            if "## Data used" not in text:
                out.append(Finding(WARNING, rel, "no `## Data used` section; a report must trace back to its "
                                   "snapshots (reports/README.md)", "report-data"))
            else:
                section = text.split("## Data used", 1)[1].split("\n## ", 1)[0]
                for path in re.findall(r"`(data/[^`\s]+)`", section):
                    if not ctx.exists(path):
                        out.append(Finding(WARNING, rel, f"Data used lists `{path}`, which does not exist",
                                           "report-data", line=line_of(text, path)))
        elif rel.endswith(".html"):
            text = ctx.text(rel)
            sentinels = ctx.schema.get("reports", {}).get("dashboard_sentinels", [])
            left = next((s for s in sentinels if s in text), None)
            if left:
                out.append(Finding(ERROR, rel, "dashboard still holds the template's example numbers; replace the "
                                   "DATA block, set the title, and remove data-example from the <html> tag",
                                   "report-example", line=line_of(text, left)))
    return out


def check_binaries(ctx):
    """Plain text first: binaries only in brand/ (playgrounds/ tolerated)."""
    out = []
    b = ctx.schema["binaries"]
    exts = set(b["extensions"])
    for rel in ctx.files:
        if any(rel.startswith(d) for d in b["allowed_dirs"]):
            continue
        ext = Path(rel).suffix.lstrip(".").lower()
        binary = ext in exts
        if not binary and ext not in {"md", "csv", "json", "yml", "yaml", "py", "sh", "html", "svg", "txt", "toml"}:
            try:
                binary = b"\0" in ctx.path(rel).read_bytes()[:8000]
            except OSError:
                binary = False
        if binary:
            level = WARNING if any(rel.startswith(d) for d in b["tolerated_dirs"]) else ERROR
            out.append(Finding(level, rel, "binary file outside brand/; keep this repo plain text "
                               "(AGENTS.md rule 4)", "binary"))
        try:
            size = ctx.path(rel).stat().st_size
        except OSError:
            continue
        if size > b["max_file_kb"] * 1024:
            out.append(Finding(WARNING, rel, f"{size // 1024} KB; large files slow every clone", "file-size"))
    return out


def check_filenames(ctx):
    """No spaces or non-ASCII in file names; they break links and scripts."""
    out = []
    for rel in ctx.files:
        name = Path(rel).name
        if " " in name or not name.isascii():
            new = re.sub(r"\s+", "-", name.encode("ascii", "ignore").decode())
            referenced = any(name in ctx.text(f) for f in ctx.files if f != rel and f.endswith((".md", ".html", ".json")))
            fix = None if referenced or not new else (lambda r=rel, n=new: _rename(ctx, r, n))
            out.append(Finding(WARNING, rel, "file name has spaces or non-ASCII characters"
                               + ("; referenced elsewhere, rename by hand" if referenced else ""),
                               "filename", fix=fix))
    return out


def check_required(ctx):
    """Required files and folders exist (folders keep a .gitkeep)."""
    out = []
    for rel in ctx.schema["required_files"]:
        if not ctx.exists(rel):
            out.append(Finding(ERROR, rel, "required file is missing", "required"))
    for rel in ctx.schema["required_dirs"]:
        if not ctx.path(rel).is_dir() or not any(ctx.path(rel).iterdir()):
            out.append(Finding(ERROR, rel, "required folder is missing or empty (needs at least a .gitkeep)",
                               "required", fix=lambda r=rel: _mkdir_keep(ctx, r)))
    return out


def _mkdir_keep(ctx, rel):
    ctx.path(rel).mkdir(parents=True, exist_ok=True)
    keep = ctx.path(rel) / ".gitkeep"
    if not keep.exists():
        keep.write_text("")
        ctx.files = sorted(ctx.files + [f"{rel}/.gitkeep"])


def check_env_files(ctx):
    """No .env file is tracked and .gitignore still excludes them."""
    out = []
    for rel in ctx.files:
        name = Path(rel).name
        if name.startswith(".env") and name != ".env.example":
            out.append(Finding(ERROR, rel, "an .env file is tracked. Remove it from git AND rotate every key "
                               "in it (docs/secrets.md)", "env-tracked"))
    gi = ctx.text(".gitignore") if ".gitignore" in ctx.files else ""
    lines = {l.strip() for l in gi.splitlines()}
    if ".env" not in lines or ".env.*" not in lines or "!.env.example" not in lines:
        out.append(Finding(ERROR, ".gitignore", "must contain `.env`, `.env.*` and `!.env.example`", "env-tracked"))
    return out


def check_secrets(ctx):
    """Nothing that looks like a credential in any tracked text file."""
    out = []
    patterns = [re.compile(p) for p in ctx.schema["secrets"]["patterns"]]
    for rel in ctx.files:
        if rel == "docs/schema.json" or Path(rel).suffix.lower() in {".png", ".jpg", ".pdf"}:
            continue
        text = ctx.text(rel)
        for i, line in enumerate(text.splitlines(), 1):
            for pat in patterns:
                m = pat.search(line)
                if m:
                    out.append(Finding(ERROR, rel, f"looks like a credential ({m.group(0)[:10]}...); remove it "
                                       "and rotate it (docs/secrets.md)", "secret", line=i))
                    break
    return out


def check_pii(ctx):
    """Personal emails in data/ and memory/ (warning; info when the repo is private)."""
    out = []
    p = ctx.schema["pii"]
    level = INFO if ctx.schema["repo"].get("private") else WARNING
    email = re.compile(p["email"])
    for rel in ctx.files:
        if not any(rel.startswith(d) for d in p["dirs"]) or Path(rel).name == "README.md":
            continue
        for i, line in enumerate(ctx.text(rel).splitlines(), 1):
            for hit in email.findall(line):
                if hit.split("@")[1].lower() not in p["allow_domains"]:
                    out.append(Finding(level, rel, "personal email address; no PII in a public copy "
                                       "(data/README.md)", "pii", line=i))
                    break
    return out


def check_mcp_configs(ctx):
    """MCP configs parse, agree on server names, hold placeholders, and every variable is registered."""
    out = []
    m = ctx.schema["mcp"]
    placeholder = re.compile(m["placeholder"])
    secret = re.compile(r"(sk-[A-Za-z0-9_-]{8,}|xox[abp]-[A-Za-z0-9-]{8,}|Bearer\s+(?!\$\{)[A-Za-z0-9._-]{12,})")
    names, variables = {}, set()
    for rel in m["files"]:
        if not ctx.exists(rel):
            out.append(Finding(ERROR, rel, "missing MCP config (integrations/README.md)", "mcp"))
            continue
        text = ctx.text(rel)
        try:
            servers = json.loads(text).get("mcpServers", {})
        except json.JSONDecodeError as err:
            out.append(Finding(ERROR, rel, f"not valid JSON: {err}", "mcp", line=getattr(err, "lineno", 0)))
            continue
        names[rel] = set(servers)
        variables |= set(placeholder.findall(text))
        for hit in secret.findall(text):
            out.append(Finding(ERROR, rel, "looks like it holds a credential value; use a ${VAR} placeholder",
                               "mcp", line=line_of(text, hit if isinstance(hit, str) else hit[0])))
    if len(names) == len(m["files"]):
        a, b = (names[r] for r in m["files"])
        if a != b:
            out.append(Finding(ERROR, m["files"][0], f"server lists differ: {sorted(a)} vs {sorted(b)} in "
                               f"{m['files'][1]}; edit both together", "mcp"))
    example = ctx.path(".env.example").read_text(encoding="utf-8") if ctx.exists(".env.example") else ""
    registry = ctx.text(m["env_registry"]) if ctx.exists(m["env_registry"]) else ""
    for var in sorted(variables):
        if not re.search(rf"^{var}=", example, re.M):
            out.append(Finding(ERROR, ".env.example", f"`{var}` is used by an MCP config but not listed here",
                               "mcp-env"))
        if f"`{var}`" not in registry:
            out.append(Finding(WARNING, m["env_registry"], f"`{var}` is used by an MCP config but not in the "
                               "registry's Env vars column", "mcp-env"))
    return out


def check_settings(ctx):
    """.claude/settings.json parses and carries every deny rule docs/secrets.md promises."""
    spec = ctx.schema.get("settings", {})
    rel = spec.get("file", ".claude/settings.json")
    if not ctx.exists(rel):
        return []
    try:
        data = json.loads(ctx.text(rel))
    except json.JSONDecodeError as err:
        return [Finding(ERROR, rel, f"not valid JSON: {err}", "settings")]
    perms = data.get("permissions", {})
    deny = perms.get("deny", [])
    required = spec.get("required_deny", ["Read(./.env)"])
    missing = [d for d in required if d not in deny]
    out = []
    if missing:
        out.append(Finding(ERROR, rel, "permissions.deny is missing " + ", ".join(f"`{d}`" for d in missing)
                           + " (docs/secrets.md)", "settings", fix=lambda: _fix_settings(ctx, rel, spec)))
    if spec.get("disable_bypass") and perms.get("disableBypassPermissionsMode") != "disable":
        out.append(Finding(ERROR, rel, "permissions.disableBypassPermissionsMode must be \"disable\" "
                           "(docs/secrets.md)", "settings", fix=lambda: _fix_settings(ctx, rel, spec)))
    return out


def _fix_settings(ctx, rel, spec):
    """Add the missing deny rules and the bypass switch; keep everything else."""
    data = json.loads(ctx.text(rel))
    perms = data.setdefault("permissions", {})
    deny = perms.setdefault("deny", [])
    for rule in spec.get("required_deny", []):
        if rule not in deny:
            deny.append(rule)
    if spec.get("disable_bypass"):
        perms["disableBypassPermissionsMode"] = "disable"
    ctx.path(rel).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    ctx.forget(rel)


def check_skills(ctx):
    """Each skill's name matches its folder and it carries description and metadata."""
    out = []
    name_re = re.compile(ctx.schema["naming"]["skill_name"])
    for rel in ctx.glob(".agents/skills/*/SKILL.md"):
        folder = rel.split("/")[2]
        fm = ctx.fm(rel) or {}
        if fm.get("name") != folder or not name_re.match(folder):
            out.append(Finding(ERROR, rel, f"`name:` must equal the folder name `{folder}` (lowercase, hyphens)",
                               "skill", line=line_of(ctx.text(rel), "name:")))
        if not fm.get("description"):
            out.append(Finding(ERROR, rel, "`description:` is empty; agents route on it", "skill", line=1))
        meta = fm.get("metadata")
        if not isinstance(meta, dict) or meta.get("kind") not in ("role", "workflow") or not meta.get("needs"):
            out.append(Finding(WARNING, rel, "add `metadata:` with `kind: role|workflow` and `needs: ...`; "
                               "the roster in agents/README.md is generated from them", "skill", line=1))
    return out


def check_paths(ctx):
    """Backticked repo paths in skills and docs point at things that exist."""
    out = []
    p = ctx.schema["paths"]
    tops = tuple(p["top_dirs"])
    future = tuple(p.get("future_words", []))
    path_re = re.compile(r"`((?:\.?[A-Za-z0-9_-]+/)+[A-Za-z0-9_./-]*|[A-Z][A-Za-z_.-]+\.md)`")
    seen = set()
    for pattern in p["check_in"]:
        for rel in ctx.glob(pattern):
            if rel in seen or rel in p.get("skip", []):
                continue
            seen.add(rel)
            text = ctx.text(rel)
            in_example = False
            for i, line in enumerate(text.splitlines(), 1):
                if line.startswith("#"):
                    in_example = "example" in line.lower()
                low = line.lower()
                if in_example or any(w in low for w in future):
                    continue
                for path in path_re.findall(line):
                    if any(ch in path for ch in "<>*{}") or re.search(r"\d{4}-\d{2}|YYYY|\.\./", path):
                        continue
                    if "/" not in path:
                        if path not in p.get("root_files", []):
                            continue
                    elif path.split("/")[0] not in tops:
                        continue
                    if ctx.exists(path.rstrip("/")):
                        continue
                    level = ERROR if path.startswith(tuple(p["error_prefixes"])) else WARNING
                    out.append(Finding(level, rel, f"`{path}` does not exist", "path", line=i))
    return out


def check_links(ctx):
    """Relative Markdown links resolve."""
    out = []
    link_re = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
    for rel in ctx.files:
        if not rel.endswith(".md"):
            continue
        text = ctx.text(rel)
        in_code = False
        for i, line in enumerate(text.splitlines(), 1):
            if line.strip().startswith("```"):
                in_code = not in_code
            if in_code:
                continue
            for target in link_re.findall(line):
                if re.match(r"[a-z]+:", target) or target.startswith("#"):
                    continue
                target = target.split("#", 1)[0]
                if not target:
                    continue
                resolved = (ctx.path(rel).parent / target).resolve()
                if not resolved.exists():
                    out.append(Finding(ERROR, rel, f"broken link: {target}", "link", line=i))
    return out


def check_generated_blocks(ctx):
    """README roster blocks match the files they index."""
    out = []
    for rel, blocks in ctx.schema["generated"].items():
        if rel.startswith("_") or rel not in ctx.files:
            continue
        text = ctx.text(rel)
        for block in blocks:
            start, end = f"<!-- generated:{block} -->", f"<!-- /generated:{block} -->"
            if start not in text or end not in text:
                out.append(Finding(ERROR, rel, f"missing generated block markers for `{block}`", "generated",
                                   fix=lambda r=rel, b=block: _write_block(ctx, r, b)))
                continue
            current = text.split(start, 1)[1].split(end, 1)[0].strip()
            if current != render_block(ctx, block).strip():
                out.append(Finding(ERROR, rel, f"generated block `{block}` is out of date; run lint --fix",
                                   "generated", line=line_of(text, start),
                                   fix=lambda r=rel, b=block: _write_block(ctx, r, b)))
    return out


def render_block(ctx, block):
    if block in ("skills-roles", "skills-workflows"):
        kind = "role" if block == "skills-roles" else "workflow"
        head = "Agent" if kind == "role" else "Skill"
        rows = [f"| {head} | What it does | Needs |", "| --- | --- | --- |"]
        for rel in ctx.glob(".agents/skills/*/SKILL.md"):
            fm = ctx.fm(rel) or {}
            meta = fm.get("metadata") if isinstance(fm.get("metadata"), dict) else {}
            if meta.get("kind", "workflow") != kind:
                continue
            name = rel.split("/")[2]
            what = re.split(r"\.\s+Use\b", str(fm.get("description", "")), maxsplit=1)[0].rstrip(".")
            rows.append(f"| [{name}](../.agents/skills/{name}/SKILL.md) | {cell(what)} | {cell(meta.get('needs', 'nothing'))} |")
        return "\n".join(rows)
    if block == "scripts":
        rows = ["| Script | What it does |", "| --- | --- |"]
        files = sorted(ctx.glob("scripts/*.py") + ctx.glob("scripts/*.sh") + ctx.glob("scripts/hooks/*"))
        for rel in files:
            name = rel[len("scripts/"):]
            rows.append(f"| [{name}]({name}) | {cell(script_summary(ctx.text(rel)))} |")
        return "\n".join(rows)
    raise ValueError(block)


def script_summary(text):
    """A script's first paragraph: the docstring for Python, the leading comment block for shell."""
    doc = re.search(r'^"""(.*?)(?:\n\n|""")', text, re.S | re.M)
    if doc:
        return " ".join(doc.group(1).split())
    lines = []
    for line in text.splitlines():
        if line.startswith("#!"):
            continue
        if line.startswith("#"):
            body = line[1:].strip()
            if not body:
                break
            lines.append(body)
        elif lines or line.strip():
            break
    return " ".join(lines)


def cell(text):
    return str(text).replace("|", "\\|")


def _write_block(ctx, rel, block):
    start, end = f"<!-- generated:{block} -->", f"<!-- /generated:{block} -->"
    body = f"{start}\n{render_block(ctx, block)}\n{end}"

    def transform(text):
        if start in text and end in text:
            head = text.split(start, 1)[0]
            tail = text.split(end, 1)[1]
            return head + body + tail
        return text.rstrip("\n") + "\n\n" + body + "\n"
    _rewrite(ctx, rel, transform)


def check_docs_index(ctx):
    """docs/README.md links every doc; the operating model names every workflow."""
    out = []
    for rel, pattern in ctx.schema["docs_index"].items():
        if rel not in ctx.files:
            continue
        text = ctx.text(rel)
        for doc in ctx.glob(pattern):
            name = Path(doc).name
            if name == "README.md" or doc == rel:
                continue
            if f"({name})" not in text and f"({doc})" not in text:
                out.append(Finding(ERROR, rel, f"does not list {name}", "docs-index",
                                   fix=lambda r=rel, d=doc: _append_doc_link(ctx, r, d)))
    om = "docs/operating-model.md"
    if om in ctx.files:
        text = ctx.text(om)
        for wf in ctx.glob(".github/workflows/*.yml"):
            if Path(wf).name not in text:
                out.append(Finding(WARNING, om, f"the who-triggers-what table does not mention {Path(wf).name}",
                                   "docs-index"))
    return out


def _append_doc_link(ctx, rel, doc):
    text = ctx.text(doc)
    title = next((l[2:].strip() for l in text.splitlines() if l.startswith("# ")), Path(doc).stem)
    _rewrite(ctx, rel, lambda t: t.rstrip("\n") + f"\n- [{Path(doc).name}]({Path(doc).name}): {title}.\n")


def check_skill_links(ctx):
    """.claude/skills/ mirrors .agents/skills/ (scripts/sync_skills.py)."""
    script = ctx.path("scripts/sync_skills.py")
    if not script.is_file():
        return []
    run = subprocess.run([sys.executable, str(script), "--check"], capture_output=True, text=True, cwd=str(ctx.root))
    if run.returncode == 0:
        return []
    return [Finding(ERROR, ".claude/skills", "skill links out of sync: " + " ".join(run.stdout.split()),
                    "skill-links", fix=lambda: subprocess.run([sys.executable, str(script)], check=False,
                                                              capture_output=True, cwd=str(ctx.root)))]


def check_adoption(ctx):
    """What an adopting team still has to make its own (docs/make-it-yours.md); informational."""
    out = []
    spec = ctx.schema.get("adoption")
    if not spec:
        return out
    where = "(docs/make-it-yours.md)"
    for m in spec.get("markers", []):
        rel = m["file"]
        if rel in ctx.files and m["text"] in ctx.text(rel):
            out.append(Finding(INFO, rel, f"make it yours: {m['what']} {where}", "adoption",
                               line=line_of(ctx.text(rel), m["text"])))
    tag = spec.get("example_rows", "example row:")
    for rel in ctx.schema["csv"]["canonical"]:
        if rel in ctx.files and tag in ctx.text(rel):
            out.append(Finding(INFO, rel, f"make it yours: replace the rows marked `{tag}` in {rel} with your own {where}",
                               "adoption", line=line_of(ctx.text(rel), tag)))
    templates = [(rel, marker) for rel, marker in ctx.schema["templates"].items() if not rel.startswith("_")]
    unfilled = sum(1 for rel, marker in templates if ctx.exists(rel) and marker in ctx.text(rel))
    examples = spec.get("examples_dir", "examples/")
    if any(f.startswith(examples) for f in ctx.files) and unfilled < len(templates):
        out.append(Finding(INFO, examples.rstrip("/"), "make it yours: the example company is still here; delete "
                           f"the folder now that your own templates are filled {where}", "adoption"))
    if not ctx.schema["repo"].get("private"):
        accounts = "data/accounts/target-accounts.csv"
        has_rows = accounts in ctx.files and any(l.strip() for l in ctx.text(accounts).splitlines()[1:])
        has_transcripts = any(f.startswith(("memory/transcripts/inbox/", "memory/transcripts/processed/"))
                              and Path(f).name not in (".gitkeep", "README.md") for f in ctx.files)
        if has_rows or has_transcripts:
            out.append(Finding(INFO, "docs/schema.json", "make it yours: repo.private is false but the repository "
                               "holds account rows or transcripts; make it private and set repo.private to true, "
                               f"or keep personal data out {where}", "adoption"))
    return out


def check_templates(ctx):
    """Which templates are still unfilled (informational; /setup fills them)."""
    out = []
    for rel, marker in ctx.schema["templates"].items():
        if rel.startswith("_"):
            continue
        if ctx.exists(rel) and marker in ctx.text(rel):
            out.append(Finding(INFO, rel, "template still unfilled; run /setup", "template"))
    return out


# scope "file": runs under --file PATH with ctx.files reduced to that file.
CHECKS = [
    (check_frontmatter_syntax, "file"),
    (check_frontmatter_schema, "file"),
    (check_content, "file"),
    (check_content_readme_enums, "file"),
    (check_projects_readme_enums, "file"),
    (check_context_freshness, "file"),
    (check_projects, "file"),
    (check_decision_log, "file"),
    (check_transcripts, "file"),
    (check_snapshots, "file"),
    (check_csv, "file"),
    (check_reports, "file"),
    (check_binaries, "file"),
    (check_filenames, "file"),
    (check_env_files, "file"),
    (check_secrets, "file"),
    (check_pii, "file"),
    (check_paths, "file"),
    (check_links, "file"),
    (check_skills, "file"),
    (check_required, "repo"),
    (check_mcp_configs, "repo"),
    (check_settings, "repo"),
    (check_generated_blocks, "repo"),
    (check_docs_index, "repo"),
    (check_skill_links, "repo"),
    (check_templates, "repo"),
    (check_adoption, "repo"),
]


def run_checks(ctx, scope=None):
    findings = []
    for check, check_scope in CHECKS:
        if scope and check_scope != scope:
            continue
        findings.extend(check(ctx))
    order = {ERROR: 0, WARNING: 1, INFO: 2}
    findings.sort(key=lambda f: (order[f.level], f.path, f.line))
    return findings


def apply_fixes(ctx, findings):
    fixed = []
    for f in findings:
        if f.fix is not None:
            try:
                f.fix()
                fixed.append(f)
            except Exception as err:  # a fix that fails is reported, never hidden
                f.message += f" (auto-fix failed: {err})"
    ctx.files = tracked_files(ctx.root)
    ctx._text.clear()
    return fixed


# Paths that are never bookkeeping, whatever docs/schema.json says: they are
# the machinery that decides what bookkeeping is. Hard-coded on purpose, so a
# proposal that edits the schema cannot widen the list for itself. The gate
# (gate.yml) runs this file from main, never from the proposal.
NEVER_BOOKKEEPING = (
    ".github/**", "scripts/**", "docs/schema.json", ".claude/**", ".mcp.json", ".cursor/**",
    ".agents/**", "integrations/**", "AGENTS.md", "CLAUDE.md", ".gitignore",
)


def classify_paths(schema, paths):
    """bookkeeping if every path matches a bookkeeping glob and none is machinery, else needs-review."""
    if not paths:
        return "needs-review"
    never = tuple(schema.get("bookkeeping", {}).get("never", ())) + NEVER_BOOKKEEPING
    if any(match_glob(p, n) for p in paths for n in never):
        return "needs-review"
    globs = schema["bookkeeping"]["globs"]
    return "bookkeeping" if all(any(match_glob(p, g) for g in globs) for p in paths) else "needs-review"


def classify(ctx, base, head="HEAD"):
    """The kind of the proposal BASE...HEAD, and its changed paths."""
    for spec in (f"{base}...{head}", f"{base}..{head}", base):
        run = subprocess.run(["git", "-C", str(ctx.root), "diff", "--name-only", spec],
                             capture_output=True, text=True)
        if run.returncode == 0:
            break
    paths = [p for p in run.stdout.split("\n") if p]
    return classify_paths(ctx.schema, paths), paths


# ------------------------------------------------------------------ cli --

def format_text(findings):
    lines = []
    for f in findings:
        loc = f"{f.path}:{f.line}" if f.line else f.path
        tag = {ERROR: "✗", WARNING: "!", INFO: "i"}[f.level]
        fix = "  [fixable: run lint.py --fix]" if f.fixable else ""
        lines.append(f"{tag} {loc}: {f.message}{fix}")
    return "\n".join(lines)


def format_github(findings):
    lines = []
    for f in findings:
        kind = {ERROR: "error", WARNING: "warning", INFO: "notice"}[f.level]
        where = f"file={f.path}" + (f",line={f.line}" if f.line else "")
        msg = f.message.replace("%", "%25").replace("\n", "%0A")
        lines.append(f"::{kind} {where},title={f.check}::{msg}")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--fix", action="store_true", help="apply safe fixes, then re-check")
    ap.add_argument("--strict", action="store_true", help="warnings fail too")
    ap.add_argument("--format", choices=["text", "github"], default="text")
    ap.add_argument("--json", action="store_true", help="print findings as JSON")
    ap.add_argument("--file", help="check one file only (file-level checks)")
    ap.add_argument("--classify", metavar="BASE", help="bookkeeping or needs-review vs BASE")
    ap.add_argument("--head", default="HEAD", help="with --classify: the proposal's commit (default HEAD)")
    ap.add_argument("--root", help="check this checkout instead of the one this script lives in "
                                   "(the schema and the checks still come from here; gate.yml uses it)")
    ap.add_argument("--quiet", action="store_true", help="no output, exit code only")
    args = ap.parse_args(argv)

    if args.root:
        ctx = Ctx(root=Path(args.root).resolve(), schema=json.loads(SCHEMA_PATH.read_text(encoding="utf-8")))
    else:
        ctx = Ctx()
    if args.classify:
        kind, paths = classify(ctx, args.classify, args.head)
        print(kind)
        for p in paths:
            print(p)
        return 0

    scope = None
    if args.file:
        rel = str(Path(args.file).resolve().relative_to(ctx.root).as_posix()) if Path(args.file).is_absolute() else args.file
        if rel not in ctx.files:
            ctx.files = sorted(ctx.files + [rel])
        ctx.files = [rel]
        scope = "file"

    findings = run_checks(ctx, scope)
    fixed = []
    if args.fix:
        fixed = apply_fixes(ctx, findings)
        findings = run_checks(ctx, scope)

    if args.json:
        print(json.dumps({"fixed": [f.as_dict() for f in fixed],
                          "findings": [f.as_dict() for f in findings]}, indent=2))
    elif not args.quiet:
        if fixed:
            print(f"fixed {len(fixed)}:")
            for f in fixed:
                print(f"  {f.path}: {f.message}")
            print()
        visible = [f for f in findings if f.level != INFO]
        if visible:
            print(format_github(visible) if args.format == "github" else format_text(visible))
        else:
            print("ok: no findings")

    errors = [f for f in findings if f.level == ERROR]
    warnings = [f for f in findings if f.level == WARNING]
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
