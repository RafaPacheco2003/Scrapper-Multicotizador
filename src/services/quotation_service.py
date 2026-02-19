"""
Servicio de Quotation
"""
from sqlalchemy.orm import Session
from src.repositories.quotation_repository import QuotationRepository
from src.schemas.QuotationDetail import QuotationDetail
from typing import Optional


class QuotationService:
    """Servicio de lógica de negocio de Quotation"""
    
    def __init__(self, db: Session):
        """
        Constructor del servicio
        
        Args:
            db: Sesión de base de datos
        """
        self.repository = QuotationRepository(db)
    
    def get_quotation_by_id(self, quotation_id: str) -> Optional[QuotationDetail]:
        """
        Obtiene cotización por ID
        
        Args:
            quotation_id: ID de la cotización
            
        Returns:
            QuotationDetail o None si no existe
        """
        data = self.repository.get_by_id(quotation_id)
        
        if not data:
            return None
        
        return QuotationDetail(**data)
