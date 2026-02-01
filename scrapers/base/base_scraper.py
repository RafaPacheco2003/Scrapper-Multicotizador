"""
Clase base para todos los scrapers
Implementa la interfaz que deben seguir todos los scrapers
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging


class BaseScraper(ABC):
    """
    Clase base abstracta para todos los scrapers
    Define la interfaz que deben implementar todos los scrapers
    """
    
    def __init__(self, name: str):
        """
        Inicializar el scraper
        
        Args:
            name: Nombre del scraper
        """
        self.name = name
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    async def scrape(self, url: str) -> Dict[str, Any]:
        """
        Realizar el scraping de la URL
        
        Args:
            url: URL a scrapear
            
        Returns:
            Diccionario con datos extraídos
        """
        pass
    
    @abstractmethod
    def parse_response(self, html: str) -> Dict[str, Any]:
        """
        Parsear la respuesta HTML y extraer datos
        
        Args:
            html: Contenido HTML
            
        Returns:
            Datos extraídos
        """
        pass
    
    def get_name(self) -> str:
        """Obtener nombre del scraper"""
        return self.name
