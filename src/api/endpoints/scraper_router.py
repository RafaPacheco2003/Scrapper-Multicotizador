"""
Rutas de scraping
"""
from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from src.schemas.request_schemas import ScrapeRequest
from src.schemas.response_schemas import ScrapeResponse
from src.services import ScraperService
from src.exceptions import AppException

router = APIRouter(prefix="/api/v1/scrapers", tags=["Scrapers"])
scraper_service = ScraperService()


@router.get(
    "/scrape/mapfre",
    response_model=ScrapeResponse,
    status_code=status.HTTP_200_OK,
    summary="Scraping Mapfre (Prueba)",
    description="Endpoint de prueba para Mapfre - Genera la URL y extrae datos"
)
async def scrape_mapfre() -> ScrapeResponse:
    """
    Endpoint GET para probar scraping de Mapfre
    
    Parámetros de ejemplo:
    - marca: dodge
    - submarca: dodge-attitude
    - year: 2024
    - codigo: 97289
    - fecha: 2003-10-16
    - genero: m
    """
    try:
        # Parámetros de prueba
        test_params = {
            "marca": "dodge",
            "submarca": "dodge-attitude",
            "year": 2024,
            "codigo": 97289,
            "fecha": "2003-10-16",
            "genero": "m"
        }
        
        # Realizar scraping CON extracción de datos
        result = await scraper_service.scrape(
            scraper_name="mapfre",
            params=test_params,
            extract_data=True  # Ahora extrae datos reales
        )
        
        # Convertir a response schema
        return ScrapeResponse(
            success=result["success"],
            message=result["message"],
            scraper_name=result["scraper_name"],
            url=result.get("url"),
            data=result.get("data"),
            error=result.get("error"),
            timestamp=datetime.now()
        )
        
    except AppException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(e)}"
        )


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Verifica el estado del servicio"
)
async def health_check():
    """Health check del servicio"""
    return {
        "status": "healthy",
        "service": "Web Scraping Backend",
        "timestamp": datetime.now().isoformat()
    }


@router.get(
    "/scrape/hdi",
    response_model=ScrapeResponse,
    status_code=status.HTTP_200_OK,
    summary="Scraping HDI",
    description="Endpoint para acceder a la página de HDI"
)
async def scrape_hdi() -> ScrapeResponse:
    """
    Endpoint GET para probar scraping de HDI
    
    Accede a: https://www.hdiconnect.com.mx/productos/autos
    """
    try:
        # Realizar scraping de HDI (sin parámetros, solo accede a la página)
        result = await scraper_service.scrape(
            scraper_name="hdi",
            params={},
            extract_data=True
        )
        
        # Convertir a response schema
        return ScrapeResponse(
            success=result["success"],
            message=result["message"],
            scraper_name=result["scraper_name"],
            url=result.get("url"),
            data=result.get("data"),
            error=result.get("error"),
            timestamp=datetime.now()
        )
        
    except AppException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(e)}"
        )
