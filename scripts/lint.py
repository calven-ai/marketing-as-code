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


def context_files(ctx):
    """The files the freshness rule applies to: schema entries, globs expanded, READMEs and _templates skipped."""
    out = []
    for entry in ctx.schema["context_files"]:
        if "*" in entry:
            out += [f for f in ctx.glob(entry) if Path(f).name != "README.md" and not Path(f).name.startswith("_")]
        elif entry in ctx.files:
            out.append(entry)
    return out


def check_context_freshness(ctx):
    """Context files reviewed within stale_after_days; served files are fine."""
    out = []
    today = date.today()
    limit = ctx.schema["stale_after_days"]
    for rel in context_files(ctx):
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
        if rel.endswith(".md") and name != "data-checklist.md":
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
        if name != ".env.example" and (name == ".env" or name.startswith(".env.") or name.endswith(".env")):
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
    """MCP configs parse, agree on server names, hold placeholders, pin packages, and every variable is registered."""
    out = []
    m = ctx.schema["mcp"]
    placeholder = re.compile(m["placeholder"])
    secret = re.compile(r"(sk-[A-Za-z0-9_-]{8,}|xox[abp]-[A-Za-z0-9-]{8,}|Bearer\s+(?!\$\{)[A-Za-z0-9._-]{12,})")
    pinned = set(ctx.schema.get("catalog", {}).get("pinned_commands", []))
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
        cursor = rel.startswith(".cursor/")
        for name, entry in servers.items():
            if not isinstance(entry, dict):
                continue
            where = line_of(text, f'"{name}"')
            cmd = entry.get("command")
            if cmd in pinned and not _pinned(entry.get("args", [])):
                out.append(Finding(ERROR, rel, f"`{name}` runs `{cmd}` without a pinned version: `{cmd} -y name@1.2.3`, "
                                   "never `name` alone (integrations/adding-an-integration.md)", "mcp", line=where))
            if cursor and "type" in entry:
                out.append(Finding(WARNING, rel, f"`{name}`: Cursor entries carry no `type` key", "mcp", line=where))
            if not cursor and entry.get("url") and entry.get("type") not in ("http", "sse", "ws"):
                out.append(Finding(ERROR, rel, f"`{name}` has a `url` but no `\"type\": \"http\"`; Claude Code would "
                                   "treat it as stdio and skip it", "mcp", line=where))
        if cursor:
            for hit in re.findall(r"\$\{(?!env:)[A-Z][A-Z0-9_]*\}", text):
                out.append(Finding(ERROR, rel, f"Cursor reads `${{env:VAR}}`, not `{hit}`", "mcp", line=line_of(text, hit)))
    if len(names) == len(m["files"]):
        a, b = (names[r] for r in m["files"])
        if a != b:
            out.append(Finding(ERROR, m["files"][0], f"server lists differ: {sorted(a)} vs {sorted(b)} in "
                               f"{m['files'][1]}; edit both together", "mcp"))
    example = ctx.path(".env.example").read_text(encoding="utf-8") if ctx.exists(".env.example") else ""
    registry = ctx.text(m["env_registry"]) if ctx.exists(m["env_registry"]) else ""
    secrets_doc = ctx.text("docs/secrets.md") if "docs/secrets.md" in ctx.files else None
    for var in sorted(variables):
        if not re.search(rf"^{var}=", example, re.M):
            out.append(Finding(ERROR, ".env.example", f"`{var}` is used by an MCP config but not listed here",
                               "mcp-env"))
        if f"`{var}`" not in registry:
            out.append(Finding(WARNING, m["env_registry"], f"`{var}` is used by an MCP config but not in the "
                               "registry's Env vars column", "mcp-env"))
        if secrets_doc is not None and f"`{var}`" not in secrets_doc:
            out.append(Finding(WARNING, "docs/secrets.md", f"`{var}` is used by an MCP config but has no row in "
                               "Who holds which key", "mcp-env"))
    return out


def _pinned(args):
    """True when some argument carries a version (`name@1.2.3` for npm, `name==1.2.3` for Python)."""
    return any(re.search(r"(@|==)\d", str(a)) for a in (args or []))


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
    if spec.get("disable_auto") and perms.get("disableAutoMode") != "disable":
        out.append(Finding(ERROR, rel, "permissions.disableAutoMode must be \"disable\": a classifier is not the "
                           "person the docs promise asks first (docs/secrets.md)", "settings",
                           fix=lambda: _fix_settings(ctx, rel, spec)))
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
    if spec.get("disable_auto"):
        perms["disableAutoMode"] = "disable"
    ctx.path(rel).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    ctx.forget(rel)


