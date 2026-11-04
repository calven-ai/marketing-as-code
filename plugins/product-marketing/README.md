# Product marketing skills for Claude

Standalone skills for the work product marketers do every week: competitive
intelligence, market research, ICP and personas, positioning and messaging,
product intelligence, customer voice and win/loss. Each one runs in the
Claude app with nothing else installed: no repository, no folder structure,
no setup interview. You give it your materials, a CRM export or a list of
competitors, and it returns a document you can paste into your own docs.

They come from the prompts behind [Calven](https://calven.ai)'s product
agents. We kept the method (the rubrics, the severity scales, the evidence
rules and the verification passes) and removed everything tied to our
product. Every example uses Beacon, the fictional company in
[`examples/`](../../examples/README.md).

## Install

**In the Claude app** (claude.ai or the desktop app):

1. Download a skill's ZIP from the table below (the `.zip` link).
2. Open Customize > Skills, choose upload, and pick the ZIP. Code execution
   must be on in your settings.
3. On a Team or Enterprise plan, share it with colleagues or publish it to
   your organization from the same page.

Claude picks a skill when your request matches its description, or when you
name it: "use the battlecard skill for Northstar".

**In Claude Code:**

```
/plugin install product-marketing --marketplace calven-ai/marketing-as-code
```

**Run on a schedule:** a Claude scheduled task can call any of them. Write
the task as you would brief a colleague: which skill, which competitors or
files, and where the result goes. `competitor-changes` is built for a weekly
run.

## Before your team relies on them

- **Read each skill before you run it.** It is a page of plain instructions.
  Change what does not fit how your team works.
- **Give it your context.** The skills ask for your positioning, ICP and
  voice and work without them, but the output is generic until they have
  them. `company-profile` and `readiness-check` are the place to start.
- **Test it on a case you know.** Run a battlecard for a competitor you know
  well and check every claim before anyone in sales sees one.
- **Retest when the model changes.** The same skill behaves differently on a
  new model.

What a skill does not give you: sources collected on a schedule into one
shared, approved knowledge base; a change in positioning carried into every
asset that depends on it; evals that catch a skill getting worse; review
gates before anything reaches sales. That is the difference between a skill
and an agent product, and it is what [Calven](https://calven.ai) is for.

## The skills

<!-- generated:plugin-product-marketing -->
### Foundations

| Skill | What it does | Claude app |
| --- | --- | --- |
| [company-profile](skills/company-profile/SKILL.md) | A sourced company profile from its website (what it sells, to whom, business model, products, proof) as a shared fact base | [company-profile.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/company-profile.zip) |
| [readiness-check](skills/readiness-check/SKILL.md) | Grades the positioning, messaging, ICP and personas you already have and says what is solid, thin or missing, and which skill fills each gap | [readiness-check.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/readiness-check.zip) |

### Competitive intelligence

| Skill | What it does | Claude app |
| --- | --- | --- |
| [battlecard](skills/battlecard/SKILL.md) | Writes a sales battlecard for one competitor with strengths to concede, weaknesses to attack, how we win, traps, objections, talk track, proof | [battlecard.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/battlecard.zip) |
| [battlecard-refresh](skills/battlecard-refresh/SKILL.md) | Updates an existing battlecard with new evidence, keeping what is still true and marking each change with its reason and source | [battlecard-refresh.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/battlecard-refresh.zip) |
| [comparison-page](skills/comparison-page/SKILL.md) | Writes a fair "us vs X" or "X alternatives" web page from a battlecard and public evidence, honest about where X fits better | [comparison-page.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/comparison-page.zip) |
| [competitive-deals](skills/competitive-deals/SKILL.md) | Win rate, cycle length and loss stage by competitor from a CRM export or connected CRM, with sample sizes stated and nothing estimated | [competitive-deals.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/competitive-deals.zip) |
| [competitor-changes](skills/competitor-changes/SKILL.md) | Weekly digest of what changed at your competitors, with verified moves rated by severity, what they mean, what to do | [competitor-changes.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/competitor-changes.zip) |
| [competitor-deep-dive](skills/competitor-deep-dive/SKILL.md) | Sourced deep dive on one competitor covering pricing, positioning, product, trust, legal, press, market activity, strengths, weaknesses | [competitor-deep-dive.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/competitor-deep-dive.zip) |
| [competitor-document-analysis](skills/competitor-document-analysis/SKILL.md) | Analyzes a competitor's deck, datasheet, pricing sheet or analyst note for claims, pricing, positioning, weak spots and what to do | [competitor-document-analysis.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/competitor-document-analysis.zip) |
| [competitor-mentions-in-calls](skills/competitor-mentions-in-calls/SKILL.md) | Pulls each competitor mention from call transcripts, verbatim, with speaker role, context and sentiment, rolled up by competitor | [competitor-mentions-in-calls.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/competitor-mentions-in-calls.zip) |
| [find-competitors](skills/find-competitors/SKILL.md) | Finds and tiers a company's direct, indirect and emerging competitors from its site and web search, each with why it competes and evidence | [find-competitors.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/find-competitors.zip) |
| [new-entrant-scan](skills/new-entrant-scan/SKILL.md) | Scans a category for new entrants (funding, launches, hiring, reviews), drop the noise, and name the few to watch and why | [new-entrant-scan.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/new-entrant-scan.zip) |

### Market research

| Skill | What it does | Claude app |
| --- | --- | --- |
| [analyst-report-digest](skills/analyst-report-digest/SKILL.md) | Digests an analyst report (Gartner, Forrester, IDC) into page-cited findings on the market, vendors, buyers and what to do | [analyst-report-digest.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/analyst-report-digest.zip) |
| [market-opportunities](skills/market-opportunities/SKILL.md) | Finds market opportunities (segments, messages, counters, pricing plays), each tested against evidence and your own site before you act | [market-opportunities.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/market-opportunities.zip) |
| [market-research-report](skills/market-research-report/SKILL.md) | Writes a sourced market research report on a company's category (size signals, segments, buyers, forces, competitor moves) and what it means | [market-research-report.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/market-research-report.zip) |
| [market-trends](skills/market-trends/SKILL.md) | Finds and rates the trends shaping a category, or checks one trend you name, with evidence, severity, horizon and what it means for you | [market-trends.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/market-trends.zip) |
| [vertical-analysis](skills/vertical-analysis/SKILL.md) | Maps the industry verticals in a market, ranks the ones your product fits with evidence, and says what each needs in messaging | [vertical-analysis.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/vertical-analysis.zip) |

### ICP and personas

| Skill | What it does | Claude app |
| --- | --- | --- |
| [account-enrichment](skills/account-enrichment/SKILL.md) | Enriches an account list (CSV) with firmographics, tech stack and triggers from public web data, each value sourced and dated, unknowns blank | [account-enrichment.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/account-enrichment.zip) |
| [icp-from-materials](skills/icp-from-materials/SKILL.md) | Writes a cited ideal customer profile (firmographics, triggers, tiers, disqualifiers, fit scorecard) from your decks, win stories, CRM exports and website | [icp-from-materials.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/icp-from-materials.zip) |
| [icp-scorecard](skills/icp-scorecard/SKILL.md) | Turns your ICP into a weighted fit scorecard (dimensions, weights totalling 100, value levels, tiers) and scores an account list with it | [icp-scorecard.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/icp-scorecard.zip) |
| [persona-research](skills/persona-research/SKILL.md) | Builds a cited buyer persona (role, buying role, goals, pains, objections, words they use) from interviews, materials and public research | [persona-research.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/persona-research.zip) |
| [persona-review](skills/persona-review/SKILL.md) | Audits personas for gaps, stereotypes, unsupported claims and missing evidence, with severity-rated findings and sourced fixes | [persona-review.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/persona-review.zip) |

### Positioning and messaging

| Skill | What it does | Claude app |
| --- | --- | --- |
| [ai-answer-audit](skills/ai-answer-audit/SKILL.md) | Audits how ChatGPT, Claude, Gemini and Perplexity describe your company and whether they name you for buyer questions | [ai-answer-audit.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/ai-answer-audit.zip) |
| [category-reading](skills/category-reading/SKILL.md) | Reads how buyers, analysts, competitors and AI assistants name your category, finds the consensus label, and recommends claim, reframe or create | [category-reading.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/category-reading.zip) |
| [messaging-drift-audit](skills/messaging-drift-audit/SKILL.md) | Audits pages, decks and profiles against approved messaging (what drifted or is off-strategy, which messages appear where), scored with fixes | [messaging-drift-audit.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/messaging-drift-audit.zip) |
| [messaging-framework](skills/messaging-framework/SKILL.md) | Derives a messaging framework from positioning (value proposition, pillars with proof, messages per persona and stage, words to use and avoid) | [messaging-framework.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/messaging-framework.zip) |
| [positioning-framework](skills/positioning-framework/SKILL.md) | Writes a positioning doc (target customer, alternatives, unique attributes, value, category, proof) from your materials, each choice justified | [positioning-framework.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/positioning-framework.zip) |

### Product intelligence

| Skill | What it does | Claude app |
| --- | --- | --- |
| [product-change-impact](skills/product-change-impact/SKILL.md) | Rates a release, changelog or pricing change (ours or a competitor's) by severity and lists the assets to update | [product-change-impact.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/product-change-impact.zip) |
| [product-profile](skills/product-profile/SKILL.md) | A sourced product profile (what it does, for whom, capabilities, integrations, pricing, proof) from site, docs and decks | [product-profile.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/product-profile.zip) |

### Customer voice and win/loss

| Skill | What it does | Claude app |
| --- | --- | --- |
| [deal-summary](skills/deal-summary/SKILL.md) | Writes a win/loss summary of one deal from its calls, emails and CRM notes, covering who decided, why, the rival and turning points | [deal-summary.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/deal-summary.zip) |
| [loss-drivers](skills/loss-drivers/SKILL.md) | Finds why deals are won and lost across many deals, labeled in a stable driver taxonomy and counted with the sample stated | [loss-drivers.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/loss-drivers.zip) |
| [quote-extraction](skills/quote-extraction/SKILL.md) | Pulls verbatim customer quotes from call transcripts or surveys by speaker role and category, scored for marketing use and anchored | [quote-extraction.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/quote-extraction.zip) |
| [theme-synthesis](skills/theme-synthesis/SKILL.md) | Groups many customer quotes or transcripts into named, counted themes with representative verbatim quotes and the sample stated | [theme-synthesis.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/theme-synthesis.zip) |
| [win-loss-interview-guide](skills/win-loss-interview-guide/SKILL.md) | Drafts a non-leading win/loss interview guide or survey for a won or lost buyer, with answer formats and follow-up probes | [win-loss-interview-guide.zip](https://github.com/calven-ai/marketing-as-code/releases/latest/download/win-loss-interview-guide.zip) |
<!-- /generated:plugin-product-marketing -->

## Contributing

Each skill is one folder in `skills/`: a `SKILL.md` and, where the method is
long, a `references/` folder. The check holds them to what the Claude app
accepts (a description of at most 200 characters, nothing outside the skill
folder); `python3 scripts/lint.py --fix` regenerates the table above. See
[CONTRIBUTING.md](../../CONTRIBUTING.md).

MIT licensed, like the rest of this repository. The win/loss driver
taxonomy and interview questions adapt NEON-Rutger's MIT-licensed
win-loss-program skill; the files carry their source on line one and in
[THIRD_PARTY.md](../../THIRD_PARTY.md).
