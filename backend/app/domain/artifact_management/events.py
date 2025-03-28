"""
Artifact Management domain events.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

from app.domain.common.events import DomainEvent
from app.domain.artifact_management.entities import Tag, Version


class ArtifactCreated(DomainEvent):
    """Event raised when a new artifact is created."""

    project_id: str
    name: str
    artifact_type: str
    owner_id: str
    description: Optional[str]


class VersionAdded(DomainEvent):
    """Event raised when a new version is added to an artifact."""

    artifact_id: str
    version: Version
    created_by: str


class TagAdded(DomainEvent):
    """Event raised when a tag is added to an artifact."""

    artifact_id: str
    tag: Tag
    added_by: str


class TagRemoved(DomainEvent):
    """Event raised when a tag is removed from an artifact."""

    artifact_id: str
    tag: Tag
    removed_by: str


class ArtifactStateChanged(DomainEvent):
    """Event raised when an artifact's state changes."""

    artifact_id: str
    previous_state: str
    new_state: str
    changed_by: str


class ArtifactMetadataUpdated(DomainEvent):
    """Event raised when an artifact's metadata is updated."""

    artifact_id: str
    metadata_changes: Dict[str, Any]
    updated_by: str
