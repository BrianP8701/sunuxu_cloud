from typing import Dict

from core.database import Database
from core.enums.deal_document_status import DealDocumentStatus
from core.models.deal_document import DealDocumentModel
from core.objects.rows.base_row import BaseRow


class DealDocumentRow(BaseRow):
    id: int
    name: str
    url: str
    status: DealDocumentStatus

    participants: Dict[str, str]  # Person name -> Status

    orm: DealDocumentModel

    @classmethod
    async def query(cls, deal_id: int):
        """Get all deal documents for a deal"""
        db = Database()
        sql = """
        SELECT dd.*
        FROM deal_documents dd
        WHERE dd.deal_id = :deal_id
        """
        params = {"deal_id": deal_id}
        result = await db.execute_raw_sql(sql, params)
        return [cls.from_model(DealDocumentModel(**row)) for row in result]

    @classmethod
    def from_model(cls, orm: DealDocumentModel):
        participants = {
            assoc.participant.name: assoc.status for assoc in orm.participants
        }
        return cls(
            id=orm.id,
            name=orm.name,
            participants=participants,
            url=orm.url,
            status=orm.status,
            orm=orm,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "participants": self.participants,
            "status": self.status,
            "url": self.url,
        }
