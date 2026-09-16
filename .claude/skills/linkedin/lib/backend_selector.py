"""Detect which publishing backend is configured and format user-facing messages.

Two tiers:

  TIER 0 — manual (default, zero setup)
    No credentials in env. Skills produce drafts; you copy and paste them
    into LinkedIn yourself. Works with nothing configured.

  TIER 1 — publora (2-min setup, opt-in)
    `PUBLORA_API_KEY` + `LINKEDIN_PLATFORM_ID` present. Skills publish on
    your explicit approval via the Publora REST API (an OAuth-connected
    publishing service — this is what actually posts; Apify only reads).
    Free tier: 15 posts/month. Sign up: https://app.publora.com/signup

`active_backend()` picks the highest-privilege available. `publish()` is
the single call every skill uses on approval — it hides tier detection so
SKILL.md files don't repeat the branch. **No skill calls `publish()` until
the user has typed an explicit yes on a rendered approval card
(`lib/approval.py`).** That gate is a convention here, not enforced by this
file — it's on every skill's SKILL.md to honor it.

Adapted from https://github.com/sergebulaev/linkedin-skills (MIT); the
Pixfaro (image-generation) tier from the upstream file is dropped here as
out of scope for job-search use.
"""
from __future__ import annotations
import os
from typing import Any, Literal, Optional

from ._env import load_env

load_env()

BackendName = Literal["publora", "manual"]
PublishKind = Literal["comment", "reply", "post", "reshare"]

PUBLORA_SIGNUP_URL = "https://app.publora.com/signup"


def resolve_reshare_parent(post: dict) -> Optional[str]:
    """Pick the reshare `parent` URN from an Apify `fetch_post` payload."""
    share = post.get("shareUrn") or ""
    if share.startswith(("urn:li:share:", "urn:li:ugcPost:")):
        return share
    urn = post.get("urn") or ""
    if urn.startswith(("urn:li:share:", "urn:li:ugcPost:")):
        return urn
    if urn.startswith("urn:li:activity:"):
        return "urn:li:share:" + urn.rsplit(":", 1)[-1]
    return None


def active_backend() -> BackendName:
    """Return the active publishing backend: publora if fully configured,
    else manual (draft-and-paste)."""
    if os.getenv("PUBLORA_API_KEY") and os.getenv("LINKEDIN_PLATFORM_ID"):
        return "publora"
    return "manual"


def _half_configured() -> str:
    key = bool(os.getenv("PUBLORA_API_KEY"))
    pid = bool(os.getenv("LINKEDIN_PLATFORM_ID"))
    if key and not pid:
        return ("\n> **Publora is half configured.** `PUBLORA_API_KEY` is set but "
                "`LINKEDIN_PLATFORM_ID` is not, so publishing stays manual.\n")
    if pid and not key:
        return ("\n> **Publora is half configured.** `LINKEDIN_PLATFORM_ID` is set but "
                "`PUBLORA_API_KEY` is not, so publishing stays manual.\n")
    return ""


def manual_mode_message(draft_text: str, target_url: str, kind: str = "comment") -> str:
    """Copy-paste output for the manual tier."""
    return f"""Approved. Copy the text below and paste it as a {kind} on LinkedIn:

```
{draft_text}
```

**Target URL:** {target_url}

---

To let me publish this myself on your next approval, connect Publora (2 min):

1. Sign up free at {PUBLORA_SIGNUP_URL} (15 LinkedIn posts/month, free tier)
2. Connect your LinkedIn account (Channels -> Add Channel)
3. Copy your API key (Settings -> API)
4. Add to `.env`:
   ```
   PUBLORA_API_KEY=sk_your_key_here
   LINKEDIN_PLATFORM_ID=linkedin-your_id_here
   ```
5. Next approved draft publishes automatically.
{_half_configured()}"""


def publish(
    kind: PublishKind,
    draft_text: str,
    target_url: str,
    **kwargs: Any,
) -> Optional[dict]:
    """Dispatch an ALREADY-APPROVED draft to the active backend.

    Callers must have rendered an approval card (lib/approval.py) and
    received an explicit yes from the user before calling this. Routes to
    publora or manual based on `active_backend()`.

    Args:
        kind: "comment" | "reply" | "post" | "reshare".
        draft_text: The approved draft body.
        target_url: Where the draft lands (post URL for comments/replies).
        **kwargs: Backend-specific payload for publora:
            - comment: post_urn, platform_id, reaction_type (optional)
            - reply:   post_urn, platform_id, parent_comment, reaction_type (optional)
            - post:    platforms, scheduled_time (optional), media_urls (optional)
            - reshare: parent, platform_id, visibility (optional)

    Returns:
        - publora: dict from PubloraClient.
        - manual: {"mode": "manual", "message": <copy-paste block>}.
    """
    backend = active_backend()

    if backend == "manual":
        return {"mode": "manual", "message": manual_mode_message(draft_text, target_url, kind=kind)}

    from .publora_client import PubloraClient

    client = PubloraClient()
    platform_id = kwargs.get("platform_id") or os.getenv("LINKEDIN_PLATFORM_ID")

    if kind in ("comment", "reply"):
        post_urn = kwargs["post_urn"]
        parent_comment = kwargs.get("parent_comment") if kind == "reply" else None
        reaction_type = kwargs.get("reaction_type")
        if reaction_type:
            try:
                react_target = parent_comment or post_urn
                client.create_reaction(
                    post_urn=react_target,
                    platform_id=platform_id,
                    reaction_type=reaction_type,
                )
            except Exception:
                pass
        return client.create_comment(
            post_urn=post_urn,
            message=draft_text,
            platform_id=platform_id,
            parent_comment=parent_comment,
        )

    if kind == "post":
        platforms = kwargs.get("platforms") or [platform_id]
        return client.create_post(
            content=draft_text,
            platforms=platforms,
            scheduled_time=kwargs.get("scheduled_time"),
            media_urls=kwargs.get("media_urls"),
        )

    if kind == "reshare":
        parent = kwargs.get("parent")
        if not parent:
            return None
        return client.create_reshare(
            parent=parent,
            platform_id=platform_id,
            commentary=draft_text or None,
            visibility=kwargs.get("visibility", "PUBLIC"),
        )

    raise ValueError(f"unknown publish kind: {kind!r}")


def fetch_post(url: str, **kwargs: Any) -> Optional[dict]:
    """Fetch a LinkedIn post body via Apify, or None if unavailable.

    Skills treat `None` as "ask the user to paste the post text":
        post = lib.fetch_post(url) or ask_user_to_paste(url)
    """
    if not os.getenv("APIFY_TOKEN"):
        return None
    try:
        from .apify_client import ApifyClient

        client = ApifyClient()
        return client.fetch_post(url, **kwargs)
    except Exception:
        return None


def fetch_profile(profile_url_or_username: str, **kwargs: Any) -> Optional[dict]:
    """Fetch a profile via Apify, or None if unavailable (no token / error)."""
    if not os.getenv("APIFY_TOKEN"):
        return None
    try:
        from .apify_client import ApifyClient

        client = ApifyClient()
        return client.fetch_profile(profile_url_or_username=profile_url_or_username, **kwargs)
    except Exception:
        return None
