"""Application configuration via environment variables."""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration loaded from environment / .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "MRG Integrated Simulation Suite"
    app_version: str = "1.2.0"
    environment: str = Field(default="development", description="development|staging|production")
    debug: bool = False
    log_level: str = "INFO"
    log_format: str = "json"  # json | text

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1
    root_path: str = ""

    # CORS
    cors_origins: list[str] = Field(default_factory=lambda: ["*"])
    cors_allow_credentials: bool = True

    # Database
    database_url: str | None = None
    db_pool_min_size: int = 2
    db_pool_max_size: int = 10
    db_command_timeout: float = 5.0

    # External AI providers (optional — sandbox mode works without them)
    nvidia_nim_api_key: str | None = None
    deepseek_api_key: str | None = None
    deepseek_base_url: str = "https://api.deepseek.com"
    deepseek_model: str = "deepseek-chat"
    deepseek_timeout_seconds: float = 30.0

    # Streaming / media
    livepeer_api_key: str | None = None
    social_automation_webhook_url: str | None = None

    # Stripe / billing (optional)
    stripe_secret_key: str | None = None
    stripe_webhook_secret: str | None = None
    stripe_publishable_key: str | None = None

    # Security
    api_key_header: str = "X-API-Key"
    rate_limit_per_minute: int = 120
    max_ws_connections_per_ip: int = 20
    max_message_size_bytes: int = 65_536
    trusted_hosts: list[str] = Field(default_factory=lambda: ["*"])

    # Observability
    enable_metrics: bool = True
    metrics_path: str = "/metrics"
    sentry_dsn: str | None = None

    # Feature flags
    admin_api_token: str | None = None
    enable_billing: bool = False
    enable_sensory: bool = True
    sandbox_mode: bool = True  # True when no external keys configured

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors(cls, v):
        if isinstance(v, str):
            if v.strip() == "*":
                return ["*"]
            return [o.strip() for o in v.split(",") if o.strip()]
        return v

    @field_validator("environment")
    @classmethod
    def normalize_env(cls, v: str) -> str:
        return v.lower().strip()

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
    def has_nvidia(self) -> bool:
        return bool(self.nvidia_nim_api_key)


@lru_cache
def get_settings() -> Settings:
    """Cached settings singleton."""
    return Settings()
