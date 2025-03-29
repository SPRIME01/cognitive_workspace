"""
Project Management domain interfaces.
"""

from typing import List, Optional, Protocol
from datetime import datetime

from app.domain.common.interfaces import Repository
from app.domain.project_management.entities import Project


class ProjectRepository(Repository[Project, str], Protocol):
    """Repository interface for Project aggregate."""

    async def get_by_owner(
        self, owner_id: str, skip: int = 0, limit: int = 100
    ) -> List[Project]:
        """Get projects by owner ID."""
        ...

    async def get_by_member(
        self, member_id: str, skip: int = 0, limit: int = 100
    ) -> List[Project]:
        """Get projects where the user is a member."""
        ...

    async def search_by_name(
        self, name: str, skip: int = 0, limit: int = 100
    ) -> List[Project]:
        """Search projects by name."""
        ...

    async def get_active_projects(
        self, skip: int = 0, limit: int = 100
    ) -> List[Project]:
        """Get all active projects."""
        ...


class ProjectEventStore(Protocol):
    """Interface for storing project domain events."""

    async def append_events(self, project_id: str, events: List[dict]) -> None:
        """Append events to the project event stream."""
        pass

    async def get_events(
        self, project_id: str, since: Optional[datetime] = None
    ) -> List[dict]:
        """Get events for a project since a specific time."""
        raise NotImplementedError
