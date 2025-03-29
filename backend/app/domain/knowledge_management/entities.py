"""
Knowledge Management domain entities.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class ItemType:
    """Knowledge item type value object."""

    CONCEPT = "concept"
    FACT = "fact"
    PRINCIPLE = "principle"
    PROCEDURE = "procedure"
    INSIGHT = "insight"
    REFERENCE = "reference"


class RelationshipType:
    """Knowledge relationship type value object."""

    RELATED_TO = "related_to"
    PART_OF = "part_of"
    LEADS_TO = "leads_to"
    DEPENDS_ON = "depends_on"
    DERIVED_FROM = "derived_from"
    CONFLICTS_WITH = "conflicts_with"
    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"


class Relationship(BaseModel):
    """Knowledge relationship entity."""

    id: str
    source_id: str
    target_id: str
    relationship_type: str = Field(
        ...,
        pattern=f"^({'|'.join([v for v in vars(RelationshipType).values() if isinstance(v, str)])})$",
    )
    weight: float = Field(default=1.0, ge=0.0, le=1.0)
    bidirectional: bool = Field(default=False)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Tag(BaseModel):
    """Knowledge tag value object."""

    name: str = Field(..., min_length=1, max_length=50)
    category: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(from_attributes=True)


class Source(BaseModel):
    """Knowledge source value object."""

    id: str
    name: str
    source_type: str
    url: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(from_attributes=True)


class KnowledgeItem(BaseModel):
    """Knowledge item aggregate root entity."""

    id: str
    title: str = Field(..., min_length=1, max_length=200)
    content: str
    item_type: str = Field(
        ..., pattern=f"^({'|'.join([v for v in vars(ItemType).values() if isinstance(v, str)])})$"
    )
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    tags: List[Tag] = Field(default_factory=list)
    source: Optional[Source] = None
    relationships: List[Relationship] = Field(default_factory=list)
    artifact_references: List[str] = Field(default_factory=list)  # List of artifact IDs
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def add_relationship(self, relationship: Relationship) -> None:
        """Add a relationship to the knowledge item."""
        if relationship not in self.relationships:
            self.relationships.append(relationship)
            self.updated_at = datetime.utcnow()

    def remove_relationship(self, relationship: Relationship) -> None:
        """Remove a relationship from the knowledge item."""
        if relationship in self.relationships:
            self.relationships.remove(relationship)
            self.updated_at = datetime.utcnow()

    def add_tag(self, tag: Tag) -> None:
        """Add a tag to the knowledge item."""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.utcnow()

    def remove_tag(self, tag: Tag) -> None:
        """Remove a tag from the knowledge item."""
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.utcnow()

    def add_artifact_reference(self, artifact_id: str) -> None:
        """Add an artifact reference to the knowledge item."""
        if artifact_id not in self.artifact_references:
            self.artifact_references.append(artifact_id)
            self.updated_at = datetime.utcnow()

    def update_confidence(self, confidence: float) -> None:
        """Update the confidence score of the knowledge item."""
        if 0.0 <= confidence <= 1.0:
            self.confidence = confidence
            self.updated_at = datetime.utcnow()

    model_config = ConfigDict(from_attributes=True)
