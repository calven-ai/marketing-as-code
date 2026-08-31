# projects/

How the team organizes the work. **Everything is a project; a campaign is a
project big enough to have children.**

```
projects/
├── q4-launch/                 # a campaign: has campaign.md + child projects
│   ├── campaign.md            #   narrative, goals, budget, timeline
│   ├── webinar/brief.md       #   a project inside the campaign
│   └── abm-push/brief.md
├── website-refresh/           # a standalone project: just a brief
│   ├── brief.md
│   └── status.md
├── _template/                 # copy me (or use the new-project skill)
└── _archive/                  # finished projects move here
```

## Conventions (load-bearing)

- A project folder holds **only project-management artifacts**: `brief.md`
  (goal, audience, deliverables, owner, dates), `status.md`, working notes.
- **No content, no data in here.** The brief's Deliverables section lists
  repo paths into `content/`; data a project produces goes to `data/`. This
  is the lifecycle-owner rule: content and data outlive the project, so they
  live where they belong and the project folder can be archived without loss.
- **Tasks live in the team's task tool**, filed per
  [`integrations/tasks.md`](../integrations/tasks.md). The brief links to the
  project there. Until a task tool is connected, keep a checklist in
  `status.md`.
- When a project closes: final `status.md` update, log outcomes worth keeping
  in `memory/decision-log.md`, then move the folder to `_archive/`.

## For agents

- "What is the team working on?" → list folders here (excluding `_archive/`),
  read each `status.md`.
- Which pieces belong to a project → its brief's Deliverables list, or grep
  `content/` frontmatter for `project: projects/<name>`.
