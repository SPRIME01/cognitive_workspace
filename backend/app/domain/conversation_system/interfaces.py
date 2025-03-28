"""
Conversation System domain interfaces.
"""

from typing import List, Optional, Protocol, Dict, Any
from datetime import datetime

from app.domain.common.interfaces import Repository
from app.domain.conversation_system.entities import Conversation, Message, Context


class ConversationRepository(Repository[Conversation], Protocol):
    """Repository interface for Conversation aggregate."""

    async def get_by_project(
        self, project_id: str, skip: int = 0, limit: int = 100
    ) -> List[Conversation]:
        """Get conversations by project ID."""
        pass

    async def get_by_participant(
        self, participant_id: str, skip: int = 0, limit: int = 100
    ) -> List[Conversation]:
        """Get conversations by participant ID."""
        pass

    async def search_by_title(
        self, title: str, skip: int = 0, limit: int = 100
    ) -> List[Conversation]:
        """Search conversations by title."""
        pass

    async def get_active_conversations(
        self, project_id: str, skip: int = 0, limit: int = 100
    ) -> List[Conversation]:
        """Get active conversations for a project."""
        pass


class MessageRepository(Repository[Message], Protocol):
    """Repository interface for Message entity."""

    async def get_by_conversation(
        self, conversation_id: str, skip: int = 0, limit: int = 100
    ) -> List[Message]:
        """Get messages by conversation ID."""
        pass

    async def get_by_sender(
        self, sender_id: str, skip: int = 0, limit: int = 100
    ) -> List[Message]:
        """Get messages by sender ID."""
        pass

    async def search_by_content(
        self, content: str, skip: int = 0, limit: int = 100
    ) -> List[Message]:
        """Search messages by content."""
        pass


class ContextRepository(Repository[Context], Protocol):
    """Repository interface for Context entity."""

    async def get_by_conversation(self, conversation_id: str) -> List[Context]:
        """Get all context entries for a conversation."""
        pass

    async def get_by_type(
        self, conversation_id: str, context_type: str
    ) -> Optional[Context]:
        """Get context by type for a conversation."""
        pass


class ConversationEventStore(Protocol):
    """Interface for storing conversation domain events."""

    async def append_events(self, conversation_id: str, events: List[dict]) -> None:
        """Append events to the conversation event stream."""
        pass

    async def get_events(
        self, conversation_id: str, since: Optional[datetime] = None
    ) -> List[dict]:
        """Get events for a conversation since a specific time."""
        pass
