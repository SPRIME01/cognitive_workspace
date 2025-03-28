"""
Configuration settings for the application.

This module defines the application settings using Pydantic's BaseSettings.
"""

from typing import List, Optional, Union
import secrets
from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    """Application settings.

    These settings can be configured using environment variables.
    """

    # API settings
    API_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Cognitive Workspace"
    DEBUG: bool = False

    # CORS settings
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "https://localhost:3000"]

    # Database settings
    DATABASE_URI: Optional[Union[str, PostgresDsn]] = (
        "postgresql://postgres:postgres@localhost:5432/cognitive_workspace"
    )
    SQL_ECHO: bool = False

    # JWT settings
    JWT_SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Security settings
    SECRET_KEY: str = secrets.token_urlsafe(32)

    class Config:
        """Pydantic config for Settings."""

        env_file = ".env"
        case_sensitive = True


# Create global settings object
settings = Settings()