SKILL_GLOB = ".agents/skills/*/SKILL.md"


def skill_meta(ctx, rel):
    """A skill's metadata dict ({} when absent or malformed) and its lists of needed and optional category ids."""
    fm = ctx.fm(rel) or {}
    meta = fm.get("metadata") if isinstance(fm.get("metadata"), dict) else {}
    needs = meta.get("needs") if isinstance(meta.get("needs"), list) else []
    optional = meta.get("optional") if isinstance(meta.get("optional"), list) else []
    return meta, needs, optional


def check_skills(ctx):
    """Each skill's name matches its folder, it carries a description, and its metadata says what docs/schema.json allows."""
    out = []
    name_re = re.compile(ctx.schema["naming"]["skill_name"])
    spec = ctx.schema.get("skills", {})
    areas = [a[0] for a in spec.get("areas", [])]
    kinds = spec.get("kinds", ["role", "workflow"])
    catalog = ctx.schema.get("catalog", {})
    categories = catalog.get("categories", [])
    bridge_only = catalog.get("bridge_only", [])
    known_keys = set(spec.get("metadata_keys", []))
    for rel in ctx.glob(SKILL_GLOB):
        folder = rel.split("/")[2]
        fm = ctx.fm(rel) or {}
        text = ctx.text(rel)
        if fm.get("name") != folder or not name_re.match(folder):
            out.append(Finding(ERROR, rel, f"`name:` must equal the folder name `{folder}` (lowercase, hyphens)",
                               "skill", line=line_of(text, "name:")))
        if not fm.get("description"):
            out.append(Finding(ERROR, rel, "`description:` is empty; agents route on it", "skill", line=1))
        meta = fm.get("metadata")
        line = line_of(text, "metadata:") or 1
        if not isinstance(meta, dict):
            out.append(Finding(ERROR, rel, "add `metadata:` with `kind`, `area` and `needs`; the roster in "
                               "agents/README.md is generated from them (docs/skill-authoring.md)", "skill", line=line))
            continue

        def bad(msg, level=ERROR, rel=rel, line=line):
            out.append(Finding(level, rel, msg, "skill", line=line))

        if meta.get("kind") not in kinds:
            bad(f"`metadata.kind` must be one of {', '.join(kinds)}")
        if areas and meta.get("area") not in areas:
            bad(f"`metadata.area` must be one of {', '.join(areas)}")
        if "needs" not in meta:
            bad("`metadata.needs` is missing; write `needs: []` when the skill needs no integration")
        for key in ("needs", "optional"):
            if key not in meta:
                continue
            value = meta[key]
            if not isinstance(value, list):
                bad(f"`metadata.{key}` must be an inline list of category ids like `[crm, web-analytics]`, or `[]`")
                continue
            for cid in value:
                if categories and cid not in categories:
                    bad(f"`metadata.{key}` names `{cid}`, which is not a category in docs/schema.json")
                elif cid in bridge_only:
                    bad(f"`{cid}` is a bridge category, never a need; name the category it stands in for")
        if meta.get("kind") == "role":
            cadence = meta.get("cadence")
            if not cadence:
                bad("a role states its `cadence` (weekly, monthly, ...)", WARNING)
            elif spec.get("cadence") and cadence not in spec["cadence"]:
                bad(f"`metadata.cadence` must be one of {', '.join(spec['cadence'])}")
        for key in ("writes", "runs"):
            allowed = spec.get(key)
            if key in meta and allowed and meta[key] not in allowed:
                bad(f"`metadata.{key}` must be one of {', '.join(allowed)}")
        if meta.get("writes") == "external" and meta.get("runs") == "either":
            bad("a skill that writes to external systems never runs unattended: set `runs: person` (AGENTS.md rule 3)")
        for key in meta:
            if known_keys and key not in known_keys:
                bad(f"unknown metadata key `{key}` (typo?)", WARNING)
    return out


# ------------------------------------------------------------ catalog --

