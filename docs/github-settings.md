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
| Allow auto-merge | Kept on so a person can click "merge when ready" on a proposal that is still checking |
| Allow "update branch" | The button that brings a proposal up to date with the approved copy, no terminal |
| Workflow token read-only by default; Actions may not approve pull requests | A workflow gets write access only where a job asks for it, and no automation can approve a proposal on a person's behalf |
| Environment `automation`, restricted to `main` | The three bot keys live here ([secrets.md](secrets.md)); only a job running on the approved copy can read them |
| Labels `bookkeeping`, `needs-review`, `stale` | The gate labels every proposal; the housekeeping cron marks stale ones |
| Ruleset `main` | A proposal is the only way onto the approved copy: pull request required, review from the code owner of any machinery path, the `doctor` and `review-gate` checks green, no deleting or force-pushing the branch. Repository admins can bypass it in an emergency |

`.github/CODEOWNERS` names who is asked to review each area. Replace the
placeholder with real handles; `/setup` does it during onboarding. Until
then the code-owner rule has nobody to ask and stays silent.

## How a proposal lands

Two workflows share the work, and the split is the security model:

- **`check.yml`** runs on every proposal and executes the proposal's own
  code (its tests, its lint). It is untrusted by design: read-only token,
  no secrets, cannot merge, push or label. It reports, in annotations and
  one sticky comment.
- **`gate.yml`** runs from `main` after every check run, never from the
  proposal, so a proposal cannot change the rules it is judged by. It
  classifies the proposal (bookkeeping or needs-review, per
  `docs/schema.json`; anything touching `.github/`, `scripts/`,
  `docs/schema.json`, the agent settings or the skills is never
  bookkeeping), pushes the safe fixes as a Tidy commit, publishes the
  `review-gate` check, and merges a bookkeeping proposal itself only when
  the health check passed on that exact commit. A needs-review proposal
  passes only once someone other than the author has approved it.

The `review-gate` check is published by the gate through the Checks API,
which is why it must run on GitHub: run locally,
`python3 scripts/review_gate.py --pr N --dry-run` only says what it would
do.

## The plan question, plainly

Rulesets and environment branch rules are **enforced** on public
repositories on every plan, and on private repositories under **GitHub
Pro** (personal accounts) or **GitHub Team** (organizations). On a
**private repository under GitHub Free**, the ruleset and the environment
are created but show "not enforced": nothing stops someone from pushing
straight to the approved copy or merging a red proposal, and a workflow
on any branch could read the bot keys.

This repository holds transcripts and strategy, so it should be private.
That makes Team (or Pro) the plan this template assumes: it is what turns
"humans decide" from a habit into a rule. Team is priced per seat and the
marketing team is small; it is the cheapest line item in the whole setup.

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
gate's classification, and a weekly housekeeping proposal. It works for a
careful team of two that runs no automation with keys. Upgrade the day a
third person joins, the first time somebody merges red by accident, or
before you put a bot key in the `automation` environment.

## Secrets for the optional automations

**Settings → Environments → `automation` → Environment secrets.** None are
needed for the deterministic checks. [secrets.md](secrets.md) explains who
owns each key and why they live here and not under "Secrets and variables".

| Secret or variable | Where | Turns on |
| --- | --- | --- |
| `GRANOLA_API_KEY` | environment `automation` | the daily transcript pull (`transcripts-cron.yml`) |
| `ANTHROPIC_API_KEY` | environment `automation` | the agent in Actions that processes the inbox (`transcripts-process.yml`) |
| `SLACK_BOT_TOKEN` | environment `automation` | a Slack message when the approved copy fails its check, and the "a proposal is waiting" pointer after the agent runs |
| `SLACK_TEAM_CHANNEL_ID`, `SLACK_LEADERSHIP_CHANNEL_ID`, `SLACK_REQUESTS_CHANNEL_ID` | Settings → Secrets and variables → Actions → **Variables** | where those messages go; not secrets |

## Secret scanning and push protection

GitHub can refuse a push that contains a key it recognizes (push
protection) and alert on any that slipped through (secret scanning). Turn
both on under **Settings → Advanced Security** (older layouts: Settings →
Code security). They are free on public repositories; on a private
repository they are part of the GitHub Secret Protection add-on, sold per
committer on the Team plan. The repo's own lint (`scripts/lint.py`,
`docs/schema.json` → `secrets.patterns`) scans every tracked file for the
common key shapes and the pre-push hook runs it before anything leaves
your machine, so the add-on is a second net, not the only one.

## Pinned actions

Every `uses:` in `.github/workflows/` is pinned to a commit SHA with the
version in a comment, so a tag that moves cannot run different code on
the team's behalf. `.github/dependabot.yml` opens a needs-review proposal
when a new release exists; that is the only way a SHA changes.

## What to click if you cannot run the script

Settings → General → Pull Requests: tick only "Allow squash merging", tick
"Always suggest updating pull request branches", "Allow auto-merge" and
"Automatically delete head branches". Settings → Actions → General →
Workflow permissions: choose "Read repository contents and packages
permissions" and untick "Allow GitHub Actions to create and approve pull
requests". Settings → Environments → New environment: name it `automation`;
under Deployment branches and tags choose "Selected branches and tags",
Add deployment branch rule, `main`; then add the three secrets under
Environment secrets. Settings → Rules → Rulesets → New branch ruleset: name
`main`, target the default branch, enable "Restrict deletions", "Block
force pushes", "Require a pull request before merging" (0 approvals, tick
"Require review from Code Owners"; the `review-gate` check carries the
rest), "Require status checks to pass" with `doctor` and `review-gate`,
and add "Repository admin" under bypass. Issues → Labels: create
`bookkeeping`, `needs-review`, `stale`.
