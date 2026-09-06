# Week one: from a copy to your first merged piece

In order. Each step says the one thing you type and what you should see.
Stop anywhere; `/sync` picks up where you left off. The five words in
[workflow.md](workflow.md) are the whole ritual; this page is the first
week of saying them.

## Before you start

Someone with admin rights on GitHub, once: on the template's page, "Use
this template", "Create a new repository", owned by your organization (on
GitHub Team), private. On each computer:
[GitHub Desktop](https://desktop.github.com),
[Claude Code](https://claude.com/claude-code) (the desktop app is fine),
the [GitHub CLI](https://cli.github.com), and Python 3.9 or newer (a Mac
has it after `xcode-select --install`; Windows gets it from python.org).

## Day one

1. **Clone.** GitHub Desktop, "Clone a repository", your copy. *A folder
   on your computer.*
2. **Open the agent.** Open that folder in Claude Code. It asks whether to
   start three project MCP servers: say No to all three for now. *Three
   lines from the doctor: problems, stale context, unfilled templates.*
3. **`/doctor`.** *It names one action, `gh auth login --web`, and where to
   type it. A code, a browser, paste the code. Say `/doctor` again: "your
   machine is ready to propose".*
4. **`/setup`.** Rounds 1 to 5 today (positioning, messaging, ICP and one
   persona, competitors, voice) and round 10 (who reviews, how many
   merge). The rest can wait. *Filled files in `strategy/` and
   `brand/`, and the first entry in `memory/decision-log.md`.*
5. **Repository settings** (the admin, once). `sh scripts/github_setup.sh`,
   or the click path in [github-settings.md](github-settings.md).
   *`python3 scripts/doctor.py --github` prints nothing under "GitHub
   settings".*
6. **`/propose`.** *A link. Open it, read the diff, click Merge. This is
   the ritual for everything from now on.*

## Day two

7. **`/sync`.** *"Nothing waiting on you", and your checkout is the
   approved copy.*
8. **`/new-content`** and a sentence: "a blog post about X". *A folder in
   `content/` with a brief. Read the brief; say "draft it".*
9. **`/review`.** *Findings by severity and a verdict. Fix what it names,
   or say "apply the voice fixes".*
10. **`/propose`**, then Merge. *Your first piece is on the approved copy
    with `status: in-review`. Publishing is a person's call: when it is
    live, set `status: published`, the date and the URL, and propose
    again.*

## Day three

11. **A meeting.** Drop its transcript into `memory/transcripts/inbox/`,
    named `YYYY-MM-DD-<meeting>.md` (`.txt` and `.vtt` work too), and say
    **`/chief-of-staff`**. *Decisions appended to the log, status entries,
    action items per owner, and a summary. `/propose`: the bookkeeping
    parts merge themselves once the check is green.*

## Day four

12. **Make it yours.** Work through [make-it-yours.md](make-it-yours.md):
    delete the example company, the maintainer's community files, the
    example rows. `/propose`, Merge. *`python3 scripts/doctor.py` no longer
    prints "Make it yours".*

## Monday

13. A "Housekeeping" proposal appears and merges itself. Expected
    ([operating-model.md](operating-model.md#turning-a-workflow-off)).

## Week two, when you are ready

- **`/add-integration`** for the tool that hurts most: your task tool, your
  meeting recorder. "We use Zoom for meetings. Automate reading the
  transcripts into the inbox."
- **`/seo-analyst`** once DataForSEO is connected, **`/new-project`** for the
  first campaign, **`/battlecard`** for the competitor you lose to most,
  **`/qmr`** at quarter end.
- **A second person.** Send them this page. Their day one is steps 1 to 3
  and 6; `/setup` is already done.
