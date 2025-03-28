"""
User Management domain repository interfaces.

This module defines the repository interfaces (ports) for the User Management domain
following the Ports and Adapters pattern.
"""

from abc import abstractmethod
from typing import List, Optional, Protocol
from uuid import UUID

from app.domain.common.base import Repository
from app.domain.user_management.entities import User, UserProfile


class UserRepository(Repository[User, UUID], Protocol):
    """Repository interface for User entities."""

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get a user by username.

        Args:
            username: The username to search for

        Returns:
            The user if found, None otherwise
        """
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by email.

        Args:
            email: The email to search for

        Returns:
            The user if found, None otherwise
        """
        pass

    @abstractmethod
    async def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get a list of users with pagination.

        Args:
            skip: Number of users to skip
            limit: Maximum number of users to return

        Returns:
            List of users
        """
        pass

    @abstractmethod
    async def search_users(
        self, query: str, skip: int = 0, limit: int = 100
    ) -> List[User]:
        """Search for users by username, email, or full name.

        Args:
            query: The search query
            skip: Number of users to skip
            limit: Maximum number of users to return

        Returns:
            List of matching users
        """
        pass


class UserProfileRepository(Repository[UserProfile, UUID], Protocol):
    """Repository interface for UserProfile entities."""

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> Optional[UserProfile]:
        """Get a user profile by user ID.

        Args:
            user_id: The ID of the user

        Returns:
            The user profile if found, None otherwise
        """
        pass
