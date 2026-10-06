# agents/prompts/: the prompt library

**Kind:** agents, instructions a person gives an agent.

The skills cover the work that repeats the same way every time. Most days
aren't like that. You're thirty minutes from a pipeline review, or a
competitor just repriced, or someone asks which persona the new page is
for. This library is the work between the skills: prompts and one-line
questions for each marketing team, grounded in what this repo holds.

Open your coding agent at the repo root and paste a prompt. Fill in the
FILL IN block, send, and the agent reads `strategy/`, `brand/`,
`content/`, `data/` and the rest before it answers. Keep the ones that
work as a snippet, or turn one into a skill when it settles
([docs/skill-authoring.md](../../docs/skill-authoring.md)).

It's a starting point, not a manual. Take a prompt, change it, keep the
version that works. Start with the questions at the bottom of each page to
see what the repo knows; move to the workflow prompts when a task repeats.
[prompt-patterns.md](prompt-patterns.md) explains the three flavours and how
to write your own.

Every prompt asks for the file path behind each point and for gaps to be
named, never filled. If a prompt needs data the repo doesn't hold yet, the
agent says which export to drop where. Empty templates give thin answers:
run `/setup` first.

## Teams

| Team | Use cases |
| --- | --- |
| [Product marketing](product-marketing/README.md) | [Launch messaging](product-marketing/launch-messaging.md), [Win/loss readouts](product-marketing/win-loss-readouts.md), [Competitive teardowns](product-marketing/competitive-teardowns.md), [Messaging audits](product-marketing/messaging-audits.md), [Claim checks](product-marketing/claim-checks.md), [Customer evidence packs](product-marketing/customer-evidence-packs.md) |
| [Demand generation](demand-generation/README.md) | [Campaign briefs](demand-generation/campaign-briefs.md), [Email nurtures](demand-generation/email-nurtures.md), [Paid ads](demand-generation/paid-ads.md), [ABM plays](demand-generation/abm-plays.md), [Campaign retros](demand-generation/campaign-retros.md) |
| [Content and SEO](content-and-seo/README.md) | [Content briefs](content-and-seo/content-briefs.md), [Editorial planning](content-and-seo/editorial-planning.md), [Content audit and refresh](content-and-seo/content-audit-and-refresh.md), [Comparison pages](content-and-seo/comparison-pages.md), [Answer pages](content-and-seo/answer-pages.md) |
| [Brand and communications](brand-and-communications/README.md) | [Press releases](brand-and-communications/press-releases.md), [Executive thought leadership](brand-and-communications/executive-thought-leadership.md), [Voice consistency audit](brand-and-communications/voice-consistency-audit.md), [Competitive response](brand-and-communications/competitive-response.md) |
| [Customer marketing](customer-marketing/README.md) | [Case studies](customer-marketing/case-studies.md), [References and reviews](customer-marketing/references-and-reviews.md), [Customer feedback digest](customer-marketing/customer-feedback-digest.md), [Expansion campaigns](customer-marketing/expansion-campaigns.md), [Release communications](customer-marketing/release-communications.md) |
| [Marketing operations](marketing-operations/README.md) | [Funnel and lead definitions](marketing-operations/funnel-and-lead-definitions.md), [Pipeline reporting](marketing-operations/pipeline-reporting.md), [Attribution](marketing-operations/attribution.md), [A/B tests](marketing-operations/ab-tests.md), [CRM data quality](marketing-operations/crm-data-quality.md) |
| [Marketing leadership](marketing-leadership/README.md) | [Quarterly review](marketing-leadership/quarterly-review.md), [Annual planning and OKRs](marketing-leadership/annual-planning-and-okrs.md), [Budget allocation](marketing-leadership/budget-allocation.md), [Board and exec updates](marketing-leadership/board-and-exec-updates.md), [Keeping strategy current](marketing-leadership/keeping-strategy-current.md) |

## Adding a page

One page per use case, in the team's folder: the title, a **Reads** line
(the folders it leans on and the skills that already do part of the job),
an intro paragraph, two to four workflow prompts, one or two advanced
prompts, and the questions. Every prompt has to be answerable from the repo
or a wired integration category. Add the page to its team table and to the
table above.
