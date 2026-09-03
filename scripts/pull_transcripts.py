#!/usr/bin/env python3
"""Pull new Granola meeting transcripts into memory/transcripts/inbox/.

Granola is the shipped example of a transcript connector. A connector for
another provider (Zoom, Fireflies, anything with an API) is a copy of this
script that writes the same files: the inbox contract is in
memory/transcripts/README.md, and integrations/adding-an-integration.md has
the worked example. The chief-of-staff skill does not care who wrote the
file.

Standard library only. Talks to Granola's public API
(https://docs.granola.ai/api-reference, Business plan or higher) and writes
one Markdown file per meeting: a small frontmatter header followed by the
transcript, speaker by speaker.

Usage, from the repo root:
    python3 scripts/pull_transcripts.py                    # pull new notes
    python3 scripts/pull_transcripts.py --since 2026-09-01 # only meetings from that date
    python3 scripts/pull_transcripts.py --dry-run          # list, write nothing
    python3 scripts/pull_transcripts.py --limit 5          # stop after 5 notes

The key: GRANOLA_API_KEY from the environment, or from a .env file at the
repo root (copied from .env.example). The value is never printed. Agents do
not read .env; this script may, because it never echoes what it finds.

Dedupe: a note whose output filename already exists in inbox/ or processed/
is skipped, so re-running is safe and processed meetings never come back.
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from _common import ROOT, setting

INBOX = ROOT / "memory" / "transcripts" / "inbox"
PROCESSED = ROOT / "memory" / "transcripts" / "processed"

BASE = "https://public-api.granola.ai/v1"
PAGE_SIZE = 30          # API maximum for /notes
TRANSCRIPT_PAGE = 100   # API maximum for /notes/{id}/transcript

# Granola labels a transcript segment by audio source, not by person:
# "microphone" is the note owner's own mic, "speaker" is everyone else.
SPEAKER_LABELS = {"me": "Me", "them": "Them"}


# --- key resolution ---------------------------------------------------------

def api_key():
    key = setting("GRANOLA_API_KEY")
    if not key:
        sys.exit(
            "error: GRANOLA_API_KEY is not set.\n"
            "  Put it in the environment, or in .env at the repo root "
            "(copy .env.example).\n"
            "  Get a key in Granola: Settings -> Connectors -> API keys "
            "(Business plan or higher)."
        )
    return key


# --- HTTP -------------------------------------------------------------------

def get_json(key, path, params=None):
    """One GET against the Granola API. Exits with a readable message on
    failure; never prints the key or the request headers."""
    url = BASE + path
    if params:
        url += "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v})
    req = urllib.request.Request(url, headers={
        "Authorization": "Bearer " + key,
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read() or b"{}")
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:300]
        if e.code in (401, 403):
            sys.exit(f"error: Granola rejected the API key ({e.code}). "
                     "Check GRANOLA_API_KEY and the plan it belongs to.")
        sys.exit(f"error: GET {path} returned {e.code}: {detail}")
    except urllib.error.URLError as e:
        sys.exit(f"error: could not reach Granola ({e.reason}).")


def list_notes(key, since, limit):
    """All notes (newest first), following the cursor until `limit`."""
    notes, cursor = [], None
    while len(notes) < limit:
        resp = get_json(key, "/notes", {
            "page_size": min(PAGE_SIZE, limit - len(notes)),
            "created_after": since,
            "cursor": cursor,
        })
        batch = resp.get("notes") or []
        notes.extend(batch)
        cursor = resp.get("cursor")
        if not batch or not resp.get("hasMore") or not cursor:
            break
    return notes[:limit]


def fetch_transcript(key, note_id):
    """Every transcript segment of one note, following the cursor."""
    segments, cursor = [], None
    while True:
        resp = get_json(key, f"/notes/{note_id}/transcript",
                        {"page_size": TRANSCRIPT_PAGE, "cursor": cursor})
        segments.extend(resp.get("transcript") or [])
        cursor = resp.get("cursor")
        if not resp.get("hasMore") or not cursor:
            return segments


def fetch_attendees(key, note_id):
    """Attendee names if the note exposes them; an empty list otherwise.
    Best effort: the note detail is optional for the pipeline."""
    note = get_json(key, f"/notes/{note_id}")
    people = note.get("attendees") or note.get("participants") or []
    names = []
    for p in people:
        if isinstance(p, dict):
            name = p.get("name") or p.get("email")
        else:
            name = str(p)
        if name:
            names.append(str(name))
    return names


# --- rendering --------------------------------------------------------------

def slugify(text, maxlen=50):
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return s[:maxlen].strip("-") or "meeting"


def date_of(note):
    raw = note.get("created_at") or ""
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00")).strftime("%Y-%m-%d")
    except ValueError:
        return raw[:10] or datetime.now(timezone.utc).strftime("%Y-%m-%d")


def speaker_label(segment):
    sp = segment.get("speaker") or {}
    if isinstance(sp, dict):
        return sp.get("name") or SPEAKER_LABELS.get(sp.get("attribution", ""), "Speaker")
    return str(sp) or "Speaker"


def render_transcript(segments):
    """Merge consecutive segments from the same speaker into one paragraph."""
    blocks, label, buf = [], None, []
    for seg in segments:
        text = (seg.get("text") or "").strip()
        if not text:
            continue
        who = speaker_label(seg)
        if who != label and buf:
            blocks.append(f"**{label}:** {' '.join(buf)}")
            buf = []
        label = who
        buf.append(text)
    if buf:
        blocks.append(f"**{label}:** {' '.join(buf)}")
    return "\n\n".join(blocks)


def quote(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def render_file(title, date, attendees, note_id, body):
    lines = [
        "---",
        f"title: {quote(title)}",
        f"date: {date}",
        "source: granola",
        f"granola_id: {note_id}",
    ]
    if attendees:
        lines.append("attendees: [" + ", ".join(quote(a) for a in attendees) + "]")
    lines += ["---", "", f"# {title}", "", body, ""]
    return "\n".join(lines)


# --- main -------------------------------------------------------------------

def existing_filenames():
    names = set()
    for folder in (INBOX, PROCESSED):
        if folder.is_dir():
            names.update(p.name for p in folder.iterdir() if p.is_file())
    return names


def main():
    ap = argparse.ArgumentParser(
        description="Pull new Granola transcripts into memory/transcripts/inbox/.")
    ap.add_argument("--since", metavar="YYYY-MM-DD",
                    help="only notes created on or after this date")
    ap.add_argument("--limit", type=int, default=50,
                    help="stop after this many notes (default 50)")
    ap.add_argument("--dry-run", action="store_true",
                    help="list what would be written; write nothing")
    args = ap.parse_args()

    if args.since:
        try:
            datetime.strptime(args.since, "%Y-%m-%d")
        except ValueError:
            sys.exit("error: --since expects YYYY-MM-DD")

    key = api_key()
    seen = existing_filenames()
    notes = list_notes(key, args.since, args.limit)
    if not notes:
        print("Granola: no notes returned" + (f" since {args.since}" if args.since else "") + ".")
        return

    written, skipped, empty = [], 0, 0
    for note in notes:
        note_id = note.get("id")
        title = (note.get("title") or "Untitled meeting").strip()
        date = date_of(note)
        filename = f"{date}-{slugify(title)}.md"
        if filename in seen:
            skipped += 1
            continue
        if args.dry_run:
            print(f"  would write: memory/transcripts/inbox/{filename}")
            written.append(filename)
            seen.add(filename)
            continue
        segments = fetch_transcript(key, note_id)
        body = render_transcript(segments)
        if not body:
            empty += 1
            continue
        attendees = fetch_attendees(key, note_id)
        INBOX.mkdir(parents=True, exist_ok=True)
        (INBOX / filename).write_text(
            render_file(title, date, attendees, note_id, body), encoding="utf-8")
        print(f"  + memory/transcripts/inbox/{filename}")
        written.append(filename)
        seen.add(filename)

    verb = "would write" if args.dry_run else "wrote"
    print(f"Granola: {verb} {len(written)} new, skipped {skipped} already in inbox/ or processed/"
          + (f", {empty} without a transcript" if empty else "") + ".")
    if written and not args.dry_run:
        print("Next: process them with the chief-of-staff skill (/chief-of-staff).")


if __name__ == "__main__":
    main()
