---
name: li-plan
description: >-
  Build a weekly LinkedIn plan for an active job search: what to post, when,
  and a specific list of people to engage with — researchers in the user's
  field, people at target companies pulled from JOB_HUNT's tracked
  applications, and recruiters. Writes ~/.claude/linkedin/plan.md. Use for
  "plan my LinkedIn week", "who should I engage with", "networking plan".
---

# li-plan

The weekly plan that turns the other skills into a routine instead of
one-off drafts.

## Flow

1. **Pull job-search context.** If this repo's JOB_HUNT data is available
   (tracked applications, target companies, resume/CV), use it: which
   companies is the user actively applying to, what domain/role are they
   targeting. Ask directly if that data isn't accessible from this session.
2. **Ask for the researcher/field angle** if not already known: what
   field/subfield, and any specific researchers or labs the user wants to
   stay visible to (this matters for research-adjacent roles where
   engagement with a specific research community is itself a signal).
3. **Build the week:**
   - 2-4 post slots (`li-post` topics): a project update, a reaction to
     something in the target domain, an open-to-work signal if wanted — each
     with a suggested day/time and hook formula from `li-post/hooks.json`.
   - 8-10 people to engage with (`li-comment` targets): mix of researchers
     in the field, people at the 3-5 companies the user is most actively
     targeting, and 1-2 recruiters — with *why* each one, not just a name.
     If `APIFY_TOKEN` is set, `lib.fetch_post` can pull a target's recent
     post to ground a comment in something real rather than a cold "Great
     work!".
4. **Write `~/.claude/linkedin/plan.md`** with the week's slate. Overwrite
   only after showing the plan and getting a yes — this file drives what
   `li-post`/`li-comment` draft next, so a bad overwrite loses the week.
5. This skill only plans and writes a local file — it never posts or
   comments on its own. Each planned item still goes through `li-post` or
   `li-comment`'s own approval gate when the user is ready to act on it.

## Rules

- Never invent a "target company" or "researcher" the user hasn't
  confirmed — pull from their real tracked applications/CV or ask.
- Recruiters go on the list by name only if the user names them; otherwise
  list the *type* of recruiter to look for (e.g. "technical recruiter at
  [target company]") and let the user supply names.
