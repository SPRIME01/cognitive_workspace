"""
Agent System domain interfaces.
"""

from typing import List, Optional, Protocol, Dict, Any
from datetime import datetime

from app.domain.common.interfaces import Repository
from app.domain.agent_system.entities import Agent, Capability, KnowledgeSource


class AgentRepository(Repository[Agent], Protocol):
    """Repository interface for Agent aggregate."""

    async def get_by_owner(
        self, owner_id: str, skip: int = 0, limit: int = 100
    ) -> List[Agent]:
        """Get agents by owner ID."""
        pass

    async def get_by_type(
        self, agent_type: str, skip: int = 0, limit: int = 100
    ) -> List[Agent]:
        """Get agents by type."""
        pass

    async def search_by_name(
        self, name: str, skip: int = 0, limit: int = 100
    ) -> List[Agent]:
        """Search agents by name."""
        pass

    async def get_by_capability(
        self, capability_type: str, skip: int = 0, limit: int = 100
    ) -> List[Agent]:
        """Get agents by capability type."""
        pass


class CapabilityRepository(Repository[Capability], Protocol):
    """Repository interface for Capability entity."""

    async def get_by_agent(self, agent_id: str) -> List[Capability]:
        """Get all capabilities for an agent."""
        pass

    async def get_by_type(
        self, capability_type: str, skip: int = 0, limit: int = 100
    ) -> List[Capability]:
        """Get capabilities by type."""
        pass

    async def get_popular_capabilities(self, limit: int = 10) -> List[Capability]:
        """Get most frequently used capabilities."""
        pass


class KnowledgeSourceRepository(Repository[KnowledgeSource], Protocol):
    """Repository interface for KnowledgeSource entity."""

    async def get_by_agent(self, agent_id: str) -> List[KnowledgeSource]:
        """Get all knowledge sources for an agent."""
        pass

    async def get_by_source_type(
        self, source_type: str, skip: int = 0, limit: int = 100
    ) -> List[KnowledgeSource]:
        """Get knowledge sources by type."""
        pass

    async def get_by_priority(
        self, min_priority: int = 0, max_priority: int = 100
    ) -> List[KnowledgeSource]:
        """Get knowledge sources within a priority range."""
        pass


class AgentExecutionStore(Protocol):
    """Interface for storing agent execution history and metrics."""

    async def record_execution(
        self, agent_id: str, execution_data: Dict[str, Any]
    ) -> str:
        """Record an agent execution instance."""
        pass

    async def get_execution_history(
        self, agent_id: str, since: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """Get execution history for an agent."""
        pass

    async def get_execution_metrics(
        self, agent_id: str, since: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get execution metrics for an agent."""
        pass


class AgentEventStore(Protocol):
    """Interface for storing agent domain events."""

    async def append_events(self, agent_id: str, events: List[dict]) -> None:
        """Append events to the agent event stream."""
        pass

    async def get_events(
        self, agent_id: str, since: Optional[datetime] = None
    ) -> List[dict]:
        """Get events for an agent since a specific time."""
        pass
