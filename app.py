"""Compatibility entrypoint for the canonical MRG FastAPI app."""

from mrg.main import app, create_app

__all__ = ["app", "create_app"]
