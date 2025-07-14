"""Base entity with created_at and updated_at timestamps."""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime

from ..database.core import Base


class BaseEntity(Base):
    """Base entity with created_at and updated_at timestamps."""

    __abstract__ = True

    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
