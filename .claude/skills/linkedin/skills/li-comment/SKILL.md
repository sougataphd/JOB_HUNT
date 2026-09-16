---
name: li-comment
description: >-
  Draft a comment on someone else's LinkedIn post — fetches the post body via
  Apify if given a URL (falls back to asking the user to paste it), drafts a
  thoughtful, specific comment in the user's voice, humanized. Use for
  networking outreach to researchers, hiring managers, or people at target
  companies: "comment on this post: <url>". Never posts without explicit
  approval on the exact text and target.
---

# li-comment

Comments on someone else's post. In a job search this is the highest-signal
low-cost networking move — a specific, substantive comment on a target
company's or researcher's post gets you seen by people you couldn't
otherwise reach.

## Flow

1. **Get the post.** If given a URL: try
   `lib.fetch_post(url)` (from `../../lib`). Returns `None` if `APIFY_TOKEN`
   isn't set or the post is private/unavailable — in that case ask the user
   to paste the post text. Never guess at post content.
2. **Read the post for what it actually is** — a launch, a hire, a research
   result, a hot take — and pick one of nine comment types (agree-and-extend,
   respectful disagreement, ask a real question, add a data point, share a
   parallel experience, etc.). Never "Great post!" or "So true!".
3. **One sharp insight beats three vague ones.** 200-350 characters. If the
   user has domain knowledge relevant to the post (from their resume/CV in
   this repo), use it — but don't claim expertise they don't have.
4. **Humanize it** via `li-human/humanize.py`.
5. **Render the approval card** (`lib.render_approval_card(kind="comment",
   preview_text=..., target_url=url)`) and wait for an explicit yes.
6. On yes: `lib.publish("comment", text, url, post_urn=parsed["post_urn"],
   platform_id=...)` — use `lib.parse_linkedin_url(url)` from `../../lib`
   to get `post_urn`. Prints a copy-paste block instead if Publora isn't
   connected.

## Rules

- Never fabricate familiarity with the author or their work.
- No "Congrats on the milestone!" filler — say what's actually notable.
- If the post is more than a few days old or already has hundreds of
  comments, say so — a comment there won't be seen; suggest a fresher target
  instead of drafting into the void.
