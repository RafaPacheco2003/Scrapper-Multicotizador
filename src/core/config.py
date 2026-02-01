"""
Configuración centralizada de la aplicación
"""
from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # App
    APP_NAME: str = "Web Scraping Backend"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "API para web scraping escalable y modular"
    DEBUG: bool = True
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]
    
    
    #Database
    DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Obtener configuración (cached)"""
    return Settings()


settings = get_settings()
