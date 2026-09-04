# Is this for your team? A fit check

Marketing as code is designed for specific teams. Whether it fits depends
on how many people you are, what your work is made of, who already likes
tools, and, more than anything, how the team handles change. The
[README](../README.md) explains the approach. This page is about whether
you should do it.

If this page talks you out of it, good. A team that forces the repo without
a fit check and loses a quarter does not get a second try. The repo is the
final form of the pattern, not the entry ticket. [stages.md](stages.md)
describes two earlier stages that are complete places to stop, and most
teams should start there.

## What you are signing up for

| You will have to | Who | How often |
| --- | --- | --- |
| Run a Git-backed repository, through GitHub Desktop or the website if not the terminal ([new-to-github.md](new-to-github.md)) | everyone who edits | daily |
| Read diffs and merge pull requests; merging is the approval ([workflow.md](workflow.md)) | the people who decide what "done" means | daily, briefly |
| Keep API keys out of chat and in a secrets manager ([secrets.md](secrets.md)) | one owner | at setup, then rarely |
| Fill in the strategy and brand templates, put a name and a review date on each, and keep the dates true (`strategy/`, `brand/`) | the owner of each document | quarterly |
| Pay for a coding-agent seat per active user and pay-as-you-go data instead of subscription suites | whoever owns the budget | monthly |
| Pay for GitHub Team or Pro, so the repository's rules are enforced rather than suggested ([github-settings.md](github-settings.md)) | whoever owns the budget | monthly, per seat |
| Decide, per recurring workflow, whether a person runs it or GitHub Actions does ([operating-model.md](operating-model.md)) | the owner | once per workflow |
| Change where the team looks for the truth, and stop maintaining the old place | everyone | once, and it is the hard part |

The technical rows are the smaller half. Most of this page is about the
larger half.

## Who this is for

A team with at least one person who already likes tools. A team whose work
is mostly text that recurs: content, reports, meetings, briefs, positioning,
the quarterly review. A team whose strategy is scattered across a drive and
a wiki, with one person in the middle acting as the human API. And a leader
who will read a pull request, because here merging is how decisions get
made.

## The self-assessment

Eight questions. No score at the end, because a score would pretend to be
data and this is judgment. Each "no" names the stage in
[stages.md](stages.md) that fits instead.

1. **Who owns the repo, by name?** A name means keep reading. "The team"
   means nobody: stage 1, where the assistant owns the plumbing.
2. **Who has already set up an automation, edited HTML, or used a coding
   agent? Would a second person learn?** One person is enough to start. If
   nobody would join them, the first becomes the new human API within a
   quarter: stage 2, one agent, and pair from day one.
3. **Will the person who decides what "done" means read a diff?** If yes,
   the review workflow holds. If they want a deck about it, the repo becomes
   a second place where drafts wait: stage 1 until that changes.
4. **Can the owner spend two days a week on this for the first month?**
   Setup, the first workflow, and teaching two colleagues take that long.
   A few hours a week caps you at stage 2.
5. **What hurts today, in one concrete sentence?** Seven logins and one
   person routing between them. Positioning nobody trusts. Meetings that
   evaporate. Reports rebuilt by hand every quarter. The repo fixes these.
   "We should be using AI more" is a mood. No pain named, no stage yet.
6. **How did the last tool change go?** Adopted, old one switched off:
   change is a skill you have. Two tools still running a year later: pick
   stage 2 with one activity and a clear cut-over. And if a core tool
   changed in the last six months, the change budget is spent. Stage 1 now.
7. **How much recurring text work exists to pay back the learning?** A blog,
   a newsletter, monthly reports, weekly meetings, a quarterly review:
   enough. One campaign a year and the rest is events, design or paid
   media: stage 1, or stage 2 for reporting only.
8. **What do IT or security say about AI tools, API keys, and a private
   repo?** "Yes, with rules" is fine; the rules go in
   [secrets.md](secrets.md). "No" ends the assessment at stage 1. "Nobody
   has asked" means ask before the pilot.

## By team size

Types of teams, not companies. The effort figures are the maintainer's
estimates from running this pattern, not survey data.

| Team | Realistic goal in year one | Who has to learn what | Effort shape | Start at |
| --- | --- | --- | --- | --- |
| One or two people | The full repo | The person: GitHub Desktop, a coding agent, keys | A few days, then habit | Stage 3, or stage 1 if tools are not your thing |
| About five | The repo for the whole team | One champion: everything; everyone else: GitHub Desktop and PR review | Champion two to three weeks part-time, then ten minutes a day for everyone | Stage 2 as a pilot, stage 3 within a quarter |
| About twenty | The repo for one or two functions, shared context for all | A named owner and one person per function; leadership: reading diffs | An owner at a third to half of their time for a quarter, plus a sponsor | Stage 1 for all, stage 2 for one function, stage 3 for the pilot |
| About a hundred | One lighthouse sub-team on the repo, sanctioned AI tools for the rest | A MarOps lead, a technical marketer, an IT contact | A group of two or three for one to two quarters, with a change plan | Stage 1 under IT's rules, stage 2 for one MarOps workflow, stage 3 for the lighthouse |

