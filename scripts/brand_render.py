#!/usr/bin/env python3
"""Render the brand image templates in brand/templates/ (banner, post, icon, shot) to exact-size PNGs with headless Chrome, in the colors, fonts and logos of brand/tokens.json (a neutral default while it is empty). Subcommands: presets (the size registry), render <template> --preset ID | --size WxH --param k=v, og <content piece> (the link preview from the draft's title), batch <kit.json> (a listing kit), logos (PNG exports of the SVGs in brand/logos/), book (the brand library: brand/library/library.js for the pages beside it; open index.html), check (tokens.json against visual-identity.md, and a kit's PNGs against the registry). Output goes to the gitignored brand/renders/ unless --out says otherwise; --brand DIR reads another brand folder (examples/beacon/brand) and renders into DIR/renders/; --print-url and --dry-run render nothing. Rules for the content: brand/image-rules.md. Chrome from $CHROME or the usual install paths. Standard library only."""

import argparse
import concurrent.futures
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import time
import urllib.parse
import xml.etree.ElementTree as ET
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRAND = ROOT / "brand"
TEMPLATES = BRAND / "templates"
SIZES = TEMPLATES / "sizes.json"
TOKENS = BRAND / "tokens.json"
IDENTITY = BRAND / "visual-identity.md"
SCREENSHOTS = BRAND / "screenshots"
OUT_DEFAULT = BRAND / "renders"
EXTERNAL_BRAND = False   # --brand: asset URLs are relative to brand/templates/, where the templates stay

TEMPLATE_PARAMS = {
    "banner": {"headline", "theme", "debug"},
    "post": {"headline", "stat", "shot", "focus", "theme", "debug"},
    "icon": {"bg", "mark", "pad", "radius", "debug"},
    "shot": {"shot", "fit", "focus", "debug"},
}
HEADLINE_MAX = {"banner": 45, "post": 60}   # visible characters; image-rules.md asks for about 40 and 50
NEUTRAL = {"bg": "111111", "fg": "F5F5F5", "primary": "8B93A1", "accent": "D4D8DE"}
FONT_FILE = re.compile(r"\.(woff2?|ttf|otf)$", re.I)
IMAGE_FILE = re.compile(r"^[\w.-]+\.(png|jpe?g|webp)$", re.I)
FOCUS = re.compile(r"^(0(\.\d+)?|1(\.0+)?),(0(\.\d+)?|1(\.0+)?)$")
HEX = re.compile(r"^#?([0-9a-fA-F]{6})$")
CHROME_CANDIDATES = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
)
CHROME_NAMES = ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome")
# Headless Chrome's viewport is shorter than --window-size and the strip below it is only partly
# painted, so render taller and keep the top h rows.
CHROME_PAD = 200


class BrandError(ValueError):
    """A job, a spec or the tokens are not usable; the message says what to change."""


def use_brand(path):
    """Read tokens, identity, logos and screenshots from another brand/ folder (examples/beacon/brand)."""
    global BRAND, TOKENS, IDENTITY, SCREENSHOTS, OUT_DEFAULT, EXTERNAL_BRAND
    BRAND = Path(path).resolve()
    if not (BRAND / "tokens.json").is_file():
        raise BrandError(f"{path} has no tokens.json")
    TOKENS, IDENTITY = BRAND / "tokens.json", BRAND / "visual-identity.md"
    SCREENSHOTS, OUT_DEFAULT = BRAND / "screenshots", BRAND / "renders"
    EXTERNAL_BRAND = True


def asset_url(rel):
    """A file under the brand folder, as a URL the templates can load."""
    if not EXTERNAL_BRAND:
        return "../" + Path(rel).as_posix()
    return Path(os.path.relpath(BRAND / rel, TEMPLATES)).as_posix()


# ---------------------------------------------------------------- registry --

def load_sizes(path=SIZES):
    return json.loads(Path(path).read_text(encoding="utf-8"))["sizes"]


