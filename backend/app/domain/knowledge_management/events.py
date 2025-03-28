"""
Knowledge Management domain events.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

from app.domain.common.events import DomainEvent
from app.domain.knowledge_management.entities import Tag, Source, Relationship


class KnowledgeItemCreated(DomainEvent):
    """Event raised when a new knowledge item is created."""

    title: str
    item_type: str
    content: str
    confidence: float
    source: Optional[Source]
    created_by: str


class RelationshipEstablished(DomainEvent):
    """Event raised when a relationship is established between knowledge items."""

    source_id: str
    target_id: str
    relationship: Relationship
    established_by: str


class RelationshipRemoved(DomainEvent):
    """Event raised when a relationship between knowledge items is removed."""

    source_id: str
    target_id: str
    relationship: Relationship
    removed_by: str


class KnowledgeTagAdded(DomainEvent):
    """Event raised when a tag is added to a knowledge item."""

    knowledge_item_id: str
    tag: Tag
    added_by: str


class ArtifactReferenceAdded(DomainEvent):
    """Event raised when an artifact reference is added to a knowledge item."""

    knowledge_item_id: str
    artifact_id: str
    added_by: str


class ConfidenceUpdated(DomainEvent):
    """Event raised when a knowledge item's confidence score is updated."""

    knowledge_item_id: str
    previous_confidence: float
    new_confidence: float
    updated_by: str
    reason: Optional[str]


class KnowledgeSourceAdded(DomainEvent):
    """Event raised when a source is added to a knowledge item."""

    knowledge_item_id: str
    source: Source
    added_by: str
    metadata: Dict[str, Any]
