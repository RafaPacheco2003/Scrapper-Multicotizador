"""
Definición de excepciones personalizadas
"""


class AppException(Exception):
    """Excepción base de la aplicación"""
    
    def __init__(self, message: str, code: str = "INTERNAL_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class ScraperException(AppException):
    """Excepción relacionada con scraping"""
    
    def __init__(self, message: str, code: str = "SCRAPER_ERROR"):
        super().__init__(message, code)


class InvalidURLException(ScraperException):
    """URL inválida o mal formada"""
    
    def __init__(self, message: str):
        super().__init__(message, "INVALID_URL")


class MissingParameterException(ScraperException):
    """Parámetro requerido faltante"""
    
    def __init__(self, param_name: str, scraper_name: str):
        message = f"Parámetro requerido '{param_name}' faltante para scraper '{scraper_name}'"
        super().__init__(message, "MISSING_PARAMETER")


class ScraperNotFoundError(ScraperException):
    """Scraper no encontrado"""
    
    def __init__(self, scraper_name: str):
        available = "mapfre, seguros_xyz, seguros_abc"  # Se puede mejorar después
        message = f"Scraper '{scraper_name}' no encontrado. Disponibles: {available}"
        super().__init__(message, "SCRAPER_NOT_FOUND")