def find_preset(sizes, pid):
    for s in sizes:
        if s["id"] == pid:
            return s
    raise BrandError(f"unknown preset '{pid}'; `scripts/brand_render.py presets` lists them")


def parse_size(value):
    m = re.fullmatch(r"(\d{2,5})x(\d{2,5})", value or "")
    if not m:
        raise BrandError(f"size must look like 1200x630, got '{value}'")
    return int(m.group(1)), int(m.group(2))


# ------------------------------------------------------------------ tokens --

def load_tokens(path=None):
    path = Path(path or TOKENS)
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def _brand_path(value, what):
    """A path under brand/ from tokens.json, as a URL relative to brand/templates/."""
    rel = Path(value)
    if rel.is_absolute() or ".." in rel.parts:
        raise BrandError(f"{what} must be a path under brand/, got '{value}'")
    if not (BRAND / rel).is_file():
        raise BrandError(f"{what} points at brand/{value}, which does not exist")
    return asset_url(rel)


def token_query(tokens, template, params):
    """The query parameters that carry the tokens into a template, and notes for the person.

    An empty color, font or logo falls back to the neutral default, and the note says so.
    """
    colors, fonts, logo = tokens.get("colors", {}), tokens.get("fonts", {}), tokens.get("logo", {})
    query, notes = {}, []
    for key, token in (("bg", "background"), ("fg", "text"), ("primary", "primary"), ("accent", "accent")):
        value = str(colors.get(token, "") or "")
        m = HEX.match(value)
        if value and not m:
            raise BrandError(f"tokens.json colors.{token} must be #RRGGBB, got '{value}'")
        query["c_" + key] = m.group(1).upper() if m else NEUTRAL[key]
    if not any(colors.get(t) for t in ("background", "text", "primary", "accent")):
        notes.append("brand/tokens.json has no colors: rendering the neutral default (fill it with /setup)")
    for role in ("heading", "body"):
        value = str(fonts.get(role, "") or "")
        if FONT_FILE.search(value):
            query[role + "_src"] = _brand_path(value, f"fonts.{role}")
            query[role] = Path(value).stem
        elif value:
            query[role] = value
    if not (fonts.get("heading") or fonts.get("body")):
        notes.append("brand/tokens.json has no fonts: using the system fallback")
    if fonts.get("fallback"):
        query["fallback"] = fonts["fallback"]
    if template != "shot":
        inverse = params.get("theme") == "inverse" or params.get("bg") == "inverse"
        base = "mark" if template == "icon" and params.get("mark", "mark") == "mark" else "primary"
        names = ([base + "_inverse"] if inverse else []) + [base, "primary" if base == "mark" else "mark"]
        chosen = next((n for n in names if logo.get(n)), None)
        if chosen:
            query["logo"] = _brand_path(logo[chosen], f"logo.{chosen}")
            if inverse and not chosen.endswith("_inverse"):
                notes.append(f"no logo.{base}_inverse in tokens.json: using logo.{chosen} on the inverse background")
        else:
            notes.append("brand/tokens.json has no logo: rendering without one")
    return query, notes


# -------------------------------------------------------------------- jobs --

def check_headline(text, template):
    """Problems with a headline: length, and at most one *gradient* phrase of up to three words."""
    problems = []
    if text.count("*") % 2:
        problems.append("unbalanced * in the headline; mark the gradient phrase as *like this*")
    phrases = re.findall(r"\*([^*]+)\*", text)
    if len(phrases) > 1:
        problems.append(f"{len(phrases)} gradient phrases; one at most")
    if any(len(p.split()) > 3 for p in phrases):
        problems.append("the gradient phrase is longer than three words")
    visible = text.replace("*", "")
    limit = HEADLINE_MAX.get(template)
    if limit and len(visible) > limit:
        problems.append(f"headline is {len(visible)} characters; at most {limit} on a {template} "
                        "(image-rules.md: cut the copy, do not shrink the type)")
    return problems


