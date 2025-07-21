"""Service module for user-related operations."""

import logging
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.auth.service import get_password_hash, verify_password
from src.entities.user import User
from src.exceptions import InvalidPasswordError, PasswordMismatchError, UserNotFoundError

from src.users.model import UserUpdate
from .model import PasswordChange, UserResponse


def get_user_by_id(db: Session, user_id: UUID) -> UserResponse:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logging.warning(f"User not found with ID: {user_id}")
        raise UserNotFoundError(user_id)
    logging.info(f"Successfully retrieved user with ID: {user_id}")
    return user


def change_password(db: Session, user_id: UUID, password_change: PasswordChange) -> None:
    try:
        user = get_user_by_id(db, user_id)

        # Verify current password
        if not verify_password(password_change.current_password, user.password_hash):
            logging.warning(f"Invalid current password provided for user ID: {user_id}")
            raise InvalidPasswordError()

        # Verify new passwords match
        if password_change.new_password != password_change.new_password_confirm:
            logging.warning(f"Password mismatch during change attempt for user ID: {user_id}")
            raise PasswordMismatchError()

        # Update password
        user.password_hash = get_password_hash(password_change.new_password)
        db.commit()
        logging.info(f"Successfully changed password for user ID: {user_id}")
    except Exception as e:
        logging.error(f"Error during password change for user ID: {user_id}. Error: {str(e)}")
        raise


def update_user(db: Session, user_id: UUID, user_update: UserUpdate) -> Optional[UserUpdate]:
    """
    Update an existing user.

    Args:
        db: Database session
        user_id: User unique identifier
        user_update: User update data

    Returns:
        Updated profile instance or None if not found
    """
    try:
        db_user = get_user_by_id(db, user_id)
        if not db_user:
            logging.warning(f"User not found for update with ID: {user_id}")
            return None

        # Update only provided fields
        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)

        db.commit()
        db.refresh(db_user)
        logging.info(f"Successfully updated user with ID: {user_id}")
        return db_user
    except Exception as e:
        logging.error(f"Error updating user with ID: {user_id}. Error: {str(e)}")
        raise
