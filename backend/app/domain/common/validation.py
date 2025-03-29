"""
Domain validation framework.

This module provides a robust validation mechanism for domain objects,
ensuring that business rules are consistently enforced.
"""

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    Set,
    Type,
    TypeVar,
    Union,
)

from pydantic import ValidationError
from pydantic.error_wrappers import ErrorWrapper

T = TypeVar("T")


class ValidationSeverity(Enum):
    """Severity levels for validation errors."""

    INFO = "info"  # Informational only, not an error
    WARNING = "warning"  # Warning, but can proceed
    ERROR = "error"  # Error that prevents proceeding


@dataclass
class ValidationResult:
    """Result of a validation operation."""

    is_valid: bool
    errors: List[Dict[str, Any]] = field(default_factory=list)
    warnings: List[Dict[str, Any]] = field(default_factory=list)
    infos: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        """Check if there are any errors."""
        return len(self.errors) > 0

    @property
    def has_warnings(self) -> bool:
        """Check if there are any warnings."""
        return len(self.warnings) > 0

    @property
    def has_infos(self) -> bool:
        """Check if there are any information messages."""
        return len(self.infos) > 0

    def add_message(
        self, field: str, message: str, severity: ValidationSeverity
    ) -> None:
        """Add a validation message with the specified severity."""
        entry = {"field": field, "message": message}
        if severity == ValidationSeverity.ERROR:
            self.errors.append(entry)
            self.is_valid = False
        elif severity == ValidationSeverity.WARNING:
            self.warnings.append(entry)
        elif severity == ValidationSeverity.INFO:
            self.infos.append(entry)

    def add_error(self, field: str, message: str) -> None:
        """Add an error message."""
        self.add_message(field, message, ValidationSeverity.ERROR)

    def add_warning(self, field: str, message: str) -> None:
        """Add a warning message."""
        self.add_message(field, message, ValidationSeverity.WARNING)

    def add_info(self, field: str, message: str) -> None:
        """Add an informational message."""
        self.add_message(field, message, ValidationSeverity.INFO)

    def merge(self, other: "ValidationResult") -> None:
        """Merge another validation result into this one."""
        self.is_valid = self.is_valid and other.is_valid
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)
        self.infos.extend(other.infos)

    @staticmethod
    def valid() -> "ValidationResult":
        """Create a valid result with no messages."""
        return ValidationResult(is_valid=True)

    @staticmethod
    def invalid(field: str, message: str) -> "ValidationResult":
        """Create an invalid result with an error message."""
        result = ValidationResult(is_valid=False)
        result.add_error(field, message)
        return result


class ValidationRule(Generic[T], ABC):
    """Base class for validation rules."""

    @abstractmethod
    def validate(self, value: T) -> ValidationResult:
        """Validate a value against this rule."""
        pass


class PropertyValidationRule(ValidationRule[T]):
    """Validation rule for a specific property."""

    def __init__(
        self,
        property_name: str,
        error_message: str,
        validation_func: Callable[[Optional[T]], bool],
        severity: ValidationSeverity = ValidationSeverity.ERROR,
    ):
        """Initialize a new property validation rule."""
        self.property_name = property_name
        self.error_message = error_message
        self.validation_func = validation_func
        self.severity = severity

    def validate(self, value: Any) -> ValidationResult:
        """Validate a value against this rule."""
        result = ValidationResult.valid()

        # Get the property value
        property_value = getattr(value, self.property_name, None)

        # Validate the property
        if not self.validation_func(property_value):
            result.add_message(self.property_name, self.error_message, self.severity)

        return result


class CrossPropertyValidationRule(ValidationRule[T]):
    """Validation rule for relationships between multiple properties."""

    def __init__(
        self,
        error_message: str,
        validation_func: Callable[[T], bool],
        affected_properties: List[str],
        severity: ValidationSeverity = ValidationSeverity.ERROR,
    ):
        """Initialize a new cross-property validation rule."""
        self.error_message = error_message
        self.validation_func = validation_func
        self.affected_properties = affected_properties
        self.severity = severity

    def validate(self, value: T) -> ValidationResult:
        """Validate a value against this rule."""
        result = ValidationResult.valid()

        # Validate the object as a whole
        if not self.validation_func(value):
            # Use the first affected property as the field name
            field_name = (
                self.affected_properties[0] if self.affected_properties else "object"
            )
            result.add_message(field_name, self.error_message, self.severity)

        return result


