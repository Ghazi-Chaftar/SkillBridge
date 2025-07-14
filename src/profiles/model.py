"""
Profile Pydantic models for request/response serialization.

This module defines Pydantic models for Profile-related operations:
- ProfileCreate: Model for creating a new profile
- ProfileUpdate: Model for updating an existing profile
- ProfileResponse: Model for profile responses
- ProfileInDB: Model representing profile data as stored in database
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from ..entities.profile import EducationLevel, Gender, TeachingMethod


class ProfileBase(BaseModel):
    """Base Profile model with common fields."""

    bio: str = Field(..., min_length=1, max_length=1000, description="Profile biography")
    profile_picture: Optional[str] = Field(None, description="URL to profile picture")
    degrees: Optional[List[str]] = Field(None, description="List of academic degrees")
    years_of_experience: Optional[str] = Field(None, description="Years of teaching experience")
    subjects: Optional[List[str]] = Field(None, description="List of subjects taught")
    levels: Optional[List[EducationLevel]] = Field(None, description="Education levels taught")
    teaching_method: Optional[TeachingMethod] = Field(None, description="Preferred teaching method")
    location: Optional[str] = Field(None, description="Teaching location")
    gender: Gender = Field(..., description="Gender")
    hourly_rate: Optional[str] = Field(None, description="Hourly rate for teaching")
    currency: str = Field(default="TND", description="Currency for hourly rate")


class ProfileCreate(ProfileBase):
    """Model for creating a new profile."""

    user_id: UUID = Field(..., description="ID of the user this profile belongs to")


class ProfileUpdate(BaseModel):
    """Model for updating an existing profile."""

    bio: Optional[str] = Field(None, min_length=1, max_length=1000, description="Profile biography")
    profile_picture: Optional[str] = Field(None, description="URL to profile picture")
    degrees: Optional[List[str]] = Field(None, description="List of academic degrees")
    years_of_experience: Optional[str] = Field(None, description="Years of teaching experience")
    subjects: Optional[List[str]] = Field(None, description="List of subjects taught")
    levels: Optional[List[EducationLevel]] = Field(None, description="Education levels taught")
    teaching_method: Optional[TeachingMethod] = Field(None, description="Preferred teaching method")
    location: Optional[str] = Field(None, description="Teaching location")
    gender: Optional[Gender] = Field(None, description="Gender")
    hourly_rate: Optional[str] = Field(None, description="Hourly rate for teaching")
    currency: Optional[str] = Field(None, description="Currency for hourly rate")


class ProfileResponse(ProfileBase):
    """Model for profile responses."""

    id: UUID = Field(..., description="Profile unique identifier")
    user_id: UUID = Field(..., description="ID of the user this profile belongs to")
    created_at: datetime = Field(..., description="Profile creation timestamp")
    updated_at: datetime = Field(..., description="Profile last update timestamp")

    class Config:
        from_attributes = True


class ProfileInDB(ProfileResponse):
    """Model representing profile data as stored in database."""

    pass


class ProfileListResponse(BaseModel):
    """Model for paginated profile list responses."""

    profiles: List[ProfileResponse] = Field(..., description="List of profiles")
    total: int = Field(..., description="Total number of profiles")
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Number of profiles per page")
    has_next: bool = Field(..., description="Whether there are more pages")
    has_prev: bool = Field(..., description="Whether there are previous pages")
