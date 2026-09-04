# Troubleshooting: what the message means, and the one thing to do

Every message the lifecycle commands print is listed here with its fix.
Say `/doctor` first; it fixes most of these on its own.

## Getting connected

**"This folder is not connected to GitHub yet."** The folder is not a copy
of the repository, or it has no link to GitHub. Create your copy from the
template and clone it with GitHub Desktop
([new-to-github.md](new-to-github.md)).

**"Could not reach GitHub."** No connection, or GitHub is down. Check your
network and try again. Your work is safe on this computer.

**"GitHub CLI is not installed."** The agent talks to GitHub through the
GitHub CLI. Download it from cli.github.com (on a Mac, `brew install gh`
works too), then say `/doctor` again. Without it, `/propose` still saves
and pushes your work and prints a link to open the proposal yourself.

**"Not logged in to GitHub."** In your own terminal, or the desktop app's
terminal, run `gh auth login --web`. It shows a code, opens your browser,
and you paste the code. Then say `/doctor`.

**"Git does not know your name yet."** Commits carry a name and an email.
Once you are logged in to GitHub, `/doctor` sets both from your GitHub
account, with GitHub's private email address, so nothing personal leaks.

**"git may ask for a password when pushing."** Run `gh auth setup-git`
once, or say `/doctor` and let it do that.

**git or Python is missing.** On a Mac, run `xcode-select --install` and
accept the prompt; it installs both. On Windows, install Git for Windows
and Python from python.org, ticking "add to PATH".

## Proposing

**"Nothing has changed since the approved copy."** There is nothing to
propose. If you edited files in another app, save them first.

**"N problems to fix before this can be proposed."** The files have
problems the check on GitHub would refuse too. Nothing was sent. Say
`/doctor`, or ask the agent to fix what the list names, then propose again.

**"That proposal already landed."** You are still on a branch whose
proposal merged. Say `/sync`; it moves you on and removes the old branch.

**"GitHub did not accept your login."** Your login expired or was revoked.
Run `gh auth login --web` again, then propose again.

**"GitHub refused this because it contains something shaped like a key."**
Push protection caught a credential. Remove it from the file, rotate the
key at the vendor ([secrets.md](secrets.md)), then propose again. Never
keep a key in a file the repo tracks.

**"Your change is saved on this computer. In GitHub Desktop click Push
origin, then Create pull request."** The push needs a login the agent
does not have. GitHub Desktop has one: push from there and open the
proposal in the browser. To let the agent do it next time, install the
GitHub CLI and log in.

**"Open this link and click Create pull request."** The push worked, but
without the GitHub CLI the agent cannot open the proposal for you. The
link has the title and description filled in.

**"Pushed, but could not open the proposal."** Same as above, with the
reason GitHub gave. The link that follows opens it by hand.

## Syncing

**"You have unsaved edits to X; propose or discard them, then sync
again."** Sync will not bring the approved copy into a checkout with
unsaved work. Say `/propose` to save it, or ask the agent to discard it.

**"Your proposal and the approved copy changed the same lines in X."**
Two people changed the same lines. The agent resolves it: it keeps both
intents, or shows you both versions and asks. Then `/propose` saves the
result.

**"Your proposal and its copy on GitHub have drifted apart."** The branch
on GitHub and the one on this computer disagree in a way a plain merge
cannot settle. Ask the agent to sort it out; it will not force anything.

**"Your copy has changes GitHub does not."** Something was committed on
the approved copy locally instead of on a branch. `/propose` turns those
commits into a proposal; nothing is lost.

## Reviewing and merging

**The check is red on the proposal.** Open the proposal; the sticky
comment lists what the health check found. Say `/doctor` in your checkout
to fix it, then `/propose` to update the proposal.

**The proposal says "waiting for approval from" someone.** It needs a
person who is not the author to read the diff and approve. One
maintainer? Set `review.self_merge` in `docs/schema.json`
([workflow.md](workflow.md)).

**Merge button is grey.** The two checks, `doctor` and `review-gate`,
must be green. On GitHub Free with a private repository the button stays
usable but the rules are advice
([github-settings.md](github-settings.md)).

## Two tools, one folder

GitHub Desktop and the coding agent work in the same folder. Whatever one
of them saves, the other sees. Commit in one place at a time, and say
`/sync` after you pushed or merged from Desktop so the agent catches up.
