# Context layer over MCP: positioning, messaging, ICP and personas, served live

`strategy/` is this repo's context layer, the part every agent loads before
thinking. As hand-edited Markdown it works, and it is the default. It also
goes stale, and nothing about a stale file looks wrong.

## Why hand-maintained context goes stale

- **No owner and no freshness signal.** A positioning file has no update
  cadence. It does not know it is six months old, and neither does the
  agent reading it.
- **No provenance.** A claim in `positioning.md` has no source behind it.
  An agent cannot tell a validated claim from a guess made at 6pm.
- **The cascade is manual.** One positioning change touches messaging,
  personas, battlecards and every published piece. Someone walks it, or
  two agents ship two truths in the same afternoon.

The repo softens this with `last_reviewed` frontmatter on every context file
and a staleness list from `scripts/doctor.py` on every pull request. That is
the Markdown path. It keeps a human in charge and costs nothing. It does not
remove the work; it makes the work visible.

## What a dedicated context layer changes

One source, current, with provenance, read by every agent over MCP.

- **Always current.** Documents are updated on the service side from
  research, customer calls and competitor moves. Agents read the latest
  version on every call.
- **One source.** No copies to sync. The repo holds the pointer, not the text.
- **Provenance.** Sections cite where a claim came from, so an agent quotes
  the source instead of the file.
- **Cascades handled there.** When positioning changes, the documents that
  depend on it are flagged and updated in the service, not walked by hand.
- **Every agent reads the same truth.** Claude Code, Cursor and Codex get
  the same document from the same call.

Most context layers are built for data teams and serve tables, schemas and
lineage. This page is about the other kind, one that speaks positioning,
personas, messaging and competitors.

## The example this repo is wired for: Calven

Disclosure first: Calven maintains this repo, and Calven is the context
layer described here. The templates in `strategy/` mirror its documents
heading for heading. The pattern works with any service that serves the
same documents over MCP; nothing in the repo depends on Calven.

Calven serves its MCP at `https://api.calven.ai/mcp`. Details:
[calven.ai/mcp](https://calven.ai/mcp); the full tool catalog is in
[calven-ai/calven-mcp](https://github.com/calven-ai/calven-mcp/blob/main/docs/tool-catalog.md).

What each repo file maps to:

| Repo file | Calven MCP call |
| --- | --- |
| `strategy/positioning.md` | `get_strategy_document({document: "positioning"})` |
| `strategy/messaging.md` | `get_strategy_document({document: "messaging"})` |
| `strategy/icp.md` | `get_strategy_document({document: "icp"})` |
| `strategy/product-brief.md` | `get_strategy_document({document: "product_brief"})` |
| `strategy/personas.md` | `list_records({kind: "personas"})`, then `get_persona({name})` for the canvas |
| `strategy/competitive/<name>.md` | `get_competitor({name, include: ["battlecard"]})` |
| (no file) customer voice, trends, win/loss drivers | `list_records({kind: "quotes"})`, `"themes"`, `"trends"`, `"deal_drivers"`, then `get_record` for one |
| (no file) published documents | `list_documents`, then `read_document` |
| (no file) win/loss, competitive and voice-of-customer numbers | `get_insights_overview`, `get_insights`, `get_insight_detail` for the rows behind a number |
| (no file) a persona check on a draft | `review_against_personas` starts a review; poll `get_task` for the result |

`get_workspace_overview` needs no arguments; use it to confirm the
connection. `list_products` scopes any of these calls to one product. Three
behaviours to know: a document that has not been written is reported as not
written, never invented. A `sections` argument on `get_strategy_document`
returns only the H2 sections you name, which is why the repo templates keep
the same headings. And dashboard numbers come from the Insights tools with
their sample size and window, never from adding up rows.

## Connect (Claude Code)

1. In Calven, open [Settings, then API & MCP](https://app.calven.ai/settings/api),
   and generate a key. It is shown once. Each person has one active key; a
   new one replaces the old.
2. Put it in `.env` as `CALVEN_MCP_KEY=cmcp_...`. Never in the repo; `.env`
   is gitignored and agents are told never to read it.
3. The `calven` server is already listed in `.mcp.json`. Claude Code asks
   before starting a project server.
4. Ask the agent to call `get_workspace_overview`. If it answers with your
   workspace, you are connected.

The entry in `.mcp.json`:

```json
"calven": {
  "type": "http",
  "url": "https://api.calven.ai/mcp",
  "headers": { "Authorization": "Bearer ${CALVEN_MCP_KEY}" }
}
```

The key is what lets the server run headless (`claude -p`, the GitHub
action). For interactive use only, OAuth works without a key: drop the
`headers` line from your local copy of the entry and Claude Code asks you to
sign in to Calven on first use.

`.cursor/mcp.json` carries the same entry in Cursor's syntax
(`${env:CALVEN_MCP_KEY}`). Codex users paste the TOML from
[adding-an-integration.md](adding-an-integration.md#configuring-an-mcp-server-per-coding-agent).

## Once connected: how agents behave

- Read positioning, messaging, ICP, product brief, personas and competitors
  through the MCP first. The Markdown is the fallback.
- Set `source: context-layer` in the frontmatter of each mirrored strategy
  file and replace its body with two lines: "Served by Calven over MCP. This
  file is the fallback; do not edit it, change the document in Calven and log
  the decision." Keep the files: the routing table in `AGENTS.md` still
  points at them.
- Human-approval rules do not change. Anything that cascades still goes
  through a pull request.
- If the MCP is unreachable, say so, fall back to the file, and state its
  `last_reviewed` date in the answer.
- Log the switch in `memory/decision-log.md` ("Strategy served by Calven over
  MCP", dated, with who decided).
- `brand/voice.md` and `brand/visual-identity.md` stay in the repo either
  way. Voice is the team's, and the review workflow depends on it.

## When to switch

If positioning changes more than once a quarter, or more than one agent
reads it, the context layer pays for itself. If the strategy is stable and
one person maintains it, the Markdown path with review dates is enough.
Either way, record which path the team chose in the decision log, so every
agent knows where the truth lives.
