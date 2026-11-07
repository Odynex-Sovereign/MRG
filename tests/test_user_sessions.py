import pytest
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import SessionLocal, engine
from app.database.models import Base
from app.services.session_manager import session_manager

@pytest.mark.asyncio
async def test_user_session_lifecycle():
    """
    Ensures that session rows migrate cleanly, generate cryptographic keys,
    pass validation gates, and respond to logout cancellation triggers.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, checkfirst=True)

    async with SessionLocal() as session:
        tenant = "beta_test_enterprise"
        email = "executive_user@beta.com"
        
        # 1. Test Session Creation
        db_sess = await session_manager.create_session(
            session, tenant_id=tenant, user_email=email, ip="127.0.0.1", ua="pytest-agent"
        )
        assert db_sess.session_token is not None
        token = db_sess.session_token
        await session.commit()

        # 2. Test Validation Gate (Should Pass)
        is_valid = await session_manager.validate_session(session, token)
        assert is_valid is True

        # 3. Test Session Revocation / Logout Execution
        revoked = await session_manager.revoke_session(session, token)
        assert revoked is True
        await session.commit()

        # 4. Test Validation Post-Revocation (Should Fail)
        is_valid_after = await session_manager.validate_session(session, token)
        assert is_valid_after is False

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
