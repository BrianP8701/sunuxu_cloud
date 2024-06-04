from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from core.models.rows.deal import DealRowOrm
from core.models.entities.deal import DealOrm
from core.database import Database
from core.objects.rows.property_row import PropertyRow
from core.enums import DealType, DealStatus
from core.objects.rows.user_row import UserRow
from core.objects.rows.property_row import PropertyRow
from core.objects.rows.participant_row import ParticipantRow
from core.objects.rows.deal_document_row import DealDocumentRow
from core.models.associations import UserDealAssociation
from core.objects.objects.base_object import BaseObject

class Deal(BaseObject):
    id: int
    is_listing: bool
    status: DealStatus
    type: DealType
    created: datetime
    updated: Optional[datetime]
    viewed: Optional[datetime]

    transaction_platform: Optional[str]
    notes: Optional[str]

    users: Optional[List[UserRow]]
    property: Optional[PropertyRow]
    participants: Optional[List[ParticipantRow]]
    documents: Optional[List[DealDocumentRow]]

    deal_orm: Optional[DealRowOrm]
    deal_details_orm: Optional[DealOrm]

    @classmethod
    async def read(cls, id: int):
        db = Database()
        deal = await db.read(DealRowOrm, id, eager_load=[
            'deal_details',
            'deal_details.property',
            'deal_details.participants',
            'deal_details.documents'
            ])

        users = [UserRow.from_orm(user) for user in deal.users]
        participants = [ParticipantRow.from_orm(participant) for participant in deal.deal_details.participants]
        documents = [DealDocumentRow.from_orm(document) for document in deal.deal_details.documents]

        return cls(
            id=deal.id,
            address=deal.address,
            buyer_name=deal.buyer_name,
            status=deal.status,
            type=deal.type,
            created=deal.created,
            updated=deal.updated,
            viewed=deal.viewed,
            transaction_platform=deal.deal_details.transaction_platform,
            notes=deal.deal_details.notes,
            users=users,
            property=PropertyRow.from_orm(deal.deal_details.property),
            participants=participants,
            documents=documents,
            deal_orm=deal,
            deal_details_orm=deal.deal_details,
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
            "notes": self.notes,
            "users": [user.to_dict() for user in self.users],
            "property": self.property.to_dict(),
            "participants": [participant.to_dict() for participant in self.participants],
            "documents": [document.to_dict() for document in self.documents]
        }

    async def update(self, **kwargs):
        db = Database()

        deal_updates = {}
        deal_detail_updates = {}

        for key, value in kwargs.items():
            if hasattr(DealRowOrm, key):
                deal_updates[key] = value
            if hasattr(DealOrm, key):
                deal_detail_updates[key] = value

        async with db.get_session() as session:
            if deal_updates:
                await db.update_fields(DealRowOrm, self.id, deal_updates, session)
            if deal_detail_updates:
                await db.update_fields(DealOrm, self.id, deal_detail_updates, session)

    @classmethod
    async def delete(cls, id: int):
        db = Database()
        deal = await db.read(DealRowOrm, id)

        await db.delete(deal)

    async def create(self):
        db = Database()

        deal = self._create_new_deal_orm()
        deal_details = self._create_new_deal_details_orm()

        async with db.get_session() as session:
            deal = await db.create(deal, session)
            deal_details = await db.create(deal_details, session)

        self.id = deal.id
        self.deal_orm = deal
        self.deal_details_orm = deal_details

    def _create_new_deal_orm(self):
        deal_data = {
            'is_listing': self.is_listing,
            'address': self.address,
            'name': self.name,
            'status': self.status,
            'type': self.type,
            'created': self.created,
            'updated': self.updated,
            'viewed': self.viewed,
            'user_ids': self.user_ids
        }
        return DealRowOrm(**deal_data)

    def _create_new_deal_details_orm(self, propert_id, person_id):
        """ 
        Create a new deal details object, retrieving either the corresponing person or property. 
        
        """
        deal_details_data = {
            'transaction_platform': self.transaction_platform,
            'notes': self.notes,
        }
        
        user_associations = [UserDealAssociation(user_id=user_id, deal_id=self.id) for user_id in self.user_ids]
        deal_details_data['users'] = user_associations
        
        return DealOrm(**deal_details_data)
