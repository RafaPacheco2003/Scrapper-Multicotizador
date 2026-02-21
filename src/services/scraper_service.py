"""Servicio de Scraping - Orquestador del patrón Strategy

Cumple Open/Closed:
- NO tiene diccionario hardcodeado
- Usa auto-registro de estrategias
- Para agregar scraper: solo crear nueva estrategia e importarla
"""
import logging
from typing import Dict, Any, Union
from src.services.extendScrapers.base_strategy import ScraperStrategy
from src.schemas.response import SuccessResponse, ErrorResponse
# Importar estrategias para que se auto-registren
from src.services.extendScrapers import scraper_mapfre, scraper_hdi


class ScraperService:
    """Context del patrón Strategy - Selecciona y ejecuta estrategias"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    async def scrape(self, scraper_name: str, params: Dict[str, Any], extract_data: bool = True) -> Union[SuccessResponse, ErrorResponse]:
        """Ejecuta scraping usando la estrategia correspondiente"""
        try:
            strategy = ScraperStrategy.get(scraper_name)
            
            if not strategy:
                available = list(ScraperStrategy.all().keys())
                return ErrorResponse(
                    message=f"Scraper '{scraper_name}' no encontrado",
                    error_code="SCRAPER_NOT_FOUND",
                    details={"available_scrapers": available}
                )
            
            self.logger.info(f"Ejecutando: {strategy.__class__.__name__}")
            return await strategy.execute(params, extract_data)
            
        except Exception as e:
            self.logger.error(f"Error ejecutando scraper: {str(e)}")
            return ErrorResponse(
                message="Error ejecutando scraper",
                error_code="SCRAPER_EXECUTION_ERROR",
                details={"error": str(e)}
            )


scraper_service = ScraperService()
