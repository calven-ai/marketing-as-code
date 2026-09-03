# Is this for your team? An honest fit check

Marketing as code is designed for specific teams. Not for every marketing
team, and not for every team that likes the idea. Whether it fits depends on
how many people you are, what your work is made of, who on the team already
likes tools, how much appetite there is for learning semi-technical things
(a repository, pull requests, MCP servers, API keys, a coding agent), and,
more than anything else, how the team handles change. The [README](../README.md)
explains what the approach is. This page is about whether you should do it.

If this page talks you out of it, that is a good outcome. A team that reads
"move marketing to GitHub" somewhere, forces it without a fit check, and
loses a quarter does not get a second try, and the idea gets the blame. The
repo is the ultimate form of the pattern, not the entry ticket:
[stages.md](stages.md) describes two earlier stages that are complete,
useful places to stop, and most teams should start there.

## What you are actually signing up for

| You will have to | Who | How often |
| --- | --- | --- |
| Run a Git-backed repository, through GitHub Desktop or the website if not the terminal ([new-to-github.md](new-to-github.md)) | everyone who edits | daily |
| Read diffs and merge pull requests; merging is the approval ([workflow.md](workflow.md)) | the people who decide what "done" means | daily, briefly |
| Keep API keys out of chat and in a secrets manager ([secrets.md](secrets.md)) | one owner | at setup, then rarely |
| Fill in the strategy and brand templates, put a name and a review date on each, and keep the dates honest (`strategy/`, `brand/`) | the owner of each document | quarterly |
| Pay for a coding-agent seat per active user and pay-as-you-go data instead of subscription suites | whoever owns the budget | monthly |
| Change where the team looks for the truth, and stop maintaining the old place | everyone | once, and it is the hard part |

The technical rows are the smaller half. Most of this page is about the
larger half.

## Who this is for

A team with at least one person who already likes tools: someone who has set
up an automation, edited a template, or opened a coding agent out of
curiosity. A team whose work is mostly text that recurs: content, reports,
meetings, briefs, positioning, the quarterly review. A team whose strategy is
scattered across a drive and a wiki and nobody trusts either, with one
person in the middle acting as the human API between them. And a leader who
will read a pull request, because in this model merging is how decisions get
made, and a leader who wants a summary instead is a leader who will stop
deciding.

## Who this is not for (yet)

Blunt, on purpose. Each line ends with the stage in [stages.md](stages.md)
that fits instead.

- **Nobody can be named as the owner.** A repo with no owner is a folder
  with history. Start at stage 1, where the assistant owns the plumbing.
- **The work is mostly events, design, or paid media** with little recurring
  text. The agents here read and write prose and tables; they do not run a
  booth or a bid strategy. Stage 1, or stage 2 for reporting only.
- **Leadership wants a deck about it, not a diff.** The review ritual is the
  approval mechanism. If it will not be practised, the repo becomes a
  second place where drafts go to wait. Stage 1 until that changes.
- **IT or security forbid API keys, AI tools, or a private GitHub repo.**
  Get that conversation done first; nothing here works around it. Stage 1
  inside whatever is sanctioned.
- **The current stack is fine and the pain is imaginary.** If nobody can
  say what hurts today, in one concrete sentence, there is nothing for the
  repo to fix. Stay where you are.
- **A core tool changed in the last six months** and the team is still
  recovering. Change has a budget, and it has been spent. Stage 1 now, stage
  2 next quarter.

## The self-assessment

Eight questions, in prose, with what each answer means. There is no score
at the end: a score would pretend to be data, and this is judgment.

1. **Who owns the repo, by name?** If a name comes immediately, keep
   reading. If the answer is "the team", nobody owns it: stage 1.
2. **Who on the team has already set up an automation, edited HTML, or used
   a coding agent? And would a second person learn?** One person is enough
   to start. If a second person would not learn, the first one becomes the
   new human API within a quarter: stage 2, one agent, and pair from day
   one.
3. **Will the person who decides what "done" means for marketing read a
   diff?** If yes, the review workflow will hold. If they will only read a
   summary, stage 1, and revisit when that person changes or changes their
   mind.
4. **Can the owner spend about two days a week on this for the first
   month?** Setup, the first workflow, and teaching two colleagues take that
   long. If the honest answer is a few hours, stage 2 is the ceiling until
   the time exists.
5. **What hurts today, concretely?** Seven logins and one person routing
   between them, positioning nobody trusts, meetings that evaporate, reports
   rebuilt by hand every quarter: the repo fixes these. "We should be using
   AI more" is not a pain, it is a mood. No pain named, no stage yet.
6. **How did the last tool change go?** If the team adopted it and the old
   one is switched off, change is a skill you have. If two tools still run
   in parallel a year later, plan for that here too, and pick stage 2 with
   a single activity that has a clear cut-over.
7. **How much recurring text work exists to pay back the learning?** A blog
   and a newsletter, monthly reports, weekly meetings, a quarterly review:
   enough. One campaign a year and the rest is events: stage 1.
