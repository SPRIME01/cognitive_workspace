"""
User schemas for API requests and responses.
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    """Base User schema."""

    email: EmailStr
    name: str = Field(None)
    is_active: bool = True


class UserCreate(UserBase):
    """Schema for User creation."""

    password: str


class UserUpdate(BaseModel):
    """Schema for User updates."""

    email: EmailStr = None
    name: str = None
    password: str = None


class UserResponse(UserBase):
    """Schema for User responses."""

    id: str
    model_config = ConfigDict(from_attributes=True)
