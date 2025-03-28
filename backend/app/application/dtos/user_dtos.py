"""
Data Transfer Objects (DTOs) for the User Management domain.

These DTOs facilitate data exchange between the application and presentation layers.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Set
from pydantic import BaseModel, Field, EmailStr


class UserRole(str, Enum):
    """User role enumeration for API representation."""

    REGULAR = "regular"
    PROJECT_OWNER = "project_owner"
    ADMINISTRATOR = "administrator"
    SYSTEM_ADMINISTRATOR = "system_administrator"


class UserCreate(BaseModel):
    """DTO for creating a new user."""

    username: str = Field(
        ...,
        min_length=3,
        max_length=30,
        pattern=r"^[a-zA-Z0-9_.]{3,30}$",
        description="Username for the new user (3-30 alphanumeric characters, dots, underscores)",
        example="john_doe",
    )
    email: EmailStr = Field(
        ..., description="Email address of the user", example="john.doe@example.com"
    )
    password: str = Field(
        ...,
        min_length=8,
        description="Password for the new user (min 8 chars)",
        example="SecureP@ssw0rd",
    )
    full_name: str = Field(
        ..., min_length=1, description="Full name of the user", example="John Doe"
    )


class UserLogin(BaseModel):
    """DTO for user login."""

    username_or_email: str = Field(
        ...,
        description="Username or email of the user",
        example="john_doe or john.doe@example.com",
    )
    password: str = Field(..., description="User's password", example="SecureP@ssw0rd")


class UserResponse(BaseModel):
    """DTO for user data returned in API responses."""

    id: str = Field(
        ...,
        description="Unique identifier for the user",
        example="123e4567-e89b-12d3-a456-426614174000",
    )
    username: str = Field(..., description="Username of the user", example="john_doe")
    email: EmailStr = Field(
        ..., description="Email address of the user", example="john.doe@example.com"
    )
    full_name: str = Field(..., description="Full name of the user", example="John Doe")
    roles: List[UserRole] = Field(
        default=[UserRole.REGULAR],
        description="Roles assigned to the user",
        example=["regular"],
    )
    is_active: bool = Field(
        True, description="Whether the user account is active", example=True
    )
    created_at: datetime = Field(
        ..., description="When the user was created", example="2023-01-01T00:00:00Z"
    )
    last_login: Optional[datetime] = Field(
        None, description="When the user last logged in", example="2023-01-02T12:34:56Z"
    )


class UserProfileResponse(BaseModel):
    """DTO for user profile data returned in API responses."""

    id: str = Field(
        ...,
        description="Unique identifier for the profile",
        example="223e4567-e89b-12d3-a456-426614174000",
    )
    user_id: str = Field(
        ...,
        description="User ID that this profile belongs to",
        example="123e4567-e89b-12d3-a456-426614174000",
    )
    bio: Optional[str] = Field(
        None,
        description="User's biography",
        example="Software engineer with 10 years of experience",
    )
    avatar_url: Optional[str] = Field(
        None,
        description="URL to the user's avatar image",
        example="https://example.com/avatars/john_doe.jpg",
    )
    preferences: dict = Field(
        default_factory=dict,
        description="User preferences as key-value pairs",
        example={"theme": "dark", "notifications": "email"},
    )


class UserProfileUpdate(BaseModel):
    """DTO for updating user profile information."""

    bio: Optional[str] = Field(
        None,
        description="User's biography",
        example="Software engineer with 10 years of experience",
    )
    avatar_url: Optional[str] = Field(
        None,
        description="URL to the user's avatar image",
        example="https://example.com/avatars/john_doe.jpg",
    )


class UserUpdate(BaseModel):
    """DTO for updating user information."""

    full_name: Optional[str] = Field(
        None, description="Full name of the user", example="John Doe"
    )
    email: Optional[EmailStr] = Field(
        None, description="Email address of the user", example="john.doe@example.com"
    )


class PasswordChange(BaseModel):
    """DTO for changing a user's password."""

    current_password: str = Field(
        ..., description="User's current password", example="OldSecureP@ssw0rd"
    )
    new_password: str = Field(
        ...,
        min_length=8,
        description="User's new password (min 8 chars)",
        example="NewSecureP@ssw0rd",
    )


class PasswordReset(BaseModel):
    """DTO for resetting a forgotten password."""

    token: str = Field(
        ...,
        description="Password reset token",
        example="reset-token-123e4567-e89b-12d3-a456-426614174000",
    )
    new_password: str = Field(
        ...,
        min_length=8,
        description="User's new password (min 8 chars)",
        example="NewSecureP@ssw0rd",
    )


class TokenResponse(BaseModel):
    """DTO for authentication token response."""

    access_token: str = Field(
        ...,
        description="JWT access token",
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    )
    token_type: str = Field("bearer", description="Token type", example="bearer")
    expires_in: int = Field(
        ..., description="Token expiration time in seconds", example=3600
    )
    refresh_token: Optional[str] = Field(
        None,
        description="JWT refresh token",
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    )
