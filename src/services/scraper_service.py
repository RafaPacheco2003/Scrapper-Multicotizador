"""
Servicio de scraping - Orquestador principal
"""
import logging
from typing import Dict, Any, Optional
from src.utils import URLBuilder
from src.exceptions import ScraperException
from scrapers.implementations.mapfre_scraper import mapfre_scraper

logger = logging.getLogger(__name__)


class ScraperService:
    """
    Servicio principal de scraping
    Orquesta la construcción de URLs y ejecución de scrapers
    """
    
    def __init__(self):
        """Inicializar el servicio"""
        self.logger = logging.getLogger(self.__class__.__name__)
        self.scrapers = {
            "mapfre": mapfre_scraper
            # Aquí irán más scrapers
        }
    
    async def scrape(
        self,
        scraper_name: str,
        params: Dict[str, Any],
        extract_data: bool = True
    ) -> Dict[str, Any]:
        """
        Realizar scraping
        
        Args:
            scraper_name: Nombre del scraper
            params: Parámetros para la URL
            extract_data: Si se deben extraer datos
            
        Returns:
            Diccionario con resultado del scraping
        """
        try:
            # Construir URL
            self.logger.info(f"Construyendo URL para scraper: {scraper_name}")
            builder = URLBuilder(scraper_name)
            url = builder.build(params)
            self.logger.info(f"URL construida: {url}")
            
            # Obtener el scraper
            scraper = self.scrapers.get(scraper_name.lower())
            if not scraper:
                return {
                    "success": False,
                    "message": f"Scraper '{scraper_name}' no configurado",
                    "scraper_name": scraper_name,
                    "url": url,
                    "data": None,
                    "error": f"Scraper '{scraper_name}' no encontrado"
                }
            
            # Realizar scraping si se solicita
            if extract_data:
                self.logger.info(f"Iniciando extracción de datos...")
                scraped_data = await scraper.scrape(url)
            else:
                scraped_data = None
            
            return {
                "success": True,
                "message": "Scraping completado exitosamente" if extract_data else "URL generada correctamente",
                "scraper_name": scraper_name,
                "url": url,
                "data": scraped_data
            }
            
        except ScraperException as e:
            self.logger.error(f"Error de scraping: {e.message}")
            return {
                "success": False,
                "message": "Error en scraping",
                "scraper_name": scraper_name,
                "url": None,
                "data": None,
                "error": e.message
            }
        except Exception as e:
            self.logger.error(f"Error inesperado: {str(e)}")
            return {
                "success": False,
                "message": "Error inesperado",
                "scraper_name": scraper_name,
                "url": None,
                "data": None,
                "error": str(e)
            }


# Instancia singleton
scraper_service = ScraperService()
