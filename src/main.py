"""Main entry point for the FastAPI application."""

from fastapi import FastAPI

from src.database.core import Base, engine

from .api import register_routes
from .logging import LogLevels, configure_logging
from fastapi.middleware.cors import CORSMiddleware

configure_logging(LogLevels.info)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; adjust in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)
""" Only uncomment the following line if you want to create the database tables automatically. """
Base.metadata.create_all(bind=engine)


register_routes(app)
