# ==========================================================================
# PURPOSE: CONFIG SETTINGS
# ==========================================================================
# IMPORTS & MODULE LOADING
# ==========================================================================
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


# ==========================================================================
# CLASSES / DATA STRUCTURE: Settings
# ==========================================================================
class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Template"
    ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: list[str] = ["http://localhost:5173"]

    SUPABASE_URL: str = ""
    SUPABASE_JWT_SECRET: str = ""
    AUTH_DEV_BYPASS: bool = False
    AUTH_DEV_USER_ID: str = "dev-user-123"
    AUTH_DEV_USER_EMAIL: str = "dev@example.com"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# ==========================================================================
# MAIN SETTINGS
# ==========================================================================
@lru_cache(maxsize=3)
def get_settings() -> Settings:
    settings = Settings()
    return settings


settings = get_settings()
