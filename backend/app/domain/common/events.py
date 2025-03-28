"""
Base domain event definitions.

This module provides base classes and utilities for domain events
across all bounded contexts.
"""

from datetime import datetime
from typing import Dict, Any
from pydantic import BaseModel, Field


class DomainEvent(BaseModel):
    """Base class for all domain events."""

    event_id: str
    event_type: str
    aggregate_id: str
    aggregate_type: str
    occurred_on: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        """Pydantic configuration."""

        json_encoders = {datetime: lambda dt: dt.isoformat()}


"""
Domain event bus implementation for publishing and subscribing to domain events.

This module provides a central event bus for domain events to facilitate
communication between bounded contexts following the Domain-Driven Design approach.
"""

from abc import ABC, abstractmethod
from typing import Callable, Dict, List, Type, Set, Any
import logging
import asyncio
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)


class EventHandler(ABC):
    """Interface for domain event handlers."""

    @abstractmethod
    async def handle(self, event: DomainEvent) -> None:
        """Handle a domain event."""
        pass


class EventBus(ABC):
    """Interface for the domain event bus."""

    @abstractmethod
    async def publish(self, event: DomainEvent) -> None:
        """Publish an event to the event bus."""
        pass

    @abstractmethod
    def subscribe(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        """Subscribe a handler to a specific event type."""
        pass

    @abstractmethod
    def unsubscribe(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        """Unsubscribe a handler from a specific event type."""
        pass


class InMemoryEventBus(EventBus):
    """In-memory implementation of the event bus for domain events."""

    def __init__(self):
        """Initialize a new in-memory event bus."""
        self._handlers: Dict[Type[DomainEvent], Set[EventHandler]] = {}

    async def publish(self, event: DomainEvent) -> None:
        """Publish an event to registered handlers."""
        event_type = type(event)
        if event_type not in self._handlers:
            logger.debug(f"No handlers registered for event type {event_type.__name__}")
            return

        handlers = self._handlers[event_type]
        publish_tasks = [handler.handle(event) for handler in handlers]

        if publish_tasks:
            try:
                await asyncio.gather(*publish_tasks)
            except Exception as e:
                logger.error(f"Error publishing event {event_type.__name__}: {e}")
                # Re-raise the exception to allow the caller to handle it
                raise

    def subscribe(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        """Subscribe a handler to a specific event type."""
        if event_type not in self._handlers:
            self._handlers[event_type] = set()
        self._handlers[event_type].add(handler)
        logger.debug(
            f"Handler {handler.__class__.__name__} subscribed to event {event_type.__name__}"
        )

    def unsubscribe(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        """Unsubscribe a handler from a specific event type."""
        if event_type in self._handlers and handler in self._handlers[event_type]:
            self._handlers[event_type].remove(handler)
            logger.debug(
                f"Handler {handler.__class__.__name__} unsubscribed from event {event_type.__name__}"
            )


# Singleton instance of the event bus
_event_bus_instance = None


def get_event_bus() -> EventBus:
    """Get the singleton event bus instance."""
    global _event_bus_instance
    if _event_bus_instance is None:
        _event_bus_instance = InMemoryEventBus()
    return _event_bus_instance


@asynccontextmanager
async def transaction_context():
    """Context manager for transaction-like behavior with the event bus.

    Events are collected during the transaction and published only if
    the transaction completes successfully.
    """
    events: List[DomainEvent] = []

    try:
        # Yield the events list to the caller
        yield events

        # If we get here, the transaction was successful, so publish the events
        event_bus = get_event_bus()
        for event in events:
            await event_bus.publish(event)

    except Exception as e:
        # If an exception occurs, log it and re-raise
        logger.error(f"Transaction failed, events not published: {e}")
        raise
