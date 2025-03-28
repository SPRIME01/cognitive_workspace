"""
User Management application service.

This module defines the application service for the User Management domain.
Application services coordinate the use of domain objects to fulfill use cases.
"""

from typing import List, Optional
from uuid import UUID

from app.domain.common.events import get_event_bus
from app.domain.user_management.entities import User, UserProfile
from app.domain.user_management.events import (
    UserRegisteredEvent,
    UserAuthenticationSucceededEvent,
    UserAuthenticationFailedEvent,
)
from app.domain.user_management.repositories import (
    UserRepository,
    UserProfileRepository,
)
from app.domain.user_management.services import (
    AuthenticationService,
    RegistrationService,
)


class UserApplicationService:
    """Application service for user management functionality."""

    def __init__(
        self,
        user_repository: UserRepository,
        user_profile_repository: UserProfileRepository,
        authentication_service: AuthenticationService,
        registration_service: RegistrationService,
    ):
        """Initialize the user application service.

        Args:
            user_repository: Repository for user entities
            user_profile_repository: Repository for user profile entities
            authentication_service: Service for user authentication
            registration_service: Service for user registration
        """
        self.user_repository = user_repository
        self.user_profile_repository = user_profile_repository
        self.authentication_service = authentication_service
        self.registration_service = registration_service
        self.event_bus = get_event_bus()

    async def register_user(
        self, username: str, email: str, password: str, full_name: str
    ) -> User:
        """Register a new user.

        Args:
            username: The username for the new user
            email: The email for the new user
            password: The password for the new user
            full_name: The full name of the new user

        Returns:
            The newly created user

        Raises:
            ValueError: If the username or email is already taken
        """
        # Use the domain service to register the user
        user = await self.registration_service.register_user(
            username, email, password, full_name
        )

        # Publish event
        await self.event_bus.publish(UserRegisteredEvent(user.id, username, email))

        return user

    async def authenticate_user(
        self, username_or_email: str, password: str, ip_address: str
    ) -> Optional[User]:
        """Authenticate a user.

        Args:
            username_or_email: The username or email of the user
            password: The password to check
            ip_address: The IP address of the request

        Returns:
            The authenticated user if successful, None otherwise
        """
        # Use the domain service to authenticate the user
        user = await self.authentication_service.authenticate(
            username_or_email, password
        )

        # Publish appropriate event
        if user:
            await self.event_bus.publish(UserAuthenticationSucceededEvent(user.id))
        else:
            await self.event_bus.publish(
                UserAuthenticationFailedEvent(username_or_email, ip_address)
            )

        return user

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Get a user by ID.

        Args:
            user_id: The ID of the user

        Returns:
            The user if found, None otherwise
        """
        return await self.user_repository.get_by_id(user_id)

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get a user by username.

        Args:
            username: The username to search for

        Returns:
            The user if found, None otherwise
        """
        return await self.user_repository.get_by_username(username)

    async def get_user_profile(self, user_id: UUID) -> Optional[UserProfile]:
        """Get a user profile by user ID.

        Args:
            user_id: The ID of the user

        Returns:
            The user profile if found, None otherwise
        """
        return await self.user_profile_repository.get_by_user_id(user_id)

    async def update_user_profile(
        self,
        user_id: UUID,
        full_name: Optional[str] = None,
        email: Optional[str] = None,
    ) -> Optional[User]:
        """Update a user's profile.

        Args:
            user_id: The ID of the user
            full_name: New full name, if provided
            email: New email, if provided

        Returns:
            The updated user if found, None otherwise
        """
        user = await self.user_repository.get_by_id(user_id)
        if user is None:
            return None

        user.update_profile(full_name, email)
        return await self.user_repository.save(user)

    async def change_user_password(
        self, user_id: UUID, current_password: str, new_password: str
    ) -> bool:
        """Change a user's password.

        Args:
            user_id: The ID of the user
            current_password: The current password
            new_password: The new password

        Returns:
            True if the password was changed successfully, False otherwise
        """
        user = await self.user_repository.get_by_id(user_id)
        if user is None:
            return False

        try:
            user.change_password(current_password, new_password)
            await self.user_repository.save(user)
            return True
        except ValueError:
            return False

    async def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get a list of users with pagination.

        Args:
            skip: Number of users to skip
            limit: Maximum number of users to return

        Returns:
            List of users
        """
        return await self.user_repository.list_users(skip, limit)

    async def search_users(
        self, query: str, skip: int = 0, limit: int = 100
    ) -> List[User]:
        """Search for users.

        Args:
            query: The search query
            skip: Number of users to skip
            limit: Maximum number of users to return

        Returns:
            List of matching users
        """
        return await self.user_repository.search_users(query, skip, limit)

    async def activate_user(self, user_id: UUID) -> Optional[User]:
        """Activate a user.

        Args:
            user_id: The ID of the user

        Returns:
            The updated user if found, None otherwise
        """
        user = await self.user_repository.get_by_id(user_id)
        if user is None:
            return None

        user.activate()
        return await self.user_repository.save(user)

    async def deactivate_user(self, user_id: UUID) -> Optional[User]:
        """Deactivate a user.

        Args:
            user_id: The ID of the user

        Returns:
            The updated user if found, None otherwise
        """
        user = await self.user_repository.get_by_id(user_id)
        if user is None:
            return None

        user.deactivate()
        return await self.user_repository.save(user)
