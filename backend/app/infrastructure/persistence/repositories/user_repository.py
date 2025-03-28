"""
User Management repository adapters.

This module implements the repository interfaces defined in the domain layer,
providing concrete implementations that use SQLAlchemy for data persistence.
"""

from typing import List, Optional, cast
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.domain.user_management.entities import User as UserEntity
from app.domain.user_management.entities import UserProfile as UserProfileEntity
from app.domain.user_management.repositories import (
    UserRepository,
    UserProfileRepository,
)
from app.domain.user_management.value_objects import Username, Password
from app.domain.common.value_objects import Email, NonEmptyString
from app.infrastructure.persistence.models.user import User as UserModel
from app.infrastructure.persistence.models.user import UserProfile as UserProfileModel


class SQLAlchemyUserRepository(UserRepository):
    """SQLAlchemy implementation of the UserRepository interface."""

    def __init__(self, db: Session):
        """Initialize with SQLAlchemy database session.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    async def get_by_id(self, id: UUID) -> Optional[UserEntity]:
        """Get a user by ID.

        Args:
            id: The user ID

        Returns:
            The user entity if found, None otherwise
        """
        user_model = self.db.query(UserModel).filter(UserModel.id == id).first()
        if not user_model:
            return None

        return self._map_to_entity(user_model)

    async def get_by_username(self, username: str) -> Optional[UserEntity]:
        """Get a user by username.

        Args:
            username: The username to search for

        Returns:
            The user entity if found, None otherwise
        """
        user_model = (
            self.db.query(UserModel).filter(UserModel.username == username).first()
        )
        if not user_model:
            return None

        return self._map_to_entity(user_model)

    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        """Get a user by email.

        Args:
            email: The email to search for

        Returns:
            The user entity if found, None otherwise
        """
        user_model = self.db.query(UserModel).filter(UserModel.email == email).first()
        if not user_model:
            return None

        return self._map_to_entity(user_model)

    async def list_users(self, skip: int = 0, limit: int = 100) -> List[UserEntity]:
        """Get a list of users with pagination.

        Args:
            skip: Number of users to skip
            limit: Maximum number of users to return

        Returns:
            List of user entities
        """
        user_models = self.db.query(UserModel).offset(skip).limit(limit).all()
        return [self._map_to_entity(user_model) for user_model in user_models]

    async def search_users(
        self, query: str, skip: int = 0, limit: int = 100
    ) -> List[UserEntity]:
        """Search for users by username, email, or full name.

        Args:
            query: The search query
            skip: Number of users to skip
            limit: Maximum number of users to return

        Returns:
            List of matching user entities
        """
        search = f"%{query}%"
        user_models = (
            self.db.query(UserModel)
            .filter(
                or_(
                    UserModel.username.ilike(search),
                    UserModel.email.ilike(search),
                    UserModel.full_name.ilike(search),
                )
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

        return [self._map_to_entity(user_model) for user_model in user_models]

    async def save(self, entity: UserEntity) -> UserEntity:
        """Save a user entity.

        If the user already exists, update it; otherwise, create a new user.

        Args:
            entity: The user entity to save

        Returns:
            The saved user entity
        """
        user_model = self.db.query(UserModel).filter(UserModel.id == entity.id).first()

        if user_model:
            # Update existing user
            user_model.username = str(entity.username)
            user_model.email = str(entity.email)
            user_model.hashed_password = entity.password.hashed_password
            user_model.full_name = str(entity.full_name)
            user_model.is_active = entity.is_active
            user_model.updated_at = entity.updated_at
            user_model.last_login = entity.last_login
            user_model.roles = entity.roles
        else:
            # Create new user
            user_model = UserModel(
                id=entity.id,
                username=str(entity.username),
                email=str(entity.email),
                hashed_password=entity.password.hashed_password,
                full_name=str(entity.full_name),
                is_active=entity.is_active,
                created_at=entity.created_at,
                updated_at=entity.updated_at,
                last_login=entity.last_login,
                roles=entity.roles,
            )
            self.db.add(user_model)

        self.db.commit()
        self.db.refresh(user_model)

        return self._map_to_entity(user_model)

    async def delete(self, entity: UserEntity) -> None:
        """Delete a user entity.

        Args:
            entity: The user entity to delete
        """
        user_model = self.db.query(UserModel).filter(UserModel.id == entity.id).first()
        if user_model:
            self.db.delete(user_model)
            self.db.commit()

    def _map_to_entity(self, model: UserModel) -> UserEntity:
        """Map a SQLAlchemy model to a domain entity.

        Args:
            model: The SQLAlchemy model

        Returns:
            The corresponding domain entity
        """
        return UserEntity(
            id=model.id,
            username=Username(model.username),
            email=Email(model.email),
            password=Password(model.hashed_password),
            full_name=NonEmptyString(model.full_name),
            roles=set(model.roles),
            created_at=model.created_at,
            updated_at=model.updated_at,
            last_login=model.last_login,
            is_active=model.is_active,
        )


class SQLAlchemyUserProfileRepository(UserProfileRepository):
    """SQLAlchemy implementation of the UserProfileRepository interface."""

    def __init__(self, db: Session):
        """Initialize with SQLAlchemy database session.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    async def get_by_id(self, id: UUID) -> Optional[UserProfileEntity]:
        """Get a user profile by ID.

        Args:
            id: The profile ID

        Returns:
            The profile entity if found, None otherwise
        """
        profile_model = (
            self.db.query(UserProfileModel).filter(UserProfileModel.id == id).first()
        )
        if not profile_model:
            return None

        return self._map_to_entity(profile_model)

    async def get_by_user_id(self, user_id: UUID) -> Optional[UserProfileEntity]:
        """Get a user profile by user ID.

        Args:
            user_id: The ID of the user

        Returns:
            The profile entity if found, None otherwise
        """
        profile_model = (
            self.db.query(UserProfileModel)
            .filter(UserProfileModel.user_id == user_id)
            .first()
        )
        if not profile_model:
            return None

        return self._map_to_entity(profile_model)

    async def save(self, entity: UserProfileEntity) -> UserProfileEntity:
        """Save a user profile entity.

        If the profile already exists, update it; otherwise, create a new profile.

        Args:
            entity: The profile entity to save

        Returns:
            The saved profile entity
        """
        profile_model = (
            self.db.query(UserProfileModel)
            .filter(UserProfileModel.id == entity.id)
            .first()
        )

        if profile_model:
            # Update existing profile
            profile_model.bio = entity.bio
            profile_model.avatar_url = entity.avatar_url
            profile_model.preferences = entity.preferences
        else:
            # Create new profile
            profile_model = UserProfileModel(
                id=entity.id,
                user_id=entity.user_id,
                bio=entity.bio,
                avatar_url=entity.avatar_url,
                preferences=entity.preferences,
            )
            self.db.add(profile_model)

        self.db.commit()
        self.db.refresh(profile_model)

        return self._map_to_entity(profile_model)

    async def delete(self, entity: UserProfileEntity) -> None:
        """Delete a user profile entity.

        Args:
            entity: The profile entity to delete
        """
        profile_model = (
            self.db.query(UserProfileModel)
            .filter(UserProfileModel.id == entity.id)
            .first()
        )
        if profile_model:
            self.db.delete(profile_model)
            self.db.commit()

    def _map_to_entity(self, model: UserProfileModel) -> UserProfileEntity:
        """Map a SQLAlchemy model to a domain entity.

        Args:
            model: The SQLAlchemy model

        Returns:
            The corresponding domain entity
        """
        return UserProfileEntity(
            id=model.id,
            user_id=model.user_id,
            bio=model.bio,
            avatar_url=model.avatar_url,
            preferences=model.preferences or {},
        )
