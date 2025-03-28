"""
Authentication API endpoints.

This module defines the FastAPI endpoints for authentication operations.
"""

from datetime import datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

from app.application.dtos.user_dtos import TokenResponse, UserCreate, UserResponse
from app.application.services.user_service import UserApplicationService
from app.core.config import settings
from app.core.deps import get_user_service

router = APIRouter()


def create_access_token(subject: str, expires_delta: timedelta = None) -> str:
    """Create a JWT access token.

    Args:
        subject: Subject of the token (usually user ID)
        expires_delta: Optional token expiration time

    Returns:
        Encoded JWT token
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(subject: str) -> str:
    """Create a JWT refresh token.

    Args:
        subject: Subject of the token (usually user ID)

    Returns:
        Encoded JWT token
    """
    expire = datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="User login",
    description="Authenticate a user and return access and refresh tokens",
    responses={
        200: {"description": "Successful login"},
        401: {"description": "Invalid credentials"},
    },
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserApplicationService = Depends(get_user_service),
) -> Any:
    """Login a user.

    Args:
        form_data: OAuth2 password request form
        user_service: User application service

    Returns:
        JWT tokens

    Raises:
        HTTPException: If authentication fails
    """
    # Use the user service to authenticate
    user = await user_service.authenticate_user(
        form_data.username,
        form_data.password,
        "127.0.0.1",  # IP would be from request in real app
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create tokens
    access_token = create_access_token(str(user.id))
    refresh_token = create_refresh_token(str(user.id))

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "refresh_token": refresh_token,
    }


@router.post(
    "/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Refresh access token",
    description="Use a refresh token to get a new access token",
    responses={
        200: {"description": "New access token"},
        401: {"description": "Invalid refresh token"},
    },
)
async def refresh_token(
    refresh_token: str,
    user_service: UserApplicationService = Depends(get_user_service),
) -> Any:
    """Refresh an access token.

    Args:
        refresh_token: The refresh token
        user_service: User application service

    Returns:
        New JWT tokens

    Raises:
        HTTPException: If the refresh token is invalid
    """
    try:
        # Decode the refresh token
        payload = jwt.decode(
            refresh_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )

        # Check token type
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Get the user ID
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Check that the user exists
        user = await user_service.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create new tokens
        new_access_token = create_access_token(str(user.id))
        new_refresh_token = create_refresh_token(str(user.id))

        return {
            "access_token": new_access_token,
            "token_type": "bearer",
            "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "refresh_token": new_refresh_token,
        }

    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Register a new user with the provided details",
    responses={
        201: {"description": "User created successfully"},
        400: {"description": "Invalid input or user already exists"},
    },
)
async def register(
    user_data: UserCreate,
    user_service: UserApplicationService = Depends(get_user_service),
) -> Any:
    """Register a new user.

    Args:
        user_data: User creation data
        user_service: User application service

    Returns:
        The created user

    Raises:
        HTTPException: If the user already exists or input is invalid
    """
    try:
        # Register the user
        user = await user_service.register_user(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name,
        )

        # Map user entity to response DTO
        return UserResponse(
            id=str(user.id),
            username=str(user.username),
            email=str(user.email),
            full_name=str(user.full_name),
            roles=[role.name.lower() for role in user.roles],
            is_active=user.is_active,
            created_at=user.created_at,
            last_login=user.last_login,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
