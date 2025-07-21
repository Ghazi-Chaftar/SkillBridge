"""This module provides authentication routes for the application."""

from fastapi import APIRouter, Request

from src.auth.model import LoginRequest

from ..database.core import DbSession
from ..rate_limiting import limiter
from ..utils import build_response
from . import service
from .model import RegisterUserRequest

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/")
@limiter.limit("5/hour")
async def register_user(request: Request, db: DbSession, register_user_request: RegisterUserRequest):
    service.register_user(db, register_user_request)
    return build_response(success=True, message="User registered successfully", status_code=201)


@router.post("/token")
async def login_for_access_token(form_data: LoginRequest, db: DbSession):
    token = service.login_for_access_token(form_data, db)
    return build_response(success=True, message="Login successful", data=token.model_dump(), status_code=200)
