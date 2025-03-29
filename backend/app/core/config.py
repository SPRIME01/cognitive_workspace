"""
Application configuration settings.
"""

from typing import Optional
from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Cognitive Workspace"

    # Security
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database
    DATABASE_URL: str = Field(..., env="DATABASE_URL")

    # CORS
    BACKEND_CORS_ORIGINS: list = ["*"]

    # OpenAI
    OPENAI_API_KEY: Optional[str] = Field(None, env="OPENAI_API_KEY")

    # Storage
    STORAGE_PROVIDER: str = "local"  # Options: local, s3, azure
    STORAGE_BUCKET_NAME: Optional[str] = None

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)


# Create global settings object
settings = Settings()
