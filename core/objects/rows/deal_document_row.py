from typing import Dict, Any

from core.models.deal_document import DealDocumentOrm
from core.objects.rows.base_row import BaseRow
from core.enums.deal_document_status import DealDocumentStatus

class DealDocumentRow(BaseRow):
    id: int
    name: str
    url: str
    status: DealDocumentStatus
    
    participants: Dict[str, str] # Person name -> Status

    orm: DealDocumentOrm

    @classmethod
    def from_orm(cls, deal_document: DealDocumentOrm):
        participants = {
            assoc.participant.name: assoc.status
            for assoc in deal_document.participants
        }
        return cls(
            id=deal_document.id,
            name=deal_document.name,
            participants=participants,
            url=deal_document.url,
            status=deal_document.status,
            orm=deal_document
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "participants": self.participants,
            "status": self.status,
            "url": self.url
        }
