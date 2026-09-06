# scripts/

**Kind:** code, deterministic scripts and throwaway prototypes the agent writes.

Deterministic, non-AI code. Skills call these instead of reimplementing
them. Python 3.9 or newer, standard library only unless a script says
otherwise. The table is generated from each script's docstring, or the
comment block at the top of a shell script (`python3 scripts/lint.py --fix`
refreshes it). Edit the docstring, not the table.

<!-- generated:scripts -->
| Script | What it does |
| --- | --- |
| [_common.py](_common.py) | Shared helpers for the scripts in this folder. Standard library only. |
| [_lifecycle.py](_lifecycle.py) | Shared pieces of the marketer's lifecycle (scripts/sync.py and scripts/propose.py): where a checkout stands, its proposals on GitHub in plain words, and the outcome a proposal will have. Standard library only; git and gh through scripts/_common.py. |
| [doctor.py](doctor.py) | Health check for a marketing-as-code checkout: runs every check in scripts/lint.py against docs/schema.json, then reports unfilled templates, context files past their review date, whether an .env exists, and whether this machine is ready to propose (git, your name, the pre-push hook, the GitHub CLI and its login). --fix applies the safe fixes first, turns the hook on and sets your name from your GitHub login; --strict fails on warnings too (CI on main); --brief prints three lines for the session-start hook; --github checks the repository settings through gh. Exit 1 only on real breakage. |
| [github_setup.sh](github_setup.sh) | Apply the GitHub repository settings this repo's lifecycle assumes (docs/github-settings.md). Idempotent: run it again any time. Needs the gh CLI logged in as someone who administers the repository. |
| [hooks/pre-push](hooks/pre-push) | Refuses a push straight to main and runs the lint before any push. |
| [lint.py](lint.py) | Deterministic checks for everything docs/schema.json says is valid: frontmatter, naming, file placement, CSV headers, links, secrets, the generated README tables. --fix applies the safe fixes; --strict, --format github, --json, --file and --classify serve CI, hooks and skills. |
| [propose.py](propose.py) | Propose: turn what changed in this checkout into a proposal (a pull request) and hand back the link. Checks the files first and fixes what is safe, refuses on real problems with nothing committed, commits, pushes the branch, opens or updates the proposal from the template, and says what happens next: bookkeeping merges itself, needs-review waits for a person. Never pushes to the approved copy, never force-pushes, never merges. |
| [pull_transcripts.py](pull_transcripts.py) | Pull new Granola meeting transcripts into memory/transcripts/inbox/, one Markdown file per meeting in the inbox contract (memory/transcripts/README.md); skips anything already in inbox/ or processed/. Options: --since YYYY-MM-DD, --limit N, --dry-run. Needs GRANOLA_API_KEY (environment or .env). Also run daily by .github/workflows/transcripts-cron.yml, which opens a PR with what landed. |
| [review_gate.py](review_gate.py) | The review gate: run from main by gate.yml after every check run, never from the proposal. Classifies a proposal as bookkeeping (agent-maintained files only, per docs/schema.json plus the hard-coded never-bookkeeping list in scripts/lint.py) or needs-review, applies the safe fixes as a Tidy commit, labels it, publishes the `review-gate` check on its head commit, and merges a bookkeeping proposal itself once the health check succeeded on that exact commit. A needs-review proposal passes only when a person other than the author has approved it (a bot's approval never counts), unless docs/schema.json sets review.self_merge (one maintainer): then the author's own merge is the approval. A proposal from a fork, or one an agent opened unattended (transcripts-process.yml, role-run.yml), is needs-review whatever files it touches. |
| [role_env.py](role_env.py) | Hand a role run the keys its MCP servers need, and nothing else: reads the run's MCP config (the --subset output of scripts/wire_integration.py), finds every ${VAR} placeholder in it, takes each value from the ALL_SECRETS JSON that .github/workflows/role-run.yml passes in, masks it in the log, and appends VAR=value to the file GITHUB_ENV names. A placeholder with no secret behind it is reported by name so the run fails early. Never prints a value, never reads .env. |
| [seo_snapshot.py](seo_snapshot.py) | Pull search volume and keyword difficulty for every row of data/seo/keywords.csv from DataForSEO and save data/seo/snapshots/YYYY-MM-DD-dataforseo-volume.csv. --update also refreshes volume, difficulty and last_checked in the canonical table; --dry-run lists what would be pulled. Needs DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD (environment or .env). Standard library only. |
| [slack_post.py](slack_post.py) | Post a message as the team's Slack bot (integrations/slack/). --channel team\|requests\|leadership\|<id>, text from --text or stdin, --thread <ts> to reply in a thread, --dry-run to print the payload. Needs SLACK_BOT_TOKEN plus the channel ID variables. |
| [sync.py](sync.py) | Sync: bring the latest approved copy into this checkout, tidy up, and say where you are and what is waiting on you. The first thing to say in a session and the way to look again while a proposal is checking. Never pushes, never merges a proposal, never touches the approved copy on GitHub. |
| [sync_skills.py](sync_skills.py) | Keep .claude/skills/ symlinks pointing at the canonical .agents/skills/ definitions; --check reports drift without fixing it (used by CI). |
| [test_lifecycle.py](test_lifecycle.py) | Tests for scripts/sync.py and scripts/propose.py: a real git repository per test with a local bare "origin" that answers to a github.com URL, and a fake `gh` on PATH that logs every call and answers from canned JSON. |
| [test_lint.py](test_lint.py) | Tests for scripts/lint.py: one fixture repo per test, one test per check. |
| [test_pull_transcripts.py](test_pull_transcripts.py) | Tests for the parts of scripts/pull_transcripts.py that turn API output into filenames: what the provider sends is data, and none of it may choose a path outside memory/transcripts/inbox/. No network. |
| [test_sync_skills.py](test_sync_skills.py) | Tests for scripts/sync_skills.py: a throwaway checkout per test. The script is part of the gate's trust boundary (scripts/lint.py runs main's copy against a proposal's worktree through --root), so its behaviour is pinned here. |
| [test_wire_integration.py](test_wire_integration.py) | Tests for scripts/wire_integration.py: a temp checkout with a two-category catalog per test, never the live catalog. |
| [wire_integration.py](wire_integration.py) | Wire a catalog vendor into this repo: read integrations/catalog/, write the MCP entry into .mcp.json and .cursor/mcp.json, add the missing variable names to .env.example, deny the vendor's write tools in .claude/settings.json, record the binding in integrations/wired.json, and print the Codex TOML plus the docs/secrets.md row. --list shows every category with its wired vendor, --category the routes of one, --unwire removes a vendor, --subset --stdout prints a filtered .mcp.json for an unattended run. Standard library only. |
| [with_env.sh](with_env.sh) | Start a command with the keys from .env in its environment, so the MCP servers in .mcp.json (which read ${VAR} placeholders from the environment, not from .env) find them. The usual command is your coding agent. |
<!-- /generated:scripts -->

Run from the repo root: `python3 scripts/doctor.py`.

## Running the tests

```
python3 -m unittest discover -s scripts -p 'test_*.py'
```

About twenty-five seconds; every `scripts/test_*.py` file. The check on
GitHub runs the same command before it runs the lint, so a broken check
never guards a proposal.

Scripts are the only code in this repo allowed to open `.env`. They read
the keys they need and never print them. Agents read the variable names
from `integrations/README.md` instead.
