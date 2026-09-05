# Typeform for review-monitor

Typeform fills the `surveys-reviews` category for NPS and survey responses,
not for review sites. This skill reads it when the monthly report includes
NPS; `voice-of-customer` reads it for survey synthesis. Catalog entry:
`integrations/catalog/surveys-reviews.json`.

## Connection

- Remote MCP at `https://api.typeform.com/mcp`, streamable HTTP. Two
  routes: OAuth in the browser (default, cannot run headless) or a personal
  token in `TYPEFORM_TOKEN` (the headless route; scope it to read where
  the Typeform UI allows). EU-hosted accounts use a different host; check
  the developer page before wiring.
- MCP access is plan-gated.
- The server has write tools whose names were not verified when catalogued,
  so the whole server is denied for writes until checked. This skill only
  reads.

## Tools

Check the server's tool list in the session before calling. Expect:

- list forms (find the NPS form by title);
- list responses for a form, filtered by a date range, paginated;
- an insights or summary read per form.

One responses call per form per month, paged to the end. State the count.

## Field mapping to the snapshot

`data/reviews/snapshots/YYYY-MM-DD-typeform-nps.csv`, columns
`source,form,response_id,date,score,verbatim,role,company,segment`:

| Snapshot column | Typeform field |
| --- | --- |
| `source` | `typeform` |
| `form` | form title |
| `response_id` | response token |
| `date` | submitted at, ISO |
| `score` | the 0 to 10 answer of the NPS question |
| `verbatim` | the open-text follow-up |
| `role`, `company`, `segment` | hidden fields or answers, when the form carries them |

Promoter, passive and detractor are computed at read time from the
ontology's definition, not stored. Email and name fields are dropped unless
`repo.private` is true in `docs/schema.json` and the decision log says so.

## Manual route

Typeform Results exports responses as CSV. Map the columns above and drop
the file at `data/reviews/snapshots/YYYY-MM-DD-typeform-nps.csv` (a survey
that is not NPS: `-survey.csv`).
