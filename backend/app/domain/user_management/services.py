"""
User Management domain services.

This module defines the domain services for the User Management domain.
Domain services implement operations that don't naturally fit into entities
or value objects.
"""

from abc import ABC, abstractmethod
from typing import Optional, Protocol
from uuid import UUID

from app.domain.common.base import DomainService
from app.domain.user_management.entities import User
from app.domain.user_management.repositories import UserRepository


class AuthenticationService(DomainService, Protocol):
    """Domain service for authenticating users."""

    @abstractmethod
    async def authenticate(
        self, username_or_email: str, password: str
    ) -> Optional[User]:
        """Authenticate a user with username/email and password.

        Args:
            username_or_email: The username or email of the user
            password: The password to check

        Returns:
            The authenticated user if successful, None otherwise
        """
        pass

    @abstractmethod
    async def generate_password_reset_token(self, email: str) -> Optional[str]:
        """Generate a password reset token for a user.

        Args:
            email: The email of the user

        Returns:
            The reset token if the user exists, None otherwise
        """
        pass

    @abstractmethod
    async def reset_password(self, token: str, new_password: str) -> bool:
        """Reset a user's password using a reset token.

        Args:
            token: The password reset token
            new_password: The new password to set

        Returns:
            True if the password was reset successfully, False otherwise
        """
        pass


class DefaultAuthenticationService(AuthenticationService):
    """Default implementation of the authentication service."""

    def __init__(self, user_repository: UserRepository):
        """Initialize the authentication service.

        Args:
            user_repository: The repository for accessing users
        """
        self.user_repository = user_repository

    async def authenticate(
        self, username_or_email: str, password: str
    ) -> Optional[User]:
        """Authenticate a user with username/email and password.

        Args:
            username_or_email: The username or email of the user
            password: The password to check

        Returns:
            The authenticated user if successful, None otherwise
        """
        # Try to find the user by username or email
        user = await self.user_repository.get_by_username(username_or_email)
        if user is None:
            user = await self.user_repository.get_by_email(username_or_email)

        # Check if user exists and password is correct
        if user is not None and user.password.verify(password):
            # Record the login
            user.record_login()
            await self.user_repository.save(user)
            return user

        return None

    async def generate_password_reset_token(self, email: str) -> Optional[str]:
        """Generate a password reset token for a user.

        Args:
            email: The email of the user

        Returns:
            The reset token if the user exists, None otherwise
        """
        # Implementation would include token generation logic
        # This is a simplified version
        user = await self.user_repository.get_by_email(email)
        if user is None:
            return None

        # In a real implementation, we would generate a secure token,
        # store it with an expiration time, and send it to the user's email
        return f"reset-token-{user.id}"

    async def reset_password(self, token: str, new_password: str) -> bool:
        """Reset a user's password using a reset token.

        Args:
            token: The password reset token
            new_password: The new password to set

        Returns:
            True if the password was reset successfully, False otherwise
        """
        # Implementation would validate the token and reset the password
        # This is a simplified version
        # In a real implementation, we would look up the token,
        # check if it's valid and not expired, and then reset the password

        # For demonstration purposes only
        if token.startswith("reset-token-"):
            try:
                user_id = UUID(token.replace("reset-token-", ""))
                user = await self.user_repository.get_by_id(user_id)
                if user:
                    # In a real application, we would bypass the current password check
                    # Here we're using a dummy current password for simplicity
                    user.change_password("dummy-current-password", new_password)
                    await self.user_repository.save(user)
                    return True
            except ValueError:
                pass

        return False


class RegistrationService(DomainService, Protocol):
    """Domain service for registering new users."""

    @abstractmethod
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
        pass


class DefaultRegistrationService(RegistrationService):
    """Default implementation of the registration service."""

    def __init__(self, user_repository: UserRepository):
        """Initialize the registration service.

        Args:
            user_repository: The repository for accessing users
        """
        self.user_repository = user_repository

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
        # Check if username is already taken
        existing_user = await self.user_repository.get_by_username(username)
        if existing_user is not None:
            raise ValueError(f"Username '{username}' is already taken")

        # Check if email is already taken
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user is not None:
            raise ValueError(f"Email '{email}' is already registered")

        # Create new user
        user = User.create(username, email, password, full_name)

        # Save user to repository
        await self.user_repository.save(user)

        return user
