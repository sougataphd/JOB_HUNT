"""Shared helpers for the JOB_HUNT LinkedIn skill.

Public surface (everything in `__all__`) is what skills import.
"""
from ._env import load_env
from .url_parser import parse_linkedin_url
from .approval import render_approval_card

load_env()

from .backend_selector import (
    active_backend,
    manual_mode_message,
    publish,
    fetch_post,
    fetch_profile,
)

# The two HTTP clients import `requests`, which manual-tier (draft-only)
# users are not required to install. Load them on first attribute access
# (PEP 562) so `import lib` keeps working with no dependencies at all.
_LAZY_CLIENTS = {
    "PubloraClient": "publora_client",
    "PubloraError": "publora_client",
    "ApifyClient": "apify_client",
    "ApifyError": "apify_client",
}


def __getattr__(name: str):
    module = _LAZY_CLIENTS.get(name)
    if module is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    from importlib import import_module

    value = getattr(import_module(f".{module}", __name__), name)
    globals()[name] = value
    return value


__all__ = [
    "parse_linkedin_url",
    "PubloraClient",
    "PubloraError",
    "ApifyClient",
    "ApifyError",
    "render_approval_card",
    "active_backend",
    "manual_mode_message",
    "publish",
    "fetch_post",
    "fetch_profile",
]
