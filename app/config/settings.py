# app/config/settings.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    ENABLE_BORROW: bool = True
    ENABLE_RETURN: bool = True
    ENABLE_BOOKS: bool = True
    ENABLE_USERS: bool = True
    ENABLE_CACHE: bool = True
    CACHE_EXPIRE: int = 60  # seconds
    DEBUG: bool = True
    API_RATE_LIMIT: int = 100  # requests per minute

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Global settings instance
settings = Settings()