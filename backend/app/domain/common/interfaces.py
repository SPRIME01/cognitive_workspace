"""
Common domain interfaces.
"""

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import (
    Any,
    AsyncIterator,
    Generic,
    List,
    Optional,
    Protocol,
    Type,
    TypeVar,
    Union,
)

T = TypeVar("T")
ID = TypeVar("ID")


class SortDirection(Enum):
    """Sort direction options."""

    ASCENDING = "asc"
    DESCENDING = "desc"


@dataclass
class SortOption:
    """Sorting option for queries."""

    field: str
    direction: SortDirection = SortDirection.ASCENDING


class FilterOperator(Enum):
    """Filter operators for query criteria."""

    EQ = "eq"  # Equal
    NE = "ne"  # Not equal
    GT = "gt"  # Greater than
    GTE = "gte"  # Greater than or equal
    LT = "lt"  # Less than
    LTE = "lte"  # Less than or equal
    IN = "in"  # In a list of values
    NOT_IN = "not_in"  # Not in a list of values
    CONTAINS = "contains"  # String contains
    STARTS_WITH = "starts_with"  # String starts with
    ENDS_WITH = "ends_with"  # String ends with
    BETWEEN = "between"  # Between two values
    EXISTS = "exists"  # Field exists
    REGEX = "regex"  # Matches regex pattern


@dataclass
class FilterCriteria:
    """Filter criteria for queries."""

    field: str
    operator: FilterOperator
    value: Any


class LogicalOperator(Enum):
    """Logical operators for combining filters."""

    AND = "and"
    OR = "or"


@dataclass
class FilterGroup:
    """Group of filter criteria combined with a logical operator."""

    filters: List[Union[FilterCriteria, "FilterGroup"]]
    operator: LogicalOperator = LogicalOperator.AND


@dataclass
class QueryOptions:
    """Options for repository queries."""

    filters: Optional[FilterGroup] = None
    sort: Optional[List[SortOption]] = None
    skip: int = 0
    limit: int = 100
    include_count: bool = False


@dataclass
class QueryResult(Generic[T]):
    """Result of a query that includes items and optional count."""

    items: List[T]
    total_count: Optional[int] = None


class SpecificationVisitor(ABC):
    """Visitor for converting specifications to database-specific queries."""

    @abstractmethod
    def visit_and(self, spec: "AndSpecification") -> Any:
        """Visit an AND specification."""
        pass

    @abstractmethod
    def visit_or(self, spec: "OrSpecification") -> Any:
        """Visit an OR specification."""
        pass

    @abstractmethod
    def visit_not(self, spec: "NotSpecification") -> Any:
        """Visit a NOT specification."""
        pass

    @abstractmethod
    def visit_field(self, spec: "FieldSpecification") -> Any:
        """Visit a field specification."""
        pass


class Specification(Generic[T], ABC):
    """Base specification interface for domain object queries."""

    @abstractmethod
    def is_satisfied_by(self, item: T) -> bool:
        """Check if the item satisfies this specification."""
        pass

    @abstractmethod
    def accept(self, visitor: SpecificationVisitor) -> Any:
        """Accept a visitor to convert the specification to a query."""
        pass

    def and_(self, other: "Specification[T]") -> "Specification[T]":
        """Combine with another specification using logical AND."""
        return AndSpecification(self, other)

    def or_(self, other: "Specification[T]") -> "Specification[T]":
        """Combine with another specification using logical OR."""
        return OrSpecification(self, other)

    def not_(self) -> "Specification[T]":
        """Negate this specification using logical NOT."""
        return NotSpecification(self)


class AndSpecification(Specification[T]):
    """AND specification that combines two specifications."""

    def __init__(self, left: Specification[T], right: Specification[T]):
        """Initialize a new AND specification."""
        self.left = left
        self.right = right

    def is_satisfied_by(self, item: T) -> bool:
        """Check if the item satisfies both specifications."""
        return self.left.is_satisfied_by(item) and self.right.is_satisfied_by(item)

    def accept(self, visitor: SpecificationVisitor) -> Any:
        """Accept a visitor to convert the specification to a query."""
        return visitor.visit_and(self)


class OrSpecification(Specification[T]):
    """OR specification that satisfies if either specification is satisfied."""

    def __init__(self, left: Specification[T], right: Specification[T]):
        """Initialize a new OR specification."""
        self.left = left
        self.right = right

    def is_satisfied_by(self, item: T) -> bool:
        """Check if the item satisfies either specification."""
        return self.left.is_satisfied_by(item) or self.right.is_satisfied_by(item)

    def accept(self, visitor: SpecificationVisitor) -> Any:
        """Accept a visitor to convert the specification to a query."""
        return visitor.visit_or(self)


