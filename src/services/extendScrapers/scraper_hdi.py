from typing import Dict, Any, Optional
from . import ScraperStrategy


class HdiScraperStrategy(ScraperStrategy):
    """Estrategia para HDI - NO usa URLBuilder, solo base_url"""
    
    def __init__(self):
        self.scraper_name = "hdi"
        self.base_url = "https://www.hdiconnect.com.mx/productos/autos"
    
    def prepare_url(self, params: Dict[str, Any]) -> Optional[str]:
        """HDI no necesita construir URL, usa base_url directamente"""
        return self.base_url  # Retornar base_url en lugar de None
    
    def get_scraper_name(self) -> str:
        return self.scraper_name
    
    def get_base_url(self) -> str:
        return self.base_url