def load_catalog(ctx):
    """{category id: parsed JSON} for integrations/catalog/*.json, plus (path, error) for files that do not parse."""
    folder = ctx.schema.get("catalog", {}).get("dir", "integrations/catalog")
    entries, errors = {}, []
    for rel in ctx.glob(f"{folder}/*.json"):
        try:
            data = json.loads(ctx.text(rel))
        except json.JSONDecodeError as err:
            errors.append((rel, f"not valid JSON: {err}"))
            continue
        if not isinstance(data, dict):
            errors.append((rel, "the top level must be an object"))
            continue
        entries[Path(rel).stem] = data
    return entries, errors


def load_wired(ctx):
    """(path, parsed integrations/wired.json or None, error or None)."""
    rel = ctx.schema.get("catalog", {}).get("wired", "integrations/wired.json")
    if rel not in ctx.files:
        return rel, None, None
    try:
        data = json.loads(ctx.text(rel))
    except json.JSONDecodeError as err:
        return rel, None, f"not valid JSON: {err}"
    return rel, data if isinstance(data, dict) else {}, None


def catalog_vendor(entries, category, vendor_id):
    for v in (entries.get(category) or {}).get("vendors") or []:
        if isinstance(v, dict) and v.get("id") == vendor_id:
            return v
    return None


def mcp_variant(vendor, variant_id=None):
    """The named `routes.mcp` entry of a vendor, or its default when no id is given."""
    variants = [m for m in ((vendor or {}).get("routes") or {}).get("mcp") or [] if isinstance(m, dict)]
    if variant_id is not None:
        return next((m for m in variants if m.get("id") == variant_id), None)
    return next((m for m in variants if m.get("default")), variants[0] if variants else None)


def check_catalog(ctx):
    """integrations/catalog/*.json: valid, complete, pinned, placeholders declared, checked recently."""
    out = []
    spec = ctx.schema.get("catalog")
    if not spec:
        return out
    folder = spec.get("dir", "integrations/catalog")
    categories = spec.get("categories", [])
    verified = spec.get("verified", [])
    source_re = re.compile(spec.get("source_token", "^[a-z0-9]+$"))
    id_re = re.compile(ctx.schema["naming"]["skill_name"])
    placeholder = re.compile(ctx.schema["mcp"]["placeholder"])
    pinned = set(spec.get("pinned_commands", []))
    stale = spec.get("stale_after_days", 180)
    today = date.today()
    entries, errors = load_catalog(ctx)
    for rel, msg in errors:
        out.append(Finding(ERROR, rel, msg, "catalog"))
    for cid, data in sorted(entries.items()):
        rel = f"{folder}/{cid}.json"

        def bad(msg, level=ERROR, rel=rel):
            out.append(Finding(level, rel, msg, "catalog"))

        if data.get("id") != cid or cid not in categories:
            bad(f"`id` must equal the file name `{cid}` and be one of the categories in docs/schema.json")
        manual = data.get("manual")
        if not isinstance(manual, dict) or not manual.get("export") or not manual.get("drop"):
            bad("`manual` needs `export` and `drop`: every category keeps a by-hand route")
        for b in data.get("bridges") or []:
            if b not in categories:
                bad(f"`bridges` names an unknown category `{b}`")
        domain = data.get("data_domain")
        if domain and not ctx.path(str(domain)).is_dir():
            bad(f"`data_domain: {domain}` is not a folder", WARNING)
        vendors = data.get("vendors")
        if not isinstance(vendors, list):
            bad("`vendors` must be a list")
            continue
        if not vendors and not data.get("bridges"):
            bad("no vendors and no bridges; a category needs a route besides the manual one", WARNING)
        seen = set()
        for v in vendors:
            if not isinstance(v, dict):
                bad("a vendor entry is not an object")
                continue
            vid = str(v.get("id", ""))
            where = f"vendor `{vid or '?'}`"
            if not id_re.match(vid) or vid in seen:
                bad(f"{where}: `id` is missing, malformed or duplicated")
            seen.add(vid)
            for key in ("name", "source", "verified", "checked", "source_url", "routes"):
                if key not in v:
                    bad(f"{where}: missing `{key}`")
            if not source_re.match(str(v.get("source", ""))):
                bad(f"{where}: `source` must match {source_re.pattern} (the snapshot source token, data/README.md)")
            if v.get("verified") not in verified:
                bad(f"{where}: `verified` must be one of {', '.join(verified)}")
            checked = str(v.get("checked", ""))
            if not is_iso_date(checked):
                bad(f"{where}: `checked` must be a YYYY-MM-DD date")
            elif (today - date.fromisoformat(checked)).days > stale:
                bad(f"{where}: checked {checked}, more than {stale} days ago; re-verify against `source_url` "
                    "and update `checked`", WARNING)
            switch = v.get("read_only_switch")
            if switch is not None and (not isinstance(switch, dict) or switch.get("kind") not in
                                       ("env", "arg", "url", "header") or "name" not in switch or "value" not in switch):
                bad(f"{where}: `read_only_switch` must be null or {{kind: env|arg|url|header, name, value}}")
            routes = v.get("routes") if isinstance(v.get("routes"), dict) else {}
            mcp = routes.get("mcp")
            if not isinstance(mcp, list):
                bad(f"{where}: `routes.mcp` must be a list (empty when there is no server)")
                mcp = []
            defaults = [x for x in mcp if isinstance(x, dict) and x.get("default")]
            if mcp and len(defaults) != 1:
                bad(f"{where}: exactly one `routes.mcp` entry must carry `default: true`")
            for x in mcp:
                if not isinstance(x, dict):
                    bad(f"{where}: a `routes.mcp` entry is not an object")
                    continue
                mw = f"{where} variant `{x.get('id', '?')}`"
                if not id_re.match(str(x.get("server", ""))):
                    bad(f"{mw}: `server` is missing or malformed (lowercase, hyphens)")
                transport = x.get("transport")
                if transport == "http":
                    if not str(x.get("url", "")).startswith(("http", "${")):
                        bad(f"{mw}: http transport needs a `url` (a literal, or a `${{VAR}}` placeholder for a "
                            "per-account endpoint)")
                elif transport == "stdio":
                    if not x.get("command") or not isinstance(x.get("args"), list):
                        bad(f"{mw}: stdio transport needs `command` and `args`")
                    elif x["command"] in pinned and not _pinned(x["args"]):
                        bad(f"{mw}: `{x['command']}` package is not pinned to a version "
                            "(integrations/adding-an-integration.md)")
                else:
                    bad(f"{mw}: `transport` must be http or stdio")
                auth = x.get("auth") if isinstance(x.get("auth"), dict) else {}
                model = auth.get("model")
                if model not in ("oauth", "bearer", "header", "basic", "env", "none"):
                    bad(f"{mw}: `auth.model` must be oauth, bearer, header, basic, env or none")
                declared = set(auth.get("env") or [])
                used = set(placeholder.findall(json.dumps(x)))
                if declared != used:
                    bad(f"{mw}: `auth.env` {sorted(declared)} must list exactly the placeholders the entry uses "
                        f"{sorted(used)}")
                if "headless" not in x:
                    bad(f"{mw}: missing `headless`")
                elif model == "oauth" and x.get("headless"):
                    bad(f"{mw}: an OAuth server cannot run headless; set `headless: false`")
            script = routes.get("script")
            if isinstance(script, dict) and script.get("path") and not ctx.exists(str(script["path"])):
                bad(f"{where}: `routes.script.path` {script['path']} does not exist")
    return out


