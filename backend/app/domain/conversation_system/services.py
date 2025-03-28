"""
Conversation System domain services.

This module contains domain services that encapsulate complex business logic
for conversation management operations.
"""

from datetime import datetime
from typing import List, Optional, Protocol, Dict, Any

from app.domain.conversation_system.entities import (
    Conversation,
    Message,
    Context,
    MessageType,
    ConversationState,
)
from app.domain.conversation_system.interfaces import (
    ConversationRepository,
    MessageRepository,
    ContextRepository,
)
from app.domain.conversation_system.events import (
    ConversationCreated,
    MessageAdded,
    ContextUpdated,
    ConversationStateChanged,
    ParticipantAdded,
)
from app.domain.common.event_publisher import EventPublisher


class ConversationDomainService(Protocol):
    """Domain service for conversation-related operations."""

    async def create_conversation(
        self,
        project_id: str,
        title: str,
        created_by: str,
        initial_context: Optional[Dict[str, Any]] = None,
    ) -> Conversation:
        """Create a new conversation."""
        pass

    async def add_message(
        self,
        conversation_id: str,
        content: str,
        sender_id: str,
        message_type: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Message:
        """Add a message to a conversation."""
        pass

    async def update_context(
        self,
        conversation_id: str,
        context_type: str,
        data: Dict[str, Any],
        updated_by: str,
    ) -> Context:
        """Update conversation context."""
        pass

    async def validate_participant_access(
        self, conversation_id: str, user_id: str
    ) -> bool:
        """Validate user's access to a conversation."""
        pass


class DefaultConversationDomainService:
    """Default implementation of ConversationDomainService."""

    def __init__(
        self,
        conversation_repository: ConversationRepository,
        message_repository: MessageRepository,
        context_repository: ContextRepository,
        event_publisher: EventPublisher,
    ):
        """Initialize the service.

        Args:
            conversation_repository: Repository for conversation operations
            message_repository: Repository for message operations
            context_repository: Repository for context operations
            event_publisher: Service for publishing domain events
        """
        self._conversation_repository = conversation_repository
        self._message_repository = message_repository
        self._context_repository = context_repository
        self._event_publisher = event_publisher

    async def create_conversation(
        self,
        project_id: str,
        title: str,
        created_by: str,
        initial_context: Optional[Dict[str, Any]] = None,
    ) -> Conversation:
        """Create a new conversation.

        Args:
            project_id: ID of the project this conversation belongs to
            title: Conversation title
            created_by: ID of the user creating the conversation
            initial_context: Optional initial context data

        Returns:
            The created conversation

        Raises:
            ValueError: If the conversation title is invalid
        """
        if not title or len(title.strip()) == 0:
            raise ValueError("Conversation title cannot be empty")

        conversation = Conversation(
            id=f"conv_{datetime.utcnow().timestamp()}",  # Simple ID generation
            project_id=project_id,
            title=title,
            state=ConversationState.ACTIVE,
            participants=[created_by],
            messages=[],
            context=[],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        if initial_context:
            context = Context(
                context_type="initial",
                data=initial_context,
                timestamp=datetime.utcnow(),
            )
            conversation.add_context(context)

        # Save the conversation
        conversation = await self._conversation_repository.add(conversation)

        # Publish conversation created event
        await self._event_publisher.publish_event(
            ConversationCreated(
                event_id=f"evt_{datetime.utcnow().timestamp()}",
                event_type="conversation.created",
                aggregate_id=conversation.id,
                aggregate_type="conversation",
                project_id=project_id,
                title=title,
                created_by=created_by,
            )
        )

        if initial_context:
            # Publish context updated event
            await self._event_publisher.publish_event(
                ContextUpdated(
                    event_id=f"evt_{datetime.utcnow().timestamp()}_ctx",
                    event_type="conversation.context_updated",
                    aggregate_id=conversation.id,
                    aggregate_type="conversation",
                    conversation_id=conversation.id,
                    context_type="initial",
                    data=initial_context,
                    updated_by=created_by,
                )
            )

        return conversation

    async def add_message(
        self,
        conversation_id: str,
        content: str,
        sender_id: str,
        message_type: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Message:
        """Add a message to a conversation.

        Args:
            conversation_id: ID of the conversation
            content: Message content
            sender_id: ID of the message sender
            message_type: Type of message (user, assistant, system)
            metadata: Optional message metadata

        Returns:
            The created message

        Raises:
            ValueError: If the conversation doesn't exist or validation fails
        """
        conversation = await self._conversation_repository.get_by_id(conversation_id)
        if not conversation:
            raise ValueError(f"Conversation {conversation_id} not found")

        if conversation.state != ConversationState.ACTIVE:
            raise ValueError("Cannot add message to non-active conversation")

        if sender_id not in conversation.participants:
            raise ValueError("Sender must be a conversation participant")

        message = Message(
            id=f"msg_{datetime.utcnow().timestamp()}",  # Simple ID generation
            conversation_id=conversation_id,
            content=content,
            message_type=message_type,
            sender_id=sender_id,
            created_at=datetime.utcnow(),
            metadata=metadata or {},
        )

        # Add message to conversation and save both
        conversation.add_message(message)
        await self._conversation_repository.update(conversation)
        message = await self._message_repository.add(message)

        # Publish message added event
        await self._event_publisher.publish_event(
            MessageAdded(
                event_id=f"evt_{datetime.utcnow().timestamp()}",
                event_type="conversation.message_added",
                aggregate_id=conversation.id,
                aggregate_type="conversation",
                message_id=message.id,
                conversation_id=conversation_id,
                message_type=message_type,
                sender_id=sender_id,
                content=content,
                metadata=metadata or {},
            )
        )

        return message

    async def update_context(
        self,
        conversation_id: str,
        context_type: str,
        data: Dict[str, Any],
        updated_by: str,
    ) -> Context:
        """Update conversation context.

        Args:
            conversation_id: ID of the conversation
            context_type: Type of context being updated
            data: Context data
            updated_by: ID of the user updating the context

        Returns:
            The updated context

        Raises:
            ValueError: If the conversation doesn't exist or validation fails
        """
        conversation = await self._conversation_repository.get_by_id(conversation_id)
        if not conversation:
            raise ValueError(f"Conversation {conversation_id} not found")

        if updated_by not in conversation.participants:
            raise ValueError("Only participants can update context")

        context = Context(
            context_type=context_type, data=data, timestamp=datetime.utcnow()
        )

        conversation.add_context(context)
        await self._conversation_repository.update(conversation)

        # Publish context updated event
        await self._event_publisher.publish_event(
            ContextUpdated(
                event_id=f"evt_{datetime.utcnow().timestamp()}",
                event_type="conversation.context_updated",
                aggregate_id=conversation.id,
                aggregate_type="conversation",
                conversation_id=conversation_id,
                context_type=context_type,
                data=data,
                updated_by=updated_by,
            )
        )

        return context

    async def validate_participant_access(
        self, conversation_id: str, user_id: str
    ) -> bool:
        """Validate user's access to a conversation.

        Args:
            conversation_id: ID of the conversation to check
            user_id: ID of the user requesting access

        Returns:
            True if the user has access, False otherwise
        """
        conversation = await self._conversation_repository.get_by_id(conversation_id)
        if not conversation:
            return False

        return user_id in conversation.participants
