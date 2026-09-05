# GA4 touch and source dimensions

The pull is `snapshot-pull` (`.agents/skills/snapshot-pull/references/ga4.md`).
GA4 already holds three attribution scopes; the readout uses the scope
that matches each view and says which.

## Dimension scopes

| View | Dimensions |
| --- | --- |
| first touch (user scope) | `firstUserSource`, `firstUserMedium`, `firstUserCampaignName`, `firstUserDefaultChannelGroup`: the user's first acquisition |
| last touch (session scope) | `sessionSource`, `sessionMedium`, `sessionCampaignName`, `sessionDefaultChannelGroup`: the session that contained the conversion; GA4's session attribution is last non-direct within the lookback |
| event scope (the property's reporting model) | `source`, `medium`, `campaignName`, `defaultChannelGroup` on a key-event query: credit per the model set in Admin > Attribution settings (data-driven by default, or last click) |
| manual UTMs | `manualSource`, `manualMedium`, `manualCampaignName`, `manualContent`, `manualTerm` when raw UTM values are wanted |

Run one `run_report` per scope over the period with the key events as
metrics (`keyEvents:<event>` or `conversions`), and save each as
`data/analytics/snapshots/YYYY-MM-DD-ga4-conversions-<scope>.csv`
(`date,source,medium,campaign,event,count`). The three scopes are the
three views for the web-side of the funnel; the CRM supplies the deal
side.

## Settings that change the numbers

- Admin > Attribution settings: the reporting model (data-driven or paid
  and organic last click) and the lookback windows (30 days for
  acquisition events, 30 or 90 days for other key events; view-through 7
  days). Record both in the report's caveats.
- Data-driven attribution needs volume (Google's threshold is on the
  order of a thousand key events a month); below it GA4 falls back and
  says so in the admin page.
- Channel groups come from source and medium through GA4's default
  rules: a medium outside the recognised set lands in "Unassigned".
  `data/ontology/naming.md` decides the team's grouping; report GA4's
  label and the team's side by side when they differ.
- Thresholding hides rows on small properties when Google signals are
  on; a row count that looks low may be that, say so.

## Joining to the CRM

GA4 does not know the deal. The join is the contact's form submission
(`user_id` or the client id passed into the CRM as a hidden field) or the
UTM campaign slug matched to `data/ontology/naming.md`. Without a join
key, the web view and the deal view are reported as two tables, not
merged.
