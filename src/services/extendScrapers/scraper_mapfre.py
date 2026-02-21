from typing import Dict, Any, Optional
from src.utils import URLBuilder
from scrapers.implementations.mapfre_scraper import mapfre_scraper
from .base_strategy import ScraperStrategy


class MapfreScraperStrategy(ScraperStrategy):
    """Estrategia Mapfre: construye URL dinámica con parámetros"""
    
    def __init__(self):
        super().__init__("mapfre", "https://cotizadorautos.mapfre.com.mx", mapfre_scraper)
    
    def prepare_url(self, params: Dict[str, Any]) -> Optional[str]:
        builder = URLBuilder(self.scraper_name)
        return builder.build(params)


# Instancia única que se auto-registra
MapfreScraperStrategy()
