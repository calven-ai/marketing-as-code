<!-- source: https://raw.githubusercontent.com/thatrebeccarae/claude-marketing/main/agents/gtm-implementer/README.md | license: MIT | fetched: 2026-09-04 -->

# Handing a tag-manager change over safely

This skill never touches the tag manager; the ticket it writes has to
let a person (or the team's own automation) make the change without
breaking tracking. These are the rules the ticket encodes.

## What the ticket contains

For every event in the gap list: the event name from the taxonomy; the
data-layer variables it reads (name, type, example value); the trigger
(the data-layer event or the DOM condition, and where on the site it
fires); the tag (destination, measurement id, the event parameters and
which variable fills each); the priority.

Resources go in dependency order: variables, then triggers, then tags.
Name everything after the taxonomy event so the container stays
searchable (`var - demo_requested - plan`, `trg - demo_requested`,
`tag - ga4 - demo_requested`).

## Safety rules

- Work in a named workspace, never the default one: `agent-<purpose>-<date>`
  or the team's own pattern. The free tier allows three workspaces; a
  full account blocks the change, so check first.
- Nobody publishes from a ticket. A person reviews the workspace diff and
  publishes in the tag manager UI; the account used for automation lacks
  publish rights on purpose.
- Idempotent: check for an existing resource by name and reuse it rather
  than creating a duplicate; duplicates fire twice.
- Server-side containers are a different object model; a ticket written
  for a web container does not apply, say so.
- Rate limit API writes (the vendor's tooling waits about four seconds
  between calls); a burst of creates gets throttled and half-applied.
- Consent: where consent mode applies (EU and UK visitors), every new tag
  states which consent type gates it; unaudited consent wiring is a
  release blocker, not a follow-up.

## A useful extra: AI referrals

When the taxonomy tracks AI answer-engine traffic (the `brand-monitor`
skill covers the mention side), the implementation is one variable that
matches the referrer domain against the assistants' domains (ChatGPT,
Claude, Perplexity, Gemini, Copilot and the rest), one pageview trigger
on that match, and one event tag (`ai_referral`, with the matched domain
as a parameter). Skip it when the taxonomy already defines the event.

## Acceptance

The ticket is done when the event appears in the tool's debug view with
every property filled, once per action, and the next `tracking-spec`
audit shows no gap for it.
