---
name: li-human
description: >-
  Strip AI tells out of any LinkedIn draft (or any text): invisible
  characters, em dashes, curly quotes, and 113 stock words/phrases, then
  score what's left on five heuristics (0-100). Runs locally, no API calls,
  no uploads. Every draft from li-post/li-comment runs through this
  automatically. Use directly when asked to "humanize this" or "check this
  for AI tells".
---

# li-human

Two zero-dependency Python scripts, from
[Jake Schincariol's linkedin-agent-skill](https://github.com/Jakeschincariol/linkedin-agent-skill)
(MIT). Nothing leaves your machine.

```bash
python3 humanize.py draft.txt --report      # clean it, show every change
python3 detect.py draft.txt                  # score it, five checks
python3 detect.py before.txt after.txt       # prove the delta
```

**Fixed automatically:** invisible/zero-width characters, em/en dash and
curly-quote typography, 113-term slop lexicon (`slop.json` — delve,
leverage, robust, seamless, "in today's fast-paced world", etc.), URLs left
untouched.

**Flagged, not auto-fixed** (needs judgment): "it's not just X, it's Y",
rule-of-three triads, one-word rhetorical questions, hashtag walls, uniform
sentence length. Rewrite these yourself.

**Five checks, 0-100, higher is more human:** BURSTINESS (sentence-length
variation), SPECIFICITY (numbers/names per 100 words), SLOP DENSITY
(lexicon hits), FINGERPRINT (invisible chars/em dashes/curly quotes per
1,000), VOICE (contractions, person, structural tells). Verdict weights the
mean 60% and the weakest single check 40% — a detector only needs one
signal to fire.

**What this is not:** these are local heuristics modeled on the signals
public detectors key on (GPTZero, Originality, Copyleaks, etc.) — not those
detectors themselves, and not a claim of "undetectable". Fixing what they
measure tends to move those numbers because they're measuring the same
underlying things; that's the whole claim.

Every skill in this bundle (`li-post`, `li-comment`) runs its draft through
`humanize.py` before showing it to you, and reports the `detect.py` score in
the approval card.
