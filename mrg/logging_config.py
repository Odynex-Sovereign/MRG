"""Application logging configuration."""

from __future__ import annotations

import logging


def setup_logging(settings) -> None:
    """Configure structured logging for the MRG service."""
    logging.basicConfig(
        level=getattr(logging, str(settings.log_level).upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
