"""
Workspace schemas for API requests and responses.
"""

from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class WorkspaceBase(BaseModel):
    """Base Workspace schema."""

    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    is_public: bool = False


class WorkspaceCreate(WorkspaceBase):
    """Schema for Workspace creation."""

    pass


class WorkspaceUpdate(BaseModel):
    """Schema for Workspace updates."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    is_public: Optional[bool] = None


class WorkspaceResponse(WorkspaceBase):
    """Schema for Workspace responses."""

    id: str
    owner_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
