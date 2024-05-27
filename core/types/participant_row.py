from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from core.models.participant import ParticipantOrm
from core.enums.participant_role import ParticipantRole

class ParticipantRow(BaseModel):
    id: Optional[int]
    deal_id: int
    role: ParticipantRole
    custom_role: Optional[str]

    orm: Optional[ParticipantOrm]

    @classmethod
    def from_orm(cls, participant: ParticipantOrm):
        return cls(
            id=participant.id,
            deal_id=participant.deal_id,
            role=participant.role,
            custom_role=participant.custom_role,
            orm=participant
        )