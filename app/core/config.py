import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "MRG Simulation Grid"
    API_V1_STR: str = "/api/v1"
    
    POSTGRES_SERVER: str = Field(default="localhost")
    POSTGRES_USER: str = Field(default="postgres")
    POSTGRES_PASSWORD: str = Field(default="postgres")
    POSTGRES_DB: str = Field(default="mrg_db")
    POSTGRES_PORT: str = Field(default="5432")
    
    DEEPSEEK_API_KEY: str = Field(default="mock_key")
    NVIDIA_RIVA_URL: str = Field(default="localhost:50051")
    AUDIO2FACE_URL: str = Field(default="localhost:50052")
    
    STRIPE_SECRET_KEY: str = Field(default="sk_test_placeholder")
    STRIPE_WEBHOOK_SECRET: str = Field(default="whsec_placeholder")
    DOMAIN_URL: str = Field(default="https://fly.dev")
    
    # Finalized Live Production Utility Rates
    RATE_PER_MINUTE: float = 1.50          # $1.50 per simulation compute minute
    RATE_PER_AUDIO_SEC: float = 0.04       # $0.04 per real-time voice synthesis second
    RATE_PER_1K_TOKENS: float = 0.05       # $0.05 per 1,000 processed DeepSeek tokens

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = Settings()
