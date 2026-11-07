import datetime
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from mrg.core.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserSubscription(Base):
    __tablename__ = "user_subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True, nullable=False)
    stripe_customer_id = Column(String, unique=True, index=True, nullable=True)
    stripe_subscription_id = Column(String, unique=True, index=True, nullable=True)
    plan_tier = Column(String, default="Free")
    status = Column(String, default="active")
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    simulations = relationship("SimulationRun", back_populates="user")

class SimulationRun(Base):
    __tablename__ = "simulation_runs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("user_subscriptions.user_id"), nullable=False)
    scenario_type = Column(String, default="Global Macro")
    peak_vocal_stress = Column(Float, default=0.0)
    final_stability_index = Column(Float, default=100.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("UserSubscription", back_populates="simulations")

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
