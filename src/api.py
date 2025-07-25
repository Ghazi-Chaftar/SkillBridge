"""API module for FastAPI application."""

from fastapi import FastAPI

from src.auth.controller import router as auth_router
from src.profiles.controller import router as profiles_router
from src.users.controller import router as users_router


def register_routes(app: FastAPI):
    app.include_router(profiles_router)
    app.include_router(auth_router)
    app.include_router(users_router)
