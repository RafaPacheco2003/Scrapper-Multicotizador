"""
Aplicación FastAPI principal
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from src.core.config import settings
from src.api.endpoints import router
from src.api.endpoints.heald_router import router as health_router
from src.api.endpoints.quotation_router import router as quotation_router  


# Configurar logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description="API para web scraping escalable y modular",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# Incluir routers
app.include_router(router)
app.include_router(health_router)
app.include_router(quotation_router)


if __name__ == "__main__":
    import uvicorn
    logger.info(f"Iniciando {settings.APP_NAME} en {settings.HOST}:{settings.PORT}")
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
