from sqlalchemy import Column, String, Integer, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class DBSubscription(Base):
    __tablename__ = "mrg_subscriptions"

    tenant_id = Column(String, primary_key=True, index=True)
    tier_name = Column(String, default="Developer")
    max_seats = Column(Integer, default=5)
    current_seats_used = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DBMeteredUsage(Base):
    __tablename__ = "mrg_metered_usage"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(String, index=True)
    session_id = Column(String)
    simulation_minutes = Column(Float)
    deepseek_tokens = Column(Integer)
    riva_audio_seconds = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

class DBUserSession(Base):
    __tablename__ = "mrg_user_sessions"

    session_token = Column(String, primary_key=True, index=True)
    tenant_id = Column(String, index=True)
    user_email = Column(String, index=True)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False)
