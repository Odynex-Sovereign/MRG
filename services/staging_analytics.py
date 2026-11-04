import logging
import asyncpg
from typing import Dict, Any
from app.config import settings

logger = logging.getLogger("mrg.services.staging_analytics")

class StagingAnalyticsEngine:
    """
    Manages high-throughput metrics ingestion from a dedicated staging database pool.
    Feeds real-time traffic, conversion funnels, and revenue metrics to front-end tracking arrays.
    """
    def __init__(self, database_url: str):
        self.db_url = database_url
        self.pool = None

    async def initialize_pool(self):
        """Initializes an asynchronous connection pool to your staging environment."""
        try:
            self.pool = await asyncpg.create_pool(dsn=self.db_url, min_size=2, max_size=10)
            logger.info("✅ Connected to live staging analytics database pool smoothly.")
        except Exception as e:
            logger.error(f"❌ Failed to connect to staging analytics DB: {str(e)}")
            raise e

    async def fetch_real_time_metrics(self) -> Dict[str, Any]:
        """Queries the staging database to pull real-time client acquisition metrics."""
        if not self.pool:
            return {"error": "Staging pool uninitialized."}
            
        async with self.pool.acquire() as conn:
            # Aggregate automated scraper hits, API token usage, and marketplace splits
            traffic_stats = await conn.fetchrow(
                "SELECT COUNT(*) as total_clicks, "
                "COUNT(CASE WHEN conversion_value > 0 THEN 1 END) as active_conversions "
                "FROM growth_loops;"
            )
            
            revenue_stats = await conn.fetchrow(
                "SELECT COALESCE(SUM(ledger_balance), 0.00) as treasury_balance "
                "FROM billing_vault WHERE wallet_type = 'system_treasury';"
            )
            
            clicks = traffic_stats["total_clicks"] if traffic_stats else 0
            conversions = traffic_stats["active_conversions"] if traffic_stats else 0
            conversion_rate = round((conversions / clicks) * 100, 2) if clicks > 0 else 0.00
            
            return {
                "live_traffic_clicks": clicks,
                "active_conversions": conversions,
                "conversion_rate_percentage": conversion_rate,
                "accumulated_revenue_usd": float(revenue_stats["treasury_balance"]) if revenue_stats else 0.00
            }

    async def close_pool(self):
        """Gracefully closes the connection pool during server teardown."""
        if self.pool:
            await self.pool.close()
            logger.info("🔒 Staging analytics database pool closed safely.")
