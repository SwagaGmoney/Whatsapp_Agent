from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # === API Keys ===
    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str = "gpt-4o-mini" 
    TWILIO_ACCOUNT_SID: str | None = None
    TWILIO_AUTH_TOKEN: str | None = None
    TWILIO_WHATSAPP_NUMBER: str | None = None

    # === Infrastructure ===
    REDIS_URL: str = "redis://localhost:6379/0"
    POSTGRES_URL: str | None = None

    # === Qdrant ===
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str | None = None
    QDRANT_COLLECTION_NAME: str = "ats_policies"

    # === Presidio ===
    PRESIDIO_ANALYZER_URL: str | None = None
    PRESIDIO_ANONYMIZER_URL: str | None = None
    PII_ENCRYPTION_KEY: str | None = None

    # === Rate Limiting ===
    RATE_LIMIT_COUNT: int = 10
    RATE_LIMIT_WINDOW: int = 300

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore"
    }


@lru_cache()
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()


settings = get_settings()

if "://qdrant" in settings.QDRANT_URL:
    settings.QDRANT_URL = "http://127.0.0.1:6333"