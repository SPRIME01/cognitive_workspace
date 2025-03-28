"""
Artifact Management domain services.

This module contains domain services that encapsulate complex business logic
for artifact management operations.
"""

from datetime import datetime
from typing import List, Optional, Protocol, Dict, Any

from app.domain.artifact_management.entities import (
    Artifact,
    Version,
    Tag,
    ArtifactState,
    ArtifactType,
)
from app.domain.artifact_management.interfaces import (
    ArtifactRepository,
    VersionRepository,
    TagRepository,
)
from app.domain.artifact_management.events import (
    ArtifactCreated,
    VersionAdded,
    TagAdded,
    TagRemoved,
    ArtifactStateChanged,
    ArtifactMetadataUpdated,
)
from app.domain.common.event_publisher import EventPublisher


class ArtifactDomainService(Protocol):
    """Domain service for artifact-related operations."""

    async def create_artifact(
        self,
        project_id: str,
        name: str,
        artifact_type: str,
        owner_id: str,
        description: Optional[str] = None,
        initial_content: Optional[Dict[str, Any]] = None,
    ) -> Artifact:
        """Create a new artifact."""
        pass

    async def add_version(
        self,
        artifact_id: str,
        content_url: str,
        content_hash: str,
        created_by: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Version:
        """Add a new version to an artifact."""
        pass

    async def update_tags(
        self, artifact_id: str, tags: List[Tag], updated_by: str
    ) -> Artifact:
        """Update artifact tags."""
        pass

    async def validate_artifact_access(
        self, artifact_id: str, user_id: str, required_permission: Optional[str] = None
    ) -> bool:
        """Validate user's access to an artifact."""
        pass


class DefaultArtifactDomainService:
    """Default implementation of ArtifactDomainService."""

    def __init__(
        self,
        artifact_repository: ArtifactRepository,
        version_repository: VersionRepository,
        tag_repository: TagRepository,
        event_publisher: EventPublisher,
    ):
        """Initialize the service.

        Args:
            artifact_repository: Repository for artifact operations
            version_repository: Repository for version operations
            tag_repository: Repository for tag operations
            event_publisher: Service for publishing domain events
        """
        self._artifact_repository = artifact_repository
        self._version_repository = version_repository
        self._tag_repository = tag_repository
        self._event_publisher = event_publisher

    async def create_artifact(
        self,
        project_id: str,
        name: str,
        artifact_type: str,
        owner_id: str,
        description: Optional[str] = None,
        initial_content: Optional[Dict[str, Any]] = None,
    ) -> Artifact:
        """Create a new artifact.

        Args:
            project_id: ID of the project this artifact belongs to
            name: Artifact name
            artifact_type: Type of artifact (document, image, etc.)
            owner_id: ID of the artifact owner
            description: Optional artifact description
            initial_content: Optional initial content data

        Returns:
            The created artifact

        Raises:
            ValueError: If the artifact data is invalid
        """
        if not name or len(name.strip()) == 0:
            raise ValueError("Artifact name cannot be empty")

        # Validate artifact type
        if artifact_type not in vars(ArtifactType).values():
            raise ValueError(f"Invalid artifact type: {artifact_type}")

        artifact = Artifact(
            id=f"art_{datetime.utcnow().timestamp()}",  # Simple ID generation
            project_id=project_id,
            name=name,
            description=description,
            artifact_type=artifact_type,
            state=ArtifactState.DRAFT,
            owner_id=owner_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        # Save the artifact
        artifact = await self._artifact_repository.add(artifact)

        # Publish artifact created event
        await self._event_publisher.publish_event(
            ArtifactCreated(
                event_id=f"evt_{datetime.utcnow().timestamp()}",
                event_type="artifact.created",
                aggregate_id=artifact.id,
                aggregate_type="artifact",
                project_id=project_id,
                name=name,
                artifact_type=artifact_type,
                owner_id=owner_id,
                description=description,
            )
        )

        # If initial content is provided, create the first version
        if initial_content:
            version = Version(
                id=f"ver_{datetime.utcnow().timestamp()}",  # Simple ID generation
                artifact_id=artifact.id,
                content_hash="initial",  # Should be properly computed in production
                content_url="",  # Should be properly set in production
                created_at=datetime.utcnow(),
                created_by=owner_id,
                metadata=initial_content,
            )
            artifact.add_version(version)
            await self._version_repository.add(version)

            # Publish version added event
            await self._event_publisher.publish_event(
                VersionAdded(
                    event_id=f"evt_{datetime.utcnow().timestamp()}_ver",
                    event_type="artifact.version_added",
                    aggregate_id=artifact.id,
                    aggregate_type="artifact",
                    artifact_id=artifact.id,
                    version=version,
                    created_by=owner_id,
                )
            )

            await self._artifact_repository.update(artifact)

        return artifact

    async def add_version(
        self,
        artifact_id: str,
        content_url: str,
        content_hash: str,
        created_by: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Version:
        """Add a new version to an artifact.

        Args:
            artifact_id: ID of the artifact
            content_url: URL where the content is stored
            content_hash: Hash of the content for verification
            created_by: ID of the user creating the version
            metadata: Optional version metadata

        Returns:
            The created version

        Raises:
            ValueError: If the artifact doesn't exist or validation fails
        """
        artifact = await self._artifact_repository.get_by_id(artifact_id)
        if not artifact:
            raise ValueError(f"Artifact {artifact_id} not found")

        # Check if this content hash already exists
        existing_version = await self._version_repository.get_by_hash(content_hash)
        if existing_version:
            raise ValueError("A version with this content already exists")

        version = Version(
            id=f"ver_{datetime.utcnow().timestamp()}",  # Simple ID generation
            artifact_id=artifact_id,
            content_hash=content_hash,
            content_url=content_url,
            created_at=datetime.utcnow(),
            created_by=created_by,
            metadata=metadata or {},
        )

        # Update the artifact with the new version
        artifact.add_version(version)
        await self._artifact_repository.update(artifact)
        version = await self._version_repository.add(version)

        # Publish version added event
        await self._event_publisher.publish_event(
            VersionAdded(
                event_id=f"evt_{datetime.utcnow().timestamp()}",
                event_type="artifact.version_added",
                aggregate_id=artifact.id,
                aggregate_type="artifact",
                artifact_id=artifact_id,
                version=version,
                created_by=created_by,
            )
        )

        return version

    async def update_tags(
        self, artifact_id: str, tags: List[Tag], updated_by: str
    ) -> Artifact:
        """Update artifact tags.

        Args:
            artifact_id: ID of the artifact
            tags: New list of tags
            updated_by: ID of the user updating the tags

        Returns:
            The updated artifact

        Raises:
            ValueError: If the artifact doesn't exist or validation fails
        """
        artifact = await self._artifact_repository.get_by_id(artifact_id)
        if not artifact:
            raise ValueError(f"Artifact {artifact_id} not found")

        # Get the current tags for event tracking
        removed_tags = set(artifact.tags)
        added_tags = set(tags)

        # Clear existing tags
        artifact.tags = []

        # Add new tags
        for tag in tags:
            artifact.add_tag(tag)
            await self._tag_repository.add(tag)

        # Publish events for removed and added tags
        for tag in removed_tags - added_tags:
            await self._event_publisher.publish_event(
                TagRemoved(
                    event_id=f"evt_{datetime.utcnow().timestamp()}_rem_{tag.name}",
                    event_type="artifact.tag_removed",
                    aggregate_id=artifact.id,
                    aggregate_type="artifact",
                    artifact_id=artifact_id,
                    tag=tag,
                    removed_by=updated_by,
                )
            )

        for tag in added_tags - removed_tags:
            await self._event_publisher.publish_event(
                TagAdded(
                    event_id=f"evt_{datetime.utcnow().timestamp()}_add_{tag.name}",
                    event_type="artifact.tag_added",
                    aggregate_id=artifact.id,
                    aggregate_type="artifact",
                    artifact_id=artifact_id,
                    tag=tag,
                    added_by=updated_by,
                )
            )

        return await self._artifact_repository.update(artifact)

    async def validate_artifact_access(
        self, artifact_id: str, user_id: str, required_permission: Optional[str] = None
    ) -> bool:
        """Validate user's access to an artifact.

        Args:
            artifact_id: ID of the artifact to check
            user_id: ID of the user requesting access
            required_permission: Optional specific permission requirement

        Returns:
            True if the user has access, False otherwise
        """
        artifact = await self._artifact_repository.get_by_id(artifact_id)
        if not artifact:
            return False

        # Owner has full access
        if artifact.owner_id == user_id:
            return True

        # TODO: Implement more sophisticated access control based on project membership
        # and specific permissions when those systems are implemented

        return False
