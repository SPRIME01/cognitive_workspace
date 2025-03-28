"""
Knowledge Management domain interfaces.
"""

from typing import List, Optional, Protocol, Dict, Any, Set
from datetime import datetime

from app.domain.common.interfaces import Repository
from app.domain.knowledge_management.entities import (
    KnowledgeItem,
    Relationship,
    Tag,
    Source,
)


class KnowledgeItemRepository(Repository[KnowledgeItem], Protocol):
    """Repository interface for KnowledgeItem aggregate."""

    async def get_by_type(
        self, item_type: str, skip: int = 0, limit: int = 100
    ) -> List[KnowledgeItem]:
        """Get knowledge items by type."""
        pass

    async def search_by_title(
        self, title: str, skip: int = 0, limit: int = 100
    ) -> List[KnowledgeItem]:
        """Search knowledge items by title."""
        pass

    async def search_by_content(
        self, content: str, skip: int = 0, limit: int = 100
    ) -> List[KnowledgeItem]:
        """Search knowledge items by content."""
        pass

    async def get_by_confidence(
        self, min_confidence: float = 0.0, max_confidence: float = 1.0
    ) -> List[KnowledgeItem]:
        """Get knowledge items within a confidence range."""
        pass

    async def get_by_tag(
        self, tag: str, skip: int = 0, limit: int = 100
    ) -> List[KnowledgeItem]:
        """Get knowledge items by tag."""
        pass

    async def get_by_artifact(self, artifact_id: str) -> List[KnowledgeItem]:
        """Get knowledge items related to an artifact."""
        pass


class RelationshipRepository(Repository[Relationship], Protocol):
    """Repository interface for Relationship entity."""

    async def get_by_source(self, source_id: str) -> List[Relationship]:
        """Get all relationships where the item is the source."""
        pass

    async def get_by_target(self, target_id: str) -> List[Relationship]:
        """Get all relationships where the item is the target."""
        pass

    async def get_by_type(
        self, relationship_type: str, skip: int = 0, limit: int = 100
    ) -> List[Relationship]:
        """Get relationships by type."""
        pass

    async def get_bidirectional(self) -> List[Relationship]:
        """Get all bidirectional relationships."""
        pass


class KnowledgeTagRepository(Repository[Tag], Protocol):
    """Repository interface for knowledge Tag entity."""

    async def get_by_category(self, category: str) -> List[Tag]:
        """Get all tags in a category."""
        pass

    async def get_popular_tags(self, limit: int = 10) -> List[Tag]:
        """Get most frequently used tags."""
        pass

    async def get_related_tags(self, tag_name: str) -> List[Tag]:
        """Get tags frequently used together with the given tag."""
        pass


class SourceRepository(Repository[Source], Protocol):
    """Repository interface for knowledge Source entity."""

    async def get_by_type(self, source_type: str) -> List[Source]:
        """Get sources by type."""
        pass

    async def get_by_url(self, url: str) -> Optional[Source]:
        """Get source by URL."""
        pass


class KnowledgeGraphService(Protocol):
    """Interface for knowledge graph operations."""

    async def get_connected_items(
        self, item_id: str, max_depth: int = 2
    ) -> List[Dict[str, Any]]:
        """Get items connected to the given item up to max_depth."""
        pass

    async def find_paths(
        self, source_id: str, target_id: str, max_depth: int = 3
    ) -> List[List[Dict[str, Any]]]:
        """Find all paths between two items up to max_depth."""
        pass

    async def get_subgraph(self, item_ids: Set[str]) -> Dict[str, Any]:
        """Get a subgraph containing the specified items and their relationships."""
        pass

    async def detect_clusters(self) -> List[Set[str]]:
        """Detect clusters of closely related items."""
        pass


class KnowledgeEventStore(Protocol):
    """Interface for storing knowledge domain events."""

    async def append_events(self, knowledge_item_id: str, events: List[dict]) -> None:
        """Append events to the knowledge item event stream."""
        pass

    async def get_events(
        self, knowledge_item_id: str, since: Optional[datetime] = None
    ) -> List[dict]:
        """Get events for a knowledge item since a specific time."""
        pass
