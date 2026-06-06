from functools import lru_cache
from typing import Optional

from pydantic import ConfigDict, field_validator, model_validator
from pydantic_settings import BaseSettings

_INSECURE_DEFAULTS = {"change-me-in-production", "secret", ""}


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = ConfigDict(env_file=".env", case_sensitive=True)

    # ===== CORE =====
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_PORT: int = 8000
    API_HOST: str = "0.0.0.0"

    # ===== DATABASE =====
    DATABASE_URL: str = "sqlite:///./trendhunter.db"
    DATABASE_ECHO: bool = False
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10
    AUTO_CREATE_TABLES: bool = True

    # ===== REDIS =====
    REDIS_URL: str = "redis://localhost:6379/0"

    # ===== QDRANT =====
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION_NAME: str = "trends"
    QDRANT_VECTOR_SIZE: int = 1536

    # ===== LLM =====
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4"
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 2000

    # ===== AUTHENTICATION =====
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    SUPABASE_SECRET_KEY: str = ""
    JWT_SECRET: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ===== SECURITY =====
    SECRET_KEY: str = "change-me-in-production"
    CORS_ORIGINS: str = "http://localhost:3000"

    # ===== EXTERNAL APIS =====
    REDDIT_CLIENT_ID: str = ""
    REDDIT_CLIENT_SECRET: str = ""
    REDDIT_USER_AGENT: str = "TrendHunter/1.0"
    PRODUCTHUNT_TOKEN: str = ""
    YOUTUBE_API_KEY: str = ""
    GITHUB_TOKEN: str = ""
    NEWSAPI_KEY: str = ""
    HACKERNEWS_API_URL: str = "https://hacker-news.firebaseio.com/v0"
    HACKERNEWS_DEFAULT_LIMIT: int = 20

    # ===== EMAIL =====
    RESEND_API_KEY: str = ""
    SENDER_EMAIL: str = "noreply@trendhunter.io"

    # ===== BILLING =====
    STRIPE_SECRET_KEY: str = ""
    STRIPE_PUBLISHABLE_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""

    # ===== ANALYTICS =====
    PLAUSIBLE_DOMAIN: str = "trendhunter.io"
    ANALYTICS_ENABLED: bool = True

    # ===== CELERY =====
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    CELERY_WORKER_CONCURRENCY: int = 4

    # ===== FEATURES =====
    ENABLE_AGENT_SCHEDULING: bool = True
    ENABLE_VECTOR_SEARCH: bool = True
    ENABLE_PDF_REPORTS: bool = True
    ENABLE_SLACK_ALERTS: bool = False

    # ===== DATA RETENTION =====
    TREND_RETENTION_DAYS: int = 90
    LOG_RETENTION_DAYS: int = 30
    SESSION_TIMEOUT_MINUTES: int = 60

    # ===== RATE LIMITING =====
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 3600  # 1 hour

    # ===== AGENTS =====
    AGENT_EXECUTION_TIMEOUT: int = 300  # 5 minutes
    AGENT_MAX_RETRIES: int = 3
    AGENT_BATCH_SIZE: int = 50

    # ===== LOGGING =====
    LOG_LEVEL: str = "INFO"
    SENTRY_DSN: Optional[str] = None
    ENABLE_STRUCTURED_LOGGING: bool = True

    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug_flag(cls, value):
        """Accept common deployment values that leak into local shells."""
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"release", "production", "prod"}:
                return False
        return value

    @model_validator(mode="after")
    def reject_insecure_secrets_in_production(self) -> "Settings":
        if self.ENVIRONMENT == "production":
            if self.JWT_SECRET in _INSECURE_DEFAULTS:
                raise ValueError("JWT_SECRET must be set to a strong secret in production")
            if self.SECRET_KEY in _INSECURE_DEFAULTS:
                raise ValueError("SECRET_KEY must be set to a strong secret in production")
        return self

    # ===== DEVELOPMENT =====
    MOCK_LLM_RESPONSES: bool = False
    SEED_DATABASE: bool = False

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from string."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    @property
    def is_production(self) -> bool:
        """Check if environment is production."""
        return self.ENVIRONMENT == "production"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
