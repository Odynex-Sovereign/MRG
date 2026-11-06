from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment and .env files."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = "MRG — Integrated Simulation Suite"
    environment: Literal["development", "staging", "production", "test"] = "development"
    debug: bool = False
    public_base_url: str = "http://localhost:8000"
    port: int = 8000
    secret_key: str = Field(
        default="dev-secret-change-me",
        min_length=16,
    )
    cors_origins: str = "http://localhost:8000,http://127.0.0.1:8000"
    database_url: str | None = None
    deepseek_api_key: str | None = None
    nvidia_nim_api_key: str | None = None
    stripe_secret_key: str | None = None
    stripe_webhook_secret: str | None = None
    stripe_publishable_key: str | None = None
    admin_api_token: str | None = None
    rate_limit_rpm: int = 120
    enable_websocket_simulation: bool = True
    enable_demo_checkout: bool = True
    log_level: str = "INFO"

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _strip_cors(cls, value: str | None) -> str:
        if value is None:
            return ""
        return value.strip()

    @property
    def cors_origin_list(self) -> list[str]:
        if not self.cors_origins or self.cors_origins.strip() == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def has_database(self) -> bool:
        return bool(self.database_url)

    @property
    def has_deepseek(self) -> bool:
        return bool(self.deepseek_api_key)

    @property
    def billing_configured(self) -> bool:
        return bool(self.stripe_secret_key and self.stripe_secret_key.startswith(("sk_", "rk_")))


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
