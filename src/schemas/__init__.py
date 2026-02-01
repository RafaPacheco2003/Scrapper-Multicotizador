"""
Schemas de validación con Pydantic
"""
from .request_schemas import ScrapeRequest
from .response_schemas import ScrapeResponse

__all__ = ["ScrapeRequest", "ScrapeResponse"]
