"""
Common domain interfaces.
"""

from typing import Generic, TypeVar, Optional, List, Protocol
from abc import ABC, abstractmethod

T = TypeVar("T")


class Repository(Generic[T], ABC):
    """Base repository interface."""

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[T]:
        """Get an entity by its ID."""
        pass

    @abstractmethod
    async def list(self, skip: int = 0, limit: int = 100) -> List[T]:
        """List entities with pagination."""
        pass

    @abstractmethod
    async def add(self, entity: T) -> T:
        """Add a new entity."""
        pass

    @abstractmethod
    async def update(self, entity: T) -> T:
        """Update an existing entity."""
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete an entity by its ID."""
        pass
