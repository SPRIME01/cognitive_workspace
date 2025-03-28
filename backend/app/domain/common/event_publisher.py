"""
Event publisher service.

This module provides a service for publishing domain events to the event bus.
"""

from typing import List, Dict, Any, Protocol
from uuid import uuid4
from datetime import datetime

from app.domain.common.events import DomainEvent


class EventPublisher(Protocol):
    """Interface for publishing domain events."""

    async def publish_event(self, event: DomainEvent) -> None:
        """Publish a single domain event."""
        pass

    async def publish_events(self, events: List[DomainEvent]) -> None:
        """Publish multiple domain events."""
        pass


class DefaultEventPublisher:
    """Default implementation of the event publisher."""

    def __init__(self, event_bus: Any):
        """Initialize the event publisher.

        Args:
            event_bus: Event bus implementation
        """
        self._event_bus = event_bus

    async def publish_event(self, event: DomainEvent) -> None:
        """Publish a single domain event.

        Args:
            event: Domain event to publish
        """
        # Generate event ID if not present
        if not hasattr(event, "event_id") or not event.event_id:
            event.event_id = str(uuid4())

        # Set timestamp if not present
        if not hasattr(event, "occurred_on") or not event.occurred_on:
            event.occurred_on = datetime.utcnow()

        await self._event_bus.publish(event)

    async def publish_events(self, events: List[DomainEvent]) -> None:
        """Publish multiple domain events.

        Args:
            events: List of domain events to publish
        """
        for event in events:
            await self.publish_event(event)