### One or two people

A founder doing the marketing, or a solo marketer. Full stage 3 is
realistic because there is nobody to convince. The challenge is the
opposite of everyone else's: "humans decide, agents propose" collapses into
self-review, so reading your own diff before merging is the whole safety
net. The benefit is that the repo is the team you don't have. The
chief-of-staff processes the meetings a solo marketer never writes up, and
the quarterly review gets built instead of skipped.

### About five

A head of marketing, content, demand generation, maybe ops or design. The
sweet spot, and still work. One champion carries the technical load, and
unless a second person learns alongside them, the team has traded one
bottleneck for a better-documented one. There is usually no ops person, so
the champion writes the metric definitions too. The benefit is shared
context for the first time: one positioning, one voice, one decision log,
read by every agent and every person. Plus agents standing in for tools the
team could never afford: the SEO analyst, the account researcher, the
dashboard builder.

### About twenty

Functions now: content, demand generation, product marketing, ops, design,
perhaps a region. Existing tools have owners and contracts, so replacing
one takes a renewal date and a conversation. Strategy files gain a named
owner and a review date, and the person named will feel it. Review needs an
owner per area. The benefit is real at this size: agencies, freelancers and
new hires all need the same positioning, and today they get whichever
version someone forwards. Ops gets a definitions file (`data/ontology/`)
the analytics tool and the CRM can be held to. Start with one willing
function (SEO and ops go first, their work is already data) and let the
rest follow when the pilot has something to show.

### About a hundred

Regions, agencies, procurement, IT and security, a marketing operations
team. Everything above applies, plus a security review of AI tools and
keys, procurement of licences and seats with single sign-on, PII governance
([data/README.md](../data/README.md), [memory/README.md](../memory/README.md)),
and the real possibility that "one repo" becomes several with shared
context. Context unification is worth the most here and is the hardest.
The low-risk wins are reporting and account research, which replace
spreadsheets rather than people. Organisation-wide stage 3 in year one is
not realistic, and a plan that says otherwise is the first thing to fix.

### Agencies

One repo per client, with the agency's own skills, voice checks and report
templates as a shared layer. Ask the fit question once per client team.
Every client's positioning, personas and competitors go stale on their own
schedule, so the choice between hand-maintained strategy files and a
context layer served live
([integrations/context-layer.md](../integrations/context-layer.md)) is made
once per client.

## Change management: the larger half

The technical parts take weeks. This part decides whether the repo is alive
in six months.

### What breaks

- **Habits.** Reflex points at the old place. "Where is X?" gets worse
  before it gets better, because during migration X exists twice.
- **Tool loyalty.** Replacing a tool removes something someone chose and is
  proud of. The argument will be about features. The feeling is about the
  person.
- **The review ritual.** Reading diffs daily is a new habit and the one
  that cannot be skipped. A stalled pull request is stalled marketing
  ([workflow.md](workflow.md)).
- **Fear of Git.** GitHub Desktop reduces it; it does not remove it. Plan
  for the first conflict to happen in a pairing session, not alone at 6pm.
- **Ownership.** Documents that were nobody's are suddenly somebody's, and
  that somebody did not ask for it.
- **The human API.** The person who routes between the seven tools today
  moves from router to owner of the system. Say it out loud, early, and
  give them the ownership. Left unsaid, they resist, and the person who
  knows where everything is cannot be overcome.
- **Two truths.** Until a cut-over date, the old document and the new file
  both exist. Set the date before you start.
- **First impressions.** An unfilled ontology makes agents ask instead of
  answer, by design. To a skeptic that looks like failure. Run `/setup`
  before anyone sees a demo, and show `examples/beacon/` in the meantime.

### What to do about it

- **Get a sponsor who reviews the first pull requests personally.** Three
  diffs in the first week, merged. That is the signal the team watches.
- **Never leave the champion alone.** Pair from day one.
- **Run one pilot workflow with an end date and a pass/fail sentence.**
  "Every meeting transcript is processed through the repo for four weeks."
  Written before the pilot starts.
- **Give everyone else the no-terminal path.**
  [new-to-github.md](new-to-github.md) and [workflow.md](workflow.md) are
  written for them.
- **Pair instead of training.** Two people, one screen, one real change.
- **Migrate context first.** `strategy/` and `brand/`, filled through the
  setup interview, before any content or data moves.
- **Keep the old tools running until the pilot passes.**
- **Write the rollback before you start.** "If by this date we have not
  done this, we export the Markdown back to the drive and stop." Plain
  text makes this cheap.
- **Log the decision to try, and the rollback**, in
  `memory/decision-log.md` (the `/log-decision` skill does it).

### Signals to slow down or stop

Pull requests older than a week. The champion is still the only person
committing after two months. People paste repo content into chat instead
of linking to it. The `last_reviewed` dates never move, and
`scripts/doctor.py` keeps saying so. Leadership asks for a deck about the
repo. A second source of truth appears and nobody closes it.

Any one of these is a conversation. Two or three together mean the team is
at a lower stage than it thinks. Stopping is allowed. The path in
[stages.md](stages.md) is built so that stopping at stage 1 or 2 is still a
gain.
