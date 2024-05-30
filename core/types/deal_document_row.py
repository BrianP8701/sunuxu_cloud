from pydantic import BaseModel
from typing import Optional, Dict

from core.models.deal_document import DealDocumentOrm

class DealDocumentRow(BaseModel):
    id: Optional[int]
    participants: Dict[str, str] # Person name -> Status

    orm: Optional[DealDocumentOrm]
