"""
This module defines the data models used for user registration and
token management
"""

from uuid import UUID  # noqa: I001
from pydantic import BaseModel, EmailStr


class RegisterUserRequest(BaseModel):
    """Data model for user registration request."""

    email: EmailStr
    first_name: str
    last_name: str
    password: str
    phone_number: str


class Token(BaseModel):
    """Data model for authentication token response."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Data model for token data containing user ID."""

    user_id: str | None = None

    def get_uuid(self) -> UUID | None:
        if self.user_id:
            return UUID(self.user_id)
        return None
