# Event taxonomy

One row per tracked event that matters to marketing. Website events come
from PostHog on example.com; product events from the Beacon backend,
forwarded to PostHog with the workspace id.

| Event name (exact) | Means | Emitted by | Key properties |
| --- | --- | --- | --- |
| `$pageview` | A page loaded on example.com | PostHog web snippet | `$current_url`, `$referrer`, `utm_*` |
| `cta_clicked` | A click on a "Start free" or "Book a demo" button | PostHog web snippet | `cta` (`start_free`, `book_demo`), `location` (page section) |
| `signed_up` | A workspace was created and its email verified; the Signup in `metrics.md` | Beacon backend | `workspace_id`, `plan`, `initial_referrer`, `first_utm_campaign`, `first_utm_content` |
| `update_published` | An incident update went out to at least one channel | Beacon backend | `workspace_id`, `first` (true on the workspace's first), `channels`, `segment_count` |
| `demo_requested` | The demo form was submitted | HubSpot form, mirrored to PostHog | `form_id`, `page_path`, `company_size` |
| `attended_event` | Joined a live webinar for 10 minutes or more; registering is not attending | HubSpot list from Zoom | `event_slug`, `minutes_watched` |

The conversion event in web reports is `signed_up`; `demo_requested`
counts as a conversion too, never twice for the same workspace.

## Marketing events (webinars, conferences)

Attendee lists land in `data/events/snapshots/` as
`YYYY-MM-DD-zoom-<event-slug>-attendees.csv`, dated the day of the event;
the public copy of this repo holds counts per segment, never names. Zoom
syncs registrants and attendees to a HubSpot list per event, which links
attendance to contacts by email. "Attended then signed up" means an
`attended_event` contact whose `signed_up` falls within 30 days after the
event, matched by email in HubSpot. The first event measured this way is
the 2026-11-12 webinar.
