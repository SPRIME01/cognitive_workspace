"""
Knowledge Management domain services.

This module contains domain services that encapsulate complex business logic
for knowledge management operations.
"""

from datetime import datetime
from typing import List, Optional, Protocol, Dict, Any, Set

from app.domain.knowledge_management.entities import (
    KnowledgeItem,
    Relationship,
    Tag,
    Source,
    ItemType,
    RelationshipType,
)
from app.domain.knowledge_management.interfaces import (
    KnowledgeItemRepository,
    RelationshipRepository,
    KnowledgeTagRepository,
    SourceRepository,
    KnowledgeGraphService,
    KnowledgeEventStore,
)
from app.domain.knowledge_management.events import (
    KnowledgeItemCreated,
    RelationshipEstablished,
    RelationshipRemoved,
    KnowledgeTagAdded,
    ArtifactReferenceAdded,
    ConfidenceUpdated,
    KnowledgeSourceAdded,
)
from app.domain.common.event_publisher import EventPublisher


class KnowledgeDomainService(Protocol):
    """Domain service for knowledge-related operations."""

    async def create_knowledge_item(
        self,
        title: str,
        content: str,
        item_type: str,
        created_by: str,
        tags: Optional[List[Tag]] = None,
        source: Optional[Source] = None,
        confidence: float = 1.0,
    ) -> KnowledgeItem:
        """Create a new knowledge item."""
        pass

    async def establish_relationship(
        self,
        source_id: str,
        target_id: str,
        relationship_type: str,
        established_by: str,
        weight: float = 1.0,
        bidirectional: bool = False,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Relationship:
        """Establish a relationship between knowledge items."""
        pass

    async def find_related_items(
        self, item_id: str, max_depth: int = 2, min_weight: float = 0.5
    ) -> List[Dict[str, Any]]:
        """Find items related to a given knowledge item."""
        pass

    async def update_item_confidence(
        self,
        item_id: str,
        new_confidence: float,
        updated_by: str,
        reason: Optional[str] = None,
    ) -> KnowledgeItem:
        """Update the confidence score of a knowledge item."""
        pass


class DefaultKnowledgeDomainService:
    """Default implementation of KnowledgeDomainService."""

    def __init__(
        self,
        knowledge_item_repository: KnowledgeItemRepository,
        relationship_repository: RelationshipRepository,
        tag_repository: KnowledgeTagRepository,
        source_repository: SourceRepository,
        graph_service: KnowledgeGraphService,
        event_store: KnowledgeEventStore,
        event_publisher: EventPublisher,
    ):
        """Initialize the service.

        Args:
            knowledge_item_repository: Repository for knowledge item operations
            relationship_repository: Repository for relationship operations
            tag_repository: Repository for tag operations
            source_repository: Repository for source operations
            graph_service: Service for graph operations
            event_store: Store for knowledge domain events
            event_publisher: Service for publishing domain events
        """
        self._knowledge_item_repository = knowledge_item_repository
        self._relationship_repository = relationship_repository
        self._tag_repository = tag_repository
        self._source_repository = source_repository
        self._graph_service = graph_service
        self._event_store = event_store
        self._event_publisher = event_publisher

    async def create_knowledge_item(
        self,
        title: str,
        content: str,
        item_type: str,
        created_by: str,
        tags: Optional[List[Tag]] = None,
        source: Optional[Source] = None,
        confidence: float = 1.0,
    ) -> KnowledgeItem:
        """Create a new knowledge item.

        Args:
            title: Item title
            content: Item content
            item_type: Type of knowledge item
            created_by: ID of the user creating the item
            tags: Optional list of tags
            source: Optional source information
            confidence: Initial confidence score (0.0 to 1.0)

        Returns:
            The created knowledge item

        Raises:
            ValueError: If the item data is invalid
        """
        if not title or len(title.strip()) == 0:
            raise ValueError("Knowledge item title cannot be empty")

        if not content or len(content.strip()) == 0:
            raise ValueError("Knowledge item content cannot be empty")

        # Validate item type
        if item_type not in vars(ItemType).values():
            raise ValueError(f"Invalid item type: {item_type}")

        # Validate confidence score
        if not 0.0 <= confidence <= 1.0:
            raise ValueError("Confidence score must be between 0.0 and 1.0")

        # Create and save source if provided
        if source:
            source = await self._source_repository.add(source)
            # Publish source added event
            await self._event_publisher.publish_event(
                KnowledgeSourceAdded(
                    event_id=f"evt_{datetime.utcnow().timestamp()}_src",
                    event_type="knowledge.source_added",
                    aggregate_id=source.id,
                    aggregate_type="knowledge_source",
                    source=source,
                    added_by=created_by,
                )
            )

        # Create knowledge item
        knowledge_item = KnowledgeItem(
            id=f"ki_{datetime.utcnow().timestamp()}",  # Simple ID generation
            title=title,
            content=content,
            item_type=item_type,
            confidence=confidence,
            tags=tags or [],
            source=source,
            relationships=[],
            artifact_references=[],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        # Save tags if provided
        if tags:
            for tag in tags:
                await self._tag_repository.add(tag)
                # Publish tag added event
                await self._event_publisher.publish_event(
                    KnowledgeTagAdded(
                        event_id=f"evt_{datetime.utcnow().timestamp()}_tag_{tag.name}",
                        event_type="knowledge.tag_added",
                        aggregate_id=knowledge_item.id,
                        aggregate_type="knowledge_item",
                        knowledge_item_id=knowledge_item.id,
                        tag=tag,
                        added_by=created_by,
                    )
                )

        # Save the knowledge item
        knowledge_item = await self._knowledge_item_repository.add(knowledge_item)

        # Publish knowledge item created event
        await self._event_publisher.publish_event(
            KnowledgeItemCreated(
                event_id=f"evt_{datetime.utcnow().timestamp()}",
                event_type="knowledge.item_created",
                aggregate_id=knowledge_item.id,
                aggregate_type="knowledge_item",
                title=title,
                item_type=item_type,
                content=content,
                confidence=confidence,
                source=source,
                created_by=created_by,
            )
        )

        return knowledge_item

    async def establish_relationship(
        self,
        source_id: str,
        target_id: str,
        relationship_type: str,
        established_by: str,
        weight: float = 1.0,
        bidirectional: bool = False,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Relationship:
        """Establish a relationship between knowledge items.

        Args:
            source_id: ID of the source knowledge item
            target_id: ID of the target knowledge item
            relationship_type: Type of relationship
            established_by: ID of the user establishing the relationship
            weight: Relationship weight (0.0 to 1.0)
            bidirectional: Whether the relationship is bidirectional
            metadata: Optional relationship metadata

        Returns:
            The created relationship

        Raises:
            ValueError: If the relationship data is invalid
        """
        # Validate relationship type
        if relationship_type not in vars(RelationshipType).values():
            raise ValueError(f"Invalid relationship type: {relationship_type}")

        # Validate weight
        if not 0.0 <= weight <= 1.0:
            raise ValueError("Relationship weight must be between 0.0 and 1.0")

        # Verify both items exist
        source_item = await self._knowledge_item_repository.get_by_id(source_id)
        target_item = await self._knowledge_item_repository.get_by_id(target_id)

        if not source_item:
            raise ValueError(f"Source item {source_id} not found")
        if not target_item:
            raise ValueError(f"Target item {target_id} not found")

        # Create the relationship
        relationship = Relationship(
            id=f"rel_{datetime.utcnow().timestamp()}",  # Simple ID generation
            source_id=source_id,
            target_id=target_id,
            relationship_type=relationship_type,
            weight=weight,
            bidirectional=bidirectional,
            metadata=metadata or {},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        # Add relationship to both items
        source_item.add_relationship(relationship)
        await self._knowledge_item_repository.update(source_item)

        if bidirectional:
            target_item.add_relationship(relationship)
            await self._knowledge_item_repository.update(target_item)

        # Save the relationship
        relationship = await self._relationship_repository.add(relationship)

        # Publish relationship established event
        await self._event_publisher.publish_event(
            RelationshipEstablished(
                event_id=f"evt_{datetime.utcnow().timestamp()}",
                event_type="knowledge.relationship_established",
                aggregate_id=relationship.id,
                aggregate_type="relationship",
                source_id=source_id,
                target_id=target_id,
                relationship=relationship,
                established_by=established_by,
            )
        )

        return relationship

    async def find_related_items(
        self, item_id: str, max_depth: int = 2, min_weight: float = 0.5
    ) -> List[Dict[str, Any]]:
        """Find items related to a given knowledge item.

        Args:
            item_id: ID of the knowledge item
            max_depth: Maximum depth to search for relationships
            min_weight: Minimum relationship weight to consider

        Returns:
            List of related items with their relationship information

        Raises:
            ValueError: If the item doesn't exist
        """
        # Verify item exists
        item = await self._knowledge_item_repository.get_by_id(item_id)
        if not item:
            raise ValueError(f"Knowledge item {item_id} not found")

        # Use graph service to find connected items
        connected_items = await self._graph_service.get_connected_items(
            item_id, max_depth=max_depth
        )

        # Filter by weight and format results
        related_items = []
        for connected_item in connected_items:
            if connected_item.get("relationship", {}).get("weight", 0) >= min_weight:
                related_items.append(connected_item)

        return related_items

    async def update_item_confidence(
        self,
        item_id: str,
        new_confidence: float,
        updated_by: str,
        reason: Optional[str] = None,
    ) -> KnowledgeItem:
        """Update the confidence score of a knowledge item.

        Args:
            item_id: ID of the knowledge item
            new_confidence: New confidence score (0.0 to 1.0)
            updated_by: ID of the user updating the confidence
            reason: Optional reason for the update

        Returns:
            The updated knowledge item

        Raises:
            ValueError: If the item doesn't exist or validation fails
        """
        # Validate confidence score
        if not 0.0 <= new_confidence <= 1.0:
            raise ValueError("Confidence score must be between 0.0 and 1.0")

        # Get the knowledge item
        item = await self._knowledge_item_repository.get_by_id(item_id)
        if not item:
            raise ValueError(f"Knowledge item {item_id} not found")

        # Store the previous confidence for the event
        previous_confidence = item.confidence

        # Update confidence
        item.update_confidence(new_confidence)

        # Save the updated item
        item = await self._knowledge_item_repository.update(item)

        # Publish confidence updated event
        await self._event_publisher.publish_event(
            ConfidenceUpdated(
                event_id=f"evt_{datetime.utcnow().timestamp()}",
                event_type="knowledge.confidence_updated",
                aggregate_id=item.id,
                aggregate_type="knowledge_item",
                knowledge_item_id=item_id,
                previous_confidence=previous_confidence,
                new_confidence=new_confidence,
                updated_by=updated_by,
                reason=reason,
            )
        )

        return item
