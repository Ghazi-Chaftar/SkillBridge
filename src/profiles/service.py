"""Service module for profile-related operations."""

import logging
from pathlib import Path
from typing import List, Optional
from uuid import UUID, uuid4

from fastapi import HTTPException, UploadFile
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..entities.profile import EducationLevel, Gender, Profile, TeachingMethod
from .model import ProfileCreate, ProfileResponse, ProfileUpdate


def create_profile(db: Session, profile_data: ProfileCreate) -> ProfileResponse:
    """
    Create a new profile.

    Args:
        db: Database session
        profile_data: Profile creation data

    Returns:
        Created profile instance

    Raises:
        ValueError: If user already has a profile
    """
    try:
        existing_profile = get_profile_by_user_id(db, profile_data.user_id)
        if existing_profile:
            logging.warning(f"User {profile_data.user_id} already has a profile")
            raise ValueError("User already has a profile")

        db_profile = Profile(**profile_data.model_dump())
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        logging.info(f"Successfully created profile for user ID: {profile_data.user_id}")
        return db_profile
    except Exception as e:
        logging.error(f"Error creating profile for user ID: {profile_data.user_id}. Error: {str(e)}")
        raise


def get_profile_by_id(db: Session, profile_id: UUID) -> Optional[ProfileResponse]:
    """
    Get profile by ID.

    Args:
        db: Database session
        profile_id: Profile unique identifier

    Returns:
        Profile instance or None if not found
    """
    try:
        profile = db.query(Profile).filter(Profile.id == profile_id).first()
        if profile:
            logging.info(f"Successfully retrieved profile with ID: {profile_id}")
        else:
            logging.warning(f"Profile not found with ID: {profile_id}")
        return profile
    except Exception as e:
        logging.error(f"Error retrieving profile with ID: {profile_id}. Error: {str(e)}")
        raise


def get_profile_by_user_id(db: Session, user_id: UUID) -> Optional[ProfileResponse]:
    """
    Get profile by user ID.

    Args:
        db: Database session
        user_id: User unique identifier

    Returns:
        Profile instance or None if not found
    """
    try:
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        if profile:
            logging.info(f"Successfully retrieved profile for user ID: {user_id}")
        else:
            logging.warning(f"Profile not found for user ID: {user_id}")
        return profile
    except Exception as e:
        logging.error(f"Error retrieving profile for user ID: {user_id}. Error: {str(e)}")
        raise


def get_profiles(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    subject: Optional[str] = None,
    level: Optional[EducationLevel] = None,
    teaching_method: Optional[TeachingMethod] = None,
    location: Optional[str] = None,
    gender: Optional[Gender] = None,
) -> List[ProfileResponse]:
    """
    Get profiles with optional filtering.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        subject: Filter by subject
        level: Filter by education level
        teaching_method: Filter by teaching method
        location: Filter by location (partial match)
        gender: Filter by gender

    Returns:
        List of profile instances
    """
    try:
        query = db.query(Profile)

        # Apply filters
        if subject:
            query = query.filter(Profile.subjects.any(subject))

        if level:
            query = query.filter(Profile.levels.any(level))

        if teaching_method:
            query = query.filter(Profile.teaching_method == teaching_method)

        if location:
            query = query.filter(Profile.location.ilike(f"%{location}%"))

        if gender:
            query = query.filter(Profile.gender == gender)

        profiles = query.offset(skip).limit(limit).all()
        logging.info(f"Successfully retrieved {len(profiles)} profiles with filters")
        return profiles
    except Exception as e:
        logging.error(f"Error retrieving profiles with filters. Error: {str(e)}")
        raise


