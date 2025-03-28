"""
Base domain interfaces and abstractions for the Cognitive Workspace application.

This module defines core domain concepts that are shared across all bounded contexts
in the application, following Domain-Driven Design principles.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import (
    Generic,
    TypeVar,
    List,
    Optional,
    Dict,
    Any,
    Protocol,
    runtime_checkable,
)
from uuid import UUID, uuid4

# Type variable for domain entities
T = TypeVar("T")
ID = TypeVar("ID")


class DomainEvent:
    """Base class for all domain events in the system.

    Domain events represent significant occurrences within the domain that
    domain experts care about.
    """

    event_id: UUID
    timestamp: datetime

    def __init__(self):
        """Initialize a new domain event with a unique ID and current timestamp."""
        self.event_id = uuid4()
        self.timestamp = datetime.now()


@runtime_checkable
class Entity(Protocol):
    """Interface for all domain entities.

    Entities are objects that have a distinct identity that runs through time
    and different states.
    """

    id: Any

    def __eq__(self, other: Any) -> bool:
        """Entities are equal if their IDs are equal."""
        if not isinstance(other, Entity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash based on the entity's ID."""
        return hash(self.id)


@runtime_checkable
class AggregateRoot(Entity, Protocol):
    """Interface for aggregate roots in the domain.

    Aggregate roots are entities that are the entry point to an aggregate,
    which is a cluster of associated objects treated as a unit for data changes.
    """

    _events: List[DomainEvent]

    def add_event(self, event: DomainEvent) -> None:
        """Add a domain event to the aggregate's collection of events."""
        self._events.append(event)

    def clear_events(self) -> List[DomainEvent]:
        """Clear and return all pending domain events."""
        events = self._events.copy()
        self._events.clear()
        return events


class Repository(Generic[T, ID], ABC):
    """Base interface for all repositories.

    Repositories mediate between the domain and data mapping layers, acting like
    collections of domain objects in memory.
    """

    @abstractmethod
    async def get_by_id(self, id: ID) -> Optional[T]:
        """Retrieve an entity by its ID."""
        pass

    @abstractmethod
    async def save(self, entity: T) -> T:
        """Save an entity and return the saved entity."""
        pass

    @abstractmethod
    async def delete(self, entity: T) -> None:
        """Delete an entity."""
        pass


class ValueObject(ABC):
    """Base class for value objects.

    Value objects are objects that describe characteristics of entities and
    don't have an identity of their own.
    """

    def __eq__(self, other: Any) -> bool:
        """Value objects are equal if all their properties are equal."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __hash__(self) -> int:
        """Hash based on all properties of the value object."""
        return hash(tuple(sorted(self.__dict__.items())))


class DomainService(ABC):
    """Base interface for domain services.

    Domain services represent operations that don't naturally fit within an entity
    or value object, often involving multiple domain objects.
    """

    pass


class DomainException(Exception):
    """Base exception for all domain-related exceptions."""

    pass
