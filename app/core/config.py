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
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = Settings()
