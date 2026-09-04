# Zoom: registrants, attendance, questions

Wired through the Zoom MCP servers (`integrations/catalog/events.json`;
OAuth). Webinar registrant and attendance tools are not confirmed in the
registry, so check the server's tool list in the session; the workspace
server does expose recordings, transcripts and summaries, which give you
the Q&A text when the attendance report does not.

## The attendee snapshot

`data/events/snapshots/YYYY-MM-DD-<vendor>-<event>-attendees.csv`:

```csv
event,event_date,registrant_id,domain,company,role,registered_at,attended,join_time,minutes,questions_asked,poll_answers,source,pulled_at
```

`registrant_id` is the vendor's id or a hash of the email; add
`name,email` only when `repo.private` in `docs/schema.json` is true.
`domain` comes from the email domain; free-mail domains stay as they are
and get no company.

## Where each column comes from

| Column | Zoom source |
| --- | --- |
| registrants | the webinar registrants list (status approved) |
| attended, join time, minutes | the webinar attendance or participants report |
| questions asked | the Q&A report, or the transcript from the workspace server |
| poll answers | the poll report |

## Manual route

No tool for a column: a person exports Registration, Attendee, Q&A and
Poll reports from the Zoom web portal (Reports, Webinar) and drops them in
`data/events/snapshots/` under the name above; you merge on the registrant
id or the email hash and record that in the hand-over.

## Other vendors

Livestorm, ON24, Goldcast, Luma, Eventbrite and Bizzabo have no MCP route
in the catalog; their CSV exports map to the same columns, `source` set to
the vendor's token.
