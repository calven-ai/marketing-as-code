# Questions people ask before adopting this

Short answers, each pointing at the page that has the long one.

**Does it run on Windows?** The scripts are written and tested on macOS
and Linux. On Windows they run in WSL or Git Bash, untested by the
maintainers: `python3` must be on the path (the python.org installer
gives you `python` and `py`; add an alias or use WSL), the shell scripts
need Git Bash, and `.claude/skills/` holds symlinks that Git for Windows
checks out as text files, which `/doctor --fix` repairs by copying
([troubleshooting.md](troubleshooting.md)).

**Do I need to pay Anthropic?** You need a coding agent per person: a
Claude Code, Cursor or Codex seat, whichever your team uses. An Anthropic
API key is only for the optional agent that runs in GitHub Actions with
nobody watching, billed per run, and nothing in the repo needs it
([operating-model.md](operating-model.md), [secrets.md](secrets.md)).

**Ninety-nine skills: does every session pay for all of them?** No. A
coding agent loads the one-line description of each skill so it can
route to the right one, and reads a skill's body only when it runs it.
The descriptions together are under 20,000 characters, and the check
warns when they grow past that ([skill-authoring.md](skill-authoring.md)).

**Can I use ChatGPT, or the chat app I already pay for?** For stage one,
yes: [stages.md](stages.md) is the path from the AI tools you already
have, to one agent for one activity, to this repo. The repo itself needs
a coding agent that reads files, because that is what the skills are.

**Where does my data go?** Nowhere you did not put it. Everything lives in
your own copy of the repository, on your GitHub, and in the tools you
connect with your own keys. No server of the maintainers sees it. The
repo will hold names from meetings and CRM exports, so keep it private
and treat it like your CRM ([github-settings.md](github-settings.md),
`data/README.md`).

**How do I get later improvements from the template?** Add the template
as a second remote and check out only the machinery paths from a released
version; your strategy, content and memory never come back from it
([make-it-yours.md](make-it-yours.md)).

**I am the only person. Does the review workflow still make sense?** Yes,
with `review.self_merge` set to true, so your own merge counts as the
approval. You still read the diff; nothing merges on its own
([workflow.md](workflow.md)).

**Do I need Node.js?** Only if you turn on the DataForSEO MCP server,
which runs through `npx`. Everything else is Python 3.9 or newer from the
standard library, and the GitHub CLI for one login.

**Is Calven required?** No. Calven maintains the template and makes the
marketing context layer described in
[../integrations/context-layer.md](../integrations/context-layer.md); the
repo works without it, with the strategy files in Markdown, and says so
wherever the layer is mentioned.

**Can an agency use it?** One repository per client, from the same
template, and the agency's own playbook as the skills it changes across
all of them. [is-this-for-you.md](is-this-for-you.md) has the agency
profile and what to watch for.
