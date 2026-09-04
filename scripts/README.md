# scripts/

**Kind:** code, deterministic scripts and throwaway prototypes the agent writes.

Deterministic, non-AI code. Skills call these instead of reimplementing
them. Python 3.9 or newer, standard library only unless a script says
otherwise. The table is generated from each script's docstring
(`python3 scripts/lint.py --fix` refreshes it). Edit the docstring, not the
table.

<!-- generated:scripts -->
| Script | What it does |
| --- | --- |
| [_common.py](_common.py) | Shared helpers for the scripts in this folder. Standard library only. |
| [doctor.py](doctor.py) | Health check for a marketing-as-code checkout: runs every check in scripts/lint.py against docs/schema.json, then reports unfilled templates, context files past their review date, and whether an .env exists. --fix applies the safe fixes first; --strict fails on warnings too (CI on main); --brief prints three lines for the session-start hook; --github checks the repository settings through gh. Exit 1 only on real breakage. |
| [lint.py](lint.py) | Deterministic checks for everything docs/schema.json says is valid: frontmatter, naming, file placement, CSV headers, links, secrets, the generated README tables. --fix applies the safe fixes; --strict, --format github, --json, --file and --classify serve CI, hooks and skills. |
| [pull_transcripts.py](pull_transcripts.py) | Pull new Granola meeting transcripts into memory/transcripts/inbox/, one Markdown file per meeting in the inbox contract (memory/transcripts/README.md); skips anything already in inbox/ or processed/. Options: --since YYYY-MM-DD, --limit N, --dry-run. Needs GRANOLA_API_KEY (environment or .env). Also run daily by .github/workflows/transcripts-cron.yml, which opens a PR with what landed. |
| [review_gate.py](review_gate.py) | The review gate: run from main by gate.yml after every check run, never from the proposal. Classifies a proposal as bookkeeping (agent-maintained files only, per docs/schema.json plus the hard-coded never-bookkeeping list in scripts/lint.py) or needs-review, applies the safe fixes as a Tidy commit, labels it, publishes the `review-gate` check on its head commit, and merges a bookkeeping proposal itself once the health check succeeded on that exact commit. A needs-review proposal passes only when someone other than the author has approved it, unless docs/schema.json sets review.self_merge (one maintainer): then the author's own merge is the approval. |
| [seo_snapshot.py](seo_snapshot.py) | Pull search volume and keyword difficulty for every row of data/seo/keywords.csv from DataForSEO and save data/seo/snapshots/YYYY-MM-DD-dataforseo-volume.csv. --update also refreshes volume, difficulty and last_checked in the canonical table; --dry-run lists what would be pulled. Needs DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD (environment or .env). Standard library only. |
| [slack_post.py](slack_post.py) | Post a message as the team's Slack bot (integrations/slack/). --channel team\|requests\|leadership\|<id>, text from --text or stdin, --thread <ts> to reply in a thread, --dry-run to print the payload. Needs SLACK_BOT_TOKEN plus the channel ID variables. |
| [sync_skills.py](sync_skills.py) | Keep .claude/skills/ symlinks pointing at the canonical .agents/skills/ definitions; --check reports drift without fixing it (used by CI). |
<!-- /generated:scripts -->

Run from the repo root: `python3 scripts/doctor.py`.

Scripts are the only code in this repo allowed to open `.env`. They read
the keys they need and never print them. Agents read the variable names
from `integrations/README.md` instead.
