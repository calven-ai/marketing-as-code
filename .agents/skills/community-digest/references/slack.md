# Slack community workspace (source token `slack`; category `community`)

A community that lives in Slack is a second workspace, separate from the
team's own. It is read through the `chat` category's Slack MCP server
(`https://mcp.slack.com/mcp`, OAuth as the person's user in that
workspace; `integrations/catalog/chat.json`), wired once per workspace. A
workspace admin has to approve the app. The bot in `integrations/slack/`
posts to the team's own workspace only; it neither reads nor posts in the
community, and this skill never posts there either.

## Tools

Tool names are not verified in the catalog; check the server's tool list
in the session. Expect: search messages, list or read a channel's
history, read a thread's replies, read a user profile. Use search with a
date qualifier (`after:YYYY-MM-DD`) to find the week's threads, then the
channel history for anything search missed, then thread reads only for
the threads that need classifying. Never call a send, react or edit tool.

## Mapping to the threads snapshot

| Column | From |
| --- | --- |
| `thread_id` | the parent message's `ts` |
| `date` | the parent message's timestamp, as a date |
| `channel` | the channel name |
| `title` | the first line of the parent message, cut to about 80 characters, with any handle or email removed |
| `replies` | `reply_count` on the parent |
| `views` | empty; Slack has none |
| `answered` | yes when a reply comes from a member of the team's staff group or the parent carries the solved reaction the community uses; else no |
| `last_reply` | `latest_reply` as a date |
| `url` | the message permalink |

Staff membership is a list the team keeps (a user group name or a short
list in the project brief); ask once, never infer from a display name.

## Limits and cost

- Search returns pages of 20 to 100; history calls page by cursor. A
  workspace with ten active channels costs on the order of 30 to 60
  calls for a week.
- Rate limits are per method tier (roughly one to several calls per
  second); back off on 429.
- Free workspaces keep 90 days of history; a digest older than that has
  a gap, say so.
- Cost: included in the plan; the MCP server needs the workspace admin's
  approval, not a paid tier.

## Export fallback

Workspace Settings > Import and export data > Export (an admin; public
channels as JSON per channel and day), or the channel's messages copied
to a CSV by hand for a small community. A person turns it into the
columns above at `data/social/snapshots/YYYY-MM-DD-slack-threads.csv`,
stripping user ids and text.
