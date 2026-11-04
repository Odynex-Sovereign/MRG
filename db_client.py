"""Database helpers for optional Postgres integration."""

from __future__ import annotations

import os
from collections.abc import AsyncIterator
from typing import Any

DATABASE_URL = os.getenv("DATABASE_URL")


async def get_db_pool():
    """Create an asyncpg pool. Raises if DATABASE_URL missing."""
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not configured")
    import asyncpg

    return await asyncpg.create_pool(
        DATABASE_URL,
        min_size=int(os.getenv("DB_POOL_MIN_SIZE", "2")),
        max_size=int(os.getenv("DB_POOL_MAX_SIZE", "10")),
        command_timeout=float(os.getenv("DB_COMMAND_TIMEOUT", "5.0")),
    )


async def get_db() -> AsyncIterator[Any]:
    """FastAPI dependency — yields None when no database is configured."""
    if not DATABASE_URL:
        yield None
        return
    pool = await get_db_pool()
    try:
        async with pool.acquire() as conn:
            yield conn
    finally:
        await pool.close()
