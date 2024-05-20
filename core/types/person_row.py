from pydantic import BaseModel, Field
from typing import Optional, List

from core.database import Database
from core.models import PersonRowOrm
from core.enums.person_type import PersonType


class PersonRow(BaseModel):
    id: Optional[int] = None
    user_id: int
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    type: PersonType = Field(default=PersonType.UNKNOWN)
    custom_type: Optional[str] = None
    active: bool = Field(default=False)

    @classmethod
    def get(cls, person_id: int) -> "PersonRow":
        db = Database()
        person = db.get(
            PersonRowOrm,
            person_id,
            columns=[
                "id",
                "user_id",
                "name",
                "email",
                "phone",
                "type",
                "custom_type",
                "active",
            ],
        )
        return cls(**person.to_dict())

    @classmethod
    def batch_get(cls, person_ids: List[int]) -> List["PersonRow"]:
        db = Database()
        people = db.batch_query(
            PersonRowOrm,
            person_ids,
            columns=[
                "id",
                "user_id",
                "name",
                "email",
                "phone",
                "type",
                "custom_type",
                "active",
            ],
        )
        return [cls(**person.to_dict()) for person in people]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "type": self.type,
            "custom_type": self.custom_type,
            "active": self.active,
        }