class Validator(Generic[T]):
    """Validator for domain objects."""

    def __init__(self, type_name: str):
        """Initialize a new validator."""
        self.type_name = type_name
        self.rules: List[ValidationRule[T]] = []

    def add_rule(self, rule: ValidationRule[T]) -> "Validator[T]":
        """Add a validation rule."""
        self.rules.append(rule)
        return self

    def add_property_rule(
        self,
        property_name: str,
        error_message: str,
        validation_func: Callable[[Any], bool],
        severity: ValidationSeverity = ValidationSeverity.ERROR,
    ) -> "Validator[T]":
        """Add a rule for a specific property."""
        rule = PropertyValidationRule(
            property_name=property_name,
            error_message=error_message,
            validation_func=validation_func,
            severity=severity,
        )
        return self.add_rule(rule)

    def add_cross_property_rule(
        self,
        error_message: str,
        validation_func: Callable[[T], bool],
        affected_properties: List[str],
        severity: ValidationSeverity = ValidationSeverity.ERROR,
    ) -> "Validator[T]":
        """Add a rule that checks relationships between properties."""
        rule = CrossPropertyValidationRule(
            error_message=error_message,
            validation_func=validation_func,
            affected_properties=affected_properties,
            severity=severity,
        )
        return self.add_rule(rule)

    def validate(self, value: T) -> ValidationResult:
        """Validate an object against all rules."""
        result = ValidationResult.valid()

        for rule in self.rules:
            rule_result = rule.validate(value)
            result.merge(rule_result)

        return result

    def validate_and_raise(self, value: T) -> None:
        """Validate an object and raise an exception if invalid."""
        result = self.validate(value)
        if not result.is_valid:
            error_messages = [f"{e['field']}: {e['message']}" for e in result.errors]
            raise ValueError('\n'.join(error_messages))


class ValidatorRegistry:
    """Registry for validators."""

    _instance = None

    def __init__(self):
        """Initialize the validator registry."""
        self._validators: Dict[Type[Any], Validator[Any]] = {}

    def __new__(cls):
        """Create or return the singleton instance."""
        if cls._instance is None:
            cls._instance = super(ValidatorRegistry, cls).__new__(cls)
            cls._instance.__init__()
        return cls._instance

    def register(self, type_: Type[T], validator: Validator[T]) -> None:
        """Register a validator for a type."""
        self._validators[type_] = validator

    def get(self, type_: Type[T]) -> Optional[Validator[T]]:
        """Get the validator for a type."""
        return self._validators.get(type_)

    def validate(self, obj: Any) -> ValidationResult:
        """Validate an object using its registered validator."""
        validator = self.get(type(obj))
        if validator:
            return validator.validate(obj)
        return ValidationResult.valid()

    def validate_and_raise(self, obj: Any) -> None:
        """Validate an object and raise an exception if invalid."""
        validator = self.get(type(obj))
        if validator:
            result = validator.validate(obj)
            if not result.is_valid:
                errors = [ErrorWrapper(exc=ValueError(e['message']), loc=(e['field'],)) for e in result.errors]
                raise ValidationError(
                    errors,
                    type(obj)
                )


# Common validation functions
def not_empty(value: Any) -> bool:
    """Check if a value is not empty."""
    if value is None:
        return False
    if isinstance(value, str):
        return len(value.strip()) > 0
    if hasattr(value, "__len__"):
        return len(value) > 0
    return True


def matches_pattern(pattern: str) -> Callable[[str], bool]:
    """Create a function that checks if a string matches a regex pattern."""
    compiled_pattern = re.compile(pattern)
    return lambda value: bool(value and compiled_pattern.match(value))


def min_length(min_len: int) -> Callable[[Any], bool]:
    """Create a function that checks if a value has at least a minimum length."""
    return (
        lambda value: value is not None
        and hasattr(value, "__len__")
        and len(value) >= min_len
    )


def max_length(max_len: int) -> Callable[[Any], bool]:
    """Create a function that checks if a value has at most a maximum length."""
    return lambda value: value is None or (
        hasattr(value, "__len__") and len(value) <= max_len
    )


def in_range(
    min_val: Union[int, float], max_val: Union[int, float]
) -> Callable[[Union[int, float]], bool]:
    """Create a function that checks if a numeric value is within a range."""
    return lambda value: value is not None and min_val <= value <= max_val


def is_one_of(valid_values: Set[Any]) -> Callable[[Any], bool]:
    """Create a function that checks if a value is one of a set of valid values."""
    return lambda value: value in valid_values


# Singleton registry
def get_validator_registry() -> ValidatorRegistry:
    """Get the singleton validator registry instance."""
    return ValidatorRegistry()


# Decorator to apply validation
def validates(cls: Type[T]) -> Type[T]:
    """Decorator to validate a class when instantiated."""

    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        """Initialize and validate the instance."""
        original_init(self, *args, **kwargs)
        registry = get_validator_registry()
        registry.validate_and_raise(self)

    cls.__init__ = new_init
    return cls
