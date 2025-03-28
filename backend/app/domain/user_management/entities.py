"""
User Management domain entities.

This module defines the core entities for the User Management domain.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import List, Optional, Set
from uuid import UUID, uuid4

from app.domain.common.base import AggregateRoot, DomainEvent, Entity
from app.domain.common.value_objects import Email, NonEmptyString
from app.domain.user_management.value_objects import Password, Username


class UserRole(Enum):
    """Enumeration of possible user roles in the system."""

    REGULAR = auto()
    PROJECT_OWNER = auto()
    ADMINISTRATOR = auto()
    SYSTEM_ADMINISTRATOR = auto()


class UserCreatedEvent(DomainEvent):
    """Event raised when a new user is created."""

    def __init__(self, user_id: UUID, username: str, email: str):
        """Initialize a new UserCreatedEvent."""
        super().__init__()
        self.user_id = user_id
        self.username = username
        self.email = email


class UserUpdatedEvent(DomainEvent):
    """Event raised when a user is updated."""

    def __init__(self, user_id: UUID, updated_fields: Set[str]):
        """Initialize a new UserUpdatedEvent."""
        super().__init__()
        self.user_id = user_id
        self.updated_fields = updated_fields


@dataclass
class User(AggregateRoot):
    """User entity representing a user in the system.

    This is an aggregate root for the User Management domain.
    """

    id: UUID
    username: Username
    email: Email
    password: Password
    full_name: NonEmptyString
    roles: Set[UserRole] = field(default_factory=set)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    is_active: bool = True
    _events: List[DomainEvent] = field(default_factory=list)

    @classmethod
    def create(cls, username: str, email: str, password: str, full_name: str) -> "User":
        """Create a new User.

        Factory method to ensure all required validation and domain events.

        Args:
            username: The username for the new user
            email: The email address for the new user
            password: The password for the new user
            full_name: The full name of the user

        Returns:
            A new User instance
        """
        user_id = uuid4()
        user = cls(
            id=user_id,
            username=Username(username),
            email=Email(email),
            password=Password.create(password),
            full_name=NonEmptyString(full_name),
            roles={UserRole.REGULAR},
        )

        # Add domain event
        user.add_event(UserCreatedEvent(user_id, username, email))

        return user

    def update_profile(
        self, full_name: Optional[str] = None, email: Optional[str] = None
    ) -> None:
        """Update the user's profile information.

        Args:
            full_name: New full name, if provided
            email: New email, if provided
        """
        updated_fields = set()

        if full_name is not None:
            self.full_name = NonEmptyString(full_name)
            updated_fields.add("full_name")

        if email is not None:
            self.email = Email(email)
            updated_fields.add("email")

        if updated_fields:
            self.updated_at = datetime.utcnow()
            self.add_event(UserUpdatedEvent(self.id, updated_fields))

    def change_password(self, current_password: str, new_password: str) -> None:
        """Change the user's password.

        Args:
            current_password: The current password for verification
            new_password: The new password to set

        Raises:
            ValueError: If the current password is incorrect
        """
        if not self.password.verify(current_password):
            raise ValueError("Current password is incorrect")

        self.password = Password.create(new_password)
        self.updated_at = datetime.utcnow()

        updated_fields = {"password"}
        self.add_event(UserUpdatedEvent(self.id, updated_fields))

    def record_login(self) -> None:
        """Record that the user has logged in."""
        self.last_login = datetime.utcnow()
        self.updated_at = self.last_login

    def add_role(self, role: UserRole) -> None:
        """Add a role to the user.

        Args:
            role: The role to add
        """
        if role not in self.roles:
            self.roles.add(role)
            self.updated_at = datetime.utcnow()

            updated_fields = {"roles"}
            self.add_event(UserUpdatedEvent(self.id, updated_fields))

    def remove_role(self, role: UserRole) -> None:
        """Remove a role from the user.

        Args:
            role: The role to remove
        """
        if role in self.roles:
            self.roles.remove(role)
            self.updated_at = datetime.utcnow()

            updated_fields = {"roles"}
            self.add_event(UserUpdatedEvent(self.id, updated_fields))

    def deactivate(self) -> None:
        """Deactivate the user."""
        if self.is_active:
            self.is_active = False
            self.updated_at = datetime.utcnow()

            updated_fields = {"is_active"}
            self.add_event(UserUpdatedEvent(self.id, updated_fields))

    def activate(self) -> None:
        """Activate the user."""
        if not self.is_active:
            self.is_active = True
            self.updated_at = datetime.utcnow()

            updated_fields = {"is_active"}
            self.add_event(UserUpdatedEvent(self.id, updated_fields))


@dataclass
class UserProfile(Entity):
    """User profile entity containing additional user information."""

    id: UUID
    user_id: UUID
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    preferences: dict = field(default_factory=dict)

    def update_bio(self, bio: str) -> None:
        """Update the user's bio."""
        self.bio = bio

    def update_avatar(self, avatar_url: str) -> None:
        """Update the user's avatar URL."""
        self.avatar_url = avatar_url

    def set_preference(self, key: str, value: str) -> None:
        """Set a user preference."""
        self.preferences[key] = value

    def get_preference(self, key: str, default: str = None) -> Optional[str]:
        """Get a user preference."""
        return self.preferences.get(key, default)
