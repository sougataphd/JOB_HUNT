# Third-party notices

This skill bundle adapts code and content from two MIT-licensed projects:

- **[Jakeschincariol/linkedin-agent-skill](https://github.com/Jakeschincariol/linkedin-agent-skill)**
  by Jake Schincariol ([opusjake.ai](https://opusjake.ai)) — `skills/li-human/`
  (`humanize.py`, `detect.py`, `slop.json`), `skills/li-post/hooks.json`,
  `skills/li-profile/rubric.json`, `templates/voice.md`. Copied with minor
  path/README edits.

- **[sergebulaev/linkedin-skills](https://github.com/sergebulaev/linkedin-skills)**
  by Serge Bulaev / Creative Content Crafts — `lib/` (`_env.py`,
  `url_parser.py`, `approval.py`, `apify_client.py`, `publora_client.py`,
  `backend_selector.py`, `__init__.py`). Adapted: added `fetch_profile` /
  `fetch_profile()` helper to `apify_client.py` and `backend_selector.py`;
  dropped the Pixfaro (image-generation) tier as out of scope here.

Both source repos are MIT licensed. See each repo's own `LICENSE` file.
