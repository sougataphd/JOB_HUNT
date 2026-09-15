---
name: li-post
description: >-
  Write a LinkedIn post from a raw idea using proven hook formulas
  (hooks.json), in the user's own voice, humanized so it doesn't read as AI.
  Use for "post about X", "write me a LinkedIn post", "turn this into a
  LinkedIn post". Job-search context: announcing a project, a skill learned,
  reacting to a role/company, open-to-work updates. Drafts only; publishes
  via Publora only after explicit approval, otherwise prints a copy-paste
  block. Never posts without a "yes" from the user, every time.
---

# li-post

Turn one raw idea into a LinkedIn post that sounds like the person posting
it, aimed at a job search: visibility with recruiters, researchers, and
people at target companies — not generic engagement farming.

## Before you write

1. Read `~/.claude/linkedin/voice.md` if it exists (copy from
   `../../templates/voice.md` and fill it in first if not). If it doesn't
   exist, ask for three of the user's own past posts, infer the voice, and
   write the file. Never invent a voice.
2. Read `hooks.json` in this folder — 21 hook formulas with templates,
   examples, and how each one usually gets ruined.
3. If the idea is thin ("post about AI"), don't pad it. Ask one batched
   question: what happened, to whom, and what changed or cost what. A post
   needs one specific true thing.
4. If the JOB_HUNT app has tracked context relevant to the post (a target
   company, a role, a skill from the resume), you may pull it in — but never
   fabricate a metric, outcome, or company relationship that isn't in the
   user's own data.

## The shape

```
Line 1     the hook, alone — has to survive truncation (~140 chars mobile)
Line 2     the payoff of line 1, not setup for line 3
Body       short paragraphs, 1-3 lines each, blank line between every one
The turn   one line that reframes what came before
Close      one specific question, or one instruction — never both
```

900-1,300 characters is the working range. No links in the body (LinkedIn
suppresses reach) — link goes in the first comment.

## The loop

1. **Pick three hooks**, from different formulas, not three variations of
   one. State which you'd ship and why, in one sentence.
2. **Draft the full post** on the strongest hook.
3. **Humanize it.** Run the draft through `li-human/humanize.py`, then
   `detect.py` for the score. This is not optional.
4. **Render the approval card** via `lib.render_approval_card(kind="post",
   preview_text=..., char_count=...)` from `../../lib`.
5. **Wait for an explicit yes.** On yes, call `lib.publish("post", text,
   target_url, platforms=[...])`. If Publora isn't connected, this prints
   the copy-paste block instead — same call, `lib.publish` handles both. On
   anything other than a clear yes, treat it as edits requested and redraft.

## Rules

- One idea per post. Two ideas is two posts.
- Numbers over adjectives — ask for the real one, never invent it.
- No engagement bait ("Thoughts?", "Agree?").
- Three hashtags max, only real categories.
- Never fabricate a metric, client, or outcome under the user's name. Leave
  `{{your number}}` and flag it if unknown.
