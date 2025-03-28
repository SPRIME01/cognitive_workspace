"""
Agent System domain services.

This module contains domain services that encapsulate complex business logic
for agent management and execution operations.
"""

from datetime import datetime
from typing import List, Optional, Protocol, Dict, Any

from app.domain.agent_system.entities import (
    Agent,
    Capability,
    KnowledgeSource,
    AgentType,
    ExecutionMode,
)
from app.domain.agent_system.interfaces import (
    AgentRepository,
    CapabilityRepository,
    KnowledgeSourceRepository,
    AgentExecutionStore,
    AgentEventStore,
)
from app.domain.agent_system.events import (
    AgentCreated,
    CapabilityAdded,
    KnowledgeSourceAdded,
    AgentExecutionStarted,
)
from app.domain.common.event_publisher import EventPublisher


class AgentDomainService(Protocol):
    """Domain service for agent-related operations."""

    async def create_agent(
        self,
        name: str,
        agent_type: str,
        owner_id: str,
        description: Optional[str] = None,
        initial_capabilities: Optional[List[Capability]] = None,
        initial_knowledge_sources: Optional[List[KnowledgeSource]] = None,
    ) -> Agent:
        """Create a new agent."""
        pass

    async def add_capability(
        self, agent_id: str, capability: Capability, added_by: str
    ) -> Agent:
        """Add a capability to an agent."""
        pass

    async def add_knowledge_source(
        self, agent_id: str, knowledge_source: KnowledgeSource, added_by: str
    ) -> Agent:
        """Add a knowledge source to an agent."""
        pass

    async def start_execution(
        self, agent_id: str, initiated_by: str, parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Start agent execution."""
        pass

    async def validate_agent_access(
        self, agent_id: str, user_id: str, required_permission: Optional[str] = None
    ) -> bool:
        """Validate user's access to an agent."""
        pass


class DefaultAgentDomainService:
    """Default implementation of AgentDomainService."""

    def __init__(
        self,
        agent_repository: AgentRepository,
        capability_repository: CapabilityRepository,
        knowledge_source_repository: KnowledgeSourceRepository,
        execution_store: AgentExecutionStore,
        event_store: AgentEventStore,
        event_publisher: EventPublisher,
    ):
        """Initialize the service.

        Args:
            agent_repository: Repository for agent operations
            capability_repository: Repository for capability operations
            knowledge_source_repository: Repository for knowledge source operations
            execution_store: Store for agent execution history and metrics
            event_store: Store for agent domain events
            event_publisher: Service for publishing domain events
        """
        self._agent_repository = agent_repository
        self._capability_repository = capability_repository
        self._knowledge_source_repository = knowledge_source_repository
        self._execution_store = execution_store
        self._event_store = event_store
        self._event_publisher = event_publisher

    async def create_agent(
        self,
        name: str,
        agent_type: str,
        owner_id: str,
        description: Optional[str] = None,
        initial_capabilities: Optional[List[Capability]] = None,
        initial_knowledge_sources: Optional[List[KnowledgeSource]] = None,
    ) -> Agent:
        """Create a new agent.

        Args:
            name: Agent name
            agent_type: Type of agent
            owner_id: ID of the agent owner
            description: Optional agent description
            initial_capabilities: Optional list of initial capabilities
            initial_knowledge_sources: Optional list of initial knowledge sources

        Returns:
            The created agent

        Raises:
            ValueError: If the agent data is invalid
        """
        if not name or len(name.strip()) == 0:
            raise ValueError("Agent name cannot be empty")

        # Validate agent type
        if agent_type not in vars(AgentType).values():
            raise ValueError(f"Invalid agent type: {agent_type}")

        agent = Agent(
            id=f"agent_{datetime.utcnow().timestamp()}",  # Simple ID generation
            name=name,
            description=description,
            agent_type=agent_type,
            owner_id=owner_id,
            execution_mode=ExecutionMode.SYNCHRONOUS,  # Default mode
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        # Save the agent
        agent = await self._agent_repository.add(agent)

        # Publish agent created event
        await self._event_publisher.publish_event(
            AgentCreated(
                event_id=f"evt_{datetime.utcnow().timestamp()}",
                event_type="agent.created",
                aggregate_id=agent.id,
                aggregate_type="agent",
                name=name,
                agent_type=agent_type,
                owner_id=owner_id,
                description=description,
            )
        )

        # Add initial capabilities if provided
        if initial_capabilities:
            for capability in initial_capabilities:
                agent.add_capability(capability)
                await self._capability_repository.add(capability)

                # Publish capability added event
                await self._event_publisher.publish_event(
                    CapabilityAdded(
                        event_id=f"evt_{datetime.utcnow().timestamp()}_cap_{capability.name}",
                        event_type="agent.capability_added",
                        aggregate_id=agent.id,
                        aggregate_type="agent",
                        agent_id=agent.id,
                        capability=capability,
                        added_by=owner_id,
                    )
                )

        # Add initial knowledge sources if provided
        if initial_knowledge_sources:
            for source in initial_knowledge_sources:
                agent.add_knowledge_source(source)
                await self._knowledge_source_repository.add(source)

                # Publish knowledge source added event
                await self._event_publisher.publish_event(
                    KnowledgeSourceAdded(
                        event_id=f"evt_{datetime.utcnow().timestamp()}_src_{source.source_id}",
                        event_type="agent.knowledge_source_added",
                        aggregate_id=agent.id,
                        aggregate_type="agent",
                        agent_id=agent.id,
                        knowledge_source=source,
                        added_by=owner_id,
                    )
                )

        # Update the agent with initial capabilities and knowledge sources
        if initial_capabilities or initial_knowledge_sources:
            await self._agent_repository.update(agent)

        return agent

    async def add_capability(
        self, agent_id: str, capability: Capability, added_by: str
    ) -> Agent:
        """Add a capability to an agent.

        Args:
            agent_id: ID of the agent
            capability: Capability to add
            added_by: ID of the user adding the capability

        Returns:
            The updated agent

        Raises:
            ValueError: If the agent doesn't exist or validation fails
        """
        agent = await self._agent_repository.get_by_id(agent_id)
        if not agent:
            raise ValueError(f"Agent {agent_id} not found")

        # Add the capability
        agent.add_capability(capability)
        await self._capability_repository.add(capability)

        # Save the updated agent
        agent = await self._agent_repository.update(agent)

        # Publish capability added event
        await self._event_publisher.publish_event(
            CapabilityAdded(
                event_id=f"evt_{datetime.utcnow().timestamp()}",
                event_type="agent.capability_added",
                aggregate_id=agent.id,
                aggregate_type="agent",
                agent_id=agent.id,
                capability=capability,
                added_by=added_by,
            )
        )

        return agent

    async def add_knowledge_source(
        self, agent_id: str, knowledge_source: KnowledgeSource, added_by: str
    ) -> Agent:
        """Add a knowledge source to an agent.

        Args:
            agent_id: ID of the agent
            knowledge_source: Knowledge source to add
            added_by: ID of the user adding the knowledge source

        Returns:
            The updated agent

        Raises:
            ValueError: If the agent doesn't exist or validation fails
        """
        agent = await self._agent_repository.get_by_id(agent_id)
        if not agent:
            raise ValueError(f"Agent {agent_id} not found")

        # Add the knowledge source
        agent.add_knowledge_source(knowledge_source)
        await self._knowledge_source_repository.add(knowledge_source)

        # Save the updated agent
        agent = await self._agent_repository.update(agent)

        # Publish knowledge source added event
        await self._event_publisher.publish_event(
            KnowledgeSourceAdded(
                event_id=f"evt_{datetime.utcnow().timestamp()}",
                event_type="agent.knowledge_source_added",
                aggregate_id=agent.id,
                aggregate_type="agent",
                agent_id=agent.id,
                knowledge_source=knowledge_source,
                added_by=added_by,
            )
        )

        return agent

    async def start_execution(
        self, agent_id: str, initiated_by: str, parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Start agent execution.

        Args:
            agent_id: ID of the agent to execute
            initiated_by: ID of the user initiating the execution
            parameters: Execution parameters

        Returns:
            Execution details including execution ID

        Raises:
            ValueError: If the agent doesn't exist or validation fails
        """
        agent = await self._agent_repository.get_by_id(agent_id)
        if not agent:
            raise ValueError(f"Agent {agent_id} not found")

        # Record the execution start
        execution_id = await self._execution_store.record_execution(
            {
                "agent_id": agent_id,
                "initiated_by": initiated_by,
                "parameters": parameters,
                "status": "started",
                "start_time": datetime.utcnow().isoformat(),
            }
        )

        # Publish execution started event
        await self._event_publisher.publish_event(
            AgentExecutionStarted(
                event_id=f"evt_{datetime.utcnow().timestamp()}",
                event_type="agent.execution_started",
                aggregate_id=agent.id,
                aggregate_type="agent",
                agent_id=agent.id,
                execution_id=execution_id,
                initiated_by=initiated_by,
                parameters=parameters,
            )
        )

        # TODO: Implement actual agent execution logic here
        # This would typically involve:
        # 1. Loading the agent's capabilities
        # 2. Preparing the knowledge sources
        # 3. Setting up the execution environment
        # 4. Running the agent's logic
        # 5. Handling results and errors

        return {
            "execution_id": execution_id,
            "agent_id": agent_id,
            "status": "started",
            "start_time": datetime.utcnow().isoformat(),
        }

    async def validate_agent_access(
        self, agent_id: str, user_id: str, required_permission: Optional[str] = None
    ) -> bool:
        """Validate user's access to an agent.

        Args:
            agent_id: ID of the agent to check
            user_id: ID of the user requesting access
            required_permission: Optional specific permission requirement

        Returns:
            True if the user has access, False otherwise
        """
        agent = await self._agent_repository.get_by_id(agent_id)
        if not agent:
            return False

        # Owner has full access
        if agent.owner_id == user_id:
            return True

        # TODO: Implement more sophisticated access control when needed
        # This could include:
        # - Team-based access
        # - Role-based permissions
        # - Shared agent access rules

        return False
