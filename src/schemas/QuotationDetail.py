


from pydantic import BaseModel


class QuotationDetail(BaseModel):
    """Schema de respuesta para detalles de cotización"""
    quotation_id: str
    branch_name: str
    model_name: str
    description: str
    year: int
    
    class Config:
        from_attributes = True