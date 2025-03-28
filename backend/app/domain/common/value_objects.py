"""
Common value objects used across domains.

This module provides base value objects that are used by multiple domains
to ensure consistent validation and behavior.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional
from uuid import UUID


@dataclass(frozen=True)
class NonEmptyString:
    """Base value object for strings that cannot be empty."""

    value: str

    def __post_init__(self):
        """Validate string is not empty or only whitespace."""
        if not self.value:
            raise ValueError("String value cannot be empty")
        if not self.value.strip():
            raise ValueError("String value cannot be only whitespace")

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, NonEmptyString):
            return NotImplemented
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)


@dataclass(frozen=True)
class Email(NonEmptyString):
    """Value object representing an email address."""

    def __post_init__(self):
        """Validate email format."""
        super().__post_init__()
        if "@" not in self.value:
            raise ValueError("Invalid email format")
        local_part, domain = self.value.split("@", 1)
        if not local_part or not domain:
            raise ValueError("Invalid email format")
        if "." not in domain:
            raise ValueError("Invalid email domain")
        if len(self.value) > 254:
            raise ValueError("Email address too long")


@dataclass(frozen=True)
class PhoneNumber(NonEmptyString):
    """Value object representing a phone number."""

    def __post_init__(self):
        """Validate phone number format."""
        super().__post_init__()
        # Remove any non-digit characters for validation
        digits = "".join(filter(str.isdigit, self.value))
        if len(digits) < 10:
            raise ValueError("Phone number must have at least 10 digits")
        if len(digits) > 15:
            raise ValueError("Phone number has too many digits")


@dataclass(frozen=True)
class Url(NonEmptyString):
    """Value object representing a URL."""

    def __post_init__(self):
        """Validate URL format."""
        super().__post_init__()
        if not (self.value.startswith("http://") or self.value.startswith("https://")):
            raise ValueError("URL must start with http:// or https://")
        if len(self.value) > 2048:
            raise ValueError("URL is too long")


@dataclass(frozen=True)
class Username(NonEmptyString):
    """Value object representing a username."""

    def __post_init__(self):
        """Validate username format."""
        super().__post_init__()
        if len(self.value) < 3:
            raise ValueError("Username must be at least 3 characters long")
        if len(self.value) > 50:
            raise ValueError("Username must not exceed 50 characters")
        if not self.value.isalnum() and not any(c in "_-" for c in self.value):
            raise ValueError(
                "Username can only contain alphanumeric characters, underscores, and hyphens"
            )


@dataclass(frozen=True)
class Password(NonEmptyString):
    """Value object representing a password."""

    def __post_init__(self):
        """Validate password strength."""
        super().__post_init__()
        if len(self.value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if len(self.value) > 128:
            raise ValueError("Password must not exceed 128 characters")
        if not any(c.isupper() for c in self.value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in self.value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in self.value):
            raise ValueError("Password must contain at least one number")
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if not any(c in special_chars for c in self.value):
            raise ValueError("Password must contain at least one special character")


@dataclass(frozen=True)
class Slug(NonEmptyString):
    """Value object representing a URL-friendly slug."""

    def __post_init__(self):
        """Validate slug format."""
        super().__post_init__()
        if not all(c.isalnum() or c == "-" for c in self.value):
            raise ValueError(
                "Slug can only contain alphanumeric characters and hyphens"
            )
        if self.value.startswith("-") or self.value.endswith("-"):
            raise ValueError("Slug cannot start or end with a hyphen")
        if "--" in self.value:
            raise ValueError("Slug cannot contain consecutive hyphens")
        if len(self.value) > 100:
            raise ValueError("Slug must not exceed 100 characters")


@dataclass(frozen=True)
class DateTimeRange:
    """Represents a time range with start and end times."""

    start: datetime
    end: Optional[datetime] = None

    def __post_init__(self):
        """Validate that start date is before end date if end date is provided."""
        if self.end is not None and self.start > self.end:
            raise ValueError("Start date must be before end date")

    @property
    def duration(self) -> Optional[float]:
        """Calculate the duration in seconds, if end date is provided."""
        if self.end is None:
            return None
        return (self.end - self.start).total_seconds()

    def contains(self, dt: datetime) -> bool:
        """Check if the given datetime is within this range."""
        if self.end is None:
            return dt >= self.start
        return self.start <= dt <= self.end

    def overlaps(self, other: "DateTimeRange") -> bool:
        """Check if this range overlaps with another range."""
        if self.end is None:
            return other.start >= self.start
        if other.end is None:
            return self.start <= other.start
        return self.start <= other.end and other.start <= self.end


@dataclass(frozen=True)
class ResourceId:
    """Represents a unique identifier for a resource."""

    value: UUID

    def __str__(self) -> str:
        """Return string representation of the resource ID."""
        return str(self.value)
