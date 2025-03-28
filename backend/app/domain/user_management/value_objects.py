"""
User Management domain value objects.

This module defines the value objects specific to the User Management domain.
"""

import re
from dataclasses import dataclass
from typing import ClassVar, Pattern
import bcrypt

from app.domain.common.base import ValueObject, DomainException


class InvalidUsernameError(DomainException):
    """Exception raised when a username is invalid."""

    pass


class InvalidPasswordError(DomainException):
    """Exception raised when a password is invalid."""

    pass


class Username(ValueObject):
    """Username value object with validation."""

    # Username validation pattern (alphanumeric with underscore and dot, 3-30 chars)
    _pattern: ClassVar[Pattern] = re.compile(r"^[a-zA-Z0-9_.]{3,30}$")

    def __init__(self, value: str):
        """Create a new Username, validating the format.

        Args:
            value: The username string.

        Raises:
            InvalidUsernameError: If the username format is invalid.
        """
        if not value or not self._pattern.match(value):
            raise InvalidUsernameError(
                f"Invalid username: {value}. Username must be 3-30 characters "
                "and can only contain letters, numbers, underscores, and dots."
            )
        self.value = value

    def __str__(self) -> str:
        """Return string representation of the username."""
        return self.value


class Password(ValueObject):
    """Password value object with hashing and verification."""

    # Password requirements
    _min_length: ClassVar[int] = 8
    _max_length: ClassVar[int] = 100
    _require_uppercase: ClassVar[bool] = True
    _require_lowercase: ClassVar[bool] = True
    _require_digit: ClassVar[bool] = True
    _require_special: ClassVar[bool] = True
    _special_chars: ClassVar[str] = "!@#$%^&*()-_=+[]{}|;:,.<>?/~"

    def __init__(self, hashed_password: str):
        """Initialize with an already hashed password.

        Args:
            hashed_password: The hashed password string.
        """
        self.hashed_password = hashed_password

    @classmethod
    def create(cls, plain_password: str) -> "Password":
        """Create a new Password from a plain text password.

        Args:
            plain_password: The plain text password to hash.

        Returns:
            A new Password instance with the hashed password.

        Raises:
            InvalidPasswordError: If the password does not meet requirements.
        """
        cls._validate_password(plain_password)

        # Hash the password with bcrypt
        hashed = bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt())
        return cls(hashed.decode())

    @classmethod
    def _validate_password(cls, password: str) -> None:
        """Validate that a password meets all requirements.

        Args:
            password: The password to validate.

        Raises:
            InvalidPasswordError: If the password does not meet requirements.
        """
        # Check length
        if not cls._min_length <= len(password) <= cls._max_length:
            raise InvalidPasswordError(
                f"Password must be between {cls._min_length} and {cls._max_length} characters."
            )

        # Check for uppercase letter
        if cls._require_uppercase and not any(c.isupper() for c in password):
            raise InvalidPasswordError(
                "Password must contain at least one uppercase letter."
            )

        # Check for lowercase letter
        if cls._require_lowercase and not any(c.islower() for c in password):
            raise InvalidPasswordError(
                "Password must contain at least one lowercase letter."
            )

        # Check for digit
        if cls._require_digit and not any(c.isdigit() for c in password):
            raise InvalidPasswordError("Password must contain at least one digit.")

        # Check for special character
        if cls._require_special and not any(c in cls._special_chars for c in password):
            raise InvalidPasswordError(
                f"Password must contain at least one special character ({cls._special_chars})."
            )

    def verify(self, plain_password: str) -> bool:
        """Verify if the given plain text password matches this password.

        Args:
            plain_password: The plain text password to check.

        Returns:
            True if the password matches, False otherwise.
        """
        return bcrypt.checkpw(plain_password.encode(), self.hashed_password.encode())

    def __str__(self) -> str:
        """Return a string representation that doesn't expose the hash."""
        return "********"
