# Discourse (source token `discourse`; category `community`)

Route (from `integrations/catalog/community.json`): the stdio server
`discourse` (`@discourse/mcp` pinned to 0.3.1, Node 24 or newer) with
`--site` the forum URL and `--profile` a JSON file outside the repo
holding the API key pair (Admin > API > New key, read-only scopes). Writes
are off unless `--allow_writes` is passed; never add it to a committed
entry. A public forum needs no profile at all. With the profile on the
machine the server runs headless, so this role can run unattended.

## Tools

Names as of 0.3.1, confirm in the session's tool list: a search tool
(Discourse search syntax: `after:YYYY-MM-DD`, `category:`, `status:unsolved`,
`order:latest`), a read-topic tool (posts of one topic, paged), category
and tag listing, a user lookup, and a Data Explorer tool when the plugin
is installed and the key allows it. Search paged to the end is the
weekly pull; topic reads are for classification only.

Data Explorer, when present, does the whole week in one query:

```sql
SELECT t.id, t.created_at::date AS date, c.name AS channel, t.title,
       t.reply_count AS replies, t.views,
       (t.id IN (SELECT topic_id FROM topic_custom_fields
                 WHERE name = 'accepted_answer_post_id')) AS answered,
       t.last_posted_at::date AS last_reply
FROM topics t JOIN categories c ON c.id = t.category_id
WHERE t.last_posted_at >= :start AND t.archetype = 'regular' AND NOT t.deleted_at IS NOT NULL
ORDER BY t.last_posted_at DESC
```

## Mapping to the threads snapshot

| Column | From |
| --- | --- |
| `thread_id` | topic `id` |
| `date` | `created_at` |
| `channel` | category name (slug when the name has commas) |
| `title` | topic `title` |
| `replies` | `reply_count` (or `posts_count - 1`) |
| `views` | `views` |
| `answered` | yes when the topic has an accepted answer (Solved plugin) or a staff reply; else no |
| `last_reply` | `last_posted_at` |
| `url` | `<site>/t/<slug>/<id>` |

Usernames, avatars and post text stay out of the snapshot; a private
category is included only when the team said so.

## Limits and cost

- The API allows on the order of 60 requests per minute per user key
  and a larger per-IP budget; search pages 50 topics at a time, so a
  week on a busy forum is a few dozen calls.
- Topic reads return 20 posts per page; read the first post only for
  classification.
- Cost: none beyond the forum's hosting.

## Export fallback

Admin > Plugins > Data Explorer > run the query above > Download CSV, or
Admin > Reports for the counts alone. Drop at
`data/social/snapshots/YYYY-MM-DD-discourse-threads.csv` with the columns
above.
