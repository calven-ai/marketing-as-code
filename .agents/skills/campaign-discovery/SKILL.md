---
name: campaign-discovery
description: Run discovery for a campaign idea given in one sentence. Composes the competitive angle, keyword volumes and current ranks, AI answer-engine prompt coverage, and an inventory of existing content into one report in reports/adhoc/. Use when asked to "explore a campaign", "run discovery on", "what would it take to campaign on X", or before a new-project brief is written.
metadata:
  kind: workflow
  needs: DataForSEO MCP for the data parts; works partially without
---

# Campaign discovery

One sentence in ("a campaign positioning us as the AI-native alternative
for marketing ops teams"), one discovery report out. You compose the
specialist skills; you do not decide whether the campaign happens.

Needs: `strategy/` filled (positioning, messaging, `competitive/`); the
DataForSEO MCP for the keyword and AI answer-engine parts (through
`seo-analyst` and `brand-monitor`). Without DataForSEO, run the parts that
work offline and mark the rest as gaps with the export the human could
provide.

## Procedure

1. **Frame the idea.** Restate the campaign in one line, name the persona
   from `strategy/personas.md` and the messaging pillar from
   `strategy/messaging.md` it leans on. If neither fits, that is the first
   open question.
2. **Competitive angle.** Read `strategy/competitive/` (the battlecards)
   for who competes on this idea and how they position. Ask `seo-analyst`
   for the SERP competitors on the campaign's two or three core terms, so
   the report lists both the known competitors and whoever actually owns
   the search results. Note the angle they leave open.
3. **Keywords.** Ask `seo-analyst` for volumes, difficulty, and our current
   rank for the core terms plus up to ten ideas; the pull lands in
   `data/seo/snapshots/`. Flag which terms are in `keywords.csv` already
   and which would be proposed additions.
4. **AI answer-engine coverage.** Ask `brand-monitor` to run the prompts
   in `data/seo/prompts.csv` that touch this idea (and to propose up to
   three new prompts for it). Report who is cited today and whether we are.
5. **Content inventory.** Grep `content/*/draft.md` frontmatter for
   `channel:` and `status:`, and read the titles. List what already exists
   that this campaign could reuse, refresh, or must not duplicate, grouped
   by channel with status and owner.
6. **Write the report** to
   `reports/adhoc/YYYY-MM-DD-<slug>-discovery.md` from
   `reports/_templates/report.md`, with these sections after the answer:
   competitive angle, keywords (table), AI answer-engine coverage (table),
   content inventory (by channel), **what we would need to produce** (a
   list: piece, channel, why, reuse or new), **open questions** for the
   team, and Data used with every snapshot path.

## Worked example

"Run discovery on a campaign about meeting transcripts turning into tasks
automatically."

- Framing: persona "marketing operations lead"; pillar "meetings stop
  evaporating".
- Competitive angle: two battlecards mention note-taking tools; SERP
  competitors for "meeting notes to tasks" are three note-taking apps, none
  positions on the marketing team. Open angle: the whole team's memory,
  not one person's notes.
- Keywords: "meeting transcript to action items" 1,900/mo, difficulty 34,
  we do not rank; "ai meeting notes" 40,500/mo, difficulty 71, not
  realistic. Snapshot `data/seo/snapshots/2026-09-03-dataforseo-keyword-overview.csv`.
- AI coverage: for "Which platforms turn meeting transcripts into
  decisions and tasks?" two note-taking apps are cited, we are not.
- Content inventory: one published blog post on decision logs (reuse), one
  LinkedIn draft in review (refresh), no email.
- What we would need to produce: a guide on the transcript pipeline (blog,
  new), an email to existing users (email, new), a refreshed LinkedIn post
  (reuse).
- Open questions: is the operations lead the buyer or the user; do we have
  a customer quote we can use.

## Rules

- Propose, never decide: the report ends with questions and a list, not a
  go / no-go.
- Every number traces to a snapshot; a skill you could not run is a named
  gap.
- Do not scaffold the project or any content from here; `new-project` and
  `new-content` are separate, human-triggered steps.
