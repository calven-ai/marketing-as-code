# New to GitHub? Start here

You do not need to live in a terminal to run your marketing from this repo.
You need a GitHub account, one desktop app, a coding agent that does the
technical parts, and one command, once, to log in to GitHub. Your agent
tells you when. This guide gets you there. Not sure the repo is for your team at
all? Read [is-this-for-you.md](is-this-for-you.md) first.

## What a repository is

A repository is a shared folder with perfect memory. Every change is saved
with a note saying who made it and why, and you can look at any earlier
version. Nothing is ever lost by accident.

It also has rules about how changes land. Nobody edits the live version
directly. You make your change on a copy, show it as a proposal, and someone
merges it. That review step is why agents can work here safely: they
propose, a person approves.

Everything in this repo is plain text. That is what lets AI agents read your
positioning and write a draft in your voice. A deck locked in a drive can't
do that.

## The words you will meet

- **Repo.** The shared folder. This one.
- **Commit.** One saved change, with a note.
- **Branch.** A copy of the repo where you make changes without touching the
  live version.
- **Pull request.** A request to merge a branch into the live version. This
  repo calls it a proposal.
- **Diff.** The changed lines, old beside new. Reading the diff is the
  review.
- **Merge.** Clicking Merge on a proposal. Merging is the approval.
- **Check.** The automatic test that runs on every proposal and says what
  is wrong in plain words.
- **Gate.** The second automatic step. It sorts a proposal into
  bookkeeping or needs-review and merges only the first kind.
- **Bookkeeping.** A proposal that touches only files the agents maintain:
  a status entry, a decision-log line, a data snapshot, a recurring
  report. It merges itself once the check is green.
- **Wired.** Connected. A tool is wired when the repo knows how to reach
  it; the table in `integrations/README.md` says which ones are.

You can ignore everything else for now.

## Get your own copy

1. Create an account at github.com if you don't have one. The account is
   free; the repository goes into your company's GitHub organization, which
   is on the Team plan (whoever runs the website repo can add you).
2. Open this repo and click **Use this template**, then **Create a new
   repository**. Choose the organization as the owner and make it private:
   meeting notes and customer names will live here. This is your team's
   copy, and it never sends anything back here.
3. Install [GitHub Desktop](https://desktop.github.com). It puts the repo on
   your computer as a normal folder and handles the saving and syncing.
4. In GitHub Desktop, choose **Clone a repository** and pick your new copy.

## Your first change

1. In GitHub Desktop, click **Current branch** and create a new branch.
   Name it after the change, like `positioning-draft`.
2. Open the repo folder and edit a file in any text editor. Try
   `strategy/positioning.md`.
3. Back in GitHub Desktop, write a one-line summary of what you changed and
   click **Commit**. Then click **Push** to send it to GitHub.
4. Click **Create pull request**. GitHub opens the proposal in your browser.
   A teammate reads the change, comments, and merges it.

That is the whole loop. Branch, edit, commit, pull request, merge. Every
change in this repo, by a person or an agent, goes through it.

## Let the agent do the technical parts

One-time setup, in this order:

1. Install [Claude Code](https://claude.com/claude-code), the desktop app
   is fine, and open your repo folder in it.
2. Install the [GitHub CLI](https://cli.github.com). It is how the agent
   talks to GitHub.
3. Say `/doctor`. It names the one command to type, `gh auth login --web`,
   and where to type it. A code appears, a browser opens, you paste the
   code. Say `/doctor` again and it tells you that you are ready.

Then the whole loop is three words:

1. **`/sync`** brings in the latest approved copy and tells you what is
   waiting on you.
2. **Work.** "Draft a blog post on X." "Process the transcript in the
   inbox." "Set up this repo for our team." The agent does it on a branch.
3. **`/propose`** checks the files, saves the change, and hands you the
   link to the proposal. Open it, read the diff, click Merge. Bookkeeping
   proposals merge themselves.

After that you never type a command. When the agent needs something technical, like
connecting your CRM or storing an API key, it tells you exactly what to
do and where. If it asks for a key value in chat, that is a red flag. Keys
go in a file the agent never reads ([secrets.md](secrets.md)).

## Where to go next

- [workflow.md](workflow.md): how review works here, in more detail.
- [troubleshooting.md](troubleshooting.md): every message the commands
  print, and the one thing to do.
- [stages.md](stages.md): if you want to start smaller than a full repo.
- [../README.md](../README.md): the quick start, once you are comfortable.
