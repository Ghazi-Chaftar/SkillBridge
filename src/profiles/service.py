"""Service module for profile-related operations."""

import logging
from typing import List, Optional
from uuid import UUID

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
        print(update_data)
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