8. **What do IT or security say about AI tools, API keys, and a private
   repo?** "Yes, with these rules" is fine, and the rules go into
   [secrets.md](secrets.md). "No" ends the assessment at stage 1. "Nobody
   has asked" means ask before the pilot, not after.

## By team size

These are types of teams, not companies. The effort figures are the
maintainer's estimates from running this pattern, in their own company and
with the teams around it, not survey data. Treat them as the shape of the
work, not a benchmark.

| Team | Realistic goal in year one | Who has to learn what | Effort shape | Start at |
| --- | --- | --- | --- | --- |
| One or two people | The full repo | The person: GitHub Desktop, a coding agent, keys | A few days, then habit | Stage 3, or stage 1 if tools are not your thing |
| About five | The repo for the whole team | One champion: everything; everyone else: GitHub Desktop and PR review | Champion two to three weeks part-time, then ten minutes a day for everyone | Stage 2 as a pilot, stage 3 within a quarter |
| About twenty | The repo for one or two functions, shared context for all | A named owner and one person per function; leadership: reading diffs | An owner at a third to half of their time for a quarter, plus a sponsor | Stage 1 for all, stage 2 for one function, stage 3 for the pilot |
| About a hundred | One lighthouse sub-team on the repo, sanctioned AI tools for the rest | A MarOps lead, a technical marketer, an IT contact | A group of two or three for one to two quarters, with a change plan | Stage 1 under IT's rules, stage 2 for one MarOps workflow, stage 3 for the lighthouse |

### One or two people

A founder doing the marketing, or a solo marketer. Full stage 3 is
realistic because there is nobody to convince: the setup interview fills
the templates in an afternoon, and the first workflow runs the same day. The
challenge is the opposite of everyone else's. The rule that humans decide
and agents propose ([AGENTS.md](../AGENTS.md), rule 3) collapses into
self-review, so the discipline of reading your own diff before merging is
the whole safety net. And the repo is a memory only if you keep feeding it:
a decision log nobody appends to is a file. The benefit is that the repo is
the team you do not have. The chief-of-staff processes the meetings a solo
marketer never writes up, and the quarterly review gets built instead of
skipped. Effort: a few days to set up, then habit. Start at stage 3 if you
already like tools; otherwise stage 1, and come back.

### About five

A head of marketing, someone on content, someone on demand generation,
maybe ops or design. This is the sweet spot, and it is still work. Everyone
is a generalist, so one champion carries the technical load: the repo, the
keys, the integrations, the first agents. Unless a second person learns
alongside them, the champion becomes the new human API, and the team has
traded one bottleneck for a better-documented one. There is usually no ops
person to own the data folder and the ontology, so the champion writes the
metric definitions too, or the analyst agents keep asking. The benefit is
shared context for the first time: one positioning, one voice, one decision
log, read by every agent and every person. And agents standing in for tools
the team could never afford: the SEO analyst, the account researcher, the
dashboard builder. Effort: the champion spends two to three weeks part-time
on setup and the first workflow; every other teammate spends half a day on
GitHub Desktop and pull-request review; after that, about ten minutes of
review a day for everyone. Start at stage 2 with one pilot workflow, and
move the whole team to stage 3 within a quarter if the pilot holds.

### About twenty

Functions now: content, demand generation, product marketing, ops, design,
perhaps a region. The challenges change kind. Existing tools have owners and
contracts, and replacing one takes a renewal date and a conversation, not a
decision. Strategy files gain a named owner and a review date, which some
functions have never had, and the person named will feel it. Review needs an
owner per area, because one head of marketing cannot read every diff. And
the change is a project with a sponsor, a pilot, and an end date, not a
weekend. The benefit is that the context problem is real at this size:
agencies, freelancers, and new hires all need the same positioning, and
today they get whichever version someone forwards them. Ops finally gets a
definitions file (`data/ontology/`) that the analytics tool and the CRM can
be held to. Effort: a named owner, usually ops or a technical product
marketer, at a third to half of their time for a quarter; two or three
pilots, one per willing function; a VP-level sponsor who reviews the first
pull requests personally. Start at stage 1 for the whole organisation,
stage 2 for one function (SEO and ops go first because their work is
already data), and stage 3 for the pilot function only. The rest follow
when the pilot has something to show, not before.

### About a hundred

Regions, agencies, procurement, IT and security, a marketing operations
team. Everything from the twenty-person profile applies, plus a security
review of AI tools and keys, procurement of coding-agent licences and
GitHub seats with single sign-on, PII governance (the rules in
[data/README.md](../data/README.md) and [memory/README.md](../memory/README.md)
become policy), enterprise suites nobody will replace, and the honest
possibility that "one repo" becomes several repos with shared context. The
benefit is that context unification is worth the most here and is also the
hardest, because there are the most copies. The low-risk wins are reporting
(the quarterly review and dashboards, which nobody will fight over) and
research (account research into snapshots, which replaces spreadsheets
rather than people). Effort: a group of two or three, a MarOps lead, a
technical marketer, and an IT contact, for one to two quarters to pilot,
with a written change plan. Start at stage 1 under IT's sanctioned tools,
stage 2 for one workflow that MarOps owns end to end, and stage 3 for one
sub-team as a lighthouse. Organisation-wide stage 3 in year one is not
realistic, and a plan that says otherwise is the first thing to fix.

