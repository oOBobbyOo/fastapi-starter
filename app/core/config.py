"""
应用配置。

所有配置项通过环境变量或 .env 文件注入，使用 pydantic-settings 进行校验。
"""

from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ---- 应用 ----
    PROJECT_NAME: str = "FastAPI Starter"
    VERSION: str = "0.1.0"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    DEBUG: bool = False

    # ---- CORS ----
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    # ---- 数据库 ----
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/app"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10
    DATABASE_ECHO: bool = False

    # ---- Redis ----
    REDIS_URL: str = "redis://localhost:6379/0"

    # ---- 安全 ----
    SECRET_KEY: str = "change-me-in-production-use-openssl-rand-hex-32"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"

    # ---- 日志 ----
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"


settings = Settings()
