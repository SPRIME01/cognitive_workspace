"""
User Management domain events.

This module defines the domain events specific to the User Management domain.
Domain events represent significant occurrences within the domain.
"""

from dataclasses import dataclass
from typing import Set
from uuid import UUID

from app.domain.common.base import DomainEvent


@dataclass
class UserRegisteredEvent(DomainEvent):
    """Event raised when a user successfully registers in the system."""

    user_id: UUID
    username: str
    email: str


@dataclass
class UserProfileUpdatedEvent(DomainEvent):
    """Event raised when a user profile is updated."""

    user_id: UUID
    updated_fields: Set[str]


@dataclass
class UserDeactivatedEvent(DomainEvent):
    """Event raised when a user is deactivated."""

    user_id: UUID


@dataclass
class UserActivatedEvent(DomainEvent):
    """Event raised when a user is activated."""

    user_id: UUID


@dataclass
class UserRoleChangedEvent(DomainEvent):
    """Event raised when a user's roles are changed."""

    user_id: UUID
    added_roles: Set[str]
    removed_roles: Set[str]


@dataclass
class UserAuthenticationSucceededEvent(DomainEvent):
    """Event raised when a user successfully authenticates."""

    user_id: UUID


@dataclass
class UserAuthenticationFailedEvent(DomainEvent):
    """Event raised when a user authentication attempt fails."""

    username_or_email: str
    ip_address: str
