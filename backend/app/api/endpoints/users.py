"""
User API endpoints.

This module defines the FastAPI endpoints for user operations.
"""
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from app.application.dtos.user_dtos import (
    UserResponse,
    UserProfileResponse,
    UserUpdate,
    UserProfileUpdate,
    PasswordChange,
)
from app.application.services.user_service import UserApplicationService
from app.core.deps import get_current_user, get_user_service
from app.domain.user_management.entities import User

router = APIRouter()


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current user",
    description="Get the current authenticated user's information",
    responses={
        200: {"description": "Current user information"},
        401: {"description": "Not authenticated"},
    },
)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
) -> Any:
    """Get the current user's information.

    Args:
        current_user: Current authenticated user

    Returns:
        Current user information
    """
    return UserResponse(
        id=str(current_user.id),
        username=str(current_user.username),
        email=str(current_user.email),
        full_name=str(current_user.full_name),
        roles=[role.name.lower() for role in current_user.roles],
        is_active=current_user.is_active,
        created_at=current_user.created_at,
        last_login=current_user.last_login,
    )


@router.put(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Update current user",
    description="Update the current authenticated user's information",
    responses={
        200: {"description": "User updated successfully"},
        400: {"description": "Invalid input"},
        401: {"description": "Not authenticated"},
    },
)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    user_service: UserApplicationService = Depends(get_user_service),
) -> Any:
    """Update the current user's information.

    Args:
        user_update: User update data
        current_user: Current authenticated user
        user_service: User application service

    Returns:
        Updated user information

    Raises:
        HTTPException: If the update fails
    """
    try:
        updated_user = await user_service.update_user_profile(
            user_id=current_user.id,
            full_name=user_update.full_name,
            email=user_update.email,
        )

        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to update user",
            )

        return UserResponse(
            id=str(updated_user.id),
            username=str(updated_user.username),
            email=str(updated_user.email),
            full_name=str(updated_user.full_name),
            roles=[role.name.lower() for role in updated_user.roles],
            is_active=updated_user.is_active,
            created_at=updated_user.created_at,
            last_login=updated_user.last_login,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.put(
    "/me/password",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Change current user password",
    description="Change the current authenticated user's password",
    responses={
        204: {"description": "Password changed successfully"},
        400: {"description": "Invalid input or current password incorrect"},
        401: {"description": "Not authenticated"},
    },
)
async def change_current_user_password(
    password_change: PasswordChange,
    current_user: User = Depends(get_current_user),
    user_service: UserApplicationService = Depends(get_user_service),
) -> None:
    """Change the current user's password.

    Args:
        password_change: Password change data
        current_user: Current authenticated user
        user_service: User application service

    Raises:
        HTTPException: If the password change fails
    """
    success = await user_service.change_user_password(
        user_id=current_user.id,
        current_password=password_change.current_password,
        new_password=password_change.new_password,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )


@router.get(
    "/me/profile",
    response_model=UserProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current user profile",
    description="Get the current authenticated user's profile",
    responses={
        200: {"description": "Current user profile"},
        401: {"description": "Not authenticated"},
        404: {"description": "Profile not found"},
    },
)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
    user_service: UserApplicationService = Depends(get_user_service),
) -> Any:
    """Get the current user's profile.

    Args:
        current_user: Current authenticated user
        user_service: User application service

    Returns:
        Current user profile

    Raises:
        HTTPException: If the profile is not found
    """
    profile = await user_service.get_user_profile(current_user.id)

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )

    return UserProfileResponse(
        id=str(profile.id),
        user_id=str(profile.user_id),
        bio=profile.bio,
        avatar_url=profile.avatar_url,
        preferences=profile.preferences,
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get user by ID",
    description="Get a user by their ID",
    responses={
        200: {"description": "User information"},
        401: {"description": "Not authenticated"},
        404: {"description": "User not found"},
    },
)
async def get_user_by_id(
    user_id: str = Path(..., description="The ID of the user to get"),
    current_user: User = Depends(get_current_user),
    user_service: UserApplicationService = Depends(get_user_service),
) -> Any:
    """Get a user by ID.

    Args:
        user_id: ID of the user to get
        current_user: Current authenticated user
        user_service: User application service

    Returns:
        User information

    Raises:
        HTTPException: If the user is not found
    """
    user = await user_service.get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

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


@router.get(
    "/",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="List users",
    description="Get a paginated list of users",
    responses={
        200: {"description": "List of users"},
        401: {"description": "Not authenticated"},
    },
)
async def list_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of users to return"),
    current_user: User = Depends(get_current_user),
    user_service: UserApplicationService = Depends(get_user_service),
) -> Any:
    """List users with pagination.

    Args:
        skip: Number of users to skip
        limit: Maximum number of users to return
        current_user: Current authenticated user
        user_service: User application service

    Returns:
        List of users
    """
    users = await user_service.list_users(skip=skip, limit=limit)

    return [
        UserResponse(
            id=str(user.id),
            username=str(user.username),
            email=str(user.email),
            full_name=str(user.full_name),
            roles=[role.name.lower() for role in user.roles],
            is_active=user.is_active,
            created_at=user.created_at,
            last_login=user.last_login,
        )
        for user in users
    ]


@router.get(
    "/search/",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Search users",
    description="Search for users by username, email, or full name",
    responses={
        200: {"description": "List of matching users"},
        401: {"description": "Not authenticated"},
    },
)
async def search_users(
    query: str = Query(..., description="Search query"),
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of users to return"),
    current_user: User = Depends(get_current_user),
    user_service: UserApplicationService = Depends(get_user_service),
) -> Any:
    """Search for users.

    Args:
        query: Search query
        skip: Number of users to skip
        limit: Maximum number of users to return
        current_user: Current authenticated user
        user_service: User application service

    Returns:
        List of matching users
    """
    users = await user_service.search_users(query=query, skip=skip, limit=limit)

    return [
        UserResponse(
            id=str(user.id),
            username=str(user.username),
            email=str(user.email),
            full_name=str(user.full_name),
            roles=[role.name.lower() for role in user.roles],
            is_active=user.is_active,
            created_at=user.created_at,
            last_login=user.last_login,
        )
        for user in users
    ]
