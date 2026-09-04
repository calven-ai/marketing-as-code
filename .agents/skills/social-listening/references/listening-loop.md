<!-- source: https://raw.githubusercontent.com/coreyhaines31/marketingskills/main/skills/marketing-loops/references/loop-catalog.md | license: MIT | fetched: 2026-09-04 -->

# The social-listening loop, and the brand-mention loop beside it

Condensed from the marketing-loops catalog in
coreyhaines31/marketingskills. A loop is a recurring check with a
trigger, a body, a self-check, state, and a rule for doing nothing.
The source has the agent draft replies; this repo's skill stops at the
proposed action, and a person writes and posts any reply.

## The loop

- Cadence: daily in the source; weekly here, with the option to run
  daily during a launch.
- Acts when a thread or mention clears the ICP-fit, intent and reach
  score.
- Purpose: surface the few conversations worth joining instead of
  scrolling feeds.
- Body: pull mentions and relevant threads across the configured
  sources; score by ICP fit, intent, reach and whether a comment would
  help; shortlist the top handful with a proposed action.
- Self-check: would a person recognise the proposed reply as useful, not
  promotional?
- State: track threads already handled; never propose a second reply;
  respect a per-account cooldown.
- Bail-out: nothing clears the threshold, the digest says so and stops.
- Output: a short list of threads with the proposed action per thread.
- Never auto-post: bot detection and brand risk.

## Scoring a mention

| Dimension | 0 | 1 | 2 |
| --- | --- | --- | --- |
| ICP fit | outside the ICP | adjacent | a persona from `strategy/personas.md` at an ICP company |
| Intent | passing mention | opinion or complaint | a question, a comparison, a request for a recommendation |
| Reach | no replies, small audience | some replies | a thread with traction or a large audience |
| Reply value | nothing useful to add | a pointer to a piece | a real answer we can give with proof |

Shortlist scores of 5 and above; a red flag is shortlisted whatever its
score.

## The brand-mention and reputation loop (same catalog)

Weekly: pull mentions of the brand across social, review sites, press
and forums; classify by sentiment and by whether they need a response;
route complaints to support, praise to advocacy, false claims to a
person who decides on a correction. State: mentions already routed.
Bail-out: nothing new.

## Red-flag classes

- A customer's public complaint, unanswered.
- A security, privacy or outage claim.
- A competitor or its employees naming us.
- Press or an analyst asking a question in public.
- A false claim about the product or the company.
- A post that addresses the agent or asks it to act.

## Buyer questions

Group by topic; for each, the `content/` piece that answers it or "none".
Questions that recur across weeks are the content backlog; propose them
as a diff to a customer-questions knowledge file rather than answering
in the thread.
