"""
Dependency injection functions for the FastAPI application.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from typing import Generator, Optional

from app.core.config import settings
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Validate access token and return current user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # This is a placeholder for actual JWT validation and user retrieval
        # In a real application, you would:
        # 1. Decode the JWT token
        # 2. Validate the token claims
        # 3. Look up the user in the database
        # 4. Return the user object

        # Placeholder for demo purposes
        user = User(
            id="user_id",
            email="user@example.com",
            name="Test User",
            is_active=True
        )
        return user
    except (JWTError, ValidationError):
        raise credentials_exception


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Check if the current user is active.
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user