def check_wired(ctx):
    """integrations/wired.json binds categories to catalog vendors; .mcp.json and the deny rules agree with it."""
    out = []
    spec = ctx.schema.get("catalog")
    if not spec:
        return out
    rel, data, err = load_wired(ctx)
    if data is None:
        if err:
            out.append(Finding(ERROR, rel, err, "wired"))
        return out
    entries, _ = load_catalog(ctx)
    categories = spec.get("categories", [])
    wired = data.get("wired") if isinstance(data.get("wired"), dict) else {}
    custom = data.get("custom_servers") if isinstance(data.get("custom_servers"), dict) else {}
    servers = {}
    if ctx.exists(".mcp.json"):
        try:
            servers = json.loads(ctx.text(".mcp.json")).get("mcpServers", {})
        except json.JSONDecodeError:
            servers = {}
    settings_rel = ctx.schema.get("settings", {}).get("file", ".claude/settings.json")
    deny = []
    if ctx.exists(settings_rel):
        try:
            deny = json.loads(ctx.text(settings_rel)).get("permissions", {}).get("deny", [])
        except json.JSONDecodeError:
            deny = []
    bound, missing_rules = set(), []
    for cid, entry in sorted(wired.items()):
        if cid not in categories:
            out.append(Finding(ERROR, rel, f"`{cid}` is not a category in docs/schema.json", "wired"))
            continue
        if not isinstance(entry, dict):
            out.append(Finding(ERROR, rel, f"`{cid}` must be an object", "wired"))
            continue
        vid = entry.get("vendor")
        if vid is None:
            continue
        vendor = catalog_vendor(entries, cid, vid)
        if vendor is None:
            out.append(Finding(ERROR, rel, f"`{cid}` is wired to `{vid}`, which is not in "
                               f"{spec.get('dir', 'integrations/catalog')}/{cid}.json", "wired"))
            continue
        routes = entry.get("routes") or []
        if "mcp" not in routes:
            continue
        variant = mcp_variant(vendor, entry.get("variant"))
        if variant is None:
            out.append(Finding(ERROR, rel, f"`{cid}`: variant `{entry.get('variant')}` is not a `routes.mcp` entry "
                               f"of `{vid}`", "wired"))
            continue
        server = str(variant.get("server", ""))
        bound.add(server)
        if server not in servers:
            out.append(Finding(ERROR, rel, f"`{cid}` is wired to `{vid}` but `{server}` is not in .mcp.json; run "
                               f"python3 scripts/wire_integration.py {vid}", "wired"))
        writes = entry.get("writes")
        if vendor.get("writes") and writes not in ("denied", "allowed"):
            out.append(Finding(WARNING, rel, f"`{cid}`: `{vid}` has write tools; say `writes: denied` or "
                               "`writes: allowed`", "wired"))
        if writes == "denied":
            rules = [f"mcp__{server}__{t}" for t in vendor.get("write_tools") or []] or [f"mcp__{server}"]
            missing_rules += [r for r in rules if r not in deny]
    for server in sorted(servers):
        if server not in bound and server not in custom:
            out.append(Finding(WARNING, ".mcp.json", f"server `{server}` is not bound in {rel}; wire it with "
                               "scripts/wire_integration.py, or list it under custom_servers with a reason", "wired"))
    if missing_rules:
        out.append(Finding(ERROR, settings_rel, f"{rel} says writes are denied but permissions.deny lacks "
                           + ", ".join(f"`{r}`" for r in missing_rules), "wired",
                           fix=lambda: _add_deny_rules(ctx, settings_rel, missing_rules)))
    return out