def resolve_job(sizes, job):
    """Turn a job dict into (template, w, h, content params with size), refusing anything but content."""
    job = dict(job)
    pid, size = job.pop("preset", None), job.pop("size", None)
    job.pop("file", None)
    p = find_preset(sizes, pid) if pid else {}
    template = job.pop("template", None) or p.get("template") or "banner"
    if template not in TEMPLATE_PARAMS:
        raise BrandError(f"no template '{template}'; one of {', '.join(TEMPLATE_PARAMS)}")
    if size:
        w, h = parse_size(size)
    elif p:
        w, h = p["w"], p["h"]
    else:
        raise BrandError("a job needs a preset or a size")
    params = {k: str(v) for k, v in {**(p.get("params") or {}), **job}.items() if v is not None}
    params = {k: v for k, v in params.items() if k in TEMPLATE_PARAMS[template] or k in job}
    unknown = sorted(set(params) - TEMPLATE_PARAMS[template])
    if unknown:
        raise BrandError(f"not allowed for {template}: {', '.join(unknown)}. Templates take content only; "
                         "the look comes from brand/tokens.json (brand/image-rules.md)")
    problems = check_headline(params["headline"], template) if params.get("headline") else []
    if "stat" in params:
        if not 0 < len(params["stat"]) <= 6:
            problems.append("stat must be 1 to 6 characters, like 3x or 41%")
        if "shot" in params:
            problems.append("a stat post carries no screenshot; drop stat or shot")
    if "shot" in params and not (IMAGE_FILE.match(params["shot"]) and (SCREENSHOTS / params["shot"]).is_file()):
        problems.append(f"shot must be a file name in brand/screenshots/, got '{params['shot']}'")
    if template == "shot" and "shot" not in params:
        problems.append("a shot job needs shot=<file in brand/screenshots/>")
    if "focus" in params and not FOCUS.match(params["focus"]):
        problems.append(f"focus must be x,y with both between 0 and 1, got '{params['focus']}'")
    for key, allowed in (("theme", ("brand", "inverse")), ("bg", ("brand", "inverse", "transparent", "glow")),
                         ("mark", ("mark", "primary")), ("fit", ("contain", "cover"))):
        if key in params and params[key] not in allowed:
            problems.append(f"{key} must be one of {', '.join(allowed)}, got '{params[key]}'")
    for key, top in (("pad", 0.45), ("radius", 0.5)):
        if key in params:
            try:
                ok = 0 <= float(params[key]) <= top
            except ValueError:
                ok = False
            if not ok:
                problems.append(f"{key} must be a number from 0 to {top}")
    if problems:
        raise BrandError("; ".join(problems))
    params["w"], params["h"] = str(w), str(h)
    params["safe"] = ",".join(str(n) for n in p["safe"]) if p and not size else ""
    if not params["safe"]:
        del params["safe"]
    return template, w, h, params


def build_url(template, params, tokens):
    """file:// URL of the template with content, size and token parameters; plus the token notes."""
    query, notes = token_query(tokens, template, params)
    query.update(params)
    if "shot" in params:
        query["shot"] = asset_url("screenshots/" + params["shot"])
    path = TEMPLATES / f"{template}.html"
    url = path.as_uri() + "?" + urllib.parse.urlencode(query, quote_via=urllib.parse.quote)
    return url, notes


# --------------------------------------------------------------- rendering --

def chrome_path():
    """$CHROME, else the first Chrome, Chromium or Edge found on macOS or Linux; None if none."""
    env = os.environ.get("CHROME")
    if env:
        return env if Path(env).is_file() else None
    for p in CHROME_CANDIDATES:
        if Path(p).is_file():
            return p
    for name in CHROME_NAMES:
        found = shutil.which(name)
        if found:
            return found
    return None


