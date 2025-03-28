"""
Project Management domain services.

This module contains domain services that encapsulate complex business logic
for project management operations.
"""

from datetime import datetime
from typing import List, Optional, Protocol, Dict, Any

from app.domain.project_management.entities import Project, ProjectStatus
from app.domain.project_management.interfaces import ProjectRepository
from app.domain.project_management.events import (
    ProjectCreated,
    ProjectDeleted,
    ProjectMemberAdded,
    ProjectMemberRemoved,
    ProjectStateChanged,
)
from app.domain.common.events import DomainEvent
from app.domain.common.event_publisher import EventPublisher


class ProjectDomainService(Protocol):
    """Domain service for project-related operations."""

    async def create_project(
        self, name: str, owner_id: str, description: Optional[str] = None
    ) -> Project:
        """Create a new project."""
        pass

    async def archive_project(self, project_id: str, user_id: str) -> Project:
        """Archive an existing project."""
        pass

    async def validate_project_access(
        self, project_id: str, user_id: str, required_role: Optional[str] = None
    ) -> bool:
        """Validate user's access to a project."""
        pass

    async def transfer_ownership(
        self, project_id: str, current_owner_id: str, new_owner_id: str
    ) -> Project:
        """Transfer project ownership to another user."""
        pass


class DefaultProjectDomainService:
    """Default implementation of ProjectDomainService."""

    def __init__(
        self, project_repository: ProjectRepository, event_publisher: EventPublisher
    ):
        """Initialize the service.

        Args:
            project_repository: Repository for project operations
            event_publisher: Service for publishing domain events
        """
        self._project_repository = project_repository
        self._event_publisher = event_publisher

    async def create_project(
        self, name: str, owner_id: str, description: Optional[str] = None
    ) -> Project:
        """Create a new project.

        Args:
            name: Project name
            owner_id: ID of the project owner
            description: Optional project description

        Returns:
            The created project

        Raises:
            ValueError: If the project name is invalid
        """
        if not name or len(name.strip()) == 0:
            raise ValueError("Project name cannot be empty")

        project = Project(
            id=f"proj_{datetime.utcnow().timestamp()}",  # Simple ID generation
            name=name,
            owner_id=owner_id,
            description=description,
            status=ProjectStatus.DRAFT,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            members=[owner_id],  # Owner is automatically a member
        )

        # Save the project
        project = await self._project_repository.add(project)

        # Publish project created event
        await self._event_publisher.publish_event(
            ProjectCreated(
                event_id=f"evt_{datetime.utcnow().timestamp()}",
                event_type="project.created",
                aggregate_id=project.id,
                aggregate_type="project",
                name=project.name,
                owner_id=project.owner_id,
                description=project.description,
            )
        )

        return project

    async def archive_project(self, project_id: str, user_id: str) -> Project:
        """Archive an existing project.

        Args:
            project_id: ID of the project to archive
            user_id: ID of the user requesting the archive

        Returns:
            The archived project

        Raises:
            ValueError: If the project doesn't exist or user is not the owner
        """
        project = await self._project_repository.get_by_id(project_id)
        if not project:
            raise ValueError(f"Project {project_id} not found")

        if project.owner_id != user_id:
            raise ValueError("Only the project owner can archive the project")

        if project.status == ProjectStatus.ARCHIVED:
            return project

        previous_state = project.status
        project.status = ProjectStatus.ARCHIVED
        project.updated_at = datetime.utcnow()

        # Save the updated project
        project = await self._project_repository.update(project)

        # Publish project state changed event
        await self._event_publisher.publish_event(
            ProjectStateChanged(
                event_id=f"evt_{datetime.utcnow().timestamp()}",
                event_type="project.state_changed",
                aggregate_id=project.id,
                aggregate_type="project",
                previous_state=previous_state,
                new_state=ProjectStatus.ARCHIVED,
                changed_by=user_id,
            )
        )

        return project

    async def validate_project_access(
        self, project_id: str, user_id: str, required_role: Optional[str] = None
    ) -> bool:
        """Validate user's access to a project.

        Args:
            project_id: ID of the project to check
            user_id: ID of the user requesting access
            required_role: Optional role requirement for access

        Returns:
            True if the user has access, False otherwise
        """
        project = await self._project_repository.get_by_id(project_id)
        if not project:
            return False

        # Owner has full access
        if project.owner_id == user_id:
            return True

        # Check membership
        if user_id not in project.members:
            return False

        # If a specific role is required, we would check it here
        # This is a placeholder for future role-based access control
        if required_role:
            # TODO: Implement role-based checks when roles are added
            pass

        return True

    async def transfer_ownership(
        self, project_id: str, current_owner_id: str, new_owner_id: str
    ) -> Project:
        """Transfer project ownership to another user.

        Args:
            project_id: ID of the project
            current_owner_id: ID of the current owner
            new_owner_id: ID of the new owner

        Returns:
            The updated project

        Raises:
            ValueError: If the project doesn't exist or validation fails
        """
        project = await self._project_repository.get_by_id(project_id)
        if not project:
            raise ValueError(f"Project {project_id} not found")

        if project.owner_id != current_owner_id:
            raise ValueError("Only the current owner can transfer ownership")

        if new_owner_id not in project.members:
            raise ValueError("New owner must be a project member")

        previous_owner_id = project.owner_id
        project.owner_id = new_owner_id
        project.updated_at = datetime.utcnow()

        # Save the updated project
        project = await self._project_repository.update(project)

        # Publish ownership transfer events
        await self._event_publisher.publish_events(
            [
                ProjectMemberRemoved(
                    event_id=f"evt_{datetime.utcnow().timestamp()}_1",
                    event_type="project.member_removed",
                    aggregate_id=project.id,
                    aggregate_type="project",
                    member_id=previous_owner_id,
                    removed_by=current_owner_id,
                ),
                ProjectMemberAdded(
                    event_id=f"evt_{datetime.utcnow().timestamp()}_2",
                    event_type="project.member_added",
                    aggregate_id=project.id,
                    aggregate_type="project",
                    member_id=new_owner_id,
                    added_by=current_owner_id,
                ),
            ]
        )

        return project
