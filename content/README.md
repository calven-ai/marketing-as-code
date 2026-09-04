# content/

**Kind:** context, what the team knows.

The single source of truth for every piece of content, at every stage: idea,
brief, draft, published, evergreen. Email sequences, webinar assets and case
studies are content *types* here. They don't get their own top-level folders.

## Conventions (load-bearing)

- **One folder per piece**, kebab-case, e.g. `2026-09-why-plain-text-wins/`.
  Brief first (`brief.md`), draft second (`draft.md`), human review before
  anything ships. Copy [`_template/`](_template/) to start, or use the
  `new-content` skill.
- **Frontmatter on every draft** is what makes the corpus queryable:

  ```yaml
  project: projects/q4-launch/webinar   # the project that produced it ("" if none)
  status: idea | brief | draft | in-review | published | evergreen
  channel: blog | email | linkedin | webinar | ad | case-study | other
  owner: name
  published: ""                         # YYYY-MM-DD, set when status flips to published
  published_url: ""                     # once live
  ```

  The folder name carries the month the piece was *started*. `published:`
  answers "what shipped in Q3?".

- **Content lives only here.** Projects link to pieces by repo path in their
  brief's Deliverables section, and the `project:` field points back. Never
  copy a piece into a project folder.

## For agents

- "What did we ship last quarter?" Grep frontmatter for `status: published`
  with `published:` in the date range. Don't ask.
- Before drafting, load `strategy/` and `brand/`. Before marking
  `in-review`, run the `review` skill. Setting `status: published` is a
  human's call.
