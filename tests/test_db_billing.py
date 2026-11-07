import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import SessionLocal, engine
from app.database.models import Base, DBSubscription
from app.models.billing import UsageMeter
from app.services.db_billing_manager import db_billing_manager
import uuid

@pytest.mark.asyncio
async def test_database_billing_transactions():
    """
    Initializes a test environment schema, writes record entries,
    and runs asynchronous transactional verification.
    """
    # Create the tables in the database target safely
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_base, checkfirst=True)

    async with SessionLocal() as session:
        # Seed an explicit enterprise contract tenant profile
        test_tenant = "beta_test_enterprise"
        db_sub = DBSubscription(
            tenant_id=test_tenant,
            tier_name="Growth",
            max_seats=15,
            current_seats_used=3
        )
        session.add(db_sub)
        await session.commit()

        # Test Read Operation
        fetched_sub = await db_billing_manager.get_tenant_subscription(session, test_tenant)
        assert fetched_sub is not None
        assert fetched_sub.tier_name == "Growth"
        assert fetched_sub.max_seats == 15

        # Test Log Write Operation
        mock_usage = UsageMeter(
            tenant_id=test_tenant,
            session_id=str(uuid.uuid4()),
            simulation_minutes=1.5,
            deepseek_tokens=150,
            riva_audio_seconds=90.0
        )
        await db_billing_manager.log_usage(session, mock_usage)
        await session.commit()

    # Teardown the verification tables safely after tests complete
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
