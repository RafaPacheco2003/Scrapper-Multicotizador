"""
Endpoints de Quotation
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.repositories.quotation_repository import QuotationRepository
from src.services.quotation_service import QuotationService
from src.schemas.QuotationDetail import QuotationDetail

router = APIRouter(prefix="/api/v1/quotations", tags=["Quotations"])


@router.get("/{quotation_id}", response_model=QuotationDetail)
def get_quotation(
    quotation_id: str,
    db: Session = Depends(get_db)
):

    repository = QuotationRepository(db)
    service = QuotationService(repository)
    quotation = service.get_quotation_by_id(quotation_id)
    
    if not quotation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cotización con ID {quotation_id} no encontrada"
        )
    
    return quotation
