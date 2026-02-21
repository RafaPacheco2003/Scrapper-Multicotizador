from typing import Any, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text


class QuotationRepository:
    
    def __init__(self, db: Session):
     
        self.db = db
    
    def get_by_id(self, quotation_id: str) -> Optional[Dict[str, Any]]:
        
        query = text("""
            SELECT 
                q.id          AS quotation_id,
                b.name        AS branch_name,
                m.name        AS model_name,
                d.description AS description,
                q.year
            FROM "Quotation" q
            INNER JOIN "Branch" b
                ON q."branchId" = b.id
            INNER JOIN "Model" m
                ON q."modelId" = m.id
            INNER JOIN "Description" d
                ON q."descriptionId" = d.id
            WHERE q.id = :quotation_id
        """)
        
        result = self.db.execute(query, {"quotation_id": quotation_id})
        row = result.fetchone()
        
        if not row:
            return None
        
        return {
            "quotation_id": row.quotation_id,
            "branch_name": row.branch_name,
            "model_name": row.model_name,
            "description": row.description,
            "year": row.year
        }