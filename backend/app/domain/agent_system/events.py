"""
Agent System domain events.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

from app.domain.common.events import DomainEvent
from app.domain.agent_system.entities import Capability, KnowledgeSource


class AgentCreated(DomainEvent):
    """Event raised when a new agent is created."""

    name: str
    agent_type: str
    owner_id: str
    description: Optional[str]


class CapabilityAdded(DomainEvent):
    """Event raised when a capability is added to an agent."""

    agent_id: str
    capability: Capability
    added_by: str


class CapabilityRemoved(DomainEvent):
    """Event raised when a capability is removed from an agent."""

    agent_id: str
    capability: Capability
    removed_by: str


class KnowledgeSourceAdded(DomainEvent):
    """Event raised when a knowledge source is added to an agent."""

    agent_id: str
    knowledge_source: KnowledgeSource
    added_by: str


class ExecutionModeChanged(DomainEvent):
    """Event raised when an agent's execution mode changes."""

    agent_id: str
    previous_mode: str
    new_mode: str
    changed_by: str


class AgentExecutionStarted(DomainEvent):
    """Event raised when an agent starts execution."""

    agent_id: str
    execution_id: str
    initiated_by: str
    parameters: Dict[str, Any]


class AgentExecutionCompleted(DomainEvent):
    """Event raised when an agent completes execution."""

    agent_id: str
    execution_id: str
    duration: float
    result: Dict[str, Any]
    metadata: Dict[str, Any]
