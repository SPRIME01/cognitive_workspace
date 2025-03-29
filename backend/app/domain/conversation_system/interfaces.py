"""
Conversation System domain interfaces.
"""

from typing import List, Optional, Protocol, Dict, Any
from datetime import datetime

from app.domain.common.interfaces import Repository
from app.domain.conversation_system.entities import Conversation, Message, Context


class ConversationRepository(Protocol):
    """Repository interface for Conversation aggregate."""

    # Include Repository methods for Conversation
    async def get_by_id(self, id: str) -> Optional[Conversation]:
        """Get an entity by its ID."""
        ...

    async def exists(self, id: str) -> bool:
        """Check if an entity with the given ID exists."""
        ...

    async def add(self, entity: Conversation) -> Conversation:
        """Add a new entity."""
        ...

    async def update(self, entity: Conversation) -> Conversation:
        """Update an existing entity."""
        ...

    async def delete(self, id: str) -> bool:
        """Delete an entity by its ID."""
        ...

    # Conversation-specific methods
    async def get_by_project(
        self, project_id: str, skip: int = 0, limit: int = 100
    ) -> List[Conversation]:
        """Get conversations by project ID."""
        ...

    async def get_by_participant(
        self, participant_id: str, skip: int = 0, limit: int = 100
    ) -> List[Conversation]:
        """Get conversations by participant ID."""
        ...

    async def search_by_title(
        self, title: str, skip: int = 0, limit: int = 100
    ) -> List[Conversation]:
        """Search conversations by title."""
        ...

    async def get_active_conversations(
        self, project_id: str, skip: int = 0, limit: int = 100
    ) -> List[Conversation]:
        """Get active conversations for a project."""
        ...


class MessageRepository(Protocol):
    """Repository interface for Message entity."""

    # Include Repository methods for Message
    async def get_by_id(self, id: str) -> Optional[Message]:
        """Get an entity by its ID."""
        ...

    async def exists(self, id: str) -> bool:
        """Check if an entity with the given ID exists."""
        ...

    async def add(self, entity: Message) -> Message:
        """Add a new entity."""
        ...

    async def update(self, entity: Message) -> Message:
        """Update an existing entity."""
        ...

    async def delete(self, id: str) -> bool:
        """Delete an entity by its ID."""
        ...

    # Message-specific methods
    async def get_by_conversation(
        self, conversation_id: str, skip: int = 0, limit: int = 100
    ) -> List[Message]:
        """Get messages by conversation ID."""
        ...

    async def get_by_sender(self, sender_id: str, skip: int = 0, limit: int = 100) -> List[Message]:
        """Get messages by sender ID."""
        ...

    async def search_by_content(
        self, content: str, skip: int = 0, limit: int = 100
    ) -> List[Message]:
        """Search messages by content."""
        ...


class ContextRepository(Protocol):
    """Repository interface for Context entity."""

    # Include Repository methods for Context
    async def get_by_id(self, id: str) -> Optional[Context]:
        """Get an entity by its ID."""
        ...

    async def exists(self, id: str) -> bool:
        """Check if an entity with the given ID exists."""
        ...

    async def add(self, entity: Context) -> Context:
        """Add a new entity."""
        ...

    async def update(self, entity: Context) -> Context:
        """Update an existing entity."""
        ...

    async def delete(self, id: str) -> bool:
        """Delete an entity by its ID."""
        ...

    # Context-specific methods
    async def get_by_conversation(self, conversation_id: str) -> List[Context]:
        """Get all context entries for a conversation."""
        ...

    async def get_by_type(self, conversation_id: str, context_type: str) -> Optional[Context]:
        """Get context by type for a conversation."""
        ...


class ConversationEventStore(Protocol):
    """Interface for storing conversation domain events."""

    async def append_events(self, conversation_id: str, events: List[dict]) -> None:
        """Append events to the conversation event stream."""
        ...

    async def get_events(
        self, conversation_id: str, since: Optional[datetime] = None
    ) -> List[dict]:
        """Get events for a conversation since a specific time."""
        ...
