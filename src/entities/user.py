"""
User entity module for database operations.

This module defines the User entity model that maps to the 'users' table in the database,
including fields for user identification and authentication.
"""

import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from .base import BaseEntity


class User(BaseEntity):
    """SQLAlchemy model representing a user in the application."""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)

    def __repr__(self):
        return f"<User(email='{self.email}', first_name='{self.first_name}', last_name='{self.last_name}')>"
