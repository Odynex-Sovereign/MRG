import os
import asyncpg
from fastapi import HTTPException

DATABASE_URL = os.getenv("DATABASE_URL")

async def get_db_pool():
    try:
        pool = await asyncpg.create_pool(
            DATABASE_URL,
            min_size=5,
            max_size=20,
            command_timeout=5.0
        )
        return pool
    except Exception as e:
        raise RuntimeError(f"Failed to securely spin up Postgres client pool: {e}")

async def verify_developer_key(pool, hashed_key: str) -> dict:
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT k.user_id, u.account_role, k.rate_limit_per_minute 
            FROM developer_api_keys k
            JOIN users u ON k.user_id = u.user_id
            WHERE k.hashed_secret_token = $1 AND (k.expires_at IS NULL OR k.expires_at > CURRENT_TIMESTAMP)
            """,
            hashed_key
        )
        if not row:
            raise HTTPException(status_code=403, detail="Invalid or expired developer credential.")
        return dict(row)
