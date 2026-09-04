# Decision log

Append-only, newest on top: a new entry goes directly below the `---`
separator, above the previous newest entry. Every entry follows this format:

```markdown
## YYYY-MM-DD: [decision in one imperative-free sentence]

- **Decided by:** [who]
- **Source:** [meeting/transcript path, PR, or discussion link]
- **Context:** [the problem and the options weighed, 1 to 3 sentences]
- **Follow-ups:** [tasks filed per integrations/tasks.md, or "none"]
```

An agent may append entries (the `log-decision` and `chief-of-staff` skills
do); nothing here is ever edited or deleted. A reversed decision gets a new
entry that references the old one.

---

## 2026-09-04: The marketer's lifecycle is three commands, and the GitHub CLI is the agent's way to GitHub

- **Decided by:** David Kolinek (repository maintainer)
- **Source:** the "lifecycle for people who never open a terminal" pull request, after shipping the docs rewrite by hand showed the gap
- **Context:** shipping a change meant knowing git and gh. The lifecycle is now five words, Sync. Work. Propose. Review. Merge., with doctor as the repair word, and three commands carry it: `/sync`, `/propose`, `/doctor`. "What is waiting on me" is the last paragraph of `/sync`, not a fourth command. `/propose` pushes and opens the proposal without a second question; saying it is the consent. The agent reaches GitHub through the GitHub CLI logged in as the person; without it, `/propose` still pushes and prints the link to open the proposal by hand, and GitHub Desktop remains the no-agent path. The four lifecycle scripts run without a permission prompt; the deny rules on merge, force-push and `.env` stay, and the scripts are tested never to do what they forbid. A repository with one maintainer sets `review.self_merge` so the gate does not wait for a second person; it goes back to `false` when one joins.
- **Follow-ups:** none

## 2026-09-03: Bot keys live in a GitHub environment only main can use; the gate runs from main; the agent in Actions gets no shell

- **Decided by:** David Kolinek (repository maintainer)
- **Source:** the "Security hardening" pull request and its review of keys, tokens, MCP servers and unattended runs
- **Context:** the repo will be run by marketers with no guaranteed developer, connected to several MCP servers and APIs. Three choices settled how keys and unattended runs work. Keys: each person makes their own vendor key and keeps it in their own `.env` and vault item; the three bot keys (Granola, the Slack bot, the Anthropic key) are made once by the integrations owner and live only in the GitHub environment `automation`, restricted to `main`, never in repository secrets (readable by any branch) and never on a laptop. Codespaces as a way to hand shared keys to local sessions was considered and rejected. Auto-merge of bookkeeping proposals is kept, but the gate that decides it now runs from `main` (`gate.yml`), the machinery paths are never bookkeeping, and `check.yml` runs a proposal's code read-only. The agent in Actions keeps working, with no shell, no network and no Slack token; Slack gets a pointer to the proposal, and a person posts the summary after review.
- **Follow-ups:** the integrations owner runs `sh scripts/github_setup.sh`, adds the three environment secrets, and replaces `@owner-placeholder` in `.github/CODEOWNERS` via `/setup`; turn on secret scanning and push protection (Team plan add-on for a private repo); every clone runs `git config core.hooksPath scripts/hooks` once; on the first `transcripts-process.yml` run, confirm the agent commits through the action's tool with bypass mode disabled.
