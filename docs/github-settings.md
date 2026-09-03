# GitHub settings: what the repository needs, and what your plan enforces

The lifecycle in [workflow.md](workflow.md) assumes a few repository
settings that cannot live in a file. This page lists them, the script that
applies them, and the one thing that depends on which GitHub plan you are
on.

## Apply them once

With the [GitHub CLI](https://cli.github.com) logged in as a repository
admin, from the repo root:

```sh
sh scripts/github_setup.sh
```

It is safe to run again. `python3 scripts/doctor.py --github` re-checks the
settings any time and says what drifted.

| Setting | Why |
| --- | --- |
| Squash merge only | Every proposal lands as one commit on the approved copy, so history reads like a changelog |
| Delete branch on merge | Old proposals do not pile up; the branch list stays empty |
| Allow auto-merge | Bookkeeping proposals (agent-maintained files only) merge themselves once the checks are green |
| Allow "update branch" | The button that brings a proposal up to date with the approved copy, no terminal |
| Labels `bookkeeping`, `needs-review`, `stale` | The check labels every proposal; the housekeeping cron marks stale ones |
| Ruleset `main` | A proposal is the only way onto the approved copy: pull request required, the `doctor` and `review-gate` checks green, no deleting or force-pushing the branch. Repository admins can bypass it in an emergency |

`.github/CODEOWNERS` names who is asked to review each area. Replace the
placeholder with real handles; `/setup` does it during onboarding.

## The plan question, plainly

Rulesets are **enforced** on public repositories on every plan, and on
private repositories under **GitHub Pro** (personal accounts) or **GitHub
Team** (organizations). On a **private repository under GitHub Free**, the
ruleset is created but shows "not enforced": nothing stops someone from
pushing straight to the approved copy or merging a red proposal.

This repository holds transcripts and strategy, so it should be private.
That makes Team (or Pro) the plan this template assumes: it is what turns
"humans decide" from a habit into a rule. Team is priced per seat and the
marketing team is small; it is the cheapest line item in the whole setup.

| | Free, private | Pro or Team, private | Any plan, public |
| --- | --- | --- | --- |
| The check runs and comments on every proposal | yes | yes | yes |
| Bookkeeping proposals merge themselves | yes | yes | yes |
| A red check blocks the merge button | no | yes | yes |
| A direct push to the approved copy is refused | only locally, by the committed pre-push hook and `/propose` | yes | yes |
| Code owners are requested automatically | no | yes | yes |

On Free, the protection is the scripts (`/sync` and `/propose` never touch
the approved copy), the committed pre-push hook, a loud check, and a weekly
housekeeping proposal. It works for a careful team of two. Upgrade the day
a third person joins, or the first time somebody merges red by accident.

## Secrets for the optional automations

Settings → Secrets and variables → Actions. None are needed for the
deterministic checks. [secrets.md](secrets.md) explains the three tiers.

| Secret or variable | Turns on |
| --- | --- |
| `GRANOLA_API_KEY` | the daily transcript pull (`transcripts-cron.yml`) |
| `ANTHROPIC_API_KEY` (or `CLAUDE_CODE_OAUTH_TOKEN`) | the agent-in-Actions workflows: transcript processing, the AI review of context changes, the weekly audit |
| `SLACK_BOT_TOKEN` + `SLACK_TEAM_CHANNEL_ID` (variable) | a Slack message instead of an issue when the approved copy fails its check |

## What to click if you cannot run the script

Settings → General → Pull Requests: tick only "Allow squash merging", tick
"Always suggest updating pull request branches", "Allow auto-merge" and
"Automatically delete head branches". Settings → Rules → Rulesets → New
branch ruleset: name `main`, target the default branch, enable "Restrict
deletions", "Block force pushes", "Require a pull request before merging"
(0 approvals; the `review-gate` check carries that), "Require status checks
to pass" with `doctor` and `review-gate`, and add "Repository admin" under
bypass. Issues → Labels: create `bookkeeping`, `needs-review`, `stale`.
