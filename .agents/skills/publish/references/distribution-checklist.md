# Distribution checklist

Written for this repo. Copy into the piece's `brief.md` under a
"Distribution" heading, tick as a person completes each step, and file
the owned rows as tasks per `integrations/tasks.md`.

## Before it goes live

- [ ] `review` verdict "ready for human review" recorded in the folder
- [ ] A person has approved the final draft
- [ ] Every internal link carries UTMs that pass `data/ontology/naming.md`
- [ ] Title, meta description, slug and social image set in the CMS draft
- [ ] Canonical URL correct when the piece also appears elsewhere
- [ ] Two or three links from existing pieces planned, with the anchor
      text and the source paths (`content-inventory` finds them)

## The day it goes live (owner per row)

- [ ] CMS entry published by a person; `published_url` given back
- [ ] Frontmatter change proposed: `status: published`, `published`,
      `published_url`
- [ ] Internal links added on the source pages
- [ ] LinkedIn post staged, then activated by a person
- [ ] X thread staged, then activated by a person
- [ ] Newsletter mention queued for the next send
- [ ] Advocacy pack (`content/<x>/advocacy.md`) sent to the team
- [ ] Community or partner channels that fit, without cross-posting the
      same text

## The weeks after

- [ ] Day 7: first `web-analyst` snapshot read for this URL
- [ ] Day 30: page performance in the monthly report; refresh brief if
      it decays
- [ ] Reshare date set for evergreen pieces (three to six months)

## What "staged" means per tool

| Tool | Staged object | Who makes it live |
| --- | --- | --- |
| CMS | a draft entry with a preview link | the site owner, in the CMS |
| Scheduling tool | an unpublished or draft post with a proposed time | the channel owner, in the tool |
| Email tool | a draft campaign, no send | the email owner, in the tool |

A skill creates the left column and stops. If a tool has no draft
state, the text goes into this checklist and a person pastes it.

## What can go wrong

- The URL changes after the frontmatter is set: propose a second
  change; never edit a merged snapshot of the truth by hand.
- The piece is published without a date: the check refuses it; add the
  date in the same proposal.
- Two people stage the same post: say the object id when you stage, so
  duplicates are visible.
