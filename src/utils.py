"""Utility functions for FastAPI responses."""

from datetime import datetime
from typing import Any, Dict, Optional, Union
from uuid import UUID

from fastapi.responses import JSONResponse


def build_response(
    success: bool = True,
    message: str = "",
    data: Optional[Union[Dict[str, Any], list, Any]] = None,
    status_code: int = 200,
) -> JSONResponse:
    """
    Build a standardized API response for FastAPI.

    Args:
        success (bool): Indicates if the request was successful.
        message (str): A message related to the response.
        data (dict, list, or any): The data to be included in the response.
        status_code (int): HTTP status code.

    Returns:
        JSONResponse: A FastAPI JSONResponse object with the standardized format.
    """

    # Function to convert snake_case to camelCase
    def to_camel_case(snake_str):
        components = snake_str.split("_")
        return components[0] + "".join(x.title() for x in components[1:])

    # Recursively convert dictionary keys to camelCase
    def convert_keys_to_camel_case(obj):
        if isinstance(obj, dict):
            return {to_camel_case(k): convert_keys_to_camel_case(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_keys_to_camel_case(item) for item in obj]
        return obj

    # Convert data to camelCase if it exists
    camel_data = convert_keys_to_camel_case(data) if data is not None else {}

    response_data = {
        "success": success,
        "message": message,
        "data": camel_data,
    }
    return JSONResponse(content=response_data, status_code=status_code)


def serialize_model(obj: Any) -> Dict[str, Any]:
    """
    Serialize a SQLAlchemy model or Pydantic model to a dictionary.

    Args:
        obj: The object to serialize (SQLAlchemy model, Pydantic model, or any object)

    Returns:
        Dict[str, Any]: Dictionary representation of the object
    """

    def convert_value(value):
        """Convert non-serializable values to serializable ones."""
        if isinstance(value, UUID):
            return str(value)
        elif isinstance(value, datetime):
            return value.isoformat()
        elif isinstance(value, (list, tuple)):
            return [convert_value(item) for item in value]
        elif isinstance(value, dict):
            return {k: convert_value(v) for k, v in value.items()}
        else:
            return value

    if hasattr(obj, "model_dump"):
        # Pydantic model
        return obj.model_dump()
    elif hasattr(obj, "__dict__"):
        # SQLAlchemy model or regular object
        data = obj.__dict__.copy()
        # Remove SQLAlchemy internal attributes
        data.pop("_sa_instance_state", None)
        # Convert all values to serializable types
        return {k: convert_value(v) for k, v in data.items()}
    else:
        # Fallback for other types
        return {}
