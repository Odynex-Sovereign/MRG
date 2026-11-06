"""Application settings — all values configurable via environment."""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # App
    app_name: str = "MRG — Integrated Simulation Suite"
    environment: Literal["development", "staging", "production"] = "development"
    debug: bool = False
    public_base_url: str = "http://localhost:8000"
    port: int = 8000
    secret_key: str = Field(
        default="change-me-in-production-use-openssl-rand-hex-32",
        min_length=16,
    )

    # CORS
    cors_origins: str = "http://localhost:8000,http://127.0.0.1:8000"

    # Database (optional)
    database_url: str | None = None

    # Optional integrations — empty = sandbox mode
    deepseek_api_key: str | None = None
    nvidia_nim_api_key: str | None = None
    stripe_secret_key: str | None = None
    stripe_webhook_secret: str | None = None
    stripe_publishable_key: str | None = None

    # Admin
    admin_api_token: str | None = None

    # Rate limiting (requests per minute per IP)
    rate_limit_rpm: int = 120

    # Feature flags
    enable_websocket_simulation: bool = True
    enable_demo_checkout: bool = True

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _strip_cors(cls, v: str) -> str:
        return v.strip() if isinstance(v, str) else v

    @property
    def cors_origin_list(self) -> list[str]:
        if self.cors_origins.strip() == "*":
            return ["*"]
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def billing_configured(self) -> bool:
        return bool(self.stripe_secret_key and self.stripe_secret_key.startswith(("sk_", "rk_")))

    @property
    def deepseek_configured(self) -> bool:
        return bool(self.deepseek_api_key)


@lru_cache
def get_settings() -> Settings:
    return Settings()
