"""
Schemas de respuesta
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class ScrapeResponse(BaseModel):
    """Respuesta de scraping"""
    
    success: bool = Field(
        ...,
        description="Indica si el scraping fue exitoso"
    )
    
    message: str = Field(
        ...,
        description="Mensaje descriptivo"
    )
    
    scraper_name: str = Field(
        ...,
        description="Nombre del scraper usado"
    )
    
    url: Optional[str] = Field(
        None,
        description="URL generada"
    )
    
    data: Optional[Dict[str, Any]] = Field(
        None,
        description="Datos extraídos de la página"
    )
    
    error: Optional[str] = Field(
        None,
        description="Mensaje de error si ocurrió alguno"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp de la respuesta"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Scraping completado",
                "scraper_name": "mapfre",
                "url": "https://cotizadorautos.mapfre.com.mx/rates/car/dodge/dodge-attitude/2024/97289/2003-10-16/m",
                "data": {
                    "precio": "$5,999",
                    "cobertura": "Completa"
                },
                "error": None,
                "timestamp": "2025-01-27T10:30:00"
            }
        }
