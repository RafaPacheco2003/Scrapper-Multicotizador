"""
Schemas de solicitud
"""
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class ScrapeRequest(BaseModel):
    """Solicitud de scraping"""
    
    scraper_name: str = Field(
        ...,
        description="Nombre del scraper a usar (mapfre, seguros_xyz, etc.)",
        examples=["mapfre"]
    )
    
    params: Dict[str, Any] = Field(
        ...,
        description="Parámetros para construir la URL",
        examples=[{
            "marca": "dodge",
            "submarca": "dodge-attitude",
            "year": 2024,
            "codigo": 97289,
            "fecha": "2003-10-16",
            "genero": "m"
        }]
    )
    
    extract_data: bool = Field(
        default=True,
        description="Si se debe extraer datos de la página (vs solo obtener la URL)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "scraper_name": "mapfre",
                "params": {
                    "marca": "dodge",
                    "submarca": "dodge-attitude",
                    "year": 2024,
                    "codigo": 97289,
                    "fecha": "2003-10-16",
                    "genero": "m"
                },
                "extract_data": True
            }
        }
