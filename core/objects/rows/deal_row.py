from typing import Any, Dict, Optional

from core.database import Database
from core.enums.deal_status import DealStatus
from core.enums.deal_type import DealType
from core.models.rows.deal import DealRowModel
from core.objects.rows.base_row import BaseRow


class DealRow(BaseRow):
    id: int
    is_listing: bool
    address: str
    name: str
    status: DealStatus
    type: DealType

    orm: Optional[DealRowModel]

    @classmethod
    def query(
        cls,
        user_id: int,
        sort_by: str,
        ascending: bool,
        page_size: int,
        offset: int,
        include: Dict[str, Any],
    ):
        """Filter and paginate deal rows"""
        db = Database()
        rows = db.query_with_user_and_conditions(
            DealRowModel, user_id, sort_by, ascending, page_size, offset, include
        )
        return [cls.from_model(row) for row in rows]

    @classmethod
    def from_model(cls, orm: DealRowModel):
        return cls(
            id=orm.id,
            is_listing=orm.is_listing,
            address=orm.address,
            name=orm.name,
            status=orm.status,
            type=orm.type,
            orm=orm,
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
