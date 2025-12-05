
from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "VitaAvanza Backend"
    API_V1_STR: str = "/api"
    BACKEND_CORS_ORIGINS: list[str] = ["*"]  # override in production
    DATABASE_URL: str = "sqlite:///./vitaavanza.db"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    JWT_SECRET_KEY: str = "CHANGE_ME_SUPER_SECRET"  # override via env
    JWT_ALGORITHM: str = "HS256"

    OPENAI_API_KEY: str | None = None

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache
def get_settings() -> Settings:
    return Settings()
