#!/usr/bin/env python3
"""Apply SQL migrations in order."""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

MIGRATIONS_DIR = Path(__file__).parent / "migrations"


async def run() -> None:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL not set — skipping migrations (sandbox mode).")
        return

    try:
        import asyncpg
    except ImportError:
        print("asyncpg not installed", file=sys.stderr)
        sys.exit(1)

    pool = await asyncpg.create_pool(database_url, min_size=1, max_size=2)
    try:
        async with pool.acquire() as conn:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    filename TEXT PRIMARY KEY,
                    applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
                """
            )
            applied = {
                row["filename"]
                for row in await conn.fetch("SELECT filename FROM schema_migrations")
            }
            files = sorted(MIGRATIONS_DIR.glob("*.sql"))
            for path in files:
                if path.name in applied:
                    print(f"skip {path.name}")
                    continue
                sql = path.read_text(encoding="utf-8")
                async with conn.transaction():
                    await conn.execute(sql)
                    await conn.execute(
                        "INSERT INTO schema_migrations (filename) VALUES ($1)",
                        path.name,
                    )
                print(f"applied {path.name}")
    finally:
        await pool.close()


if __name__ == "__main__":
    asyncio.run(run())
