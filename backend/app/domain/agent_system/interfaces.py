"""
Agent System domain interfaces.
"""

from typing import List, Optional, Protocol, Dict, Any
from datetime import datetime

from app.domain.common.interfaces import Repository
from app.domain.agent_system.entities import Agent, Capability, KnowledgeSource


class AgentRepository(Protocol):
    """Repository interface for Agent aggregate."""

    # Include Repository methods for Agent
    async def get_by_id(self, id: str) -> Optional[Agent]:
        """Get an entity by its ID."""
        ...

    async def exists(self, id: str) -> bool:
        """Check if an entity with the given ID exists."""
        ...

    async def add(self, entity: Agent) -> Agent:
        """Add a new entity."""
        ...

    async def update(self, entity: Agent) -> Agent:
        """Update an existing entity."""
        ...

    async def delete(self, id: str) -> bool:
        """Delete an entity by its ID."""
        ...

    # Agent-specific methods
    async def get_by_owner(self, owner_id: str, skip: int = 0, limit: int = 100) -> List[Agent]:
        """Get agents by owner ID."""
        ...

    async def get_by_type(self, agent_type: str, skip: int = 0, limit: int = 100) -> List[Agent]:
        """Get agents by type."""
        ...

    async def search_by_name(self, name: str, skip: int = 0, limit: int = 100) -> List[Agent]:
        """Search agents by name."""
        ...

    async def get_by_capability(
        self, capability_type: str, skip: int = 0, limit: int = 100
    ) -> List[Agent]:
        """Get agents by capability type."""
        ...


class CapabilityRepository(Protocol):
    """Repository interface for Capability entity."""

    # Include Repository methods for Capability
    async def get_by_id(self, id: str) -> Optional[Capability]:
        """Get an entity by its ID."""
        ...

    async def exists(self, id: str) -> bool:
        """Check if an entity with the given ID exists."""
        ...

    async def add(self, entity: Capability) -> Capability:
        """Add a new entity."""
        ...

    async def update(self, entity: Capability) -> Capability:
        """Update an existing entity."""
        ...

    async def delete(self, id: str) -> bool:
        """Delete an entity by its ID."""
        ...

    # Capability-specific methods
    async def get_by_agent(self, agent_id: str) -> List[Capability]:
        """Get all capabilities for an agent."""
        ...

    async def get_by_type(
        self, capability_type: str, skip: int = 0, limit: int = 100
    ) -> List[Capability]:
        """Get capabilities by type."""
        ...

    async def get_popular_capabilities(self, limit: int = 10) -> List[Capability]:
        """Get most frequently used capabilities."""
        ...


class KnowledgeSourceRepository(Protocol):
    """Repository interface for KnowledgeSource entity."""

    # Include Repository methods for KnowledgeSource
    async def get_by_id(self, id: str) -> Optional[KnowledgeSource]:
        """Get an entity by its ID."""
        ...

    async def exists(self, id: str) -> bool:
        """Check if an entity with the given ID exists."""
        ...

    async def add(self, entity: KnowledgeSource) -> KnowledgeSource:
        """Add a new entity."""
        ...

    async def update(self, entity: KnowledgeSource) -> KnowledgeSource:
        """Update an existing entity."""
        ...

    async def delete(self, id: str) -> bool:
        """Delete an entity by its ID."""
        ...

    # KnowledgeSource-specific methods
    async def get_by_agent(self, agent_id: str) -> List[KnowledgeSource]:
        """Get all knowledge sources for an agent."""
        ...

    async def get_by_source_type(
        self, source_type: str, skip: int = 0, limit: int = 100
    ) -> List[KnowledgeSource]:
        """Get knowledge sources by type."""
        ...

    async def get_by_priority(
        self, min_priority: int = 0, max_priority: int = 100
    ) -> List[KnowledgeSource]:
        """Get knowledge sources within a priority range."""
        ...


class AgentExecutionStore(Protocol):
    """Interface for storing agent execution history and metrics."""

    async def record_execution(self, agent_id: str, execution_data: Dict[str, Any]) -> str:
        """Record an agent execution instance."""
        ...

    async def get_execution_history(
        self, agent_id: str, since: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """Get execution history for an agent."""
        ...

    async def get_execution_metrics(
        self, agent_id: str, since: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get execution metrics for an agent."""
        ...


class AgentEventStore(Protocol):
    """Interface for storing agent domain events."""

    async def append_events(self, agent_id: str, events: List[dict]) -> None:
        """Append events to the agent event stream."""
        ...

    async def get_events(self, agent_id: str, since: Optional[datetime] = None) -> List[dict]:
        """Get events for an agent since a specific time."""
        ...