def search_profiles(db: Session, search_term: str, skip: int = 0, limit: int = 100) -> List[ProfileResponse]:
    """
    Search profiles by bio, subjects, or location.

    Args:
        db: Database session
        search_term: Search term to look for
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of matching profile instances
    """
    try:
        search_pattern = f"%{search_term}%"

        profiles = (
            db.query(Profile)
            .filter(
                or_(
                    Profile.bio.ilike(search_pattern),
                    Profile.subjects.any(search_pattern),
                    Profile.location.ilike(search_pattern),
                )
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

        logging.info(f"Successfully searched profiles with term '{search_term}', found {len(profiles)} results")
        return profiles
    except Exception as e:
        logging.error(f"Error searching profiles with term '{search_term}'. Error: {str(e)}")
        raise


def update_profile(db: Session, profile_id: UUID, profile_update: ProfileUpdate) -> Optional[ProfileResponse]:
    """
    Update an existing profile.

    Args:
        db: Database session
        profile_id: Profile unique identifier
        profile_update: Profile update data

    Returns:
        Updated profile instance or None if not found
    """
    try:
        db_profile = get_profile_by_id(db, profile_id)
        if not db_profile:
            logging.warning(f"Profile not found for update with ID: {profile_id}")
            return None

        # Update only provided fields
        update_data = profile_update.model_dump(exclude_unset=True)
        logging.debug(f"Update data for profile {profile_id}: {update_data}")
        for field, value in update_data.items():
            setattr(db_profile, field, value)

        db.commit()
        db.refresh(db_profile)
        logging.info(f"Successfully updated profile with ID: {profile_id}")
        return db_profile
    except Exception as e:
        logging.error(f"Error updating profile with ID: {profile_id}. Error: {str(e)}")
        raise


def delete_profile(db: Session, profile_id: UUID) -> bool:
    """
    Delete a profile.

    Args:
        db: Database session
        profile_id: Profile unique identifier

    Returns:
        True if profile was deleted, False if not found
    """
    try:
        db_profile = get_profile_by_id(db, profile_id)
        if not db_profile:
            logging.warning(f"Profile not found for deletion with ID: {profile_id}")
            return False

        db.delete(db_profile)
        db.commit()
        logging.info(f"Successfully deleted profile with ID: {profile_id}")
        return True
    except Exception as e:
        logging.error(f"Error deleting profile with ID: {profile_id}. Error: {str(e)}")
        raise


def get_profiles_count(
    db: Session,
    subject: Optional[str] = None,
    level: Optional[EducationLevel] = None,
    teaching_method: Optional[TeachingMethod] = None,
    location: Optional[str] = None,
    gender: Optional[Gender] = None,
) -> int:
    """
    Get total count of profiles with optional filtering.

    Args:
        db: Database session
        subject: Filter by subject
        level: Filter by education level
        teaching_method: Filter by teaching method
        location: Filter by location (partial match)
        gender: Filter by gender

    Returns:
        Total count of matching profiles
    """
    try:
        query = db.query(Profile)

        # Apply same filters as get_profiles
        if subject:
            query = query.filter(Profile.subjects.any(subject))

        if level:
            query = query.filter(Profile.levels.any(level))

        if teaching_method:
            query = query.filter(Profile.teaching_method == teaching_method)

        if location:
            query = query.filter(Profile.location.ilike(f"%{location}%"))

        if gender:
            query = query.filter(Profile.gender == gender)

        count = query.count()
        logging.info(f"Successfully counted {count} profiles with filters")
        return count
    except Exception as e:
        logging.error(f"Error counting profiles with filters. Error: {str(e)}")
        raise


def upload_profile_picture(db: Session, user_id: UUID, file: UploadFile) -> dict:
    """
    Upload and save a profile picture for a user.

    Args:
        db: Database session
        user_id: User ID to update profile picture for
        file: Uploaded file

    Returns:
        Dictionary with success message and file path

    Raises:
        HTTPException: If file type is invalid or profile not found
    """
    try:
        allowed_extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
        file_ext = Path(file.filename).suffix.lower() if file.filename else ""

        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400, detail=f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}"
            )

        # Validate file size (5MB max)
        max_file_size = 5 * 1024 * 1024  # 5MB in bytes
        file.file.seek(0, 2)  # Seek to end of file
        file_size = file.file.tell()  # Get file size
        file.file.seek(0)  # Reset file pointer

        if file_size > max_file_size:
            raise HTTPException(status_code=400, detail="File size too large. Maximum size is 5MB.")

        # Get the user's profile
        profile = get_profile_by_user_id(db, user_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        # Create directory if it doesn't exist
        upload_dir = Path("static/profile_pictures")
        upload_dir.mkdir(parents=True, exist_ok=True)

        # Generate unique filename to avoid conflicts
        unique_filename = f"{uuid4()}{file_ext}"
        file_path = upload_dir / unique_filename

        # Save file
        with open(file_path, "wb") as buffer:
            # Read file content synchronously
            content = file.file.read()
            buffer.write(content)

        # Update profile in database
        profile.profile_picture = str(file_path)
        db.commit()
        db.refresh(profile)

        logging.info(f"Successfully uploaded profile picture for user ID: {user_id}")

        return {
            "message": "Profile picture uploaded successfully",
            "file_path": str(file_path),
            "filename": unique_filename,
        }

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logging.error(f"Error uploading profile picture for user ID: {user_id}. Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to upload profile picture")
