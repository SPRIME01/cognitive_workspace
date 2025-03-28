"""
SQLAlchemy models for the User Management domain.

This module defines the SQLAlchemy ORM models used for persisting
User Management domain entities to a relational database.
"""

from datetime import datetime
import uuid
from typing import List, Optional
from sqlalchemy import Column, String, Boolean, DateTime, Table, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import UUID

from app.infrastructure.persistence.database import Base
from app.domain.user_management.entities import UserRole as DomainUserRole


# Association table for user roles
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column("role", Enum(DomainUserRole), primary_key=True),
)


class User(Base):
    """SQLAlchemy ORM model for users."""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, nullable=True)
    last_login = Column(DateTime, nullable=True)

    # Relationships
    roles = relationship("DomainUserRole", secondary=user_roles, collection_class=set)
    profile = relationship("UserProfile", back_populates="user", uselist=False)


class UserProfile(Base):
    """SQLAlchemy ORM model for user profiles."""

    __tablename__ = "user_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False
    )
    bio = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    preferences = Column(JSON, default=dict, nullable=False)

    # Relationships
    user = relationship("User", back_populates="profile")
