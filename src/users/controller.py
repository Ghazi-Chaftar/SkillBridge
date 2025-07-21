"""This module provides user-related routes for the application."""

from fastapi import APIRouter

from src.utils import build_response, serialize_model

from src.exceptions import UserNotFoundError
from ..auth.service import CurrentUser
from ..database.core import DbSession
from . import model, service

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/current")
def get_current_user(current_user: CurrentUser, db: DbSession):
    user = service.get_user_by_id(db, current_user.get_uuid())
    return build_response(
        success=True,
        message="User retrieved successfully",
        data=serialize_model(user),
        status_code=200,
    )


@router.put("/change-password")
def change_password(password_change: model.PasswordChange, db: DbSession, current_user: CurrentUser):
    service.change_password(db, current_user.get_uuid(), password_change)
    return build_response(success=True, message="Password changed successfully", status_code=200)


@router.put("/current")
def update_current_user(
    user_update: model.UserUpdate,
    db: DbSession,
    current_user: CurrentUser,
):
    """Update the current user's information."""
    user = service.get_user_by_id(db, current_user.get_uuid())
    if not user:
        raise UserNotFoundError()

    updated_user = service.update_user(db, user.id, user_update)
    if not updated_user:
        raise UserNotFoundError()

    return build_response(
        success=True,
        message="User updated successfully",
        data=serialize_model(updated_user),
        status_code=200,
    )