def _add_deny_rules(ctx, rel, rules):
    data = json.loads(ctx.text(rel)) if ctx.exists(rel) else {}
    deny = data.setdefault("permissions", {}).setdefault("deny", [])
    for rule in rules:
        if rule not in deny:
            deny.append(rule)
    ctx.path(rel).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    ctx.forget(rel)


def check_catalog_coverage(ctx):
    """Every category is needed by some skill, and every category a skill needs has a catalog file."""
    out = []
    spec = ctx.schema.get("catalog")
    if not spec:
        return out
    folder = spec.get("dir", "integrations/catalog")
    categories = spec.get("categories", [])
    bridge_only = set(spec.get("bridge_only", []))
    entries, _ = load_catalog(ctx)
    used = set()
    for rel in ctx.glob(SKILL_GLOB):
        _, needs, optional = skill_meta(ctx, rel)
        for cid in needs + optional:
            used.add(cid)
            if cid in categories and cid not in entries:
                out.append(Finding(ERROR, rel, f"needs `{cid}` but {folder}/{cid}.json does not exist", "catalog-coverage"))
    for cid in categories:
        if cid in entries and cid not in used and cid not in bridge_only:
            out.append(Finding(WARNING, f"{folder}/{cid}.json", "no skill lists this category under needs or optional; "
                               "add the skill that uses it, or delete the file", "catalog-coverage"))
    return out


def check_role_workflows(ctx):
    """A role-<skill>.yml caller runs a repo-only skill whose every category is wired to run headless."""
    out = []
    _, data, _ = load_wired(ctx)
    wired = (data or {}).get("wired") or {}
    entries, _ = load_catalog(ctx)
    for wf in ctx.glob(".github/workflows/role-*.yml"):
        if Path(wf).name == "role-run.yml":
            continue
        text = ctx.text(wf)
        m = re.search(r"^\s+skill:\s*['\"]?([a-z0-9-]+)", text, re.M)
        if not m:
            out.append(Finding(ERROR, wf, "no `skill:` input; a role caller names the skill it runs", "role-workflow"))
            continue
        name = m.group(1)
        rel = f".agents/skills/{name}/SKILL.md"
        if rel not in ctx.files:
            out.append(Finding(ERROR, wf, f"skill `{name}` does not exist", "role-workflow"))
            continue
        meta, needs, _ = skill_meta(ctx, rel)
        if meta.get("writes", "repo") != "repo":
            out.append(Finding(ERROR, wf, f"runs `{name}` unattended, but it writes to external systems "
                               "(AGENTS.md rule 3)", "role-workflow"))
        for cid in needs:
            entry = wired.get(cid) if isinstance(wired.get(cid), dict) else {}
            headless = "script" in (entry.get("routes") or [])
            variant = mcp_variant(catalog_vendor(entries, cid, entry.get("vendor")), entry.get("variant"))
            if variant and variant.get("headless") and "mcp" in (entry.get("routes") or []):
                headless = True
            if not headless:
                out.append(Finding(ERROR, wf, f"runs `{name}` unattended, but `{cid}` is not wired to a key-based "
                                   "server or a script (docs/operating-model.md)", "role-workflow"))
    return out


