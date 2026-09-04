# GitHub settings: what the repository needs, and what your plan enforces

The workflow in [workflow.md](workflow.md) assumes a few repository
settings that cannot live in a file. This page lists them, the script that
applies them, and the one thing that depends on your GitHub plan.

## Apply them once

With the [GitHub CLI](https://cli.github.com) logged in as a repository
admin, from the repo root:

```sh
sh scripts/github_setup.sh
```

Safe to run again. `python3 scripts/doctor.py --github` re-checks the
settings any time and says what drifted.

| Setting | Why |
| --- | --- |
| Squash merge only | Every proposal lands as one commit, so history reads like a changelog |
| Delete branch on merge | The branch list stays empty |
| Allow auto-merge | A person can click "merge when ready" on a proposal that is still checking |
| Allow "update branch" | The button that brings a proposal up to date, no terminal |
| Workflow token read-only by default; Actions may not approve pull requests | A workflow gets write access only where a job asks for it, and no automation approves on a person's behalf |
| Environment `automation`, restricted to `main` | The bot keys live here ([secrets.md](secrets.md)); only a job on the approved copy can read them |
| Labels `bookkeeping`, `needs-review`, `stale` | The gate labels every proposal; housekeeping marks stale ones |
| Ruleset `main` | A proposal is the only way onto the approved copy: pull request required, code-owner review for machinery paths, the `doctor` and `review-gate` checks green, no deleting or force-pushing. Admins can bypass in an emergency |

`.github/CODEOWNERS` names who reviews each area. Replace the placeholder
with real handles; `/setup` does it during onboarding.

## How a proposal lands

Two workflows share the work. `check.yml` runs the proposal's own tests
with a read-only token and no secrets. `gate.yml` runs from `main`,
classifies the proposal, publishes the `review-gate` check, and merges
bookkeeping once the check is green. The full split is in
[workflow.md](workflow.md). Run locally,
`python3 scripts/review_gate.py --pr N --dry-run` only says what it would
do; the check itself is published through GitHub's Checks API.

## The plan question

Rulesets and environment branch rules are enforced on public repositories
on every plan, and on private repositories under GitHub Pro (personal
accounts) or GitHub Team (organizations). On a private repository under
GitHub Free they exist but show "not enforced". This repository holds
transcripts and strategy, so it should be private. That makes Team or Pro
the plan this template assumes. It is priced per seat and is the cheapest
line item in the whole setup.

| | Free, private | Pro or Team, private | Any plan, public |
| --- | --- | --- | --- |
| The check runs and comments on every proposal | yes | yes | yes |
| Bookkeeping proposals merge themselves, after a green check | yes | yes | yes |
| A red check blocks the merge button | no | yes | yes |
| A direct push to the approved copy is refused | only locally, by the committed pre-push hook | yes | yes |
| Code owners are requested and required | no | yes | yes |
| The bot keys are readable only from `main` | no | yes | yes |

On Free, the protection is the pre-push hook (`git config core.hooksPath
scripts/hooks`, once per clone; the doctor reminds you), a loud check, the
gate's classification, and a weekly housekeeping proposal. That works for
a careful team of two running no automation with keys. Upgrade the day a
third person joins, the first time somebody merges red by accident, or
before you put a bot key in the `automation` environment.

## Secrets for the optional automations

Settings → Environments → `automation` → Environment secrets. None are
needed for the deterministic checks. [secrets.md](secrets.md) says who
owns each key.

- `GRANOLA_API_KEY` turns on the daily transcript pull
  (`transcripts-cron.yml`).
- `ANTHROPIC_API_KEY` turns on the agent in Actions that processes the
  inbox (`transcripts-process.yml`).
- `SLACK_BOT_TOKEN` turns on the Slack message when the approved copy fails
  its check, and the "a proposal is waiting" pointer after the agent runs.
- `SLACK_TEAM_CHANNEL_ID`, `SLACK_LEADERSHIP_CHANNEL_ID` and
  `SLACK_REQUESTS_CHANNEL_ID` say where those messages go. They are
  variables, not secrets: Settings → Secrets and variables → Actions →
  Variables.

## Secret scanning and push protection

GitHub can refuse a push that contains a key it recognizes and alert on any
that slipped through. Turn both on under Settings → Advanced Security
(older layouts: Settings → Code security). Free on public repositories; on
a private one they are part of the GitHub Secret Protection add-on, sold
per committer on the Team plan. The repo's own lint (`scripts/lint.py`)
scans every tracked file for common key shapes, and the pre-push hook runs
it before anything leaves your machine. The add-on is a second net.

## Pinned actions

Every `uses:` in `.github/workflows/` is pinned to a commit SHA with the
version in a comment, so a moved tag cannot run different code on the
team's behalf. `.github/dependabot.yml` opens a needs-review proposal when
a new release exists. That is the only way a SHA changes.

## What to click if you cannot run the script

1. Settings → General → Pull Requests: tick only "Allow squash merging",
   then "Always suggest updating pull request branches", "Allow
   auto-merge" and "Automatically delete head branches".
2. Settings → Actions → General → Workflow permissions: choose "Read
   repository contents and packages permissions" and untick "Allow GitHub
   Actions to create and approve pull requests".
3. Settings → Environments → New environment: name it `automation`. Under
   Deployment branches and tags choose "Selected branches and tags" and
   add `main`. Add the secrets under Environment secrets.
4. Settings → Rules → Rulesets → New branch ruleset: name it `main`, target
   the default branch, enable "Restrict deletions", "Block force pushes",
   "Require a pull request before merging" (0 approvals, tick "Require
   review from Code Owners"), "Require status checks to pass" with `doctor`
   and `review-gate`, and add "Repository admin" under bypass.
5. Issues → Labels: create `bookkeeping`, `needs-review`, `stale`.
