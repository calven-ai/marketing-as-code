---
name: new-content
description: Scaffold a new piece of content in content/. Use when asked to start, draft, or create a blog post, email, LinkedIn post, case study, webinar asset, or any content piece. Creates the folder, brief, and draft skeleton with wired frontmatter.
---

# New content piece

## Procedure

1. **Load context**: `strategy/` (positioning, messaging, personas) and
   `brand/voice.md`. If they're unfilled templates, stop and suggest
   `/setup`.
2. **Pin down the piece**: working title, channel, owner, and the project it
   belongs to (check `projects/` — if none fits, ask whether this is
   standalone or needs a `new-project` first).
3. **Create the folder**: `content/YYYY-MM-<slug>/` copied from
   `content/_template/` — fill the brief properly (the argument section is
   the work: derive it from the messaging pillars, don't leave placeholders),
   and wire the draft frontmatter (`project`, `status: brief`, `channel`,
   `owner`).
4. **Cross-link**: add the piece to the owning project's brief under
   Deliverables (path + status).
5. **Stop at the brief** unless asked to draft. The brief is the reviewable
   unit — offer to draft once the human has glanced at it.

## Rules

- If SEO-driven, check `data/seo/keywords.csv` for the target keyword; if
  it's not tracked, note that in the brief rather than silently adding it.
- Drafting later: follow the brief's argument, write in `brand/voice.md`
  voice, and run `review` before proposing `status: in-review`.
