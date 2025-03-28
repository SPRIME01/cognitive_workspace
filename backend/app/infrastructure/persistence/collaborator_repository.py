"""SQLAlchemy implementation of the ProjectCollaboratorRepository."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.project_management.entities import ProjectCollaborator
from app.domain.project_management.repositories import ProjectCollaboratorRepository
from app.infrastructure.persistence.models import ProjectCollaboratorModel
from app.infrastructure.persistence.mappers import ProjectCollaboratorMapper


class SQLAlchemyProjectCollaboratorRepository(ProjectCollaboratorRepository):
    """SQLAlchemy implementation of ProjectCollaboratorRepository."""

    def __init__(self, session: AsyncSession, mapper: ProjectCollaboratorMapper):
        """Initialize the repository.

        Args:
            session: SQLAlchemy async session
            mapper: Mapper for converting between domain and persistence models
        """
        self._session = session
        self._mapper = mapper

    async def save(self, collaborator: ProjectCollaborator) -> None:
        """Save a project collaborator.

        Args:
            collaborator: Collaborator to save
        """
        model = await self._mapper.to_persistence(collaborator)
        self._session.add(model)
        await self._session.commit()

    async def get_by_id(self, collaborator_id: UUID) -> Optional[ProjectCollaborator]:
        """Get a collaborator by ID.

        Args:
            collaborator_id: ID of the collaborator to retrieve

        Returns:
            ProjectCollaborator if found, None otherwise
        """
        stmt = select(ProjectCollaboratorModel).filter(
            ProjectCollaboratorModel.id == collaborator_id
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return await self._mapper.to_domain(model)

    async def list_by_project_id(self, project_id: UUID) -> List[ProjectCollaborator]:
        """List all collaborators for a project.

        Args:
            project_id: ID of the project

        Returns:
            List of collaborators
        """
        stmt = select(ProjectCollaboratorModel).filter(
            ProjectCollaboratorModel.project_id == project_id
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()

        return [await self._mapper.to_domain(model) for model in models]

    async def delete(self, collaborator_id: UUID) -> None:
        """Delete a collaborator.

        Args:
            collaborator_id: ID of the collaborator to delete
        """
        stmt = select(ProjectCollaboratorModel).filter(
            ProjectCollaboratorModel.id == collaborator_id
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is not None:
            await self._session.delete(model)
            await self._session.commit()

    async def get_by_project_and_user(
        self, project_id: UUID, user_id: UUID
    ) -> Optional[ProjectCollaborator]:
        """Get a collaborator by project and user IDs.

        Args:
            project_id: ID of the project
            user_id: ID of the user

        Returns:
            ProjectCollaborator if found, None otherwise
        """
        stmt = select(ProjectCollaboratorModel).filter(
            ProjectCollaboratorModel.project_id == project_id,
            ProjectCollaboratorModel.user_id == user_id,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return await self._mapper.to_domain(model)
