# data/events/

Webinar and event attendee lists, and the follow-up specs built from them.
Fed by the `events` integration category (Zoom, Luma, or whatever hosts the
team's events). See `integrations/README.md`.

## Snapshots

`snapshots/YYYY-MM-DD-<source>-<what>.csv`, immutable, named per
`data/README.md`. Typical:

- `2026-08-31-zoom-webinar-attendees.csv`: registrants and attendees, with
  join time and minutes watched
- `2026-09-15-repo-webinar-followup.csv`: the follow-up spec the
  `event-followup` skill computes in-repo (`repo` is the source token for
  that): who gets which sequence, and why

The `event-followup` skill writes here.

## Rules

- **The PII rule applies hardest here.** An attendee list is names and
  emails. It belongs in a private repo only, after the team logged that
  decision; a public copy holds counts per event and per segment.
- Load `data/ontology/` first. Whether an attendee becomes a lead or an MQL
  is defined in `data/ontology/funnel.md`, not by the event tool.
