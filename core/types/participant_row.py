from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from core.models.participant import ParticipantOrm
from core.enums.participant_role import ParticipantRole
from core.utils.strings import assemble_name

class ParticipantRow(BaseModel):
    id: Optional[int]
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    role: ParticipantRole
    custom_role: Optional[str]

    orm: Optional[ParticipantOrm]

    @classmethod
    def from_orm(cls, participant: ParticipantOrm):
        return cls(
            id=participant.id,
            name=assemble_name(participant.person.first_name, participant.person.middle_name, participant.person.last_name),
            email=participant.person.email,
            phone=participant.person.phone,
            role=participant.role,
            custom_role=participant.custom_role,
            orm=participant
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "role": self.role,
            "custom_role": self.custom_role
        }