"""
Conversation System domain entities.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class MessageType:
    """Message type value object."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ConversationState:
    """Conversation state value object."""

    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Message(BaseModel):
    """Message entity."""

    id: str
    conversation_id: str
    content: str
    message_type: str = Field(
        ...,
        pattern=f"^({MessageType.USER}|{MessageType.ASSISTANT}|{MessageType.SYSTEM})$",
    )
    sender_id: str
    created_at: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(from_attributes=True)


class Context(BaseModel):
    """Conversation context value object."""

    context_type: str
    data: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(from_attributes=True)


class Conversation(BaseModel):
    """Conversation aggregate root entity."""

    id: str
    project_id: str
    title: str = Field(..., min_length=1, max_length=200)
    state: str = Field(
        default=ConversationState.ACTIVE,
        pattern=f"^({'|'.join([v for v in vars(ConversationState).values() if isinstance(v, str)])})$",
    )
    participants: List[str] = Field(default_factory=list)  # List of user IDs
    messages: List[Message] = Field(default_factory=list)
    context: List[Context] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def add_message(self, message: Message) -> None:
        """Add a message to the conversation."""
        self.messages.append(message)
        self.updated_at = datetime.utcnow()

    def add_context(self, context: Context) -> None:
        """Add context to the conversation."""
        self.context.append(context)
        self.updated_at = datetime.utcnow()

    def add_participant(self, user_id: str) -> None:
        """Add a participant to the conversation."""
        if user_id not in self.participants:
            self.participants.append(user_id)
            self.updated_at = datetime.utcnow()

    def update_state(self, new_state: str) -> None:
        """Update the conversation state."""
        if new_state in [v for v in vars(ConversationState).values() if isinstance(v, str)]:
            self.state = new_state
            self.updated_at = datetime.utcnow()

    model_config = ConfigDict(from_attributes=True)
