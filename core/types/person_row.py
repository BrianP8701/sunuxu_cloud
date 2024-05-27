from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

from core.models.person import PersonOrm
from core.enums.person_type import PersonType
from core.utils.strings import assemble_name

class PersonRow(BaseModel):
    id: Optional[int]
    name: str
    email: Optional[EmailStr]
    phone: Optional[str]
    type: PersonType
    custom_type: Optional[str]
    active: bool
    unread: bool
    tags: Optional[List[str]]
    last_activity: Optional[datetime]
    last_messaged: Optional[datetime]
    temperature: Optional[int]

    orm: Optional[PersonOrm]

    @classmethod
    def from_orm(cls, person: PersonOrm):
        return cls(
            id=person.id,
            name=assemble_name(person.first_name, person.middle_name, person.last_name),
            email=person.email,
            phone=person.phone,
            type=person.type,
            custom_type=person.custom_type,
            active=person.active,
            unread=person.unread,
            tags=person.tags,
            last_activity=person.last_activity,
            last_messaged=person.last_messaged,
            temperature=person.temperature,
            orm=person
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "type": self.type.value,
            "custom_type": self.custom_type,
            "active": self.active,
            "unread": self.unread,
            "tags": self.tags,
            "last_activity": self.last_activity.isoformat() if self.last_activity else None,
            "last_messaged": self.last_messaged.isoformat() if self.last_messaged else None,
            "temperature": self.temperature
        }
