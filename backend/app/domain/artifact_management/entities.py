"""
Artifact Management domain entities.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ArtifactType:
    """Artifact type value object."""

    DOCUMENT = "document"
    IMAGE = "image"
    CODE = "code"
    DIAGRAM = "diagram"
    MINDMAP = "mindmap"
    COLLECTION = "collection"


class ArtifactState:
    """Artifact state value object."""

    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DELETED = "deleted"


class Version(BaseModel):
    """Version entity."""

    id: str
    artifact_id: str
    content_hash: str
    content_url: str
    created_at: datetime
    created_by: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Tag(BaseModel):
    """Tag value object."""

    name: str = Field(..., min_length=1, max_length=50)
    color: Optional[str] = None


class Artifact(BaseModel):
    """Artifact aggregate root entity."""

    id: str
    project_id: str
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    artifact_type: str = Field(
        ..., regex=f"^({'|'.join(vars(ArtifactType).values())})$"
    )
    state: str = Field(default=ArtifactState.DRAFT)
    owner_id: str
    current_version_id: Optional[str] = None
    versions: List[Version] = Field(default_factory=list)
    tags: List[Tag] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def add_version(self, version: Version) -> None:
        """Add a new version to the artifact."""
        self.versions.append(version)
        self.current_version_id = version.id
        self.updated_at = datetime.utcnow()

    def add_tag(self, tag: Tag) -> None:
        """Add a tag to the artifact."""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.utcnow()

    def remove_tag(self, tag: Tag) -> None:
        """Remove a tag from the artifact."""
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.utcnow()

    def update_state(self, new_state: str) -> None:
        """Update the artifact state."""
        if new_state in vars(ArtifactState).values():
            self.state = new_state
            self.updated_at = datetime.utcnow()

    class Config:
        """Pydantic configuration."""

        orm_mode = True
