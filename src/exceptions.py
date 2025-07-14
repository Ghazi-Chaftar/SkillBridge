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


class AuthenticationError(HTTPException):
    """Exception raised for authentication failures."""

    def __init__(self, message: str = "Could not validate user"):
        super().__init__(status_code=401, detail=message)
