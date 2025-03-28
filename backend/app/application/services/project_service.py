"""
Project Management application service.

This module provides the application service for the Project Management domain,
coordinating domain objects and providing a facade for the presentation layer.
"""

from typing import List
from uuid import UUID

from app.domain.project_management.entities import Project, ProjectStatus
from app.domain.project_management.repositories import (
    ProjectRepository,
    ProjectCollaboratorRepository,
)
from app.domain.project_management.services import (
    ProjectManagementService,
    CollaborationService,
)
from app.application.dtos import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    CollaboratorCreate,
    CollaboratorResponse,
)


class ProjectApplicationService:
    """Application service for project management operations."""

    def __init__(
        self,
        project_repository: ProjectRepository,
        collaborator_repository: ProjectCollaboratorRepository,
        project_management_service: ProjectManagementService,
        collaboration_service: CollaborationService,
    ):
        """Initialize the project application service.

        Args:
            project_repository: Repository for project entities
            collaborator_repository: Repository for project collaborator entities
            project_management_service: Domain service for project management
            collaboration_service: Domain service for project collaboration
        """
        self.project_repository = project_repository
        self.collaborator_repository = collaborator_repository
        self.project_management_service = project_management_service
        self.collaboration_service = collaboration_service

    async def create_project(
        self, project_data: ProjectCreate, owner_id: UUID
    ) -> ProjectResponse:
        """Create a new project.

        Args:
            project_data: Project creation data
            owner_id: ID of the user creating the project

        Returns:
            ProjectResponse with the created project details

        Raises:
            ValueError: If project data is invalid
        """
        project = await self.project_management_service.create_project(
            name=project_data.name,
            description=project_data.description,
            owner_id=owner_id,
            visibility=project_data.visibility,
        )
        await self.project_repository.save(project)
        return self._to_project_response(project)

    async def update_project(
        self, project_id: UUID, project_data: ProjectUpdate, user_id: UUID
    ) -> ProjectResponse:
        """Update an existing project.

        Args:
            project_id: ID of the project to update
            project_data: Project update data
            user_id: ID of the user making the update

        Returns:
            ProjectResponse with the updated project details

        Raises:
            ValueError: If project data is invalid
            PermissionError: If user lacks permission
            NotFoundError: If project not found
        """
        project = await self.project_repository.get_by_id(project_id)
        updated_project = await self.project_management_service.update_project(
            project=project,
            user_id=user_id,
            name=project_data.name,
            description=project_data.description,
            visibility=project_data.visibility,
        )
        await self.project_repository.save(updated_project)
        return self._to_project_response(updated_project)

    async def archive_project(self, project_id: UUID, user_id: UUID) -> ProjectResponse:
        """Archive a project.

        Args:
            project_id: ID of the project to archive
            user_id: ID of the user archiving the project

        Returns:
            ProjectResponse with the archived project details

        Raises:
            PermissionError: If user lacks permission
            NotFoundError: If project not found
        """
        project = await self.project_repository.get_by_id(project_id)
        archived_project = await self.project_management_service.archive_project(
            project=project,
            user_id=user_id,
        )
        await self.project_repository.save(archived_project)
        return self._to_project_response(archived_project)

    async def delete_project(self, project_id: UUID, user_id: UUID) -> None:
        """Delete a project.

        Args:
            project_id: ID of the project to delete
            user_id: ID of the user deleting the project

        Raises:
            PermissionError: If user lacks permission
            NotFoundError: If project not found
        """
        project = await self.project_repository.get_by_id(project_id)
        await self.project_management_service.delete_project(
            project=project,
            user_id=user_id,
        )
        await self.project_repository.delete(project_id)

    async def get_project(self, project_id: UUID, user_id: UUID) -> ProjectResponse:
        """Get a project by ID.

        Args:
            project_id: ID of the project to retrieve
            user_id: ID of the user requesting the project

        Returns:
            ProjectResponse with the project details

        Raises:
            PermissionError: If user lacks permission
            NotFoundError: If project not found
        """
        project = await self.project_repository.get_by_id(project_id)
        if not self.collaboration_service.can_view_project(project, user_id):
            raise PermissionError("User does not have permission to view this project")
        return self._to_project_response(project)

    async def list_projects(
        self, user_id: UUID, include_archived: bool = False
    ) -> List[ProjectResponse]:
        """List all projects accessible to a user.

        Args:
            user_id: ID of the user requesting projects
            include_archived: Whether to include archived projects

        Returns:
            List of ProjectResponse objects
        """
        projects = await self.project_repository.list_by_user_id(
            user_id, include_archived=include_archived
        )
        return [self._to_project_response(project) for project in projects]

    async def add_collaborator(
        self, project_id: UUID, collaborator_data: CollaboratorCreate, user_id: UUID
    ) -> CollaboratorResponse:
        """Add a collaborator to a project.

        Args:
            project_id: ID of the project
            collaborator_data: Collaborator creation data
            user_id: ID of the user adding the collaborator

        Returns:
            CollaboratorResponse with the added collaborator details

        Raises:
            PermissionError: If user lacks permission
            NotFoundError: If project not found
            ValueError: If collaborator data is invalid
        """
        project = await self.project_repository.get_by_id(project_id)
        collaborator = await self.collaboration_service.add_collaborator(
            project=project,
            user_id=user_id,
            collaborator_id=collaborator_data.user_id,
            role=collaborator_data.role,
        )
        await self.collaborator_repository.save(collaborator)
        return self._to_collaborator_response(collaborator)

    async def remove_collaborator(
        self, project_id: UUID, collaborator_id: UUID, user_id: UUID
    ) -> None:
        """Remove a collaborator from a project.

        Args:
            project_id: ID of the project
            collaborator_id: ID of the collaborator to remove
            user_id: ID of the user removing the collaborator

        Raises:
            PermissionError: If user lacks permission
            NotFoundError: If project or collaborator not found
        """
        project = await self.project_repository.get_by_id(project_id)
        await self.collaboration_service.remove_collaborator(
            project=project,
            user_id=user_id,
            collaborator_id=collaborator_id,
        )
        await self.collaborator_repository.delete(project_id, collaborator_id)

    def _to_project_response(self, project: Project) -> ProjectResponse:
        """Convert a Project entity to a ProjectResponse DTO."""
        return ProjectResponse(
            id=project.id,
            name=project.name,
            description=project.description,
            visibility=project.visibility,
            status=project.status,
            owner_id=project.owner_id,
            created_at=project.created_at,
            updated_at=project.updated_at,
            collaborators=[
                self._to_collaborator_response(c) for c in project.collaborators
            ],
        )

    def _to_collaborator_response(self, collaborator) -> CollaboratorResponse:
        """Convert a ProjectCollaborator entity to a CollaboratorResponse DTO."""
        return CollaboratorResponse(
            user_id=collaborator.user_id,
            project_id=collaborator.project_id,
            role=collaborator.role,
            added_at=collaborator.added_at,
        )
