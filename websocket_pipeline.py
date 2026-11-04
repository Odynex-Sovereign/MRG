"""Backward-compatible entrypoint.

Prefer: uvicorn mrg.app:app
This module re-exports the production application so existing Docker / Fly
commands and documentation continue to work.
"""

from mrg.app import app

__all__ = ["app"]
