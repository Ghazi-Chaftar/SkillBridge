"""This module provides profile-related routes for the application."""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, File, HTTPException, Query, UploadFile, Request

from src.utils import serialize_model

from ..auth.service import CurrentUser
from ..database.core import DbSession
from ..entities.profile import EducationLevel, Gender, TeachingMethod
from ..utils import build_response
from . import model, service

router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.post("/")
def create_profile(profile_data: model.ProfileCreate, db: DbSession, current_user: CurrentUser):
    """Create a new profile for the authenticated user."""
    try:
        # Override user_id with current authenticated user
        profile_data.user_id = current_user.get_uuid()
        profile = service.create_profile(db, profile_data)
        return build_response(
            success=True,
            message="Profile created successfully",
            data=serialize_model(profile),
            status_code=201,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/current")
def get_current_profile(db: DbSession, current_user: CurrentUser):
    """Get the current user's profile."""

    profile = service.get_profile_by_user_id(db, current_user.get_uuid())
    if not profile:
        return build_response(success=False, message="Profile not found", status_code=404)
    return build_response(
        success=True,
        message="Profile retrieved successfully",
        data=serialize_model(profile),
        status_code=200,
    )


@router.get("/{profile_id}")
def get_profile(profile_id: UUID, db: DbSession):
    """Get a profile by ID."""
    profile = service.get_profile_by_id(db, profile_id)
    if not profile:
        return build_response(success=False, message="Profile not found", status_code=404)
    return build_response(
        success=True,
        message="Profile retrieved successfully",
        data=serialize_model(profile),
        status_code=200,
    )


@router.get("/user/{user_id}")
def get_profile_by_user(user_id: UUID, db: DbSession):
    """Get a profile by user ID."""
    profile = service.get_profile_by_user_id(db, user_id)
    if not profile:
        return build_response(success=False, message="Profile not found", status_code=404)
    return build_response(
        success=True,
        message="Profile retrieved successfully",
        data=serialize_model(profile),
        status_code=200,
    )


@router.get("/")
def get_profiles(
    db: DbSession,
    skip: int = Query(0, ge=0, description="Number of profiles to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of profiles to return"),
    subject: Optional[str] = Query(None, description="Filter by subject"),
    level: Optional[EducationLevel] = Query(None, description="Filter by education level"),
    teaching_method: Optional[TeachingMethod] = Query(None, description="Filter by teaching method"),
    location: Optional[str] = Query(None, description="Filter by location"),
    gender: Optional[Gender] = Query(None, description="Filter by gender"),
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
        gender=gender,
    )

    total = service.get_profiles_count(
        db=db,
        subject=subject,
        level=level,
        teaching_method=teaching_method,
        location=location,
        gender=gender,
    )

    profile_list_data = {
        "profiles": [serialize_model(p) for p in profiles],
        "total": total,
        "page": (skip // limit) + 1,
        "per_page": limit,
        "has_next": (skip + limit) < total,
        "has_prev": skip > 0,
    }

    return build_response(
        success=True, message="Profiles retrieved successfully", data=profile_list_data, status_code=200
    )


@router.get("/search/")
def search_profiles(
    search_term: str = Query(..., min_length=1, description="Search term"),
    db: DbSession = DbSession,
    skip: int = Query(0, ge=0, description="Number of profiles to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of profiles to return"),
):
    """Search profiles by bio, subjects, or location."""
    profiles = service.search_profiles(db, search_term, skip, limit)
    return build_response(
        success=True,
        message="Search completed successfully",
        data=[serialize_model(p) for p in profiles],
        status_code=200,
    )


@router.put("/current")
def update_current_profile(
    profile_update: model.ProfileUpdate,
    db: DbSession,
    current_user: CurrentUser,
):
    """Update the current user's profile."""
    profile = service.get_profile_by_user_id(db, current_user.get_uuid())
    if not profile:
        return build_response(success=False, message="Profile not found", status_code=404)

    updated_profile = service.update_profile(db, profile.id, profile_update)
    if not updated_profile:
        return build_response(success=False, message="Profile not found", status_code=404)

    return build_response(
        success=True,
        message="Profile updated successfully",
        data=serialize_model(updated_profile),
        status_code=200,
    )


@router.put("/{profile_id}")
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
        return build_response(success=False, message="Profile not found", status_code=404)

    if profile.user_id != current_user.get_uuid():
        return build_response(success=False, message="Not authorized to update this profile", status_code=403)

    updated_profile = service.update_profile(db, profile_id, profile_update)
    if not updated_profile:
        return build_response(success=False, message="Profile not found", status_code=404)

    return build_response(
        success=True,
        message="Profile updated successfully",
        data=serialize_model(updated_profile),
        status_code=200,
    )


@router.delete("/")
def delete_current_profile(db: DbSession, current_user: CurrentUser):
    """Delete the current user's profile."""
    profile = service.get_profile_by_user_id(db, current_user.get_uuid())
    if not profile:
        return build_response(success=False, message="Profile not found", status_code=404)

    success = service.delete_profile(db, profile.id)
    if not success:
        return build_response(success=False, message="Profile not found", status_code=404)

    return build_response(success=True, message="Profile deleted successfully", status_code=200)


@router.delete("/{profile_id}")
def delete_profile(profile_id: UUID, db: DbSession, current_user: CurrentUser):
    """Delete a profile by ID (only profile owner can delete)."""
    profile = service.get_profile_by_id(db, profile_id)
    if not profile:
        return build_response(success=False, message="Profile not found", status_code=404)

    if profile.user_id != current_user.get_uuid():
        return build_response(success=False, message="Not authorized to delete this profile", status_code=403)

    success = service.delete_profile(db, profile_id)
    if not success:
        return build_response(success=False, message="Profile not found", status_code=404)

    return build_response(success=True, message="Profile deleted successfully", status_code=200)


@router.post("/upload-picture")
async def upload_profile_picture(
    request: Request, db: DbSession, current_user: CurrentUser, file: UploadFile = File(...)
):
    """Upload a profile picture for the current user."""
    try:
        result = service.upload_profile_picture(db, current_user.get_uuid(), file)

        return build_response(
            success=True,
            message=result["message"],
            data={"file_path": result["file_path"], "filename": result["filename"]},
            status_code=200,
        )
    except HTTPException as e:
        return build_response(success=False, message=e.detail, status_code=e.status_code)
    except Exception:
        return build_response(success=False, message="Failed to upload profile picture", status_code=500)
