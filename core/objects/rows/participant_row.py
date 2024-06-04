from pydantic import BaseModel
from typing import Optional, Dict, Any

from core.models.rows.property import PropertyRowOrm
from core.models.rows.person import PersonRowOrm
from core.database import Database
from core.objects.rows.base_row import BaseRow
from core.enums.participant_role import ParticipantRole
from core.models.entities.deal import DealOrm

class ParticipantRow(BaseRow):
    id: Optional[int]
    name: str
    role: ParticipantRole

    orm: Optional[PersonRowOrm]

    @classmethod
    def from_orm(cls, orm_object: DealOrm):
        return [
            cls(
                id=association.person.id,
                name=association.person.name,
                role=association.role,
                orm=orm_object
            )
            for association in orm_object.participants
        ]

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role.value
        }