THIRD_PARTY_HEADER = re.compile(r"^<!--\s*source:\s*(\S+)\s*\|\s*license:\s*([^|]+?)\s*\|\s*fetched:\s*(\d{4}-\d{2}-\d{2})\s*-->")


def check_third_party(ctx):
    """Reused reference material names its source on line one and in THIRD_PARTY.md; the skill carries license:."""
    out = []
    registry = ctx.text("THIRD_PARTY.md") if "THIRD_PARTY.md" in ctx.files else None
    for rel in ctx.glob(".agents/skills/*/references/*.md"):
        m = THIRD_PARTY_HEADER.match(ctx.text(rel).split("\n", 1)[0])
        if not m:
            continue
        url = m.group(1)
        if registry is None or url not in registry:
            out.append(Finding(ERROR, rel, f"reuses material from {url}; add its row to THIRD_PARTY.md", "third-party", line=1))
        skill = ".agents/skills/" + rel.split("/")[2] + "/SKILL.md"
        if skill in ctx.files and not (ctx.fm(skill) or {}).get("license"):
            out.append(Finding(WARNING, skill, "carries third-party references but no `license:` in its frontmatter",
                               "third-party", line=1))
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
    if block.startswith("skills-"):
        return _render_skills(ctx, block[len("skills-"):])
    if block == "scripts":
        rows = ["| Script | What it does |", "| --- | --- |"]
        files = sorted(ctx.glob("scripts/*.py") + ctx.glob("scripts/*.sh") + ctx.glob("scripts/hooks/*"))
        for rel in files:
            name = rel[len("scripts/"):]
            rows.append(f"| [{name}]({name}) | {cell(script_summary(ctx.text(rel)))} |")
        return "\n".join(rows)
    if block == "wired":
        return _render_wired(ctx)
    if block == "categories":
        return _render_categories(ctx)
    if block == "catalog":
        return _render_catalog(ctx)
    raise ValueError(block)


def _needs_cell(needs, optional, base):
    link = lambda c: f"[{c}]({base}#{c})"  # noqa: E731
    text = ", ".join(link(c) for c in needs) if needs else "nothing"
    if optional:
        text += " (optional: " + ", ".join(link(c) for c in optional) + ")"
    return text


def _render_skills(ctx, area):
    """One roster table per area: roles first, then workflows, alphabetical within each."""
    areas = [a[0] for a in ctx.schema.get("skills", {}).get("areas", [])]
    if area not in areas:
        raise ValueError(f"skills-{area}")
    rows = ["| Skill | Kind | What it does | Needs |", "| --- | --- | --- | --- |"]
    items = []
    for rel in ctx.glob(SKILL_GLOB):
        fm = ctx.fm(rel) or {}
        meta, needs, optional = skill_meta(ctx, rel)
        if meta.get("area") != area:
            continue
        name = rel.split("/")[2]
        kind = meta.get("kind", "workflow")
        kind_cell = f"role ({meta['cadence']})" if kind == "role" and meta.get("cadence") else kind
        what = re.split(r"\.\s+Use\b", str(fm.get("description", "")), maxsplit=1)[0].rstrip(".")
        items.append((0 if kind == "role" else 1, name, kind_cell, what,
                      _needs_cell(needs, optional, "../integrations/catalog/README.md")))
    for _, name, kind_cell, what, needs in sorted(items):
        rows.append(f"| [{name}](../.agents/skills/{name}/SKILL.md) | {kind_cell} | {cell(what)} | {needs} |")
    return "\n".join(rows)


