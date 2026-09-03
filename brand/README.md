# brand/

**Kind:** context, what the team knows.

How we sound and how we look. Any agent producing something an outsider will
see (a draft, an email, a prototype, an image) loads this folder first.

## What is authoritative here

| Path | Owns |
| --- | --- |
| [voice.md](voice.md) | Voice and tone: how we write, with do/don't examples |
| [visual-identity.md](visual-identity.md) | Colors, typography, imagery rules, logo usage |
| [tokens.json](tokens.json) | The machine-readable subset (colors, fonts) that scripts and the prototype builder read (an OG-image script is on the roadmap) |
| `logos/` | Logo files (SVG preferred) |
| `templates/` | Reusable design templates: OG-image background, social templates |

## Rules

- This is the **one sanctioned binary zone** in the repo (logos, image
  templates). Everywhere else, plain text first.
- `tokens.json` and `visual-identity.md` must agree; when the identity
  changes, update both in the same commit.
- Voice questions are settled by `voice.md`, not by taste. If it doesn't
  cover a case, propose an addition rather than improvising silently.
- `voice.md` and `visual-identity.md` carry `last_reviewed` in their
  frontmatter; `scripts/doctor.py` flags them after 90 days. Voice is not
  served by a context layer (see
  [integrations/context-layer.md](../integrations/context-layer.md)); it
  stays here and the team owns it.
