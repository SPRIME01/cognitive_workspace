"""
Configuration settings for the Cognitive Workspace backend.
"""
import os
from typing import List

from pydantic import BaseSettings, PostgresDsn, AnyHttpUrl, validator, Field


class Settings(BaseSettings):
    """Application settings."""

    # API
    API_PREFIX: str = "/api/v1"

    # CORS
    CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[AnyHttpUrl]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str) and not v.startswith("["):
            return [origin.strip() for origin in v.split(",")]
        if isinstance(v, list):
            return v
        raise ValueError(v)

    # Database
    DATABASE_URL: PostgresDsn = Field(
        default="postgresql://postgres:postgres@localhost:5432/cognitive_workspace"
    )

    # MongoDB
    MONGODB_URI: str = Field(
        default="mongodb://localhost:27017/cognitive_workspace"
    )

    # Authentication
    SECRET_KEY: str = Field(default="development_secret_key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Environment
    ENVIRONMENT: str = Field(default="development")
    DEBUG: bool = Field(default=True)

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        case_sensitive = True


settings = Settings()
