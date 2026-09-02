# scripts/

Deterministic, non-AI code. Skills call these instead of reimplementing them.
Python 3.9 or newer, standard library only unless a script says otherwise.

| Script | What it does |
| --- | --- |
| [sync_skills.py](sync_skills.py) | Keeps `.claude/skills/` symlinks pointing at the canonical `.agents/skills/` definitions. `--check` mode (used by CI) reports drift without fixing it. |
| [doctor.py](doctor.py) | Health check: skill symlinks intact, required files present, templates still unfilled where agents would need answers. Run it when something feels miswired. |
| `og_image.py` *(wave 2)* | Composes an article title over the brand background (`brand/templates/`, colors from `brand/tokens.json`). No AI involved. |
| `pull_transcripts.py` *(wave 2)* | Pulls new Granola transcripts into `memory/transcripts/inbox/`. |

Run from the repo root: `python3 scripts/doctor.py`.
