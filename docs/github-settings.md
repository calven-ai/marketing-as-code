# GitHub settings: what the repository needs, and what your plan enforces

The workflow in [workflow.md](workflow.md) assumes a few repository
settings that cannot live in a file. This page lists them, the script that
applies them, and the plan that enforces them.

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
| Workflow token read-only by default; Actions may create and approve pull requests | A workflow gets write access only where a job asks for it. GitHub's one toggle covers creating and approving: housekeeping, the transcript pull and the agent runs open their proposals with the workflow token, so it stays on, and the gate ignores an approval from any `[bot]` login, so the approving half buys nothing |
| Environment `automation`, restricted to `main` | The bot keys live here ([secrets.md](secrets.md)); only a job on the approved copy can read them. A workflow that names the environment creates it, unrestricted, the first time it runs; the script restricts it, and `doctor --github` says when it is not |
| Labels `bookkeeping`, `needs-review`, `stale` | The gate labels every proposal; housekeeping marks stale ones |
| Ruleset `main` | A proposal is the only way onto the approved copy: pull request required, code-owner review for machinery paths, the `doctor` and `review-gate` checks green, no deleting or force-pushing. Admins can bypass the checks in an emergency, but only through a pull request, never with a direct push |

`.github/CODEOWNERS` names who reviews each area. Replace the placeholder
with real handles; `/setup` does it during onboarding. A repository with
one maintainer sets `review.self_merge` in `docs/schema.json` instead (or
the Actions variable `REVIEW_SELF_MERGE` to `true`, which wins over the
file), so the gate does not wait for a second person
([workflow.md](workflow.md)).

## How a proposal lands

Two workflows share the work. `check.yml` runs the proposal's own tests
with a read-only token and no secrets. `gate.yml` runs from `main`,
classifies the proposal, publishes the `review-gate` check, and merges
bookkeeping once the check is green. The full split is in
[workflow.md](workflow.md). Run locally,
`python3 scripts/review_gate.py --pr N --dry-run` only says what it would
do; the check itself is published through GitHub's Checks API.

## Private, on a plan that enforces rules

The repository is private, always (AGENTS.md, rule 8). It holds
transcripts, strategy, CRM exports and account lists; a public copy is an
incident, not a mode. `python3 scripts/doctor.py --github` warns when
GitHub says the repository is public, and `scripts/lint.py` warns when
`repo.private` in `docs/schema.json` is not `true`. The one public copy is
the template itself, which holds no transcripts and no customer data.

GitHub enforces rulesets and environment branch rules on a private
repository only under GitHub Team (organizations) or GitHub Pro (personal
accounts). That is the plan this template assumes: priced per seat, the
cheapest line item in the setup, and the plan your website repository is
most likely on already. Put the copy in that organization and the seats are
paid for. On GitHub Free the ruleset shows "not enforced", and the doctor
says so. Free is not supported: on it

- a red check does not block the merge button,
- a direct push to the approved copy is refused only by the local pre-push
  hook, which `git push --no-verify` skips,
- code owners are neither requested nor required,
- the bot keys in the `automation` environment are readable from any
  branch, so a bot key on Free is a leak waiting for a branch.

## Secrets for the optional automations

Settings → Environments → `automation` → Environment secrets. None are
needed for the deterministic checks. [secrets.md](secrets.md) says who
owns each key.

- `GRANOLA_API_KEY` turns on the daily transcript pull
  (`transcripts-cron.yml`).
- `ANTHROPIC_API_KEY` turns on the agent in Actions that processes the
  inbox (`transcripts-process.yml`) and the role runs (`role-run.yml`).
- `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD`, with the key above, turn
  on the monthly brand-monitor run (`role-brand-monitor.yml`).
- `SLACK_BOT_TOKEN` turns on the Slack message when the approved copy fails
  its check, and the "a proposal is waiting" pointer after the agent runs.
- `SLACK_TEAM_CHANNEL_ID`, `SLACK_LEADERSHIP_CHANNEL_ID` and
  `SLACK_REQUESTS_CHANNEL_ID` say where those messages go. They are
  variables, not secrets: Settings → Secrets and variables → Actions →
  Variables.

## Secret scanning and push protection

GitHub can refuse a push that contains a key it recognizes and alert on any
that slipped through. Turn both on under Settings → Advanced Security
(older layouts: Settings → Code security). On a private repository they
are part of the GitHub Secret Protection add-on, sold per committer on the
Team plan. The repo's own lint (`scripts/lint.py`)
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
   repository contents and packages permissions" and tick "Allow GitHub
   Actions to create and approve pull requests" (the workflows open their
   proposals with it; the gate counts no bot approval).
3. Settings → Environments → New environment: name it `automation`. Under
   Deployment branches and tags choose "Selected branches and tags" and
   add `main`. Add the secrets under Environment secrets.
4. Settings → Rules → Rulesets → New branch ruleset: name it `main`, target
   the default branch, enable "Restrict deletions", "Block force pushes",
   "Require a pull request before merging" (0 approvals, tick "Require
   review from Code Owners"), "Require status checks to pass" with `doctor`
   and `review-gate`, and add "Repository admin" under bypass with "For
   pull requests only".
5. Issues → Labels: create `bookkeeping`, `needs-review`, `stale`.
