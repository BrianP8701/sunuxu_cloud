from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any

from core.models.rows.person import PersonRowOrm
from core.database import Database
from core.objects.rows.base_row import BaseRow

class PersonRow(BaseRow):
    id: Optional[int]
    name: str
    email: Optional[EmailStr]
    phone: Optional[str]
    type: str
    active: bool

    orm: Optional[PersonRowOrm]

    @classmethod
    def from_orm(cls, person: PersonRowOrm):
        return cls(
            id=person.id,
            name=person.name,
            email=person.email,
            phone=person.phone,
            type=person.custom_type if person.custom_type else person.type,
            active=person.active,
            orm=person
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

    @classmethod
    def query(cls, user_id: int, sort_by: str, ascending: bool, page_size: int, offset: int, include: Dict[str, Any]):
        db = Database()
        rows = db.query_with_user_and_conditions(PersonRowOrm, user_id, sort_by, ascending, page_size, offset, include)
        return [cls.from_orm(row) for row in rows]
