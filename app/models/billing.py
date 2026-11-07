from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UsageMeter(BaseModel):
    tenant_id: str
    session_id: str
    simulation_minutes: float
    deepseek_tokens: int
    riva_audio_seconds: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class SubscriptionTier(BaseModel):
    tenant_id: str
    tier_name: str = "Developer"  # Developer, Growth, Enterprise
    max_seats: int = 5
    current_seats_used: int = 1
    is_active: bool = True
    usage_limit_reached: bool = False
