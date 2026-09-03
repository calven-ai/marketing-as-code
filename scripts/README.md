# scripts/

**Kind:** code, deterministic scripts and throwaway prototypes the agent writes.

Deterministic, non-AI code. Skills call these instead of reimplementing them.
Python 3.9 or newer, standard library only unless a script says otherwise.

| Script | What it does |
| --- | --- |
| [sync_skills.py](sync_skills.py) | Keeps `.claude/skills/` symlinks pointing at the canonical `.agents/skills/` definitions. `--check` mode (used by CI) reports drift without fixing it. |
| [doctor.py](doctor.py) | Health check: skill symlinks intact, required files present, `.mcp.json` and `.cursor/mcp.json` listing the same servers with placeholders and no values, templates still unfilled where agents would need answers, context files past their review date. Run it when something feels miswired. |
| [_common.py](_common.py) | Shared helpers every script imports: `read_env_file`, `setting` (environment first, then `.env`), `snapshot_path` (the `YYYY-MM-DD-<source>-<what>.csv` naming from `data/README.md`). A new connector copies the closest script and gets these for free. |
| [pull_transcripts.py](pull_transcripts.py) | Pulls new Granola transcripts into `memory/transcripts/inbox/`, one Markdown file per meeting in the inbox contract (`memory/transcripts/README.md`). Skips anything already in `inbox/` or `processed/`. Options: `--since YYYY-MM-DD`, `--limit N`, `--dry-run`. Needs `GRANOLA_API_KEY` (environment or `.env`). Also run daily by `.github/workflows/transcripts-cron.yml`, which opens a PR with what landed. Granola is the shipped example; a connector for another provider is a copy of this script writing the same files. |
| [slack_post.py](slack_post.py) | Posts a message as the team's Slack bot (`integrations/slack/`). `--channel team\|requests\|leadership\|<id>`, text from `--text` or stdin, `--thread <ts>` to reply in a thread, `--dry-run` to print the payload. Needs `SLACK_BOT_TOKEN` plus the channel ID variables. |
| [seo_snapshot.py](seo_snapshot.py) | Pulls search volume and keyword difficulty for every row of `data/seo/keywords.csv` from DataForSEO and saves `data/seo/snapshots/YYYY-MM-DD-dataforseo-volume.csv`. `--update` also refreshes `volume`, `difficulty`, `last_checked` in the canonical table; `--dry-run` lists what would be pulled. Needs `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD` (environment or `.env`). |
| `og_image.py` *(wave 2)* | Composes an article title over the brand background (`brand/templates/`, colors from `brand/tokens.json`). No AI involved. |

Run from the repo root: `python3 scripts/doctor.py`.

Scripts are the only code in this repo allowed to open `.env`: they read the
keys they need and never print them. Agents keep reading the variable names
from `integrations/README.md` instead.
