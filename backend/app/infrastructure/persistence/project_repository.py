"""SQLAlchemy implementation of the ProjectRepository."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.domain.project_management.entities import Project
from app.domain.project_management.repositories import ProjectRepository
from app.infrastructure.persistence.models import ProjectModel, ProjectCollaboratorModel
from app.infrastructure.persistence.mappers import ProjectMapper


class SQLAlchemyProjectRepository(ProjectRepository):
    """SQLAlchemy implementation of ProjectRepository."""

    def __init__(self, session: AsyncSession, mapper: ProjectMapper):
        """Initialize the repository.

        Args:
            session: SQLAlchemy async session
            mapper: Mapper for converting between domain and persistence models
        """
        self._session = session
        self._mapper = mapper

    async def save(self, project: Project) -> None:
        """Save a project.

        Args:
            project: Project to save
        """
        model = await self._mapper.to_persistence(project)
        self._session.add(model)
        await self._session.commit()

    async def get_by_id(self, project_id: UUID) -> Optional[Project]:
        """Get a project by ID.

        Args:
            project_id: ID of the project to retrieve

        Returns:
            Project if found, None otherwise
        """
        stmt = (
            select(ProjectModel)
            .options(joinedload(ProjectModel.collaborators))
            .filter(ProjectModel.id == project_id)
        )
        result = await self._session.execute(stmt)
        model = result.unique().scalar_one_or_none()

        if model is None:
            return None

        return await self._mapper.to_domain(model)

    async def list_by_user_id(
        self, user_id: UUID, include_archived: bool = False
    ) -> List[Project]:
        """List all projects accessible to a user.

        Args:
            user_id: ID of the user
            include_archived: Whether to include archived projects

        Returns:
            List of projects
        """
        # Query projects where user is owner or collaborator
        stmt = (
            select(ProjectModel)
            .options(joinedload(ProjectModel.collaborators))
            .where(
                (ProjectModel.owner_id == user_id)
                | (
                    ProjectModel.collaborators.any(
                        ProjectCollaboratorModel.user_id == user_id
                    )
                )
            )
        )

        if not include_archived:
            stmt = stmt.where(ProjectModel.status != "ARCHIVED")

        result = await self._session.execute(stmt)
        models = result.unique().scalars().all()

        return [await self._mapper.to_domain(model) for model in models]

    async def delete(self, project_id: UUID) -> None:
        """Delete a project.

        Args:
            project_id: ID of the project to delete
        """
        stmt = select(ProjectModel).filter(ProjectModel.id == project_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is not None:
            await self._session.delete(model)
            await self._session.commit()
