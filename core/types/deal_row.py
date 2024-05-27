from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

from core.enums.transaction_type import DealType
from core.enums.transaction_status import DealStatus
from core.models.deal_details import DealDetailsOrm
from core.models.user import UserOrm
from core.models.deal import DealOrm

class DealRow(BaseModel):
    id: Optional[int]
    address: Optional[str]
    buyer_name: Optional[str]
    status: DealStatus
    type: DealType
    users: List[UserOrm]

    orm: Optional[DealOrm]

    @classmethod
    def from_orm(cls, deal: DealOrm):
        return cls(
            id=deal.id,
            address=deal.address,
            buyer_name=deal.buyer_name,
            status=deal.status,
            type=deal.type,
            users=deal.users,
            orm=deal
        )

    def to_dict(self):
        return {
            "id": self.id,
            "address": self.address,
            "buyer_name": self.buyer_name,
            "status": self.status.value,
            "type": self.type.value,
            "users": [user.to_dict() for user in self.users],
        }