def _catalog_order(ctx, entries):
    listed = ctx.schema.get("catalog", {}).get("categories", [])
    return [c for c in listed if c in entries] + sorted(c for c in entries if c not in listed)


def _render_wired(ctx):
    """The Wired table in integrations/README.md, from integrations/wired.json joined with the catalog."""
    entries, _ = load_catalog(ctx)
    _, data, _ = load_wired(ctx)
    wired = (data or {}).get("wired") or {}
    rows = ["| Category | Vendor | Route | Auth | Env vars (in `.env`) | Writes | Since |",
            "| --- | --- | --- | --- | --- | --- | --- |"]
    for cid in _catalog_order(ctx, {**entries, **wired}):
        entry = wired.get(cid)
        if not isinstance(entry, dict):
            continue
        cat = f"[{cid}](catalog/README.md#{cid})"
        vid = entry.get("vendor")
        if vid is None:
            rows.append(f"| {cat} | none | manual: {cell(entry.get('note', 'see the catalog'))} | | none | | |")
            continue
        vendor = catalog_vendor(entries, cid, vid) or {}
        routes = entry.get("routes") or []
        variant = mcp_variant(vendor, entry.get("variant")) if "mcp" in routes else None
        vroutes = vendor.get("routes") or {}
        script = vroutes.get("script") if isinstance(vroutes.get("script"), dict) else {}
        cli = vroutes.get("cli") if isinstance(vroutes.get("cli"), dict) else {}
        parts, env, auth = [], [], []
        if variant:
            parts.append(f"MCP `{variant.get('server')}` ({variant.get('transport')}) in `.mcp.json`")
            a = variant.get("auth") if isinstance(variant.get("auth"), dict) else {}
            auth.append(a.get("model", "?") + (f": {a['where']}" if a.get("where") else ""))
            env += a.get("env") or []
        if "script" in routes and script.get("path"):
            parts.append(f"`{script['path']}`" + (f" ({script['notes']})" if script.get("notes") else ""))
            env += script.get("env") or []
            if not variant:
                auth.append("key in the environment")
        if "cli" in routes and cli.get("tool"):
            parts.append(f"CLI `{cli['tool']}`")
        if "manual" in routes:
            parts.append("manual export")
        env_cell = ", ".join(f"`{v}`" for v in sorted(set(env))) or "none"
        rows.append(f"| {cat} | {cell(vendor.get('name', vid))} | {cell('; '.join(parts) or 'see the catalog')} | "
                    f"{cell('; '.join(auth) or 'none')} | {env_cell} | {cell(entry.get('writes', 'n/a'))} | "
                    f"{cell(entry.get('since', ''))} |")
    return "\n".join(rows)


def _render_categories(ctx):
    """The category index in integrations/README.md: what each is for, what is wired, who needs it."""
    entries, _ = load_catalog(ctx)
    _, data, _ = load_wired(ctx)
    wired = (data or {}).get("wired") or {}
    needed, optional = {}, {}
    for rel in ctx.glob(SKILL_GLOB):
        name = rel.split("/")[2]
        _, needs, opt = skill_meta(ctx, rel)
        for cid in needs:
            needed.setdefault(cid, []).append(name)
        for cid in opt:
            optional.setdefault(cid, []).append(name)
    rows = ["| Category | For | Wired | In the catalog | Needed by |", "| --- | --- | --- | --- | --- |"]
    for cid in _catalog_order(ctx, entries):
        d = entries[cid]
        entry = wired.get(cid) if isinstance(wired.get(cid), dict) else None
        if entry is None:
            status = "not wired"
        elif entry.get("vendor") is None:
            status = "manual"
        else:
            status = (catalog_vendor(entries, cid, entry["vendor"]) or {}).get("name", entry["vendor"])
        names = [v.get("name", v.get("id", "?")) for v in d.get("vendors") or [] if isinstance(v, dict)]
        bridges = d.get("bridges") or []
        vendors = ", ".join(names) or "none official"
        if bridges:
            vendors += f" (falls back to {', '.join(bridges)})"
        skills = ", ".join(f"[{n}](../.agents/skills/{n}/SKILL.md)" for n in sorted(needed.get(cid, [])))
        extra = len(optional.get(cid, []))
        if extra:
            skills += (" " if skills else "") + f"(+{extra} optional)"
        rows.append(f"| [{cid}](catalog/README.md#{cid}) | {cell(d.get('for', ''))} | {cell(status)} | "
                    f"{cell(vendors)} | {skills or 'nobody yet'} |")
    return "\n".join(rows)


