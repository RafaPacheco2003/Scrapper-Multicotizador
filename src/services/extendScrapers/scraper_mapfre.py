from typing import Dict, Any, Optional
from src.utils import URLBuilder
from . import ScraperStrategy


class MapfreScraperStrategy(ScraperStrategy):
    """Estrategia para Mapfre - USA URLBuilder con parámetros"""
    
    def __init__(self):
        self.scraper_name = "mapfre"
        self.base_url = "https://cotizadorautos.mapfre.com.mx"
    
    def prepare_url(self, params: Dict[str, Any]) -> Optional[str]:
        """Construye URL con URLBuilder"""
        builder = URLBuilder(self.scraper_name)
        return builder.build(params)
    
    def get_scraper_name(self) -> str:
        return self.scraper_name
    
    def get_base_url(self) -> str:
        return self.base_url
