from typing import Optional, Dict, Any

from core.enums.deal_type import DealType
from core.enums.deal_status import DealStatus
from core.models.rows.deal import DealRowOrm
from core.database import Database
from core.objects.rows.base_row import BaseRow

class DealRow(BaseRow):
    id: int
    is_listing: bool
    address: str
    name: str
    status: DealStatus
    type: DealType

    orm: Optional[DealRowOrm]

    @classmethod
    def from_orm(cls, deal: DealRowOrm):
        return cls(
            id=deal.id,
            is_listing=deal.is_listing,
            address=deal.address,
            name=deal.name,
            status=deal.status,
            type=deal.type,
            orm=deal
        )

    def to_dict(self):
        return {
            "id": self.id,
            "is_listing": self.is_listing,
            "address": self.address,
            "name": self.name,
            "status": self.status.value,
            "type": self.type.value,
        }

    @classmethod
    def query(cls, user_id: int, sort_by: str, ascending: bool, page_size: int, offset: int, include: Dict[str, Any]):
        db = Database()
        rows = db.query_with_user_and_conditions(DealRowOrm, user_id, sort_by, ascending, page_size, offset, include)
        return [cls.from_orm(row) for row in rows]
