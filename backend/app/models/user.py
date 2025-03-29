"""
User model for the Cognitive Workspace application.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class User(BaseModel):
    """User model."""

    id: str
    email: str
    name: Optional[str] = None
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)
