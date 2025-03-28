"""
Agent System domain entities.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class AgentType:
    """Agent type value object."""

    ASSISTANT = "assistant"
    RESEARCHER = "researcher"
    ANALYST = "analyst"
    WRITER = "writer"
    REVIEWER = "reviewer"
    CUSTOM = "custom"


class ExecutionMode:
    """Agent execution mode value object."""

    SYNCHRONOUS = "synchronous"
    ASYNCHRONOUS = "asynchronous"
    STREAMING = "streaming"


class CapabilityType:
    """Capability type value object."""

    CONVERSATION = "conversation"
    RESEARCH = "research"
    ANALYSIS = "analysis"
    GENERATION = "generation"
    REVIEW = "review"
    CUSTOM = "custom"


class Capability(BaseModel):
    """Capability entity."""

    name: str = Field(..., min_length=1, max_length=100)
    capability_type: str = Field(
        ..., regex=f"^({'|'.join(vars(CapabilityType).values())})$"
    )
    description: Optional[str] = Field(None, max_length=500)
    parameters: Dict[str, Any] = Field(default_factory=dict)
    constraints: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class KnowledgeSource(BaseModel):
    """Knowledge source value object."""

    source_type: str
    source_id: str
    access_config: Dict[str, Any] = Field(default_factory=dict)
    priority: int = Field(default=0, ge=0, le=100)


class Agent(BaseModel):
    """Agent aggregate root entity."""

    id: str
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    agent_type: str = Field(..., regex=f"^({'|'.join(vars(AgentType).values())})$")
    capabilities: List[Capability] = Field(default_factory=list)
    knowledge_sources: List[KnowledgeSource] = Field(default_factory=list)
    execution_mode: str = Field(default=ExecutionMode.SYNCHRONOUS)
    owner_id: str
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def add_capability(self, capability: Capability) -> None:
        """Add a capability to the agent."""
        if capability not in self.capabilities:
            self.capabilities.append(capability)
            self.updated_at = datetime.utcnow()

    def remove_capability(self, capability: Capability) -> None:
        """Remove a capability from the agent."""
        if capability in self.capabilities:
            self.capabilities.remove(capability)
            self.updated_at = datetime.utcnow()

    def add_knowledge_source(self, source: KnowledgeSource) -> None:
        """Add a knowledge source to the agent."""
        if source not in self.knowledge_sources:
            self.knowledge_sources.append(source)
            # Sort knowledge sources by priority in descending order
            self.knowledge_sources.sort(key=lambda x: x.priority, reverse=True)
            self.updated_at = datetime.utcnow()

    def set_execution_mode(self, mode: str) -> None:
        """Set the agent's execution mode."""
        if mode in vars(ExecutionMode).values():
            self.execution_mode = mode
            self.updated_at = datetime.utcnow()

    class Config:
        """Pydantic configuration."""

        orm_mode = True
