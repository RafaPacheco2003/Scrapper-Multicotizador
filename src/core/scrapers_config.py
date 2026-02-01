"""
Configuración de URLs y parámetros de scrapers
Permite agregar múltiples URLs con patrones diferentes
"""
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ScraperConfig:
    """Configuración de un scraper individual"""
    
    name: str                           # Nombre del scraper (mapfre, seguros_xx, etc.)
    url_template: str                   # URL con placeholders {param}
    base_url: str                       # URL base sin parámetros
    required_params: List[str]          # Parámetros requeridos
    optional_params: List[str] = None   # Parámetros opcionales
    headers: Dict[str, str] = None      # Headers personalizados
    
    def __post_init__(self):
        if self.optional_params is None:
            self.optional_params = []
        if self.headers is None:
            self.headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }


# ============================================================================
# CONFIGURACIÓN DE SCRAPERS
# Agrega aquí nuevas URLs manteniendo la estructura escalable
# ============================================================================

SCRAPERS_CONFIG: Dict[str, ScraperConfig] = {
    "mapfre": ScraperConfig(
        name="mapfre",
        url_template="https://cotizadorautos.mapfre.com.mx/rates/car/{marca}/{submarca}/{year}/{codigo}/{fecha}/{genero}",
        base_url="https://cotizadorautos.mapfre.com.mx/rates/car",
        required_params=["marca", "submarca", "year", "codigo", "fecha", "genero"],
        optional_params=[]
    ),
    
    # Ejemplo de otra estructura (cuando agegues más)
    # "seguros_xyz": ScraperConfig(
    #     name="seguros_xyz",
    #     url_template="https://ejemplo.com/cotizar?brand={marca}&model={modelo}&year={year}",
    #     base_url="https://ejemplo.com/cotizar",
    #     required_params=["marca", "modelo", "year"],
    #     optional_params=["cilindros", "combustible"]
    # ),
    
    # "seguros_abc": ScraperConfig(
    #     name="seguros_abc",
    #     url_template="https://otro-sitio.com/quote/{year}/{marca}/{model}/{engine}",
    #     base_url="https://otro-sitio.com/quote",
    #     required_params=["year", "marca", "model", "engine"],
    #     optional_params=[]
    # ),
}


def get_scraper_config(scraper_name: str) -> Optional[ScraperConfig]:
    """Obtener configuración de un scraper por nombre"""
    return SCRAPERS_CONFIG.get(scraper_name.lower())


def get_available_scrapers() -> List[str]:
    """Obtener lista de scrapers disponibles"""
    return list(SCRAPERS_CONFIG.keys())


def register_scraper(config: ScraperConfig) -> None:
    """Registrar un nuevo scraper en tiempo de ejecución"""
    SCRAPERS_CONFIG[config.name.lower()] = config
