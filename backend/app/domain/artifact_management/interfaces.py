"""
Artifact Management domain interfaces.
"""

from typing import List, Optional, Protocol
from datetime import datetime

from app.domain.common.interfaces import Repository
from app.domain.artifact_management.entities import Artifact, Version, Tag


class ArtifactRepository(Protocol):
    """Repository interface for Artifact aggregate."""

    # Include Repository methods for Artifact
    async def get_by_id(self, id: str) -> Optional[Artifact]:
        """Get an entity by its ID."""
        ...

    async def exists(self, id: str) -> bool:
        """Check if an entity with the given ID exists."""
        ...

    async def add(self, entity: Artifact) -> Artifact:
        """Add a new entity."""
        ...

    async def update(self, entity: Artifact) -> Artifact:
        """Update an existing entity."""
        ...

    async def delete(self, id: str) -> bool:
        """Delete an entity by its ID."""
        ...

    # Artifact-specific methods
    async def get_by_project(
        self, project_id: str, skip: int = 0, limit: int = 100
    ) -> List[Artifact]:
        """Get artifacts by project ID."""
        ...

    async def get_by_owner(self, owner_id: str, skip: int = 0, limit: int = 100) -> List[Artifact]:
        """Get artifacts by owner ID."""
        ...

    async def get_by_type(
        self, artifact_type: str, skip: int = 0, limit: int = 100
    ) -> List[Artifact]:
        """Get artifacts by type."""
        ...

    async def search_by_name(self, name: str, skip: int = 0, limit: int = 100) -> List[Artifact]:
        """Search artifacts by name."""
        ...

    async def get_by_tag(self, tag: str, skip: int = 0, limit: int = 100) -> List[Artifact]:
        """Get artifacts by tag."""
        ...


class VersionRepository(Protocol):
    """Repository interface for Version entity."""

    # Include Repository methods for Version
    async def get_by_id(self, id: str) -> Optional[Version]:
        """Get an entity by its ID."""
        ...

    async def exists(self, id: str) -> bool:
        """Check if an entity with the given ID exists."""
        ...

    async def add(self, entity: Version) -> Version:
        """Add a new entity."""
        ...

    async def update(self, entity: Version) -> Version:
        """Update an existing entity."""
        ...

    async def delete(self, id: str) -> bool:
        """Delete an entity by its ID."""
        ...

    # Version-specific methods
    async def get_by_artifact(
        self, artifact_id: str, skip: int = 0, limit: int = 100
    ) -> List[Version]:
        """Get versions by artifact ID."""
        ...

    async def get_latest_version(self, artifact_id: str) -> Optional[Version]:
        """Get the latest version of an artifact."""
        ...

    async def get_by_hash(self, content_hash: str) -> Optional[Version]:
        """Get version by content hash."""
        ...


class TagRepository(Protocol):
    """Repository interface for Tag entity."""

    # Include Repository methods for Tag
    async def get_by_id(self, id: str) -> Optional[Tag]:
        """Get an entity by its ID."""
        ...

    async def exists(self, id: str) -> bool:
        """Check if an entity with the given ID exists."""
        ...

    async def add(self, entity: Tag) -> Tag:
        """Add a new entity."""
        ...

    async def update(self, entity: Tag) -> Tag:
        """Update an existing entity."""
        ...

    async def delete(self, id: str) -> bool:
        """Delete an entity by its ID."""
        ...

    # Tag-specific methods
    async def get_by_artifact(self, artifact_id: str) -> List[Tag]:
        """Get all tags for an artifact."""
        ...

    async def get_popular_tags(self, limit: int = 10) -> List[Tag]:
        """Get most frequently used tags."""
        ...


class ArtifactEventStore(Protocol):
    """Interface for storing artifact domain events."""

    async def append_events(self, artifact_id: str, events: List[dict]) -> None:
        """Append events to the artifact event stream."""
        ...

    async def get_events(self, artifact_id: str, since: Optional[datetime] = None) -> List[dict]:
        """Get events for an artifact since a specific time."""
        ...
