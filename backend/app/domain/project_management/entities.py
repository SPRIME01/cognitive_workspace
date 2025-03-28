"""
Project Management domain entities.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


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

    class Config:
        """Pydantic configuration."""

        orm_mode = True
