import secrets
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.models import DBUserSession

class UserSessionManager:
    async def create_session(
        self, db: AsyncSession, tenant_id: str, user_email: str, ip: str = None, ua: str = None, lifetime_hours: int = 24
    ) -> DBUserSession:
        """
        Generates a secure cryptographically random session token and logs the login event.
        """
        token = secrets.token_urlsafe(32)
        expiry = datetime.utcnow() + timedelta(hours=lifetime_hours)
        
        db_session = DBUserSession(
            session_token=token,
            tenant_id=tenant_id,
            user_email=user_email,
            ip_address=ip,
            user_agent=ua,
            expires_at=expiry
        )
        db.add(db_session)
        await db.flush()
        return db_session

    async def validate_session(self, db: AsyncSession, token: str) -> bool:
        """
        Checks if a given session token is active, unexpired, and unrevoked.
        """
        result = await db.execute(
            select(DBUserSession).where(DBUserSession.session_token == token)
        )
        db_session = result.scalars().first()
        
        if not db_session or db_session.is_revoked or db_session.expires_at < datetime.utcnow():
            return False
        return True

    async def revoke_session(self, db: AsyncSession, token: str) -> bool:
        """
        Revokes a session immediately (handles logouts or security terminations).
        """
        result = await db.execute(
            select(DBUserSession).where(DBUserSession.session_token == token)
        )
        db_session = result.scalars().first()
        if db_session:
            db_session.is_revoked = True
            return True
        return False

session_manager = UserSessionManager()
