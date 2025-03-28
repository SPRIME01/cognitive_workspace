"""
Database configuration for SQLAlchemy.

This module provides the SQLAlchemy database session and connection setup
for the Cognitive Workspace application.
"""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

# Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URI, pool_pre_ping=True, echo=settings.SQL_ECHO
)

# Create sessionmaker with class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all SQLAlchemy models
Base = declarative_base()


async def get_db() -> Generator[Session, None, None]:
    """Get a database session.

    Creates a new SQLAlchemy Session that will be used for a single request,
    and then closed once the request is finished.

    Yields:
        SQLAlchemy Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
