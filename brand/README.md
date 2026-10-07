# brand/

**Kind:** context, what the team knows.

How we sound and how we look. Any agent producing something an outsider will
see (a draft, an email, a prototype, an image) loads this folder first.

## What is authoritative here

| Path | Owns |
| --- | --- |
| [voice.md](voice.md) | Voice and tone: how we write, with do/don't examples |
| [visual-identity.md](visual-identity.md) | Colors, typography, imagery rules, logo usage |
| [tokens.json](tokens.json) | The machine-readable subset (colors, fonts, logo paths) that scripts and the prototype builder read |
| [image-rules.md](image-rules.md) | What goes into a rendered banner, post or icon: copy, sizing, safe areas |
| `logos/` | Logo files (SVG preferred) |
| `templates/` | Image templates and the size registry that `scripts/brand_render.py` renders |
| `screenshots/` | Product screenshots the templates may use |
| `library/` | The brand library: open `library/index.html` in a browser for logos, color and type, banners, social posts and screenshots, with live template previews. `python3 scripts/brand_render.py book` regenerates its data (`library.js`) after a change; `library/samples.json` holds the sample copy |

## Rules

- This is the **one sanctioned binary zone** in the repo (logos, fonts,
  screenshots). Everywhere else, plain text first. Rendered images go to
  the gitignored `renders/`.
- `tokens.json` and `visual-identity.md` must agree. When the identity
  changes, update both in the same commit.
- Voice questions are settled by `voice.md`, not by taste. If it doesn't
  cover a case, propose an addition instead of improvising.
- `voice.md` and `visual-identity.md` carry `last_reviewed` in their
  frontmatter, and `scripts/doctor.py` flags them after 90 days. Voice is
  not served by a context layer
  ([integrations/context-layer.md](../integrations/context-layer.md)). It
  stays here, and the team owns it.