class NotSpecification(Specification[T]):
    """NOT specification that negates another specification."""

    def __init__(self, spec: Specification[T]):
        """Initialize a new NOT specification."""
        self.spec = spec

    def is_satisfied_by(self, item: T) -> bool:
        """Check if the item does not satisfy the specification."""
        return not self.spec.is_satisfied_by(item)

    def accept(self, visitor: SpecificationVisitor) -> Any:
        """Accept a visitor to convert the specification to a query."""
        return visitor.visit_not(self)


class FieldSpecification(Specification[T]):
    """Specification for a field comparison."""

    def __init__(self, field: str, operator: FilterOperator, value: Any):
        """Initialize a new field specification."""
        self.field = field
        self.operator = operator
        self.value = value

    def is_satisfied_by(self, item: T) -> bool:
        """Check if the item's field satisfies the condition."""
        field_value = getattr(item, self.field, None)

        # Handle special cases
        if self.operator == FilterOperator.EXISTS:
            return field_value is not None

        if field_value is None:
            return False

        # Define operator functions
        operators = {
            FilterOperator.EQ: lambda: field_value == self.value,
            FilterOperator.NE: lambda: field_value != self.value,
            FilterOperator.GT: lambda: field_value > self.value,
            FilterOperator.GTE: lambda: field_value >= self.value,
            FilterOperator.LT: lambda: field_value < self.value,
            FilterOperator.LTE: lambda: field_value <= self.value,
            FilterOperator.IN: lambda: field_value in self.value,
            FilterOperator.NOT_IN: lambda: field_value not in self.value,
            FilterOperator.CONTAINS: lambda: self.value in field_value,
            FilterOperator.STARTS_WITH: lambda: field_value.startswith(self.value),
            FilterOperator.ENDS_WITH: lambda: field_value.endswith(self.value),
            FilterOperator.BETWEEN: lambda: self.value[0] <= field_value <= self.value[1],
            FilterOperator.REGEX: lambda: bool(re.compile(self.value).match(str(field_value))),
        }

        return operators.get(self.operator, lambda: False)()

    def accept(self, visitor: SpecificationVisitor) -> Any:
        """Accept a visitor to convert the specification to a query."""
        return visitor.visit_field(self)


class Repository(Generic[T, ID], Protocol):
    """Base repository interface with enhanced querying capabilities."""

    async def get_by_id(self, id: ID) -> Optional[T]:
        """Get an entity by its ID."""
        ...

    async def exists(self, id: ID) -> bool:
        """Check if an entity with the given ID exists."""
        ...

    async def find_one(self, spec: Specification[T]) -> Optional[T]:
        """Find a single entity matching the specification."""
        ...

    async def find_all(
        self,
        spec: Optional[Specification[T]] = None,
        sort: Optional[List[SortOption]] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[T]:
        """Find all entities matching the specification."""
        ...

    async def find_with_query(self, options: QueryOptions) -> QueryResult[T]:
        """Find entities using query options."""
        ...

    async def count(self, spec: Optional[Specification[T]] = None) -> int:
        """Count entities matching the specification."""
        ...

    async def add(self, entity: T) -> T:
        """Add a new entity."""
        ...

    async def add_many(self, entities: List[T]) -> List[T]:
        """Add multiple entities."""
        ...

    async def update(self, entity: T) -> T:
        """Update an existing entity."""
        ...

    async def update_many(self, entities: List[T]) -> List[T]:
        """Update multiple entities."""
        ...

    async def delete(self, id: ID) -> bool:
        """Delete an entity by its ID."""
        ...

    async def delete_many(self, ids: List[ID]) -> int:
        """Delete multiple entities by their IDs and return the count of deleted items."""
        ...

    async def delete_by_spec(self, spec: Specification[T]) -> int:
        """Delete entities matching the specification and return the count of deleted items."""
        ...

    async def stream(
        self, spec: Optional[Specification[T]] = None, batch_size: int = 100
    ) -> AsyncIterator[T]:
        """Stream entities matching the specification in batches."""
        ...


class UnitOfWork(Protocol):
    """Interface for unit of work pattern to manage transactions."""

    async def begin(self) -> None:
        """Begin a transaction."""
        ...

    async def commit(self) -> None:
        """Commit the transaction."""
        ...

    async def rollback(self) -> None:
        """Rollback the transaction."""
        ...

    async def __aenter__(self) -> "UnitOfWork":
        """Enter the context manager."""
        ...

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context manager."""
        ...


class RepositoryFactory(Protocol):
    """Factory interface for creating repositories."""

    def create_repository(self, entity_type: Type[T]) -> Repository[T, Any]:
        """Create a repository for the given entity type."""
        ...