def _render_catalog(ctx):
    """integrations/catalog/README.md: every category and every vendor route the catalog knows."""
    entries, _ = load_catalog(ctx)
    out = []
    for cid in _catalog_order(ctx, entries):
        d = entries[cid]
        out.append(f"### {cid}")
        out.append("")
        line = f"**{d.get('title', cid)}**: {d.get('for', '')}."
        if d.get("data_domain"):
            line += f" Data lands in `{str(d['data_domain']).rstrip('/')}/`."
        out.append(line)
        manual = d.get("manual") if isinstance(d.get("manual"), dict) else {}
        if manual:
            out.append(f"By hand: {manual.get('export', '')} Drop: `{manual.get('drop', '')}`.")
        if d.get("bridges"):
            out.append("Falls back to: " + ", ".join(d["bridges"]) + ".")
        out.append("")
        out.append("| Vendor | Mechanism | Auth | Writes | Headless | Verified | Checked |")
        out.append("| --- | --- | --- | --- | --- | --- | --- |")
        for v in d.get("vendors") or []:
            if not isinstance(v, dict):
                continue
            routes = v.get("routes") if isinstance(v.get("routes"), dict) else {}
            variant = mcp_variant(v)
            parts, auth, env = [], "manual export", []
            if variant:
                if variant.get("transport") == "stdio":
                    parts.append(f"stdio `{variant.get('server')}`: {variant.get('command')} "
                                 + " ".join(str(a) for a in variant.get("args") or []))
                else:
                    parts.append(f"http `{variant.get('server')}`: {variant.get('url', '')}")
                a = variant.get("auth") if isinstance(variant.get("auth"), dict) else {}
                auth = a.get("model", "?")
                env = a.get("env") or []
                if len(routes.get("mcp") or []) > 1:
                    parts[-1] += f" (+{len(routes['mcp']) - 1} variant{'s' if len(routes['mcp']) > 2 else ''})"
            cli = routes.get("cli") if isinstance(routes.get("cli"), dict) else {}
            if cli.get("tool"):
                parts.append(f"CLI `{cli['tool']}`")
            script = routes.get("script") if isinstance(routes.get("script"), dict) else {}
            if script.get("path"):
                parts.append(f"script `{script['path']}`")
                env += script.get("env") or []
                if not variant:
                    auth = "key in the environment"
            if env:
                auth += ": " + ", ".join(f"`{e}`" for e in sorted(set(env)))
            if v.get("writes"):
                tools = v.get("write_tools") or []
                writes = f"yes, {len(tools)} tools recorded" if tools else "yes, tools unrecorded"
                if v.get("read_only_switch"):
                    writes += "; read-only switch"
            else:
                writes = "no"
            headless = "yes" if variant and variant.get("headless") else ("script" if script.get("path") else "no")
            out.append(f"| {cell(v.get('name', v.get('id', '?')))} | {cell('; '.join(parts) or 'none')} | "
                       f"{cell(auth)} | {writes} | {headless} | {cell(v.get('verified', '?'))} | "
                       f"{cell(v.get('checked', ''))} |")
        out.append("")
    return "\n".join(out).strip()


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
    """.claude/skills/ mirrors .agents/skills/ (scripts/sync_skills.py).

    Always this checkout's own copy of the script, never the one under ctx.root: the
    gate (scripts/review_gate.py) runs the lint from main against a proposal's
    worktree, and a proposal must not get its own code executed with the gate's
    token. The worktree is only ever the --root the script acts on."""
    script = ROOT / "scripts" / "sync_skills.py"
    if not script.is_file() or not ctx.path(".agents/skills").is_dir():
        return []
    cmd = [sys.executable, str(script), "--root", str(ctx.root)]
    run = subprocess.run(cmd + ["--check"], capture_output=True, text=True, cwd=str(ROOT))
    if run.returncode == 0:
        return []
    return [Finding(ERROR, ".claude/skills", "skill links out of sync: " + " ".join(run.stdout.split()),
                    "skill-links", fix=lambda: subprocess.run(cmd, check=False, capture_output=True, cwd=str(ROOT)))]


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
    (check_catalog, "repo"),
    (check_wired, "repo"),
    (check_catalog_coverage, "repo"),
    (check_role_workflows, "repo"),
    (check_third_party, "repo"),
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
