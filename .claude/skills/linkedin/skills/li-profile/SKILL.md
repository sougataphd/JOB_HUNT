---
name: li-profile
description: >-
  Fetch the user's own LinkedIn profile via Apify and score it against a
  12-part rubric out of 100, then rewrite the lowest-scoring sections first
  (headline, About, Featured, current role) pointed at job-search conversion
  — recruiters and hiring managers deciding whether to click through, not
  generic thought-leadership positioning. Use for "audit my LinkedIn
  profile", "score my profile", "rewrite my headline/About".
---

# li-profile

Scores and rewrites a LinkedIn profile for job-search conversion: does a
recruiter or hiring manager who lands here decide to reach out.

## Flow

1. **Fetch the profile.** Ask for the profile URL (default: the user's own,
   from their JOB_HUNT candidate profile if set up via `/setup`). Call
   `lib.fetch_profile(url_or_username)` from `../../lib`. If `APIFY_TOKEN`
   isn't set or the fetch fails, ask the user to paste headline / About /
   current-role text directly — never guess at profile content.
2. **Score against `rubric.json`** in this folder — 12 items, 100 points
   total (headline 12, about-open 10, about-body 10, featured 8, banner 6,
   photo 6, current-role 10, and five more). Score honestly; most first-pass
   profiles land in the 30s-40s. Show the score breakdown.
3. **Rewrite in fix-first order** — lowest-scoring items first. For each:
   show current text, then rewritten text, then the specific rubric gap it
   closes. Job-search framing: headline states the target role/domain and
   one proof point, not just a job title; About opens with what you're
   looking for and what you bring, not "passionate about".
4. Cross-reference the user's resume/CV in this repo (if available via the
   JOB_HUNT candidate profile) so numbers and claims in the rewrite match
   what's already documented — never invent a metric that isn't in their own
   materials.
5. **This skill never edits LinkedIn directly** — there's no API for that.
   Print the rewritten sections as copy-paste blocks for the user to paste
   into their profile themselves.

## Rules

- Full 220 characters on the headline, not the default 60.
- About body: second person to the reader's problem, one proof number, what
  to do next — under 1,400 characters.
- Never fabricate a metric, employer, or outcome not already in the user's
  own resume/profile data.
