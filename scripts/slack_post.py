#!/usr/bin/env python3
"""Post a message to Slack with the team's own bot (integrations/slack/).

Standard library only: one chat.postMessage call over urllib. Skills and
GitHub Actions call this instead of talking to Slack themselves.

Usage, from the repo root:
    python3 scripts/slack_post.py --channel team --text "Transcript processed: ..."
    echo "multi-line message" | python3 scripts/slack_post.py --channel leadership
    python3 scripts/slack_post.py --channel requests --thread 1712345678.000100 --text "Answered in the repo: ..."
    python3 scripts/slack_post.py --channel team --text "hello" --dry-run

--channel takes a name or a raw channel ID:
    team        -> SLACK_TEAM_CHANNEL_ID
    requests    -> SLACK_REQUESTS_CHANNEL_ID
    leadership  -> SLACK_LEADERSHIP_CHANNEL_ID
    C0123ABCD   -> used as-is

Configuration comes from the environment, or from a .env file at the repo
root (copied from .env.example). SLACK_BOT_TOKEN is never printed, not even
with --dry-run. Agents do not read .env; this script may.
"""

import argparse
import json
import sys
import urllib.error
import urllib.request

from _common import ENV_FILE, read_env_file, setting

API = "https://slack.com/api/chat.postMessage"

CHANNEL_VARS = {
    "team": "SLACK_TEAM_CHANNEL_ID",
    "requests": "SLACK_REQUESTS_CHANNEL_ID",
    "leadership": "SLACK_LEADERSHIP_CHANNEL_ID",
}


def resolve_channel(arg, env_file):
    if arg in CHANNEL_VARS:
        var = CHANNEL_VARS[arg]
        value = setting(var, env_file)
        if not value:
            sys.exit(f"error: {var} is not set (needed for --channel {arg}). "
                     "See integrations/slack/README.md.")
        return value
    if arg.startswith(("C", "G", "D")) and len(arg) >= 9 and arg.isalnum():
        return arg
    sys.exit(f"error: unknown channel {arg!r}. Use team, requests, leadership, "
             "or a Slack channel ID such as C0123ABCD.")


def main():
    ap = argparse.ArgumentParser(description="Post a message to Slack as the team's bot.")
    ap.add_argument("--channel", required=True,
                    help="team | requests | leadership | <channel id>")
    ap.add_argument("--text", help="message text; read from stdin when omitted")
    ap.add_argument("--thread", metavar="TS",
                    help="reply in the thread with this message timestamp")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the payload instead of sending it")
    args = ap.parse_args()

    text = args.text if args.text is not None else sys.stdin.read()
    text = text.strip()
    if not text:
        sys.exit("error: nothing to post. Pass --text or pipe the message on stdin.")

    env_file = read_env_file(ENV_FILE)
    payload = {"channel": resolve_channel(args.channel, env_file), "text": text}
    if args.thread:
        payload["thread_ts"] = args.thread

    if args.dry_run:
        print("dry run, would POST " + API)
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    token = setting("SLACK_BOT_TOKEN", env_file)
    if not token:
        sys.exit("error: SLACK_BOT_TOKEN is not set. Install the app per "
                 "integrations/slack/README.md and put the xoxb- token in .env "
                 "or the environment.")

    req = urllib.request.Request(API, data=json.dumps(payload).encode("utf-8"), headers={
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json; charset=utf-8",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read() or b"{}")
    except urllib.error.HTTPError as e:
        sys.exit(f"error: Slack returned HTTP {e.code}.")
    except urllib.error.URLError as e:
        sys.exit(f"error: could not reach Slack ({e.reason}).")

    if not body.get("ok"):
        sys.exit(f"error: Slack refused the message: {body.get('error', 'unknown error')}. "
                 "If it is not_in_channel, invite the bot to the channel first.")
    print(f"posted to {payload['channel']} (ts {body.get('ts')})")


if __name__ == "__main__":
    main()
