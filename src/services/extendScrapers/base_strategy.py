"""Estrategia base abstracta para scrapers"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from src.schemas.response import SuccessResponse

_strategies: Dict[str, 'ScraperStrategy'] = {}


class ScraperStrategy(ABC):
    """Estrategia abstracta - Define el contrato de scraping"""
    
    def __init__(self, scraper_name: str, base_url: str, scraper):
        self.scraper_name = scraper_name
        self.base_url = base_url
        self.scraper = scraper
        # Auto-registro
        _strategies[scraper_name.lower()] = self
    
    @abstractmethod
    def prepare_url(self, params: Dict[str, Any]) -> Optional[str]:
        """Cada estrategia define cómo construir su URL"""
        pass
    
    async def execute(self, params: Dict[str, Any], extract_data: bool = True) -> SuccessResponse:
        """Ejecuta el scraping: prepara URL y extrae datos"""
        url = self.prepare_url(params)
        scraped_data = await self.scraper.scrape(url) if extract_data else None
        
        return SuccessResponse(
            message="Completado",
            data={
                "scraper_name": self.scraper_name,
                "url": url or self.base_url,
                "scraped_data": scraped_data
            }
        )
    
    @staticmethod
    def get(name: str) -> Optional['ScraperStrategy']:
        """Obtiene estrategia por nombre"""
        return _strategies.get(name.lower())
    
    @staticmethod
    def all() -> Dict[str, 'ScraperStrategy']:
        """Retorna todas las estrategias"""
        return _strategies.copy()
