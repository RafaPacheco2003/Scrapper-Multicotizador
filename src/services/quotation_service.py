"""
Servicio de Quotation
"""
from src.repositories.quotation_repository import QuotationRepository
from src.schemas.QuotationDetail import QuotationDetail
from typing import Optional


class QuotationService:
    """Servicio de lógica de negocio de Quotation"""

    def __init__(self, repository: QuotationRepository):
        """
        Constructor del servicio

        Args:
            repository: Repository de cotizaciones
        """
        self.repository = repository
    
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
