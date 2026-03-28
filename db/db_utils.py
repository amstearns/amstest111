"""
Database connection utilities for the Renewable Energy Executive Dashboard.

Usage:
    from db.db_utils import get_engine, get_session, session_scope

    # Context manager (recommended)
    with session_scope() as session:
        trends = session.query(MarketTrend).all()

    # FastAPI dependency injection
    from db.db_utils import get_db
    def my_route(db: Session = Depends(get_db)):
        ...
"""

import os
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://agent:agent_dev@postgres:5432/appdb",
)

# Singleton engine
_engine = None


def get_engine():
    """Return (creating if necessary) the SQLAlchemy engine."""
    global _engine
    if _engine is None:
        _engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,  # Detect stale connections
            pool_size=5,
            max_overflow=10,
        )
    return _engine


# Session factory
_SessionLocal = None


def _get_session_factory():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(
            bind=get_engine(),
            autocommit=False,
            autoflush=False,
        )
    return _SessionLocal


@contextmanager
def session_scope() -> Generator[Session, None, None]:
    """
    Context manager providing a transactional database session.

    Example:
        with session_scope() as session:
            results = session.query(MarketTrend).all()
    """
    SessionLocal = _get_session_factory()
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_session() -> Session:
    """
    Create and return a new database session.
    Caller is responsible for closing the session.
    Prefer session_scope() context manager when possible.
    """
    SessionLocal = _get_session_factory()
    return SessionLocal()


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency for database session injection.

    Usage in FastAPI routes:
        from fastapi import Depends
        from sqlalchemy.orm import Session
        from db.db_utils import get_db

        @app.get("/market-trends")
        def get_trends(db: Session = Depends(get_db)):
            return db.query(MarketTrend).all()
    """
    SessionLocal = _get_session_factory()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
