from typing import Any, Dict, Optional

from pydantic import BaseModel

from core.database import Database
from core.models.rows.property import PropertyRowModel
from core.objects.rows.base_row import BaseRow


class PropertyRow(BaseRow):
    id: Optional[int]
    address: str
    mls_number: Optional[str]
    type: str
    active: bool

    orm: Optional[PropertyRowModel]

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
        """Filter and paginate property rows"""
        db = Database()
        rows = db.query_with_user_and_conditions(
            PropertyRowModel, user_id, sort_by, ascending, page_size, offset, include
        )
        return [cls.from_orm(row) for row in rows]

    @classmethod
    def from_orm(cls, orm: PropertyRowModel):
        return cls(
            id=orm.id, address=orm.address, type=orm.type, active=orm.active, orm=orm
        )

    def to_dict(self):
        return {
            "id": self.id,
            "address": self.address,
            "mls_number": self.mls_number,
            "type": self.type.value,
            "active": self.active,
        }
