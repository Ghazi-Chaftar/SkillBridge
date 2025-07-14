"""This module provides profile-related routes for the application."""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from ..auth.service import CurrentUser
from ..database.core import DbSession
from ..entities.profile import EducationLevel, TeachingMethod
from . import model, service

router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.post("/", response_model=model.ProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(profile_data: model.ProfileCreate, db: DbSession, current_user: CurrentUser):
    """Create a new profile for the authenticated user."""
    try:
        # Override user_id with current authenticated user
        profile_data.user_id = current_user.get_uuid()
        return service.create_profile(db, profile_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/current", response_model=model.ProfileResponse)
def get_current_profile(db: DbSession, current_user: CurrentUser):
    """Get the current user's profile."""
    profile = service.get_profile_by_user_id(db, current_user.get_uuid())
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile


@router.get("/{profile_id}", response_model=model.ProfileResponse)
def get_profile(profile_id: UUID, db: DbSession):
    """Get a profile by ID."""
    profile = service.get_profile_by_id(db, profile_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile


@router.get("/user/{user_id}", response_model=model.ProfileResponse)
def get_profile_by_user(user_id: UUID, db: DbSession):
    """Get a profile by user ID."""
    profile = service.get_profile_by_user_id(db, user_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile


@router.get("/", response_model=model.ProfileListResponse)
def get_profiles(
    db: DbSession,
    skip: int = Query(0, ge=0, description="Number of profiles to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of profiles to return"),
    subject: Optional[str] = Query(None, description="Filter by subject"),
    level: Optional[EducationLevel] = Query(None, description="Filter by education level"),
    teaching_method: Optional[TeachingMethod] = Query(None, description="Filter by teaching method"),
    location: Optional[str] = Query(None, description="Filter by location"),
):
    """Get paginated list of profiles with optional filtering."""
    profiles = service.get_profiles(
        db=db,
        skip=skip,
        limit=limit,
        subject=subject,
        level=level,
        teaching_method=teaching_method,
        location=location,
    )

    total = service.get_profiles_count(
        db=db,
        subject=subject,
        level=level,
        teaching_method=teaching_method,
        location=location,
    )

    return model.ProfileListResponse(
        profiles=profiles,
        total=total,
        page=(skip // limit) + 1,
        per_page=limit,
        has_next=(skip + limit) < total,
        has_prev=skip > 0,
    )


@router.get("/search/", response_model=List[model.ProfileResponse])
def search_profiles(
    search_term: str = Query(..., min_length=1, description="Search term"),
    db: DbSession = DbSession,
    skip: int = Query(0, ge=0, description="Number of profiles to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of profiles to return"),
):
    """Search profiles by bio, subjects, or location."""
    return service.search_profiles(db, search_term, skip, limit)


@router.put("/current", response_model=model.ProfileResponse)
def update_current_profile(
    profile_update: model.ProfileUpdate,
    db: DbSession,
    current_user: CurrentUser,
):
    """Update the current user's profile."""
    profile = service.get_profile_by_user_id(db, current_user.get_uuid())
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    updated_profile = service.update_profile(db, profile.id, profile_update)
    if not updated_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    return updated_profile


@router.put("/{profile_id}", response_model=model.ProfileResponse)
def update_profile(
    profile_id: UUID,
    profile_update: model.ProfileUpdate,
    db: DbSession,
    current_user: CurrentUser,
):
    """Update a profile by ID (only profile owner can update)."""
    # Check if profile exists and belongs to current user
    profile = service.get_profile_by_id(db, profile_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    if profile.user_id != current_user.get_uuid():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this profile")

    updated_profile = service.update_profile(db, profile_id, profile_update)
    if not updated_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    return updated_profile


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_current_profile(db: DbSession, current_user: CurrentUser):
    """Delete the current user's profile."""
    profile = service.get_profile_by_user_id(db, current_user.get_uuid())
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    success = service.delete_profile(db, profile.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(profile_id: UUID, db: DbSession, current_user: CurrentUser):
    """Delete a profile by ID (only profile owner can delete)."""
    profile = service.get_profile_by_id(db, profile_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    if profile.user_id != current_user.get_uuid():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this profile")

    success = service.delete_profile(db, profile_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
