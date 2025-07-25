"""This module defines data models for user-related operations in the application."""

from uuid import UUID

from pydantic import BaseModel, EmailStr
from fastapi_camelcase import CamelModel


class UserResponse(BaseModel):
    """Data model for user response containing user details."""

    id: UUID
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: str


class PasswordChange(BaseModel):
    """Data model for password change request."""

    current_password: str
    new_password: str
    new_password_confirm: str


class UserUpdate(CamelModel):
    """Data model for updating a user"""

    first_name: str
    last_name: str
    phone_number: str
