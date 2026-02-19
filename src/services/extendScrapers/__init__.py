from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class ScraperStrategy(ABC):
    """Estrategia base para scrapers (Open/Closed Principle)"""
    
    @abstractmethod
    def prepare_url(self, params: Dict[str, Any]) -> Optional[str]:
        """Prepara la URL para el scraper"""
        pass
    
    @abstractmethod
    def get_scraper_name(self) -> str:
        """Retorna el nombre del scraper"""
        pass
    
    @abstractmethod
    def get_base_url(self) -> str:
        """Retorna la URL base del scraper"""
        pass
