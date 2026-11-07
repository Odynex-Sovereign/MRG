from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.models import DBSubscription, DBMeteredUsage
from app.models.billing import UsageMeter, SubscriptionTier

class DBBillingManager:
    async def get_tenant_subscription(self, db: AsyncSession, tenant_id: str) -> DBSubscription:
        """
        Retrieves real-time subscription details for a specific client tenant.
        """
        result = await db.execute(select(DBSubscription).where(DBSubscription.tenant_id == tenant_id))
        return result.scalars().first()

    async def log_usage(self, db: AsyncSession, usage: UsageMeter):
        """
        Persists exact infrastructure consumption metrics to the ledger table.
        """
        db_usage = DBMeteredUsage(
            tenant_id=usage.tenant_id,
            session_id=usage.session_id,
            simulation_minutes=usage.simulation_minutes,
            deepseek_tokens=usage.deepseek_tokens,
            riva_audio_seconds=usage.riva_audio_seconds
        )
        db.add(db_usage)
        await db.flush()

db_billing_manager = DBBillingManager()
