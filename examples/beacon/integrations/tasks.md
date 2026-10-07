# tasks.md: where tasks go and how to file them

Every agent that creates a task reads this file first and follows it exactly.
This file is the single adapter between this repo and the team's task tool:
change the tool by changing this file, and every skill follows.

## Current tool

**In-repo checklists, by choice.** Three people do the marketing work and
every project already has a `status.md` they read weekly; a separate tool
would be one more place to look. We revisit this when the team grows past
five or a project needs tasks shared with sales.

- File a project's tasks in the `## Tasks` checklist of that project's
  `status.md` (`projects/<name>/status.md`, or
  `projects/<campaign>/<project>/status.md` for a campaign's child), one
  `- [ ]` line per task, with the owner in parentheses and a date only
  when one was decided.
- A task for the whole campaign goes in the campaign's own `status.md`.
- File tasks that belong to no project in `memory/decision-log.md`'s
  follow-ups line for the decision that spawned them.
- Marco Silva's outbound tasks live in HubSpot; agents never create them
  there.

## Rules for every agent, whatever the tool

1. One task = one imperative sentence, with an owner when known. No task
   soup.
2. Always link back to the source: the transcript, brief, or decision that
   spawned the task.
3. Creating tasks is fine; completing, deleting, or reassigning them needs a
   human.
4. Report what you filed: list the created tasks in your summary so the human
   can verify.
