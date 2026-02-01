"""
Servicio de Quotation
"""
from sqlalchemy.orm import Session
from src.repositories.quotation_repository import QuotationRepository
from src.schemas.QuotationDetail import QuotationDetail
from fastapi import HTTPException, status


class QuotationService:
    """Servicio de lógica de negocio de Quotation"""
    
    def __init__(self, db: Session):
        self.repository = QuotationRepository(db)
    
    def get_quotation_by_id(self, quotation_id: str) -> QuotationDetail:
        """
        Obtiene cotización por ID
        
        Args:
            quotation_id: ID de la cotización
            
        Returns:
            QuotationDetail con datos de la cotización
            
        Raises:
            HTTPException: Si la cotización no existe
        """
        data = self.repository.get_by_id(quotation_id)
        
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cotización con ID {quotation_id} no encontrada"
            )
        
        return QuotationDetail(**data)
