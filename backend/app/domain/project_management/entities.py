"""
Project Management domain entities.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class ProjectStatus:
    """Project status value object."""

    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"


class Project(BaseModel):
    """Project aggregate root entity."""

    id: str
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    owner_id: str
    status: str = Field(default=ProjectStatus.DRAFT)
    created_at: datetime
    updated_at: datetime
    members: List[str] = Field(default_factory=list)  # List of user IDs

    model_config = ConfigDict(from_attributes=True)

    def add_member(self, user_id: str) -> None:
        """Add a member to the project."""
        if user_id not in self.members:
            self.members.append(user_id)
            self.updated_at = datetime.utcnow()

    def remove_member(self, user_id: str) -> None:
        """Remove a member from the project."""
        if user_id in self.members:
            self.members.remove(user_id)
            self.updated_at = datetime.utcnow()

    def archive(self) -> None:
        """Archive the project."""
        if self.status != ProjectStatus.ARCHIVED:
            self.status = ProjectStatus.ARCHIVED
            self.updated_at = datetime.utcnow()


class ProjectCollaborator(BaseModel):
    """Represents a collaborator in a project."""

    id: UUID
    project_id: UUID
    user_id: UUID
    role: str = Field(
        ..., description="Role of the collaborator (e.g., 'owner', 'editor', 'viewer')"
    )
    permissions: List[str] = Field(
        default_factory=list, description="List of permissions assigned to the collaborator"
    )
    metadata: Dict[str, Any] = Field(default_factory=dict)
    added_at: datetime
    added_by: UUID

    model_config = ConfigDict(from_attributes=True)

    def update_role(self, new_role: str) -> None:
        """Update the role of the collaborator."""
        self.role = new_role

    def add_permission(self, permission: str) -> None:
        """Add a permission to the collaborator."""
        if permission not in self.permissions:
            self.permissions.append(permission)

    def remove_permission(self, permission: str) -> None:
        """Remove a permission from the collaborator."""
        if permission in self.permissions:
            self.permissions.remove(permission)
