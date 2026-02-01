"""
Constructor de URLs dinámico y escalable
Permite construir URLs con parámetros variables
"""
from typing import Dict, Optional
from src.core.scrapers_config import get_scraper_config
from src.exceptions import (
    MissingParameterException,
    InvalidURLException,
    ScraperNotFoundError
)


class URLBuilder:
    """
    Constructor de URLs para diferentes scrapers
    
    Ejemplo:
        builder = URLBuilder("mapfre")
        url = builder.build({
            "marca": "dodge",
            "submarca": "dodge-attitude",
            "year": 2024,
            "codigo": 97289,
            "fecha": "2003-10-16",
            "genero": "m"
        })
    """
    
    def __init__(self, scraper_name: str):
        """
        Inicializar con el nombre del scraper
        
        Args:
            scraper_name: Nombre del scraper (mapfre, seguros_xyz, etc.)
            
        Raises:
            ScraperNotFoundError: Si el scraper no existe
        """
        self.scraper_name = scraper_name.lower()
        self.config = get_scraper_config(self.scraper_name)
        
        if not self.config:
            raise ScraperNotFoundError(scraper_name)
    
    def build(self, params: Dict[str, any]) -> str:
        """
        Construir URL con los parámetros proporcionados
        
        Args:
            params: Diccionario con los parámetros
            
        Returns:
            URL construida
            
        Raises:
            MissingParameterException: Si falta algún parámetro requerido
            InvalidURLException: Si la URL resultante es inválida
        """
        # Validar parámetros requeridos
        self._validate_params(params)
        
        # Construir URL
        url = self._build_url(params)
        
        # Validar URL
        self._validate_url(url)
        
        return url
    
    def _validate_params(self, params: Dict[str, any]) -> None:
        """Validar que todos los parámetros requeridos estén presentes"""
        for required_param in self.config.required_params:
            if required_param not in params:
                raise MissingParameterException(required_param, self.scraper_name)
    
    def _build_url(self, params: Dict[str, any]) -> str:
        """Construir la URL usando el template"""
        try:
            # Convertir valores a string
            string_params = {k: str(v) for k, v in params.items()}
            
            # Reemplazar placeholders en el template
            url = self.config.url_template.format(**string_params)
            
            return url
        except KeyError as e:
            raise InvalidURLException(
                f"Parámetro no válido en URL template: {str(e)}"
            )
    
    def _validate_url(self, url: str) -> None:
        """Validar que la URL sea correcta"""
        if not url.startswith(("http://", "https://")):
            raise InvalidURLException(f"URL no válida: {url}")
        
        if "{" in url or "}" in url:
            raise InvalidURLException(
                f"URL contiene placeholders sin reemplazar: {url}"
            )
    
    @property
    def required_params(self) -> list:
        """Obtener parámetros requeridos"""
        return self.config.required_params
    
    @property
    def optional_params(self) -> list:
        """Obtener parámetros opcionales"""
        return self.config.optional_params
    
    def get_template(self) -> str:
        """Obtener el template de URL"""
        return self.config.url_template
