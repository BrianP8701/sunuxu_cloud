from pydantic import BaseModel
from typing import Optional, Dict, Any

from core.models.rows.property import PropertyRowOrm
from core.database import Database
from core.objects.rows.base_row import BaseRow

class PropertyRow(BaseRow):
    id: Optional[int]
    address: str
    mls_number: Optional[str]
    type: str
    active: bool

    orm: Optional[PropertyRowOrm]

    @classmethod
    def from_orm(cls, property: PropertyRowOrm):
        return cls(
            id=property.id,
            address=property.address,
            type=property.type,
            active=property.active,
            orm=property
        )

    def to_dict(self):
        return {
            "id": self.id,
            "address": self.address,
            "mls_number": self.mls_number,
            "type": self.type.value,
            "active": self.active,
        }

    @classmethod
    def query(cls, user_id: int, sort_by: str, ascending: bool, page_size: int, offset: int, include: Dict[str, Any]):
        db = Database()
        rows = db.query_with_user_and_conditions(PropertyRowOrm, user_id, sort_by, ascending, page_size, offset, include)
        return [cls.from_orm(row) for row in rows]
