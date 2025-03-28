"""
Project Management domain repository interfaces.

This module defines the repository interfaces (ports) for the Project Management domain
following the Ports and Adapters pattern.
"""

from abc import abstractmethod
from typing import List, Optional, Protocol, Set
from uuid import UUID

from app.domain.common.base import Repository
from app.domain.project_management.entities import (
    Project,
    ProjectCollaborator,
    ProjectStatus,
)


class ProjectRepository(Repository[Project, UUID], Protocol):
    """Repository interface for Project entities."""

    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Project]:
        """Get a project by name.

        Args:
            name: The project name to search for

        Returns:
            The project if found, None otherwise
        """
        pass

    @abstractmethod
    async def get_by_owner(self, owner_id: UUID) -> List[Project]:
        """Get all projects owned by a user.

        Args:
            owner_id: The ID of the owner

        Returns:
            List of projects owned by the user
        """
        pass

    @abstractmethod
    async def get_by_collaborator(self, user_id: UUID) -> List[Project]:
        """Get all projects where the user is a collaborator.

        Args:
            user_id: The ID of the user

        Returns:
            List of projects where the user is a collaborator
        """
        pass

    @abstractmethod
    async def list_projects(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[ProjectStatus] = None,
        category: Optional[str] = None,
        visibility: Optional[str] = None,
    ) -> List[Project]:
        """Get a filtered list of projects with pagination.

        Args:
            skip: Number of projects to skip
            limit: Maximum number of projects to return
            status: Optional status filter
            category: Optional category filter
            visibility: Optional visibility filter

        Returns:
            List of matching projects
        """
        pass

    @abstractmethod
    async def search_projects(
        self,
        query: str,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[UUID] = None,
        tags: Optional[Set[str]] = None,
    ) -> List[Project]:
        """Search for projects by name, description, or tags.

        Args:
            query: The search query
            skip: Number of projects to skip
            limit: Maximum number of projects to return
            owner_id: Optional owner ID filter
            tags: Optional set of tags to filter by

        Returns:
            List of matching projects
        """
        pass

    @abstractmethod
    async def count_projects(
        self, owner_id: Optional[UUID] = None, status: Optional[ProjectStatus] = None
    ) -> int:
        """Count projects matching the given criteria.

        Args:
            owner_id: Optional owner ID filter
            status: Optional status filter

        Returns:
            Number of matching projects
        """
        pass


class ProjectCollaboratorRepository(Repository[ProjectCollaborator, UUID], Protocol):
    """Repository interface for ProjectCollaborator entities."""

    @abstractmethod
    async def get_by_project_and_user(
        self, project_id: UUID, user_id: UUID
    ) -> Optional[ProjectCollaborator]:
        """Get a collaborator by project and user IDs.

        Args:
            project_id: The ID of the project
            user_id: The ID of the user

        Returns:
            The collaborator if found, None otherwise
        """
        pass

    @abstractmethod
    async def get_project_collaborators(
        self, project_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[ProjectCollaborator]:
        """Get all collaborators for a project.

        Args:
            project_id: The ID of the project
            skip: Number of collaborators to skip
            limit: Maximum number of collaborators to return

        Returns:
            List of project collaborators
        """
        pass

    @abstractmethod
    async def get_user_collaborations(
        self, user_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[ProjectCollaborator]:
        """Get all projects where a user is a collaborator.

        Args:
            user_id: The ID of the user
            skip: Number of collaborations to skip
            limit: Maximum number of collaborations to return

        Returns:
            List of project collaborations
        """
        pass
