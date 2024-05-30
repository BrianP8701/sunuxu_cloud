from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from core.models.deal import DealOrm
from core.models.deal_details import DealDetailsOrm
from core.database import Database
from core.types.property_row import PropertyRow
from core.enums import DealType, DealStatus
from core.types.user_row import UserRow
from core.types.property_row import PropertyRow
from core.types.participant_row import ParticipantRow

class Deal(BaseModel):
    id: int
    status: DealStatus
    type: DealType
    created: datetime
    updated: Optional[datetime]
    viewed: Optional[datetime]

    transaction_platform: Optional[str]
    transaction_platform_data: Optional[Dict[str, Any]]
    checklist: Optional[Dict[str, Optional[int]]]
    notes: Optional[str]
    description: Optional[str]

    deal_orm: Optional[DealOrm]
    deal_details_orm: Optional[DealDetailsOrm]
    users: Optional[List[UserRow]]
    property: Optional[PropertyRow]
    participants: Optional[List[ParticipantRow]]

    @classmethod
    async def get(cls, id: int):
        db = Database()
        deal = await db.get(DealOrm, id)
        deal_details = await db.get(DealDetailsOrm, id)

        users = [UserRow.from_orm(user) for user in deal.users]
        participants = [ParticipantRow.from_orm(participant) for participant in deal.participants]

        return cls(
            id=deal.id,
            address=deal.address,
            buyer_name=deal.buyer_name,
            status=deal.status,
            type=deal.type,
            created=deal.created,
            updated=deal.updated,
            viewed=deal.viewed,
            transaction_platform=deal_details.transaction_platform,
            transaction_platform_data=deal_details.transaction_platform_data,
            checklist=deal_details.checklist,
            notes=deal_details.notes,
            description=deal_details.description,
            deal_orm=deal,
            deal_details_orm=deal_details,
            users=users,
            property=PropertyRow.from_orm(deal_details.property),
            participants=participants
        )

    def to_dict(self):
        return {
            "id": self.id,
            "address": self.address,
            "buyer_name": self.buyer_name,
            "status": self.status.value,
            "type": self.type.value,
            "created": self.created.isoformat() if self.created else None,
            "updated": self.updated.isoformat() if self.updated else None,
            "viewed": self.viewed.isoformat() if self.viewed else None,
            "transaction_platform": self.transaction_platform,
            "transaction_platform_data": self.transaction_platform_data,
            "checklist": self.checklist,
            "notes": self.notes,
            "description": self.description,
            "users": [user.to_dict() for user in self.users],
            "properties": [property.to_dict() for property in self.properties]
        }

    async def insert(self):
        db = Database()

        deal = self._assemble_deal_orm()
        deal_details = self._assemble_deal_details_orm()

        async with db.get_session() as session:
            deal = await db.insert(deal, session)
            deal_details = await db.insert(deal_details, session)

        self.id = deal.id
        self.deal_orm = deal
        self.deal_details_orm = deal_details

    async def update(self, **kwargs):
        db = Database()
        deal = self.deal_orm
        deal_details = self.deal_details_orm

        deal_changed = False
        deal_details_changed = False
        for key, value in kwargs.items():
            if hasattr(deal, key):
                setattr(deal, key, value)
                deal_changed = True
            if hasattr(deal_details, key):
                setattr(deal_details, key, value)
                deal_details_changed = True

        async with db.get_session() as session:
            if deal_changed:
                await db.update(deal, session)
            if deal_details_changed:
                await db.update(deal_details, session)

    @classmethod
    async def delete(cls, id: int):
        db = Database()
        deal = await db.get(DealOrm, id)

        await db.delete(deal)

    def _assemble_deal_orm(self):
        deal_data = {
            'address': self.address,
            'buyer_name': self.buyer_name,
            'status': self.status,
            'type': self.type,
            'created': self.created,
            'updated': self.updated,
            'viewed': self.viewed
        }
        return DealOrm(**deal_data)

    def _assemble_deal_details_orm(self):
        deal_details_data = {
            'transaction_platform': self.transaction_platform,
            'transaction_platform_data': self.transaction_platform_data,
            'checklist': self.checklist,
            'notes': self.notes,
            'description': self.description
        }
        return DealDetailsOrm(**deal_details_data)
