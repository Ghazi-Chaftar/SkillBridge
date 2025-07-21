"""
This module defines the data models used for user registration and
token management
"""

from uuid import UUID  # noqa: I001
from pydantic import BaseModel, EmailStr
from fastapi_camelcase import CamelModel


class RegisterUserRequest(CamelModel):
    """Data model for user registration request."""

    email: EmailStr
    first_name: str
    last_name: str
    password: str
    phone_number: str


class LoginRequest(CamelModel):
    """Data model for user login request."""

    username: EmailStr
    password: str


class Token(CamelModel):
    """Data model for authentication token response."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Data model for token data containing user ID."""

    user_id: str | None = None

    def get_uuid(self) -> UUID | None:
        """Convert user_id string to UUID object."""
        if self.user_id:
            return UUID(self.user_id)
        return None
