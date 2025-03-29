"""
Base domain event definitions.

This module provides base classes and utilities for domain events
across all bounded contexts.
"""

from abc import ABC, abstractmethod
import asyncio
from contextlib import asynccontextmanager
from datetime import datetime
from enum import Enum
from functools import wraps
import json
import logging
from typing import Any, Dict, Generic, List, Optional, Set, Type, TypeVar
from uuid import uuid4

from pydantic import (
    BaseModel,
    Field,
    model_validator,
    field_validator,
    field_serializer,
    ConfigDict,
)

logger = logging.getLogger(__name__)

T = TypeVar("T")


class EventPriority(Enum):
    """Priority levels for domain events."""

    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3


class EventStatus(Enum):
    """Status of a domain event in the processing lifecycle."""

    CREATED = "created"
    PUBLISHED = "published"
    PROCESSED = "processed"
    FAILED = "failed"
    RETRYING = "retrying"


class DomainEvent(BaseModel):
    """Base class for all domain events."""

    event_id: str = Field(default_factory=lambda: str(uuid4()))
    event_type: str
    aggregate_id: str
    aggregate_type: str
    version: int = 1
    occurred_on: datetime = Field(default_factory=datetime.utcnow)
    causation_id: Optional[str] = None
    correlation_id: Optional[str] = None
    priority: EventPriority = EventPriority.NORMAL
    status: EventStatus = EventStatus.CREATED
    retry_count: int = 0
    max_retries: int = 3
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_serializer("occurred_on")
    def serialize_occurred_on(cls, value: datetime) -> str:
        return value.isoformat()

    @field_serializer("priority")
    def serialize_priority(cls, value: EventPriority) -> int:
        return value.value

    @field_serializer("status")
    def serialize_status(cls, value: EventStatus) -> str:
        return value.value

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("event_type", mode="before", check_fields=False)
    @classmethod
    def set_event_type(cls, v):
        """Auto-set event_type if not provided."""
        return v or cls.__name__

    @model_validator(mode="before")
    @classmethod
    def set_correlation_chain(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Establish causation and correlation chains."""
        # If this event is caused by another event but no correlation ID exists,
        # use the causation ID (from parent event) as this event's correlation ID
        if (
            isinstance(values, dict)
            and "causation_id" in values
            and values["causation_id"]
            and "correlation_id" not in values
        ):
            values["correlation_id"] = values["causation_id"]
        return values

    def to_json(self) -> str:
        """Convert the event to a JSON string."""
        return json.dumps(self.model_dump())

    @classmethod
    def from_json(cls, json_str: str) -> "DomainEvent":
        """Create an event from a JSON string."""
        data = json.loads(json_str)
        return cls(**data)

    def with_retry(self) -> "DomainEvent":
        """Create a copy of this event with incremented retry count."""
        event_dict = self.model_dump()
        event_dict["retry_count"] += 1
        event_dict["status"] = EventStatus.RETRYING
        return self.__class__(**event_dict)

    def mark_as_published(self) -> "DomainEvent":
        """Create a copy of this event marked as published."""
        event_dict = self.model_dump()
        event_dict["status"] = EventStatus.PUBLISHED
        return self.__class__(**event_dict)

    def mark_as_processed(self) -> "DomainEvent":
        """Create a copy of this event marked as processed."""
        event_dict = self.model_dump()
        event_dict["status"] = EventStatus.PROCESSED
        return self.__class__(**event_dict)

    def mark_as_failed(self) -> "DomainEvent":
        """Create a copy of this event marked as failed."""
        event_dict = self.model_dump()
        event_dict["status"] = EventStatus.FAILED
        return self.__class__(**event_dict)


class EventHandler(ABC):
    """Interface for domain event handlers."""

    @abstractmethod
    async def handle(self, event: DomainEvent) -> None:
        """Handle a domain event."""
        pass

    @property
    def supported_events(self) -> List[Type[DomainEvent]]:
        """Get the event types this handler supports."""
        return []

    @property
    def retry_on_exceptions(self) -> List[Type[Exception]]:
        """Get the exception types that should trigger a retry."""
        return []

    @property
    def priority(self) -> EventPriority:
        """Get the handler's priority."""
        return EventPriority.NORMAL


class EventStore(Generic[T], ABC):
    """Interface for event storage."""

    @abstractmethod
    async def append(self, event: DomainEvent) -> None:
        """Append an event to the store."""
        pass

    @abstractmethod
    async def get_events_for_aggregate(
        self, aggregate_id: str, aggregate_type: str, since_version: int = 0
    ) -> List[DomainEvent]:
        """Get all events for an aggregate from a specific version."""
        pass

    @abstractmethod
    async def get_events_by_correlation_id(self, correlation_id: str) -> List[DomainEvent]:
        """Get all events with a specific correlation ID."""
        pass

    @abstractmethod
    async def get_events_by_type(
        self, event_type: str, since: Optional[datetime] = None, limit: int = 100
    ) -> List[DomainEvent]:
        """Get events of a specific type."""
        pass


class InMemoryEventStore(EventStore):
    """In-memory implementation of event store."""

    def __init__(self):
        """Initialize a new in-memory event store."""
        self._events: List[DomainEvent] = []

    async def append(self, event: DomainEvent) -> None:
        """Append an event to the store."""
        self._events.append(event)

    async def get_events_for_aggregate(
        self, aggregate_id: str, aggregate_type: str, since_version: int = 0
    ) -> List[DomainEvent]:
        """Get all events for an aggregate from a specific version."""
        return [
            event
            for event in self._events
            if event.aggregate_id == aggregate_id
            and event.aggregate_type == aggregate_type
            and event.version > since_version
        ]

    async def get_events_by_correlation_id(self, correlation_id: str) -> List[DomainEvent]:
        """Get all events with a specific correlation ID."""
        return [event for event in self._events if event.correlation_id == correlation_id]

    async def get_events_by_type(
        self, event_type: str, since: Optional[datetime] = None, limit: int = 100
    ) -> List[DomainEvent]:
        """Get events of a specific type."""
        filtered_events = [
            event
            for event in self._events
            if event.event_type == event_type and (since is None or event.occurred_on >= since)
        ]
        return filtered_events[-limit:] if limit > 0 else filtered_events


class EventBus(ABC):
    """Interface for the domain event bus."""

    @abstractmethod
    async def publish(self, event: DomainEvent) -> None:
        """Publish an event to the event bus."""
        pass

    @abstractmethod
    async def publish_batch(self, events: List[DomainEvent]) -> None:
        """Publish multiple events to the event bus."""
        pass

    @abstractmethod
    def subscribe(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        """Subscribe a handler to a specific event type."""
        pass

    @abstractmethod
    def unsubscribe(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        """Unsubscribe a handler from a specific event type."""
        pass

    @property
    @abstractmethod
    def event_store(self) -> EventStore:
        """Get the event store used by this event bus."""
        pass


class RetryPolicy:
    """Configures retry behavior for event handlers."""

    def __init__(
        self,
        max_retries: int = 3,
        backoff_factor: float = 1.5,
        initial_delay: float = 1.0,
        max_delay: float = 60.0,
        retry_on_exceptions: Optional[List[Type[Exception]]] = None,
    ):
        """Initialize a new retry policy."""
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.retry_on_exceptions = retry_on_exceptions if retry_on_exceptions is not None else []

    def should_retry(self, exception: Exception, attempt: int) -> bool:
        """Determine if a retry should be attempted."""
        if attempt >= self.max_retries:
            return False

        # If no exceptions are specified, retry on any exception
        if not self.retry_on_exceptions:
            return True

        # Otherwise, only retry on specified exceptions
        return any(isinstance(exception, exc_type) for exc_type in self.retry_on_exceptions)

    def get_delay(self, attempt: int) -> float:
        """Calculate the delay before the next retry attempt."""
        delay = self.initial_delay * (self.backoff_factor**attempt)
        return min(delay, self.max_delay)


class InMemoryEventBus(EventBus):
    """In-memory implementation of the event bus for domain events."""

    def __init__(self, event_store: Optional[EventStore] = None):
        """Initialize a new in-memory event bus."""
        self._handlers: Dict[str, Set[EventHandler]] = {}
        self._event_store = event_store or InMemoryEventStore()
        self._retry_policy = RetryPolicy()
        self._lock = asyncio.Lock()

    @property
    def event_store(self) -> EventStore:
        """Get the event store used by this event bus."""
        return self._event_store

    async def publish(self, event: DomainEvent) -> None:
        """Publish an event to registered handlers."""
        # Store the event
        await self._event_store.append(event)

        # Mark as published
        published_event = event.mark_as_published()

        event_type_name = event.event_type
        if event_type_name not in self._handlers:
            logger.debug(f"No handlers registered for event type {event_type_name}")
            return

        # Sort handlers by priority
        sorted_handlers = sorted(
            self._handlers[event_type_name],
            key=lambda h: h.priority.value,
            reverse=True,  # Higher priority first
        )

        # Process handlers sequentially by priority
        for handler in sorted_handlers:
            try:
                await self._process_with_retry(handler, published_event)
            except Exception as e:
                logger.error(
                    f"Error in handler {handler.__class__.__name__} for event {event_type_name}: {str(e)}"
                )
                # We continue processing other handlers even if one fails

    async def _process_with_retry(self, handler: EventHandler, event: DomainEvent) -> None:
        """Process an event with a handler, applying retry logic."""
        attempt = 0
        last_exception = None

        while attempt <= self._retry_policy.max_retries:
            try:
                await handler.handle(event)
                return  # Success, exit retry loop
            except Exception as e:
                last_exception = e
                attempt += 1

                # Check if we should retry
                if not self._retry_policy.should_retry(e, attempt):
                    break

                # Calculate delay before next retry
                delay = self._retry_policy.get_delay(attempt)
                logger.warning(
                    f"Handler {handler.__class__.__name__} failed for event {event.event_id}. "
                    f"Retry {attempt}/{self._retry_policy.max_retries} in {delay:.2f}s: {str(e)}"
                )
                await asyncio.sleep(delay)

        # If we get here, all retries failed
        if last_exception:
            logger.error(
                f"Handler {handler.__class__.__name__} failed for event {event.event_id} "
                f"after {attempt} attempts: {str(last_exception)}"
            )
            raise last_exception

    async def publish_batch(self, events: List[DomainEvent]) -> None:
        """Publish multiple events to the event bus."""
        async with self._lock:
            for event in events:
                await self.publish(event)

    def subscribe(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        """Subscribe a handler to a specific event type."""
        event_type_name = event_type.__name__
        if event_type_name not in self._handlers:
            self._handlers[event_type_name] = set()
        self._handlers[event_type_name].add(handler)
        logger.debug(f"Handler {handler.__class__.__name__} subscribed to event {event_type_name}")

        # Also register for all events the handler explicitly supports
        for supported_event in handler.supported_events:
            supported_name = supported_event.__name__
            if supported_name != event_type_name:
                if supported_name not in self._handlers:
                    self._handlers[supported_name] = set()
                self._handlers[supported_name].add(handler)
                logger.debug(
                    f"Handler {handler.__class__.__name__} also subscribed to event {supported_name}"
                )

    def unsubscribe(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        """Unsubscribe a handler from a specific event type."""
        event_type_name = event_type.__name__
        if event_type_name in self._handlers and handler in self._handlers[event_type_name]:
            self._handlers[event_type_name].remove(handler)
            logger.debug(
                f"Handler {handler.__class__.__name__} unsubscribed from event {event_type_name}"
            )

        # Also unregister from supported events
        for supported_event in handler.supported_events:
            supported_name = supported_event.__name__
            if supported_name in self._handlers and handler in self._handlers[supported_name]:
                self._handlers[supported_name].remove(handler)


# Singleton instance of the event bus and event store
_event_bus_instance = None
_event_store_instance = None


def get_event_store() -> EventStore:
    """Get the singleton event store instance."""
    global _event_store_instance
    if _event_store_instance is None:
        _event_store_instance = InMemoryEventStore()
    return _event_store_instance


def get_event_bus() -> EventBus:
    """Get the singleton event bus instance."""
    global _event_bus_instance
    if _event_bus_instance is None:
        _event_bus_instance = InMemoryEventBus(get_event_store())
    return _event_bus_instance


def configure_event_bus(event_bus: EventBus) -> None:
    """Configure the singleton event bus instance."""
    global _event_bus_instance
    _event_bus_instance = event_bus


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
        await event_bus.publish_batch(events)

    except Exception as e:
        # If an exception occurs, log it and re-raise
        logger.error(f"Transaction failed, events not published: {e}")
        raise


def event_sourced(aggregate_class):
    """Decorator to make an aggregate class event-sourced."""

    @wraps(aggregate_class)
    class EventSourcedAggregate(aggregate_class):
        """Event-sourced version of the aggregate class."""

        _applied_events: List[DomainEvent] = []

        @classmethod
        async def from_history(cls, aggregate_id: str):
            """Reconstruct an aggregate from its event history."""
            aggregate = cls(id=aggregate_id)
            event_store = get_event_store()
            events = await event_store.get_events_for_aggregate(
                aggregate_id=aggregate_id, aggregate_type=cls.__name__
            )
            for event in events:
                aggregate.apply(event, is_new=False)
            return aggregate

        def apply(self, event: DomainEvent, is_new: bool = True):
            """Apply an event to the aggregate."""
            # This will be overridden by subclasses to handle specific event types
            handler_method = f"apply_{event.event_type}"
            if hasattr(self, handler_method):
                getattr(self, handler_method)(event)

            if is_new:
                self._applied_events.append(event)

            return self

        async def commit_events(self):
            """Commit all applied events to the event store."""
            event_bus = get_event_bus()
            if self._applied_events:
                await event_bus.publish_batch(self._applied_events)
                self._applied_events.clear()

    return EventSourcedAggregate
