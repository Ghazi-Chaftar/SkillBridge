"""
Rate limiting functionality for the API.

This module provides:
- limiter: A configured Limiter instance for controlling API request rates
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
