# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str  # ✅ remove hardcoded default, must come from .env

    # Feature toggles
    ENABLE_BORROW: bool = True
    ENABLE_RETURN: bool = True

    # Optional caching
    CACHE_URL: Optional[str] = None

    # Debug mode
    DEBUG: bool = True

    # API rate limit
    API_RATE_LIMIT: int = 100

    # Pydantic config for loading .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"   # ✅ ignore unknown env vars
    )

# Singleton instance
settings = Settings()