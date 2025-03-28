"""
Dependency injection utilities for the application.

This module provides dependency injection functions for FastAPI dependency injection system.
"""
from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.core.config import settings
from app.domain.user_management.entities import User
from app.infrastructure.persistence.database import get_db
from app.infrastructure.persistence.repositories.user_repository import (
    SQLAlchemyUserRepository,
    SQLAlchemyUserProfileRepository,
)
from app.domain.user_management.services import (
    DefaultAuthenticationService,
    DefaultRegistrationService,
)
from app.application.services.user_service import UserApplicationService

# OAuth2 token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/auth/login")


def get_user_repository(db: Session = Depends(get_db)) -> SQLAlchemyUserRepository:
    """Get a User repository instance.

    Args:
        db: Database session

    Returns:
        SQLAlchemy implementation of UserRepository
    """
    return SQLAlchemyUserRepository(db)


def get_user_profile_repository(db: Session = Depends(get_db)) -> SQLAlchemyUserProfileRepository:
    """Get a UserProfile repository instance.

    Args:
        db: Database session

    Returns:
        SQLAlchemy implementation of UserProfileRepository
    """
    return SQLAlchemyUserProfileRepository(db)


def get_authentication_service(
    user_repository: SQLAlchemyUserRepository = Depends(get_user_repository),
) -> DefaultAuthenticationService:
    """Get an authentication service instance.

    Args:
        user_repository: User repository

    Returns:
        Default implementation of AuthenticationService
    """
    return DefaultAuthenticationService(user_repository)


def get_registration_service(
    user_repository: SQLAlchemyUserRepository = Depends(get_user_repository),
) -> DefaultRegistrationService:
    """Get a registration service instance.

    Args:
        user_repository: User repository

    Returns:
        Default implementation of RegistrationService
    """
    return DefaultRegistrationService(user_repository)


def get_user_service(
    user_repository: SQLAlchemyUserRepository = Depends(get_user_repository),
    user_profile_repository: SQLAlchemyUserProfileRepository = Depends(get_user_profile_repository),
    authentication_service: DefaultAuthenticationService = Depends(get_authentication_service),
    registration_service: DefaultRegistrationService = Depends(get_registration_service),
) -> UserApplicationService:
    """Get a user application service instance.

    Args:
        user_repository: User repository
        user_profile_repository: UserProfile repository
        authentication_service: Authentication service
        registration_service: Registration service

    Returns:
        UserApplicationService instance
    """
    return UserApplicationService(
        user_repository=user_repository,
        user_profile_repository=user_profile_repository,
        authentication_service=authentication_service,
        registration_service=registration_service,
    )


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repository: SQLAlchemyUserRepository = Depends(get_user_repository),
) -> User:
    """Get the current authenticated user from the JWT token.

    Args:
        token: JWT token from Authorization header
        user_repository: User repository

    Returns:
        The current authenticated user

    Raises:
        HTTPException: If the token is invalid or the user doesn't exist
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the JWT token
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Get the user from the repository
    user = await user_repository.get_by_id(user_id)
    if user is None:
        raise credentials_exception

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    return user
