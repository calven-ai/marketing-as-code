# Case studies

**Reads:** `memory/transcripts/processed/`, `data/crm/snapshots/`
(customers and closed deals), `data/reviews/snapshots/`,
`strategy/messaging.md`, `strategy/personas.md`, `content/` (pieces with
`channel: case-study`) · **Skill:** `/case-study` writes the study and the
quote-approval checklist from a transcript; these prompts pick the
customer, prepare the interview and check the numbers.

Sales keeps asking for "a case study like them". The hard part isn't
writing it: it's picking the customer whose story covers the deals you're
losing, getting the right material out of a 45-minute interview, and making
sure every number holds up when the customer reads it. You walk away with
the right account, an interview guide and a draft you can send for
approval. Once you have the transcript, `/case-study` writes the draft.

## Prompts

### Choose the next case study customer

```
Using this repo, pick the customer whose story would help the most deals right now.

CONTEXT
We can do one case study this quarter. It should cover the segment, persona or competitor where we're short of proof.

READ FROM THE REPO
- Published and in-flight case studies in content/ (channel: case-study).
- The customer base in data/crm/snapshots/ and the segments and tiers in strategy/icp.md.
- Open and recently lost deals by segment and competitor in data/crm/snapshots/.

BUILD
- A gap grid: segment and persona by whether we have a case study.
- The open pipeline sitting in each empty cell.
- Three candidate customers that fill the biggest gap, each with tenure, segment, and anything they've already said on calls or in reviews.

OUTPUT
The grid, the three candidates, and a pick.

GROUNDING
Cite paths. Never claim a customer is happy without evidence: a review, a call line or a health field. If there's no customers snapshot, say which export to drop in data/crm/snapshots/.
```

### Write the interview guide

```
Using this repo, write the interview guide for the case study with the customer below.

FILL IN
- Account: [account]
- Persona: [persona of the person we're interviewing]

CONTEXT
I get one call. I need the before, the decision, the result with a number, and a quote that sounds like them, not like us.

READ FROM THE REPO
- Anything the account said before: calls in memory/transcripts/processed/, reviews in data/reviews/snapshots/.
- Their deal in data/crm/snapshots/: competitor, size, why they bought.
- The pillar this story should prove in strategy/messaging.md.

BUILD
- Ten questions in order: situation, trigger, alternatives, decision, rollout, result, advice to a peer.
- For each: what we already know, so I can skip or confirm it.
- The two numbers we need and how to ask for them without leading.

OUTPUT
A one-page guide I can read from on the call.

GROUNDING
Cite paths for what we already know. Don't put words in the customer's mouth: questions, not suggested answers.
```

### Check the draft before the customer sees it

```
Using this repo, check the case study draft below before it goes to the customer for approval.

FILL IN
- Draft: [name its folder in content/, or paste it]

CONTEXT
The customer will read every line. One wrong number and we lose the reference.

READ FROM THE REPO
- The interview transcript in memory/transcripts/processed/.
- Any numbers on the account in data/crm/snapshots/.
- strategy/product-brief.md, for how the product actually works.

CHECK
- Every quote: verbatim in the transcript, with the line, or not.
- Every number: the customer's own (mark for approval) or from a snapshot (with path), or unsourced.
- Product descriptions that don't match the product brief.

OUTPUT
A table of findings, then the quote-approval list for the customer.

GROUNDING
Cite paths. An unsourced number is removed, not rounded. A paraphrase in quotation marks is flagged.
```

## Advanced prompts

### Red-team the case study as a skeptical buyer

```
Red-team the case study draft as a skeptical buyer who's been burned before. Use this repo for the persona, the competitor's angle and the facts behind the story.

FILL IN
- Draft: [name its folder in content/]
- Reader: [persona]

CONTEXT
Case studies read as marketing by default. I want to find every line a serious buyer would discount before we publish.

FROM THE REPO
- The reader's objections in strategy/personas.md.
- The battlecard for the competitor this customer replaced, in strategy/competitive/.
- The transcript and any snapshot numbers behind the story.

METHOD
- Read as the persona: mark every line they'd discount and why (vague result, no baseline, too good, wrong company size).
- Read as the competitor's sales rep: what would they say to undercut it?
- For each weak line, propose the evidence that would fix it, from the transcript if it's there.
- Score the study: credible, plausible, or reads as marketing.

OUTPUT
A table of weak lines with the objection and the fix, then the overall score.

GROUNDING
Label every point as repo (file path), mine, or your assumption. A fix must come from the transcript or a snapshot; never from what the customer might have said.
```

## Questions to just ask

- Which segments have no published case study?
- What did [account] say about results on their last call?
- Which customers have left a five-star review we could build on?
- Which case studies are older than two years?
- Which case studies prove [pillar]?
- Which competitor did [account] replace, according to the deal?
- Is there a transcript for the interview with [account] yet?
- Which quotes in published case studies were never marked approved?
- Which persona do our case studies feature most, and which never?
- Which open deals are in a segment with no case study?
- What numbers did [account] give us, and where are they written down?
- Which case studies did sales link most in the last quarter's deals?
