# Slack: the team's front door

Slack is where a marketing team talks. This repo is where the work, the
analysis and the memory live. The integration has three layers, and none
of them needs a server.

| Layer | What it does | Mechanism | Status |
| --- | --- | --- | --- |
| 1. Outbound bot | Digests, "merged and live" notices, data alerts, transcript summaries and red flags, from the team's own Slack app | `scripts/slack_post.py` with a bot token, called by skills and GitHub Actions | manifest and script wired; scheduled digests are workflows you add |
| 2. Inbound intake | Reads the requests channel, answers in-thread from the repo, logs Slack decisions with a permalink | the same bot, polling from a scheduled run; no Events API | yours to add, as a script under the [integration guide](../adding-an-integration.md) |
| 3. Ask the repo from Slack | A person mentions Claude in a thread; a Claude Code session opens on the repo and posts a summary and PR link back | Anthropic's Slack app, configured by an admin; needs Claude Code on the web and a connected GitHub repo | plan-dependent |

The off-the-shelf GitHub Slack app covers "PR awaiting your review" and
needs nothing from this repo.

This folder sets up layer 1. Automated messages come from a bot the team
created, not from anyone's personal account, and the only secret is one bot
token.

## Install the app (workspace admin, about five minutes, no terminal)

1. Open https://api.slack.com/apps and click **Create New App**.
2. Choose **From a manifest**, pick your workspace, click **Next**.
3. Switch the editor to **YAML**, delete what is there, paste the whole of
   [`manifest.yml`](manifest.yml). Click **Next**, then **Create**. The
   review screen lists exactly the permissions in the file and nothing
   under "Event subscriptions" or "Interactivity".
4. On the app page, click **Install to Workspace** and **Allow**.
5. Copy the **Bot User OAuth Token** (starts with `xoxb-`). It is a bot key:
   it goes in the team's password manager and in the GitHub environment
   `automation`, nowhere else. Hand it to the integrations owner per
   [docs/secrets.md](../../docs/secrets.md). Never paste it in Slack.
6. In Slack, `/invite @Marketing Bot` to the requests channel
   (`#marketing-requests` by convention), the team channel (`#marketing`)
   and the leadership channel. The app cannot post in a channel it was not
   invited to, on purpose, so these three are the only places it can write.
7. Get the channel IDs: open the channel, click its name, scroll to the
   bottom of the "About" tab. The ID looks like `C0123ABCD`. Not secrets.

If the token is ever exposed, **Reinstall to Workspace** on the app page.
That issues a new token and invalidates the old one.

## What lands in the repo's configuration (repo owner, once)

| Name | What | Where | Secret? |
| --- | --- | --- | --- |
| `SLACK_BOT_TOKEN` | the `xoxb-` token from step 5 | GitHub: **Settings → Environments → `automation` → Environment secrets**; the integrations owner's `.env` for hand runs | yes |
| `SLACK_REQUESTS_CHANNEL_ID` | ID of the requests channel | same page, **Variables** tab; and `.env` | no |
| `SLACK_TEAM_CHANNEL_ID` | ID of the team channel | same page, **Variables** tab; and `.env` | no |
| `SLACK_LEADERSHIP_CHANNEL_ID` | ID of the leadership channel | same page, **Variables** tab; and `.env` | no |

No signing secret and no app-level token, because the app has no Request
URL and no Socket Mode. The four names mirror
[`.env.example`](../../.env.example) and the registry row in
[`integrations/README.md`](../README.md).

Posting from a script or a skill:

```sh
python3 scripts/slack_post.py --channel team --text "Transcript processed: ..."
python3 scripts/slack_post.py --channel leadership --text "Red flags from 2026-09-03-weekly-sync: ..."
python3 scripts/slack_post.py --channel team --text "..." --dry-run   # prints the payload, sends nothing
```

`--channel` accepts only the three configured names. A raw channel ID needs
`--allow-any-channel`, which a person passes on purpose and no workflow or
skill does.

## How the bot behaves (the contract every script and skill follows)

- **Slack is a notification and a queue, never the only copy.** Every
  message carries the repo path and as-of date for each fact it states. A
  decision made in a Slack thread is logged in `memory/decision-log.md`
  with the permalink as its source, or it did not happen.
- **Where:** answers go in the thread of the request, so the requests
  channel stays a queue. Digests go to the team channel. No DMs, except
  opt-in task reminders to a task's owner.
- **Acknowledge, then answer:** an eyes reaction when seen, a check mark
  when answered, a raised hand when a human is needed. An unanswered
  request becomes a task per [`integrations/tasks.md`](../tasks.md).
- **Labelled output:** each item is marked send-able (may reach a prospect)
  or internal (battlecards, transcripts, working notes).
- **Never answered without a human:** prices and discounts; product,
  compliance or uptime claims not in `strategy/`; unapproved customer
  quotes; written competitor comparisons for a prospect; launch dates
  beyond the decision log; personal data. The bot states what the repo
  says, names the owner, and stops.
- **Never:** message a customer, post outside its channels, edit
  `strategy/`, `brand/`, pricing or the ontology from a Slack request (it
  opens a PR instead), or post the contents of `memory/transcripts/`.
- **The requests channel is the content backlog.** A weekly digest of
  asks, answers and gaps is a workflow yours to add.

## The standard messages

Generated by scripts and skills, always with links. Two ship today, posted
by the `chief-of-staff` skill or the person doing the work. When the agent
in Actions did the processing, the unattended message is only a pointer to
the proposal; a person posts the summary after review.

| When | Where | Message |
| --- | --- | --- |
| Transcript processed | team channel | Decisions logged, project status updated, tasks filed per owner, knowledge diffs awaiting review, red flags (or "none"), items parked by instruction |
| Red flags in a transcript | leadership channel | The risks and red flags list from the same transcript, one line each, with the transcript path. Sent only when the list is not empty |

The scheduled digests (a morning "needs a human" list, a Monday leadership
update, "merged and live" notices, snapshot alerts) are yours to add as
workflows calling the same script. Which run mode the team uses is in
[docs/operating-model.md](../../docs/operating-model.md).
