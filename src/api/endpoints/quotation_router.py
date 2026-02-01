"""
Endpoints de Quotation
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.services.quotation_service import QuotationService
from src.schemas.QuotationDetail import QuotationDetail

router = APIRouter(prefix="/api/v1/quotations", tags=["Quotations"])


@router.get("/{quotation_id}", response_model=QuotationDetail)
def get_quotation(
    quotation_id: str,
    db: Session = Depends(get_db)
) -> QuotationDetail:
    
    service = QuotationService(db)
    return service.get_quotation_by_id(quotation_id)
