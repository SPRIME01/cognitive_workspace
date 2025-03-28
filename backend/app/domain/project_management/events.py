"""
Project Management domain events.
"""

from typing import List, Optional
from datetime import datetime

from app.domain.common.events import DomainEvent


class ProjectCreated(DomainEvent):
    """Event raised when a new project is created."""

    name: str
    owner_id: str
    description: Optional[str]


class ProjectDeleted(DomainEvent):
    """Event raised when a project is deleted."""

    owner_id: str


class ProjectMemberAdded(DomainEvent):
    """Event raised when a member is added to a project."""

    member_id: str
    added_by: str


class ProjectMemberRemoved(DomainEvent):
    """Event raised when a member is removed from a project."""

    member_id: str
    removed_by: str


class ProjectStateChanged(DomainEvent):
    """Event raised when a project's state changes."""

    previous_state: str
    new_state: str
    changed_by: str
