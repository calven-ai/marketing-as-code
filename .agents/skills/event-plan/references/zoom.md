# Zoom: staging a webinar, reading registrants

Wired through the Zoom MCP servers (`integrations/catalog/events.json`;
OAuth, an admin may need to approve the app). The registry documents the
workspace server for summaries, transcripts and recordings; webinar
registrant and attendance tools are not confirmed, so check the server's
tool list in the session before promising anything. The same host serves
`/mcp/meeting/streamable` for meetings.

## What this skill may do

1. Read: list upcoming webinars and their registration settings so the
   plan does not duplicate one; read past webinars' registrant and
   attendee counts if a tool exposes them.
2. Stage, only on a person's yes: create the webinar with registration
   required and the registration page unpublished or the webinar not yet
   listed, using the copy from `content/YYYY-MM-<slug>/`. Report the
   webinar id and the registration URL. Publishing the page, sending
   invitations and reminders are human acts in Zoom.
3. Never enable reminder emails, import registrants, or start a webinar.

## Reading attendance afterwards

Registrants and attendees (join time, minutes attended, poll answers) are
a `snapshot-pull` into
`data/events/snapshots/YYYY-MM-DD-zoom-<event>-attendees.csv`, columns in
the `event-followup` skill. No tool for it: a person exports the registrant
and attendee reports from the Zoom web portal and drops the CSV there.

## Unattended path

A Server-to-Server OAuth script copied from `scripts/pull_transcripts.py`
(env `ZOOM_ACCOUNT_ID`, `ZOOM_CLIENT_ID`, `ZOOM_CLIENT_SECRET`), not built
yet; `integrations/adding-an-integration.md` walks through it.
