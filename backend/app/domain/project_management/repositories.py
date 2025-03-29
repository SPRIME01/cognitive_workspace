"""
Project Management domain repository interfaces.

This module defines the repository interfaces (ports) for the Project Management domain
following the Ports and Adapters pattern.
"""

from typing import List, Optional, Protocol, Set
from uuid import UUID

from app.domain.project_management.entities import (
    Project,
    ProjectCollaborator,
    ProjectStatus,
)


class ProjectRepository(Protocol):
    """Repository interface for Project entities."""

    async def get_by_id(self, id: UUID) -> Optional[Project]:
        """Get a project by its ID."""
        ...

    async def get_by_name(self, name: str) -> Optional[Project]:
        """Get a project by name."""
        ...

    async def get_by_owner(self, owner_id: UUID) -> List[Project]:
        """Get all projects owned by a user."""
        ...

    async def get_by_collaborator(self, user_id: UUID) -> List[Project]:
        """Get all projects where the user is a collaborator."""
        ...

    async def list_projects(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[ProjectStatus] = None,
        category: Optional[str] = None,
        visibility: Optional[str] = None,
    ) -> List[Project]:
        """Get a filtered list of projects with pagination."""
        ...

    async def search_projects(
        self,
        query: str,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[UUID] = None,
        tags: Optional[Set[str]] = None,
    ) -> List[Project]:
        """Search for projects by name, description, or tags."""
        ...

    async def count_projects(
        self, owner_id: Optional[UUID] = None, status: Optional[ProjectStatus] = None
    ) -> int:
        """Count projects matching the given criteria."""
        ...


class ProjectCollaboratorRepository(Protocol):
    """Repository interface for ProjectCollaborator entities."""

    async def get_by_id(self, id: UUID) -> Optional[ProjectCollaborator]:
        """Get a collaborator by its ID."""
        ...

    async def get_by_project_and_user(
        self, project_id: UUID, user_id: UUID
    ) -> Optional[ProjectCollaborator]:
        """Get a collaborator by project and user IDs."""
        ...

    async def get_project_collaborators(
        self, project_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[ProjectCollaborator]:
        """Get all collaborators for a project."""
        ...

    async def get_user_collaborations(
        self, user_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[ProjectCollaborator]:
        """Get all projects where a user is a collaborator."""
        ...
