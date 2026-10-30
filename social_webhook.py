"""Deprecated compatibility shim.

This module is kept only for backwards compatibility during migration.
The canonical implementation lives at `services/streaming/social_webhook.py`.
"""

from services.streaming.social_webhook import SocialAutomationHook

__all__ = ["SocialAutomationHook"]
