"""
Excepciones personalizadas de la aplicación
"""
from .base_exceptions import (
    AppException,
    ScraperException,
    InvalidURLException,
    MissingParameterException,
    ScraperNotFoundError
)

__all__ = [
    "AppException",
    "ScraperException",
    "InvalidURLException",
    "MissingParameterException",
    "ScraperNotFoundError"
]
