"""
Project Management domain value objects.

This module defines immutable value objects that represent important domain concepts
and ensure data validation and integrity.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import FrozenSet
from uuid import UUID

from app.domain.common.value_objects import NonEmptyString


@dataclass(frozen=True)
class ProjectId:
    """Value object representing a project's unique identifier."""

    value: UUID

    def __post_init__(self):
        """Validate the project ID."""
        if not isinstance(self.value, UUID):
            raise ValueError("Project ID must be a UUID")


@dataclass(frozen=True)
class ProjectName(NonEmptyString):
    """Value object representing a project's name."""

    def __post_init__(self):
        """Validate the project name."""
        super().__post_init__()
        if len(self.value) > 100:
            raise ValueError("Project name cannot exceed 100 characters")


@dataclass(frozen=True)
class ProjectDescription(NonEmptyString):
    """Value object representing a project's description."""

    def __post_init__(self):
        """Validate the project description."""
        super().__post_init__()
        if len(self.value) > 1000:
            raise ValueError("Project description cannot exceed 1000 characters")


@dataclass(frozen=True)
class ProjectMetadata:
    """Value object representing project metadata."""

    created_at: datetime
    updated_at: datetime
    tags: FrozenSet[str] = field(default_factory=frozenset)
    category: str = "uncategorized"
    visibility: str = "private"

    def __post_init__(self):
        """Validate the metadata."""
        # Validate timestamps
        if self.updated_at < self.created_at:
            raise ValueError("Updated timestamp cannot be before created timestamp")

        # Validate tags
        if not all(isinstance(tag, str) for tag in self.tags):
            raise ValueError("All tags must be strings")
        if not all(tag.strip() for tag in self.tags):
            raise ValueError("Tags cannot be empty or whitespace")
        if any(len(tag) > 50 for tag in self.tags):
            raise ValueError("Tags cannot exceed 50 characters")

        # Validate category
        if not self.category.strip():
            raise ValueError("Category cannot be empty or whitespace")
        if len(self.category) > 50:
            raise ValueError("Category cannot exceed 50 characters")

        # Validate visibility
        allowed_visibilities = {"private", "team", "public"}
        if self.visibility not in allowed_visibilities:
            raise ValueError(
                f"Visibility must be one of: {', '.join(allowed_visibilities)}"
            )

    def update_tags(self, new_tags: FrozenSet[str]) -> "ProjectMetadata":
        """Create a new instance with updated tags.

        Args:
            new_tags: The new set of tags

        Returns:
            A new ProjectMetadata instance with updated tags
        """
        return ProjectMetadata(
            created_at=self.created_at,
            updated_at=datetime.utcnow(),
            tags=new_tags,
            category=self.category,
            visibility=self.visibility,
        )

    def update_category(self, new_category: str) -> "ProjectMetadata":
        """Create a new instance with updated category.

        Args:
            new_category: The new category

        Returns:
            A new ProjectMetadata instance with updated category
        """
        return ProjectMetadata(
            created_at=self.created_at,
            updated_at=datetime.utcnow(),
            tags=self.tags,
            category=new_category,
            visibility=self.visibility,
        )

    def update_visibility(self, new_visibility: str) -> "ProjectMetadata":
        """Create a new instance with updated visibility.

        Args:
            new_visibility: The new visibility setting

        Returns:
            A new ProjectMetadata instance with updated visibility
        """
        return ProjectMetadata(
            created_at=self.created_at,
            updated_at=datetime.utcnow(),
            tags=self.tags,
            category=self.category,
            visibility=new_visibility,
        )

    def update_timestamp(self) -> "ProjectMetadata":
        """Create a new instance with updated timestamp.

        Returns:
            A new ProjectMetadata instance with updated timestamp
        """
        return ProjectMetadata(
            created_at=self.created_at,
            updated_at=datetime.utcnow(),
            tags=self.tags,
            category=self.category,
            visibility=self.visibility,
        )
