"""
Artifact Management domain interfaces.
"""

from typing import List, Optional, Protocol
from datetime import datetime

from app.domain.common.interfaces import Repository
from app.domain.artifact_management.entities import Artifact, Version, Tag


class ArtifactRepository(Repository[Artifact], Protocol):
    """Repository interface for Artifact aggregate."""

    async def get_by_project(
        self, project_id: str, skip: int = 0, limit: int = 100
    ) -> List[Artifact]:
        """Get artifacts by project ID."""
        pass

    async def get_by_owner(
        self, owner_id: str, skip: int = 0, limit: int = 100
    ) -> List[Artifact]:
        """Get artifacts by owner ID."""
        pass

    async def get_by_type(
        self, artifact_type: str, skip: int = 0, limit: int = 100
    ) -> List[Artifact]:
        """Get artifacts by type."""
        pass

    async def search_by_name(
        self, name: str, skip: int = 0, limit: int = 100
    ) -> List[Artifact]:
        """Search artifacts by name."""
        pass

    async def get_by_tag(
        self, tag: str, skip: int = 0, limit: int = 100
    ) -> List[Artifact]:
        """Get artifacts by tag."""
        pass


class VersionRepository(Repository[Version], Protocol):
    """Repository interface for Version entity."""

    async def get_by_artifact(
        self, artifact_id: str, skip: int = 0, limit: int = 100
    ) -> List[Version]:
        """Get versions by artifact ID."""
        pass

    async def get_latest_version(self, artifact_id: str) -> Optional[Version]:
        """Get the latest version of an artifact."""
        pass

    async def get_by_hash(self, content_hash: str) -> Optional[Version]:
        """Get version by content hash."""
        pass


class TagRepository(Repository[Tag], Protocol):
    """Repository interface for Tag entity."""

    async def get_by_artifact(self, artifact_id: str) -> List[Tag]:
        """Get all tags for an artifact."""
        pass

    async def get_popular_tags(self, limit: int = 10) -> List[Tag]:
        """Get most frequently used tags."""
        pass


class ArtifactEventStore(Protocol):
    """Interface for storing artifact domain events."""

    async def append_events(self, artifact_id: str, events: List[dict]) -> None:
        """Append events to the artifact event stream."""
        pass

    async def get_events(
        self, artifact_id: str, since: Optional[datetime] = None
    ) -> List[dict]:
        """Get events for an artifact since a specific time."""
        pass