### Agencies

An agency runs one repo per client and keeps its own skills, voice
checks, and report templates as a shared layer across them. The fit
question is the same as for a five- or twenty-person team, asked once per
client team. The context problem multiplies: every client has positioning,
personas, and competitors that go stale on their own schedule, and the
agency is the one paged when a draft contradicts them. That is where the
choice between hand-maintained strategy files and a context layer served
live ([integrations/context-layer.md](../integrations/context-layer.md))
matters most, because it is made once per client.

## Change management: the larger half

The technical parts are done in weeks. This part decides whether the repo is
alive in six months.

### What breaks

**Habits.** Work lives where people open by reflex, and for a while the
reflex points at the old place. "Where is X?" gets worse before it gets
better, because during migration X exists twice.

**Tool loyalty.** Replacing a tool removes something someone chose, set up,
and is proud of. The argument against the change will be about features; the
feeling behind it is about the person.

**The review ritual.** Reading diffs daily is a new habit, and it is the
one that cannot be skipped: a stalled pull request is stalled marketing
([workflow.md](workflow.md)). Teams that treat review as optional end up
with a repo full of drafts and a drive full of the real work.

**Fear of Git.** Branches, conflicts, and the word "commit" scare people
who have never met them. GitHub Desktop and the website reduce the fear;
they do not remove it. Plan for the first conflict to happen in a pairing
session, not alone at 6pm.

**Ownership.** Who owns the repo? Who owns `strategy/positioning.md` now
that it carries a name and a review date? Documents that were nobody's are
suddenly somebody's, and that somebody did not ask for it.

**The human API.** The person who routes between the seven tools today is
the person this change affects most. Their role moves from router to owner
of the system, which is a promotion if they experience it that way and a
loss if they do not. Say it out loud, early, and give them the ownership.
If it is left unsaid they will resist quietly, and quiet resistance from
the person who knows where everything is cannot be overcome.

**Two truths.** Until a cut-over date, the old document and the new file
both exist, and people will edit the wrong one. Set the date before you
start and say what happens to the old copy on that day.

**First impressions.** An unfilled ontology makes agents ask instead of
answer, by design ([AGENTS.md](../AGENTS.md), rule 2). To a skeptic that
looks like failure. Run `/setup` and fill the templates before anyone sees
a demo.

### What to do about it

**A sponsor who reviews the first pull requests personally.** Not a
sponsor who approves the initiative: one who reads three diffs in the first
week and merges them. That is the signal the team watches.

**A champion who is never alone.** Pair from day one. The second person
does not need to match the first; they need to be able to open a pull
request and explain one to a colleague.

**One pilot workflow, with an end date and a pass/fail sentence.** "Every
meeting transcript is processed through the repo for four weeks" or "the
next quarterly review is built from the repo, not from slides". One
sentence, written before the pilot starts, so nobody argues about the
result afterwards.

**The no-terminal path for everyone else.** Most of the team should never
meet a command line. [new-to-github.md](new-to-github.md) and
[workflow.md](workflow.md) are written for them.

**Pairing sessions instead of training decks.** Nobody learns pull
requests from slides. Two people, one screen, one real change.

**Migrate context first.** `strategy/` and `brand/`, filled in through the
setup interview, before any content or data moves. Context is what the
agents need, and it is the smallest thing to move.

**Keep the old tools running until the pilot passes.** Switching off a tool
before its replacement has proven itself is how change projects earn their
reputation.

**Write the rollback before you start.** One paragraph: "If by this date we
have not done this, we export the Markdown back to the drive and stop."
Plain text is the reason this is cheap; nothing is trapped in a format.

**Log the decision to try, and the rollback.** Both go in
`memory/decision-log.md` (the `/log-decision` skill does it), dated and
attributed, so that six months from now the team knows what it agreed to.

### Signals to slow down or stop

Pull requests older than a week. The champion is still the only person
committing after two months. People paste repo content into chat instead of
linking to it. The `last_reviewed` dates never move, and `scripts/doctor.py`
keeps saying so on every pull request. Leadership asks for a deck about the
repo. A second source of truth appears and nobody closes it.

Any one of these is a conversation. Two or three together mean the team is
at a lower stage than it thinks, and the honest move is to say so. Stopping
is allowed. The path in [stages.md](stages.md) is built so that stopping at
stage 1 or stage 2 is still a gain, not a failure.

## If not now, then what

Read [stages.md](stages.md). Stage 1 is the assistant your team already pays
for, used properly. Stage 2 is one activity handed to one agent you own.
This repo is stage 3, the ultimate form, and every team that arrives here
in good shape came through the first two, whether or not they called them
that.
