from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

from core.enums.deal_type import DealType
from core.enums.deal_status import DealStatus
from core.models.user import UserOrm
from core.models.deal import DealOrm
from core.utils.strings import assemble_name, assemble_address
from core.enums.participant_role import ParticipantRole

class DealRow(BaseModel):
    id: Optional[int]
    address: Optional[str]
    buyers: Optional[str]
    status: DealStatus
    type: DealType
    users: List[UserOrm]

    orm: Optional[DealOrm]

    @classmethod
    def from_orm(cls, deal: DealOrm):
        buyers = []

        for participant in deal.participants:
            if participant.role == ParticipantRole.BUYER or participant.role == ParticipantRole.TENANT:
                buyers.append(assemble_name(participant.person.first_name, participant.person.middle_name, participant.person.last_name))

        return cls(
            id=deal.id,
            address=assemble_address(deal.property.street_number, deal.property.street_name, deal.property.street_suffix, deal.property.city, deal.property.state, deal.property.zip_code),
            buyers=buyers,
            status=deal.status,
            type=deal.type,
            users=deal.users,
            orm=deal
        )

    def to_dict(self):
        return {
            "id": self.id,
            "address": self.address,
            "buyers": self.buyers,
            "status": self.status.value,
            "type": self.type.value,
            "users": [user.to_dict() for user in self.users],
        }
