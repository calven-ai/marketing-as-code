---
name: new-project
description: Scaffold a project or campaign folder in projects/. Use when the team starts a new initiative, campaign, launch, event, or any body of work with a goal and deliverables. Creates the folder from the template and wires tasks per the task adapter.
---

# New project (or campaign)

## Procedure

1. **Ask the one structural question** if unclear: is this a single project,
   part of an existing campaign (which folder?), or a campaign that will
   contain several projects?
2. **Create the folder** from `projects/_template/`:
   - Single project → `projects/<slug>/` with `brief.md` + `status.md`.
   - Project in a campaign → `projects/<campaign>/<slug>/`, and add a row to
     the campaign's `campaign.md` projects table.
   - New campaign → `projects/<slug>/` with `campaign.md`, then scaffold its
     child projects the same way.
3. **Fill the brief with the human**, not with placeholders: goal with a
   number (defined per `data/ontology/metrics.md` — if the metric is
   undefined, flag it), audience per `strategy/icp-personas.md`,
   deliverables as `content/` paths (scaffold them via `new-content` if
   asked).
4. **Tasks**: read `integrations/tasks.md` and set the project up in the
   team's task tool per its rules (or start the checklist in `status.md` on
   the fallback). Link the task-tool project in the brief.

## Rules

- The slug is the campaign name everywhere (`data/ontology/naming.md`) —
  same slug in the task tool, UTMs, and this folder.
- Never put content or data files in the project folder (AGENTS.md rule 5).
