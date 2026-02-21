from typing import Dict, Any, Optional
from scrapers.implementations.hdi_scraper import hdi_scraper
from .base_strategy import ScraperStrategy


class HdiScraperStrategy(ScraperStrategy):
    """Estrategia HDI: usa URL estática"""
    
    def __init__(self):
        super().__init__("hdi", "https://www.hdiconnect.com.mx/productos/autos", hdi_scraper)
    
    def prepare_url(self, params: Dict[str, Any]) -> Optional[str]:
        return self.base_url


# Instancia única que se auto-registra
HdiScraperStrategy()
