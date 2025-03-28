"""
User model for the Cognitive Workspace application.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    """User model."""

    id: str
    email: str
    name: Optional[str] = None
    is_active: bool = True

    class Config:
        """Pydantic configuration."""

        orm_mode = True
