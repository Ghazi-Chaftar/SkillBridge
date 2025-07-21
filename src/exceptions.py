"""Exception definitions for the FastAPI application."""

from fastapi import HTTPException


class TodoError(HTTPException):
    """Base exception for todo-related errors"""

    pass


class TodoNotFoundError(TodoError):
    """Exception raised when a todo item is not found."""

    def __init__(self, todo_id=None):
        message = "Todo not found" if todo_id is None else f"Todo with id {todo_id} not found"
        super().__init__(status_code=404, detail=message)


class TodoCreationError(TodoError):
    """Exception raised when there is an error creating a todo item."""

    def __init__(self, error: str):
        super().__init__(status_code=500, detail=f"Failed to create todo: {error}")


class UserError(HTTPException):
    """Base exception for user-related errors"""

    pass


class UserNotFoundError(UserError):
    """Exception raised when a user is not found."""

    def __init__(self, user_id=None):
        message = "User not found" if user_id is None else f"User with id {user_id} not found"
        super().__init__(status_code=404, detail=message)


class PasswordMismatchError(UserError):
    """Exception raised when new passwords do not match."""

    def __init__(self):
        super().__init__(status_code=400, detail="New passwords do not match")


class InvalidPasswordError(UserError):
    """Exception raised when the current password is incorrect."""

    def __init__(self):
        super().__init__(status_code=401, detail="Current password is incorrect")


class DuplicateEmailError(UserError):
    """Exception raised when trying to register with an email that already exists."""

    def __init__(self, email: str = None):
        message = "Email already exists" if email is None else f"User with email {email} already exists"
        super().__init__(status_code=409, detail=message)


class AuthenticationError(HTTPException):
    """Exception raised for authentication failures."""

    def __init__(self, message: str = "Could not validate user"):
        super().__init__(status_code=401, detail=message)


class InvalidCrendentialError(HTTPException):
    """Exception raised for authentication failures."""

    def __init__(self, message: str = "Email or password are incorrect"):
        super().__init__(status_code=404, detail=message)


class DuplicatePhoneError(UserError):
    """Exception raised when trying to register with a phone number that already exists."""

    def __init__(self, phone: str = None):
        message = "Phone number already exists" if phone is None else f"User with phone number {phone} already exists"
        super().__init__(status_code=409, detail=message)