def render(url, w, h, out, chrome=None):
    chrome = chrome or chrome_path()
    if not chrome:
        raise BrandError("no Chrome or Chromium found; install one or set CHROME=/path/to/chrome")
    out = Path(out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        out.unlink()
    with tempfile.TemporaryDirectory() as td:
        # Chrome can write the screenshot and then not exit, so poll until the file size is
        # stable and stop the process ourselves.
        proc = subprocess.Popen([chrome, "--headless=new", "--no-first-run", "--no-default-browser-check",
                                 "--disable-extensions", "--disable-gpu", "--hide-scrollbars",
                                 "--force-device-scale-factor=1", "--default-background-color=00000000",
                                 f"--window-size={w},{h + CHROME_PAD}", "--virtual-time-budget=8000",
                                 "--allow-file-access-from-files", f"--user-data-dir={td}/profile",
                                 f"--screenshot={out}", url],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        deadline, last = time.time() + 60, -1
        while time.time() < deadline:
            time.sleep(0.4)
            if out.exists():
                size = out.stat().st_size
                if size and size == last:
                    break
                last = size
            if proc.poll() is not None and out.exists():
                break
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
    if not out.exists() or not out.stat().st_size:
        raise BrandError(f"Chrome did not produce {out}")
    crop_png_height(out, h)
    return out


def _chunk(kind, data):
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)


def crop_png_height(path, h):
    """Keep the top h rows of a non-interlaced 8-bit RGB(A) PNG. Each filtered scanline depends
    only on the rows above it, so truncating the decompressed stream is lossless."""
    data = Path(path).read_bytes()
    pos, chunks = 8, []
    while pos < len(data):
        n, = struct.unpack(">I", data[pos:pos + 4])
        chunks.append((data[pos + 4:pos + 8], data[pos + 8:pos + 8 + n]))
        pos += 12 + n
    ihdr = chunks[0][1]
    w, old_h, depth, ctype, _, _, interlace = struct.unpack(">IIBBBBB", ihdr)
    if old_h == h:
        return
    if depth != 8 or interlace or ctype not in (2, 6):
        raise BrandError(f"cannot crop {path}: expected a non-interlaced 8-bit RGB or RGBA PNG")
    stride = 1 + w * (4 if ctype == 6 else 3)
    raw = zlib.decompress(b"".join(c for t, c in chunks if t == b"IDAT"))[:stride * h]
    Path(path).write_bytes(data[:8] + _chunk(b"IHDR", struct.pack(">II", w, h) + ihdr[8:])
                           + _chunk(b"IDAT", zlib.compress(raw, 9)) + _chunk(b"IEND", b""))


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
        raise BrandError(f"{path} is not a PNG")
    return struct.unpack(">II", head[16:24])


def check_png(path, w, h, max_kb=None):
    problems = []
    aw, ah = png_size(path)
    if (aw, ah) != (w, h):
        problems.append(f"{aw}x{ah}, expected {w}x{h}")
    kb = Path(path).stat().st_size / 1024
    if max_kb and kb > max_kb:
        problems.append(f"{kb:.0f} KB, limit {max_kb} KB")
    return problems


def svg_size(path):
    """(width, height) of an SVG from its viewBox, else its width and height attributes."""
    root = ET.parse(path).getroot()
    box = (root.get("viewBox") or "").replace(",", " ").split()
    if len(box) == 4:
        return float(box[2]), float(box[3])
    num = lambda v: float(re.match(r"[\d.]+", v or "0").group() or 0)  # noqa: E731
    w, h = num(root.get("width")), num(root.get("height"))
    if not (w and h):
        raise BrandError(f"{path} has no viewBox or width and height")
    return w, h


def show(path):
    try:
        return str(Path(path).resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def run_jobs(jobs):
    """jobs: list of (url, w, h, out). Four at a time."""
    chrome = chrome_path()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for out in pool.map(lambda j: render(*j, chrome=chrome), jobs):
            print(show(out))


def say(notes):
    for n in dict.fromkeys(notes):
        print(f"note: {n}", file=sys.stderr)


# ------------------------------------------------------------------ checks --

ROLE_ROW = re.compile(r"^\|\s*(primary|secondary|background|text|accent)\b[^|]*\|\s*`?(#[0-9a-fA-F_]{6})`?", re.I | re.M)


def identity_check(tokens, identity_text, brand_dir=None):
    """Where tokens.json and visual-identity.md disagree, as sentences. Empty when they agree."""
    problems = []
    brand_dir = brand_dir or BRAND
    colors, fonts, logo = tokens.get("colors", {}), tokens.get("fonts", {}), tokens.get("logo", {})
    doc = {m.group(1).lower(): m.group(2) for m in ROLE_ROW.finditer(identity_text)}
    for role in ("primary", "secondary", "background", "text", "accent"):
        ours = str(colors.get(role, "") or "")
        theirs = doc.get(role, "")
        theirs = "" if "_" in theirs else theirs
        if ours and not HEX.match(ours):
            problems.append(f"tokens.json colors.{role} = {ours} is not #RRGGBB")
        elif ours.lower() != theirs.lower():
            problems.append(f"colors.{role}: tokens.json has {ours or 'nothing'}, "
                            f"visual-identity.md has {theirs or 'nothing'}")
    lowered = identity_text.lower()
    for role in ("heading", "body"):
        value = str(fonts.get(role, "") or "")
        name = Path(value).stem if FONT_FILE.search(value) else value
        if name and name.lower() not in lowered:
            problems.append(f"fonts.{role} = {value} is not named in visual-identity.md")
        if FONT_FILE.search(value) and not (Path(brand_dir) / value).is_file():
            problems.append(f"fonts.{role} points at brand/{value}, which does not exist")
    for key, value in logo.items():
        if key.startswith("$") or not value:
            continue
        if not (Path(brand_dir) / value).is_file():
            problems.append(f"logo.{key} points at brand/{value}, which does not exist")
    return problems


# ---------------------------------------------------------------- commands --

def cmd_presets(_a):
    for s in load_sizes():
        state = "own format" if s["group"] == "Generic" and not s.get("source") else \
            f"verified {s['verified']}" if s.get("verified") else "UNVERIFIED"
        print(f"{s['id']:<24} {s['w']:>5}x{s['h']:<5} {s['template']:<7} {s['group']:<12} {state:<20} {s['label']}")


def cmd_render(a):
    job = dict(kv.split("=", 1) for kv in a.param)
    job["template"] = a.template
    if a.preset:
        job["preset"] = a.preset
    if a.size:
        job["size"] = a.size
    template, w, h, params = resolve_job(load_sizes(), job)
    url, notes = build_url(template, params, load_tokens())
    say(notes)
    if a.print_url:
        print(url)
        return 0
    out = a.out or OUT_DEFAULT / f"{a.preset or f'{template}-{w}x{h}'}.png"
    run_jobs([(url, w, h, out)])
    return 0


def draft_title(piece):
    """The first # heading of a content piece's draft.md."""
    draft = Path(piece) / "draft.md"
    if not draft.is_file():
        raise BrandError(f"{show(draft)} does not exist")
    for line in draft.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise BrandError(f"{show(draft)} has no # title; pass --headline")


def cmd_og(a):
    piece = Path(a.piece).resolve()
    headline = a.headline or draft_title(piece)
    template, w, h, params = resolve_job(load_sizes(), {"preset": "og", "headline": headline})
    url, notes = build_url(template, params, load_tokens())
    say(notes)
    if a.print_url:
        print(url)
        return 0
    run_jobs([(url, w, h, a.out or OUT_DEFAULT / piece.name / "og.png")])
    return 0


def kit_jobs(kit_path, tokens=None):
    """(url, w, h, out, max_kb) per job of a kit spec, plus the token notes."""
    kit_path = Path(kit_path).resolve()
    kit = json.loads(kit_path.read_text(encoding="utf-8"))
    out_dir = ROOT / kit["out"] if kit.get("out") else OUT_DEFAULT / kit_path.parent.name
    sizes, tokens = load_sizes(), load_tokens() if tokens is None else tokens
    jobs, notes, errors = [], [], []
    for i, job in enumerate(kit.get("jobs", []), 1):
        name = str(job.get("file", ""))
        try:
            if not re.fullmatch(r"[\w.-]+\.png", name):
                raise BrandError(f"file must be a plain name ending in .png, got '{name}'")
            template, w, h, params = resolve_job(sizes, job)
            url, n = build_url(template, params, tokens)
        except BrandError as e:
            errors.append(f"job {i} ({name or 'no file'}): {e}")
            continue
        notes += n
        max_kb = find_preset(sizes, job["preset"]).get("max_kb") if job.get("preset") else None
        jobs.append((url, w, h, out_dir / name, max_kb))
    if errors:
        raise BrandError("\n".join(errors))
    return jobs, notes


def report_pngs(jobs):
    bad = 0
    for _, w, h, out, max_kb in jobs:
        problems = check_png(out, w, h, max_kb) if Path(out).exists() else ["missing"]
        bad += bool(problems)
        print(f"{'FAIL' if problems else 'ok  '} {show(out)} {'; '.join(problems)}")
    return 1 if bad else 0


def cmd_batch(a):
    jobs, notes = kit_jobs(a.kit)
    say(notes)
    if a.dry_run:
        for url, w, h, out, _ in jobs:
            print(f"{show(out)}  {w}x{h}  {url}")
        return 0
    run_jobs([j[:4] for j in jobs])
    return report_pngs(jobs)


LOGO_WIDTHS = (512, 1024, 2048)


def logo_jobs(logos_dir=None):
    logos_dir = logos_dir or BRAND / "logos"
    jobs = []
    for svg in sorted(Path(logos_dir).glob("*.svg")):
        vw, vh = svg_size(svg)
        for px in LOGO_WIDTHS:
            h = max(1, round(px * vh / vw))
            query = {"w": px, "h": h, "bg": "transparent", "pad": 0, "logo": asset_url("logos/" + svg.name)}
            url = (TEMPLATES / "icon.html").as_uri() + "?" + urllib.parse.urlencode(query)
            jobs.append((url, px, h, Path(logos_dir) / "png" / f"{svg.stem}-{px}.png"))
    return jobs


def cmd_logos(a):
    jobs = logo_jobs()
    if not jobs:
        print("no SVG in brand/logos/; add the masters there first")
        return 1
    if a.dry_run:
        for _, w, h, out in jobs:
            print(f"{show(out)}  {w}x{h}")
        return 0
    run_jobs(jobs)
    return 0


def cmd_check(a):
    tokens = load_tokens()
    identity = IDENTITY.read_text(encoding="utf-8") if IDENTITY.is_file() else ""
    status = 0
    if a.kit:
        jobs, _ = kit_jobs(a.kit, tokens)
        status = report_pngs(jobs)
    problems = identity_check(tokens, identity)
    if not any(v for k, v in tokens.get("colors", {}).items() if not k.startswith("$")) \
            and "Template: unfilled" in identity:
        print("tokens.json and visual-identity.md are both unfilled: images use the neutral default (/setup fills them)")
        return status
    for p in problems:
        print(f"DRIFT {p}")
    if not problems:
        print("tokens.json agrees with visual-identity.md")
    return status or (1 if problems else 0)


LIBRARY_PAGES = ("index.html", "logos.html", "colors.html", "banners.html", "posts.html", "screenshots.html",
                 "library.css", "library-runtime.js")
SAMPLES_DEFAULT = {
    "banner": "Your headline, *in the gradient*",
    "display": "The display line, set large", "headline": "A headline at section size",
    "title": "A title for cards and lists", "lede": "A lede sentence introduces a page in the body face.",
    "eyebrow": "Eyebrow",
    "posts": [
        {"name": "Portrait", "ratio": "4:5", "w": 1080, "h": 1350, "headline": "An opinion, *said plainly*"},
        {"name": "Square", "ratio": "1:1", "w": 1080, "h": 1080, "headline": "A claim the number proves", "stat": "3x"},
        {"name": "Landscape", "ratio": "1.91:1", "w": 1200, "h": 627, "headline": "A link post, *one idea*"},
    ],
}


def md_html(text):
    """A section of visual-identity.md as HTML: paragraphs and bullets, **bold** and `code`; tables dropped."""
    def inline(t):
        t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
        return re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    out, para, items = [], [], []
    def flush():
        if para:
            out.append(f'<p class="prose">{inline(" ".join(para))}</p>')
            para.clear()
        if items:
            out.append('<ul class="rules">' + "".join(f"<li>{inline(i)}</li>" for i in items) + "</ul>")
            items.clear()
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(("|", ">", "#")):
            flush()
        elif stripped.startswith("- "):
            if para:
                flush()
            items.append(stripped[2:])
        elif items and line.startswith("  "):
            items[-1] += " " + stripped
        else:
            para.append(stripped)
    flush()
    return "".join(out)


def identity_sections(text):
    """{heading: html} for the sections of visual-identity.md the library shows."""
    found = {}
    for m in re.finditer(r"^## ([^\n]+)\n(.*?)(?=^## |\Z)", text, re.M | re.S):
        found[m.group(1).strip().lower()] = md_html(m.group(2))
    keys = {"logo": "logo usage", "colors": "colors", "imagery": "imagery", "typography": "typography"}
    return {k: found[v] for k, v in keys.items() if found.get(v)}


def _luminance(hex_color):
    rgb = [int(hex_color.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    rgb = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]


def library_data(tokens, identity_text="", samples=None, regen="python3 scripts/brand_render.py book"):
    """window.LIB for brand/library/: tokens, assets and sample copy, every path relative to the library."""
    lib_dir = BRAND / "library"
    rel = lambda path: Path(os.path.relpath(path, lib_dir)).as_posix()  # noqa: E731
    colors = {k: v for k, v in tokens.get("colors", {}).items() if not k.startswith("$") and v and HEX.match(v)}
    fonts = {k: v for k, v in tokens.get("fonts", {}).items() if not k.startswith("$") and v}
    logo = {k: v for k, v in tokens.get("logo", {}).items() if not k.startswith("$") and v and (BRAND / v).is_file()}
    samples = {**SAMPLES_DEFAULT, **(samples or {})}
    faces, families = [], []
    for role in ("heading", "body"):
        value = fonts.get(role, "")
        if FONT_FILE.search(value) and (BRAND / value).is_file():
            faces.append({"family": Path(value).stem, "src": rel(BRAND / value)})
            fonts[role] = Path(value).stem
        elif value and value not in families:
            families.append(value)
    google = ("https://fonts.googleapis.com/css2?" + "&".join(
        "family=" + urllib.parse.quote(f).replace("%20", "+") + ":wght@300;400;500;600;700" for f in families)
        + "&display=swap") if families else ""
    logos = []
    for key in ("primary", "mark", "primary_inverse", "mark_inverse"):
        if key in logo:
            square = key.startswith("mark")
            logos.append({"key": key, "file": logo[key], "src": rel(BRAND / logo[key]), "square": square,
                          "inverse": key.endswith("_inverse"),
                          "note": ("Mark" if square else "Logo") + (", for the opposite background"
                                                                     if key.endswith("_inverse") else ", for the brand background")})
    dark_brand = _luminance(colors["background"]) < 0.4 if "background" in colors else True
    # The library chrome is black: the logo with light ink is primary on a dark brand, else primary_inverse.
    header = logo.get("primary") if dark_brand else logo.get("primary_inverse")
    pngs = sorted((BRAND / "logos" / "png").glob("*.png")) if (BRAND / "logos" / "png").is_dir() else []
    shots = []
    for f in sorted(SCREENSHOTS.glob("*")) if SCREENSHOTS.is_dir() else []:
        if IMAGE_FILE.match(f.name):
            try:
                w, h = png_size(f)
            except Exception:  # noqa: BLE001 (JPEG and WebP: size unknown, still listed)
                w = h = "?"
            shots.append({"file": f.name, "src": rel(f), "w": w, "h": h})
    query = {}
    for template in ("banner", "post", "icon"):
        q, _ = token_query(tokens, template, {})
        query[template] = urllib.parse.urlencode(q, quote_via=urllib.parse.quote)
    posts = [p for p in samples.get("posts", []) if not p.get("shot") or (SCREENSHOTS / p["shot"]).is_file()]
    return {
        "name": samples.get("name", ""), "regen": regen, "colors": colors, "fonts": fonts,
        "fontFaces": faces, "googleFonts": google, "headerLogo": rel(BRAND / header) if header else "",
        "logos": logos, "pngs": [{"name": f.name, "src": rel(f)} for f in pngs], "screenshots": shots,
        "templates": rel(TEMPLATES), "shotBase": asset_url("screenshots/x")[:-1], "query": query,
        "identity": identity_sections(identity_text), "posts": posts,
        "samples": {k: samples[k] for k in ("banner", "display", "headline", "title", "lede", "eyebrow")},
    }


def cmd_book(a):
    lib_dir = BRAND / "library"
    lib_dir.mkdir(exist_ok=True)
    if EXTERNAL_BRAND:  # another brand folder gets a copy of the pages; only library.js differs
        for name in LIBRARY_PAGES:
            shutil.copyfile(ROOT / "brand" / "library" / name, lib_dir / name)
    samples_file = lib_dir / "samples.json"
    samples = json.loads(samples_file.read_text(encoding="utf-8")) if samples_file.is_file() else {}
    identity = IDENTITY.read_text(encoding="utf-8") if IDENTITY.is_file() else ""
    regen = "python3 scripts/brand_render.py " + (f"--brand {show(BRAND)} " if EXTERNAL_BRAND else "") + "book"
    data = library_data(load_tokens(), identity, samples, regen)
    out = lib_dir / "library.js"
    out.write_text("// Generated by `" + regen + "` from tokens.json, logos/, screenshots/,\n"
                   "// visual-identity.md and library/samples.json. Do not edit; re-run it.\n"
                   "window.LIB = " + json.dumps(data, indent=1, ensure_ascii=False) + ";\n", encoding="utf-8")
    print(show(lib_dir / "index.html"))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--brand", metavar="DIR", help="another brand/ folder, e.g. examples/beacon/brand")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("presets", help="list the size registry").set_defaults(fn=cmd_presets)
    r = sub.add_parser("render", help="render one image")
    r.add_argument("template", choices=sorted(TEMPLATE_PARAMS))
    g = r.add_mutually_exclusive_group(required=True)
    g.add_argument("--preset")
    g.add_argument("--size", help="WxH, e.g. 1200x630")
    r.add_argument("--param", action="append", default=[], help="k=v, repeatable (headline, stat, shot, ...)")
    r.add_argument("--out", type=Path)
    r.add_argument("--print-url", action="store_true", help="print the template URL to open in a browser")
    r.set_defaults(fn=cmd_render)
    o = sub.add_parser("og", help="the link preview for a content piece")
    o.add_argument("piece", help="content/YYYY-MM-<slug>")
    o.add_argument("--headline", help="instead of the draft's title")
    o.add_argument("--out", type=Path)
    o.add_argument("--print-url", action="store_true")
    o.set_defaults(fn=cmd_og)
    b = sub.add_parser("batch", help="render every job in a kit spec, then check sizes")
    b.add_argument("kit")
    b.add_argument("--dry-run", action="store_true", help="list the jobs, render nothing")
    b.set_defaults(fn=cmd_batch)
    lg = sub.add_parser("logos", help="PNG exports of brand/logos/*.svg into brand/logos/png/")
    lg.add_argument("--dry-run", action="store_true")
    lg.set_defaults(fn=cmd_logos)
    bk = sub.add_parser("book", help="the brand library pages in brand/library/ (open index.html in a browser)")
    bk.set_defaults(fn=cmd_book)
    c = sub.add_parser("check", help="tokens.json against visual-identity.md; a kit's PNGs against the registry")
    c.add_argument("kit", nargs="?")
    c.set_defaults(fn=cmd_check)
    a = ap.parse_args(argv)
    try:
        if a.brand:
            use_brand(a.brand)
        return a.fn(a) or 0
    except BrandError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
