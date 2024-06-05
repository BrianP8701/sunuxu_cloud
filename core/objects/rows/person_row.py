from typing import Any, Dict, Optional

from core.database import Database
from core.models.rows.person import PersonRowModel
from core.objects.rows.base_row import BaseRow


class PersonRow(BaseRow):
    id: Optional[int]
    name: str
    email: Optional[str]
    phone: Optional[str]
    type: str
    active: bool

    orm: Optional[PersonRowModel]

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
        """Filter and paginate person rows"""
        db = Database()
        rows = db.query_with_user_and_conditions(
            PersonRowModel, user_id, sort_by, ascending, page_size, offset, include
        )
        return [cls.from_orm(row) for row in rows]

    @classmethod
    def from_orm(cls, orm: PersonRowModel):
        return cls(
            id=orm.id,
            name=orm.name,
            email=orm.email,
            phone=orm.phone,
            type=orm.custom_type if orm.custom_type else orm.type,
            active=orm.active,
            orm=orm,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "type": self.type.value,
            "active": self.active,
        }
