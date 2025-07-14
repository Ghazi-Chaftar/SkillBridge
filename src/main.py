"""Main entry point for the FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database.core import Base, engine

from .api import register_routes
from .logging import LogLevels, configure_logging

configure_logging(LogLevels.info)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
""" 
Only uncomment the following line if you want to create the database tables automatically.
With Alembic migrations, this should be commented out to let Alembic handle schema changes.
"""
Base.metadata.create_all(bind=engine)


register_routes(app)
