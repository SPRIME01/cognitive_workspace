"""
Conversation System domain events.
"""

from typing import Dict, Any, Optional
from datetime import datetime

from app.domain.common.events import DomainEvent


class ConversationCreated(DomainEvent):
    """Event raised when a new conversation is created."""

    project_id: str
    title: str
    created_by: str


class MessageAdded(DomainEvent):
    """Event raised when a message is added to a conversation."""

    message_id: str
    conversation_id: str
    message_type: str
    sender_id: str
    content: str
    metadata: Dict[str, Any]


class ContextUpdated(DomainEvent):
    """Event raised when conversation context is updated."""

    conversation_id: str
    context_type: str
    data: Dict[str, Any]
    updated_by: str


class ConversationStateChanged(DomainEvent):
    """Event raised when a conversation's state changes."""

    conversation_id: str
    previous_state: str
    new_state: str
    changed_by: str


class ParticipantAdded(DomainEvent):
    """Event raised when a participant is added to a conversation."""

    conversation_id: str
    participant_id: str
    added_by: str
