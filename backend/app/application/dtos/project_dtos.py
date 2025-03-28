"""
Project Management Data Transfer Objects (DTOs).

This module defines the DTOs used in the application layer for transferring
project management related data between layers.
"""

from datetime import datetime
from typing import Optional, Set
from uuid import UUID

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    """DTO for creating a new project."""

    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="The name of the project",
        example="My Research Project",
    )
    description: str = Field(
        ...,
        max_length=5000,
        description="A detailed description of the project",
        example="This project explores advanced cognitive computing methods.",
    )
    tags: Optional[Set[str]] = Field(
        default=set(),
        description="Tags associated with the project",
        example=["research", "cognitive-computing", "ai"],
    )
    category: str = Field(
        default="general", description="The category of the project", example="research"
    )
    visibility: str = Field(
        default="private",
        description="The visibility setting of the project",
        example="private",
    )


class ProjectUpdate(BaseModel):
    """DTO for updating a project."""

    name: Optional[str] = Field(
        None,
        min_length=3,
        max_length=100,
        description="New name for the project",
        example="Advanced Research Project",
    )
    description: Optional[str] = Field(
        None,
        max_length=5000,
        description="New description for the project",
        example="An exploration of advanced cognitive computing methods.",
    )
    tags: Optional[Set[str]] = Field(
        None,
        description="Updated tags for the project",
        example=["research", "cognitive-computing", "ai", "machine-learning"],
    )
    category: Optional[str] = Field(
        None, description="New category for the project", example="research"
    )
    visibility: Optional[str] = Field(
        None, description="New visibility setting for the project", example="public"
    )


class ProjectCollaboratorCreate(BaseModel):
    """DTO for adding a collaborator to a project."""

    user_id: UUID = Field(
        ...,
        description="The ID of the user to add as a collaborator",
        example="123e4567-e89b-12d3-a456-426614174000",
    )
    role: str = Field(
        ..., description="The role to assign to the collaborator", example="editor"
    )


class ProjectResponse(BaseModel):
    """DTO for project responses."""

    id: UUID = Field(
        ...,
        description="The unique identifier of the project",
        example="123e4567-e89b-12d3-a456-426614174000",
    )
    name: str = Field(
        ..., description="The name of the project", example="My Research Project"
    )
    description: str = Field(
        ...,
        description="The description of the project",
        example="This project explores advanced cognitive computing methods.",
    )
    owner_id: UUID = Field(
        ...,
        description="The ID of the project owner",
        example="123e4567-e89b-12d3-a456-426614174000",
    )
    status: str = Field(
        ..., description="The current status of the project", example="active"
    )
    tags: Set[str] = Field(
        ...,
        description="Tags associated with the project",
        example=["research", "cognitive-computing", "ai"],
    )
    category: str = Field(
        ..., description="The category of the project", example="research"
    )
    visibility: str = Field(
        ..., description="The visibility setting of the project", example="private"
    )
    created_at: datetime = Field(
        ..., description="When the project was created", example="2025-03-27T10:00:00Z"
    )
    updated_at: datetime = Field(
        ...,
        description="When the project was last updated",
        example="2025-03-27T11:30:00Z",
    )


class ProjectCollaboratorResponse(BaseModel):
    """DTO for project collaborator responses."""

    id: UUID = Field(
        ...,
        description="The unique identifier of the collaborator record",
        example="123e4567-e89b-12d3-a456-426614174000",
    )
    user_id: UUID = Field(
        ...,
        description="The ID of the collaborator",
        example="123e4567-e89b-12d3-a456-426614174000",
    )
    project_id: UUID = Field(
        ...,
        description="The ID of the project",
        example="123e4567-e89b-12d3-a456-426614174000",
    )
    role: str = Field(..., description="The role of the collaborator", example="editor")
    joined_at: datetime = Field(
        ...,
        description="When the collaborator joined the project",
        example="2025-03-27T10:00:00Z",
    )
    last_accessed_at: Optional[datetime] = Field(
        None,
        description="When the collaborator last accessed the project",
        example="2025-03-27T11:30:00Z",
    )


class ProjectListResponse(BaseModel):
    """DTO for paginated project list responses."""

    items: list[ProjectResponse] = Field(
        ...,
        description="List of projects",
        example=[
            {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "My Research Project",
                "description": "This project explores advanced cognitive computing methods.",
                "owner_id": "123e4567-e89b-12d3-a456-426614174000",
                "status": "active",
                "tags": ["research", "cognitive-computing", "ai"],
                "category": "research",
                "visibility": "private",
                "created_at": "2025-03-27T10:00:00Z",
                "updated_at": "2025-03-27T11:30:00Z",
            }
        ],
    )
    total: int = Field(
        ..., description="Total number of projects matching the query", example=42
    )
    skip: int = Field(..., description="Number of projects skipped", example=0)
    limit: int = Field(
        ..., description="Maximum number of projects returned", example=10
    )


class ProjectCollaboratorListResponse(BaseModel):
    """DTO for paginated project collaborator list responses."""

    items: list[ProjectCollaboratorResponse] = Field(
        ...,
        description="List of project collaborators",
        example=[
            {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "project_id": "123e4567-e89b-12d3-a456-426614174000",
                "role": "editor",
                "joined_at": "2025-03-27T10:00:00Z",
                "last_accessed_at": "2025-03-27T11:30:00Z",
            }
        ],
    )
    total: int = Field(
        ..., description="Total number of collaborators matching the query", example=5
    )
    skip: int = Field(..., description="Number of collaborators skipped", example=0)
    limit: int = Field(
        ..., description="Maximum number of collaborators returned", example=10
    )
