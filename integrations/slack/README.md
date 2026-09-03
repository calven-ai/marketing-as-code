# Slack: the team's front door

Slack is where a marketing team talks; this repo is where the work, the
analysis, the plans, and the memory live. The integration has three layers,
and none of them needs a server the team has to run.

| Layer | What it does | Identity | Mechanism | Status |
| --- | --- | --- | --- | --- |
| 1. Outbound bot | Morning digest, Monday leadership update, "merged and live" notices, data alerts, export asks, transcript summaries and red flags | the team's own Slack app (this folder) | `scripts/slack_post.py` called by GitHub Actions and skills, with a bot token | manifest and `slack_post.py` wired; the scheduled digests are workflows you add, calling the same script (`docs/operating-model.md`) |
| 2. Inbound intake | Reads `#marketing-requests`, answers in-thread from the repo or routes to an owner; turns Slack decisions into decision-log entries with a permalink | same bot | polling with the bot token from a scheduled run; no Events API | not shipped; a script under the contract in `integrations/adding-an-integration.md`, if the team wants it |
| 3. Ask the repo from Slack | A person mentions Claude in a thread; a Claude Code session opens on the repo, works, and posts a summary and PR link back | the person (Claude Code in Slack) or a shared org identity (Claude Tag, Team/Enterprise plans) | Anthropic's Slack app, configured by an admin; requires Claude Code on the web and a connected GitHub repo | available today, plan-dependent |

Plus the off-the-shelf GitHub Slack app for "PR awaiting your review"
notifications, which needs nothing from this repo.

Layer 1 is what this folder sets up. The point of a custom app is that
automated messages come from a bot the team created, not from anyone's
personal account, and that the only secret is one bot token.

## Install the app (workspace admin, about five minutes, no terminal)

1. Open https://api.slack.com/apps and click **Create New App**.
2. Choose **From a manifest**, pick your workspace, click **Next**.
3. Switch the editor to **YAML**, delete what is there, paste the whole of
   [`manifest.yml`](manifest.yml) (rename the app first if you like). Click
   **Next**, then **Create**. The review screen lists exactly the
   permissions in the file and nothing under "Event subscriptions" or
   "Interactivity".
4. On the app page, click **Install to Workspace** and **Allow**.
5. Copy the **Bot User OAuth Token** (starts with `xoxb-`). This is the only
   secret the app produces. Do not paste it in Slack; put it in the team's
   password manager and share it with whoever owns the repo's integrations,
   per [docs/secrets.md](../../docs/secrets.md).
6. In Slack, open the requests channel (`#marketing-requests` is the
   convention) and type `/invite @Marketing Bot`. Do the same in the team
   channel (`#marketing`) so the bot is visible there.
7. Get the channel IDs: open the channel, click its name, scroll to the
   bottom of the "About" tab; the ID looks like `C0123ABCD`. These are not
   secrets.

If the token is ever exposed, **Reinstall to Workspace** on the app page:
this issues a new token and invalidates the old one.

## What lands in the repo's configuration (repo owner, once)

| Name | What | Where | Secret? |
| --- | --- | --- | --- |
| `SLACK_BOT_TOKEN` | the `xoxb-` token from step 5 | GitHub: repo **Settings → Secrets and variables → Actions → Secrets**; locally in `.env` | yes |
| `SLACK_REQUESTS_CHANNEL_ID` | ID of the requests channel | same page, **Variables** tab; and `.env` | no |
| `SLACK_TEAM_CHANNEL_ID` | ID of the team channel | same page, **Variables** tab; and `.env` | no |
| `SLACK_LEADERSHIP_CHANNEL_ID` | ID of the leadership channel | same page, **Variables** tab; and `.env` | no |

There is no signing secret and no app-level token, because the app has no
Request URL and no Socket Mode. The four names mirror
[`.env.example`](../../.env.example) and the registry row in
[`integrations/README.md`](../README.md). Red flags found while processing
transcripts (slipped deadlines, blockers, customer escalations) go to the
leadership channel; the "Transcript processed" summary goes to the team
channel. Invite the bot to the leadership channel too.

Posting from a script or a skill:

```sh
python3 scripts/slack_post.py --channel team --text "Transcript processed: ..."
python3 scripts/slack_post.py --channel leadership --text "Red flags from 2026-09-03-weekly-sync: ..."
python3 scripts/slack_post.py --channel team --text "..." --dry-run   # prints the payload, sends nothing
```

## How the bot behaves (the contract every script and skill follows)

- **Slack is a notification and a queue, never the only copy.** Every
  message carries the repo path (and the as-of date of the file or
  snapshot) for each fact it states. A decision made in a Slack thread is
  logged in `memory/decision-log.md` with the thread permalink as its
  source, or it did not happen. This is what keeps the repo upstream of
  Slack rather than downstream of it.
- **Where:** answers go in the thread of the request, never as a new
  top-level message, so the requests channel stays a queue. Digests and
  announcements go to the team channel. Data alerts may go to a separate
  low-traffic data channel. No DMs, except opt-in task reminders to the
  task's owner.
- **Acknowledge, then answer:** an eyes reaction when a request is seen, a
  check mark when answered, a raised hand when a human is needed. A request
  with no answer after a set time becomes a task per
  [`integrations/tasks.md`](../tasks.md), with the permalink.
- **Labelled output:** each item in an answer is marked send-able (public,
  may be forwarded to a prospect) or internal (battlecards, transcripts,
  working notes).
- **Never answered by the bot without a human:** prices, discounts, or
  "sign before X"; any product, integration, compliance, or uptime claim
  not in `strategy/` or the approved-claims register; customer quotes not
  marked approved; competitor comparisons intended for a prospect in
  writing; launch dates or features beyond what the decision log records,
  and anything about pre-launch disclosure; personal data of any kind. For
  these the bot states what the repo says, mentions the owner from
  `team.md`, and stops.
- **Never:** message a customer, post outside its configured channels,
  edit `strategy/`, `brand/`, pricing, or the ontology from a Slack request
  (it opens a PR instead), or post the contents of `memory/transcripts/`.
- **Weekly:** the questions asked in the requests channel are the content
  backlog. A Friday digest (asks, answered / handed off, gaps) goes to the
  team channel and to `reports/recurring/requests/`.

## The standard messages

Written once, generated by scripts and skills, always with links. The
scheduled ones (morning, Monday, nightly, Friday) only exist if the team
runs them from GitHub Actions; the on-event ones are posted by the skill
or the person doing the work. Which mode the team uses per workflow is in
[docs/operating-model.md](../../docs/operating-model.md).

| When | Where | Message |
| --- | --- | --- |
| Every morning | team channel | Needs a human (open PRs by reviewer, unowned items), due this week, changed yesterday (merged PRs), data freshness (snapshots vs cadence), transcripts waiting in `inbox/` |
| Monday | leadership channel | The weekly update: project states and deltas, headline numbers vs `strategy/plan.md`, decisions last week, blockers |
| On merge | team channel (and sales channel when relevant) | "Live: <what changed>, source: <file>. What to tell prospects: …" for content published, strategy or pricing changed, decisions logged |
| Transcript processed | team channel | Decisions logged, project status updated, tasks filed per owner, knowledge diffs awaiting review, red flags (or "none"), items parked by instruction |
| Red flags in a transcript | leadership channel | The risks and red flags list from the same transcript, one line each, with the transcript path. Sent only when the list is not empty |
| Nightly snapshots | data channel | One success digest per run; alerts to the team channel when a metric moves beyond its threshold, a deal moves backwards, a pull fails, or a snapshot is older than its cadence |
| Friday | team channel | Requests digest and content gaps |
