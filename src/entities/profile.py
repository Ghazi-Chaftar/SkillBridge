"""
Profile entity module for the FastAPI application.

This module defines the Profile entity and related components:
- EducationLevel: Enum class for education levels
- TeachingMethod: Enum class for teaching methods
- Profile: SQLAlchemy model representing a user profile in the database
"""

import enum
import uuid

from sqlalchemy import ARRAY, Column, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from .base import BaseEntity


class EducationLevel(str, enum.Enum):
    """Enumeration of education levels."""

    PRIMARY = "primary"
    SECONDARY = "high school"
    UNIVERSITY = "university"


class TeachingMethod(str, enum.Enum):
    """Enumeration of teaching methods."""

    ONLINE = "online"
    IN_PERSON = "in person"
    HYBRID = "hybrid"


class Gender(str, enum.Enum):
    """Enumeration of teaching methods."""

    MALE = "male"
    FEMALE = "female"


class Profile(BaseEntity):
    """SQLAlchemy model representing a Profile."""

    __tablename__ = "profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    profile_picture = Column(String, nullable=True)
    bio = Column(String, nullable=False)
    degrees = Column(ARRAY(String), nullable=True)
    years_of_experience = Column(String, nullable=True)
    subjects = Column(ARRAY(String), nullable=True)
    levels = Column(ARRAY(Enum(EducationLevel)), nullable=True)
    teaching_method = Column(Enum(TeachingMethod), nullable=True)
    location = Column(String, nullable=True)
    gender = Column(Enum(Gender), nullable=False, default=Gender.MALE)
    hourly_rate = Column(String, nullable=True)
    languages = Column(ARRAY(String), nullable=True)

    currency = Column(String, nullable=False, default="TND")

    def __repr__(self):
        return f"<Profile(user_id='{self.user_id}', bio='{self.bio}')>"
