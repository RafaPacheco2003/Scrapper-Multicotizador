"""
Endpoint para verificar estado de la base de datos
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.core.database import get_db
from src.core.config import settings

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/database")
def check_database(db: Session = Depends(get_db)):
    """
    Verifica la conexión a la base de datos
    
    Returns:
        dict: Estado de la conexión
    """
    try:
        db.execute(text("SELECT 1"))
        
        return {
            "status": "connected",
            "message": "Base de datos conectada correctamente",
            "database": "PostgreSQL"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error de conexión a base de datos: {str(e)}"
        )


# Endpoint root
@router.get("/", tags=["Root"], include_in_schema=False)
async def root():
    """Información de la API"""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health/database"
    }