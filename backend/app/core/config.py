"""
Application configuration settings.
"""

from typing import Optional
from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings.

    All settings are loaded from environment variables.
    Required variables must be set in the .env file or system environment.
    """

    # API Settings
    API_V1_STR: str = Field(default="/api/v1", description="API version path prefix")
    PROJECT_NAME: str = Field(default="Cognitive Workspace", description="Project name")

    # Security
    SECRET_KEY: str = Field(
        ...,  # Required field
        description="Secret key for JWT token generation",
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30, description="Minutes until access token expires"
    )

    # Database
    DATABASE_URL: str = Field(
        ...,  # Required field
        description="Database connection string",
    )

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = Field(
        default=["*"], description="List of allowed CORS origins"
    )

    # OpenAI
    OPENAI_API_KEY: Optional[str] = Field(
        default=None, description="OpenAI API key for AI features"
    )

    # Storage
    STORAGE_PROVIDER: str = Field(
        default="local", description="Storage provider (local, s3, azure)"
    )
    STORAGE_BUCKET_NAME: Optional[str] = Field(
        default=None, description="Storage bucket name for cloud providers"
    )

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "case_sensitive": True}


# Create global settings object
settings = Settings()
