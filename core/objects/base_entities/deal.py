from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from core.database import Database
from core.enums import DealStatus, DealType
from core.enums.deal_category import DealCategory
from core.models.associations import UserDealAssociation
from core.models.entities.deal import DealModel
from core.models.rows.deal import DealRowModel
from core.objects.base_entities.base_entity import BaseEntity
from core.objects.rows.deal_document_row import DealDocumentRow
from core.objects.rows.participant_row import ParticipantRow
from core.objects.rows.property_row import PropertyRow
from core.objects.rows.user_row import UserRow

if TYPE_CHECKING:
    from core.models.associations import (DealDocumentAssociation,
                                          DealParticipantAssociation,
                                          UserDealAssociation)
    from core.models.rows.person import PersonRowModel
    from core.models.rows.property import PropertyRowModel


class BaseDeal(BaseEntity):
    id: int

    category: DealCategory
    status: DealStatus
    type: DealType

    transaction_platform: Optional[str]
    notes: Optional[str]

    users: Optional[List[UserRow]]
    property: Optional[PropertyRow]
    participants: Optional[List[ParticipantRow]]
    documents: Optional[List[DealDocumentRow]]

    created: datetime
    updated: Optional[datetime]
    viewed: Optional[datetime]

    deal_orm: Optional[DealRowModel]
    deal_details_orm: Optional[DealModel]

    @classmethod
    async def create(cls, user_id: int, data: Dict[str, Any]):
        """
        Creates a new deal entry in the database.

        :param user_id:
            The ID of the user creating the deal.
        :param data:
            A dictionary containing the deal details:
            - 'category' (DealCategory): Indicates if the deal is a listing. Must be 'buy', 'sell', or 'dual'. (Required)
            - 'status' (DealStatus): The current status of the deal. (Required)
            - 'type' (DealType): The type of the deal (Buy, Sell, or Dual). (Required)
            - 'participants' (Dict[int, str]): Person IDs to participant roles. Required if category is 'buy'. (Conditional)
            - 'property_id' (int): ID of the property the deal is for. Required if category is 'sell' or 'dual'. (Conditional)
            - 'transaction_platform' (Optional[str]): The platform used for the transaction. (Optional)
            - 'notes' (Optional[str]): Additional notes regarding the deal. (Optional)
        """
        db = Database()

        # Validate category
        if data["category"] not in ["buy", "sell", "dual"]:
            raise ValueError(
                f'{data["category"]} is not a valid deal category. Must be sell, buy or dual.'
            )

        # Setting row name depending on if it is a Buy, Sell or Dual deal
        if data["category"] in ["dual", "sell"]:
            property_id = data["property_id"]
            address_result = await db.query(
                PropertyRowModel, conditions={"id": property_id}, columns=["address"]
            )
            name = address_result[0].address
        elif data["category"] == "buy":
            participants = data["participants"]
            participant_name_results = await db.query(
                PersonRowModel,
                conditions={"id": list(participants.keys())},
                columns=["name"],
            )
            name = " ".join([f"{p.name}" for p in participant_name_results])

        deal_row = DealRowModel(
            name=name,
            category=data["category"],
            status=data["status"],
            type=data["type"],
            user_ids=[user_id],
        )

        deal = DealModel(
            transaction_platform=data.get("transaction_platform"),
            notes=data.get("notes"),
            property_id=data["property_id"],
        )

        # Prepare associations for participants
        participant_associations = [
            DealParticipantAssociation(deal_id=deal.id, person_id=person_id, role=role)
            for person_id, role in data["participants"].items()
        ]

        # Prepare associations for documents if any
        document_associations = []
        if "documents" in data:
            document_associations = [
                DealDocumentAssociation(deal_id=deal.id, document_id=document_id)
                for document_id in data["documents"]
            ]

        # Prepare association for the user
        user_association = UserDealAssociation(user_id=user_id, deal_id=deal.id)

        async with db.get_session() as session:
            try:
                await db.create(DealRowModel, deal_row, session)
                deal.row = deal_row
                await db.create(DealModel, deal, session)
                await db.batch_add_associations(
                    participant_associations
                    + document_associations
                    + [user_association],
                    session,
                )
            except Exception as e:
                await session.rollback()
                raise e
            else:
                await session.commit()

        return cls.from_orm(deal_row, deal)

    @classmethod
    async def read(cls, id: int):
        db = Database()
        deal = await db.read(
            DealModel,
            id,
            eager_load=[
                "property.row",
                "participants.row",
                "documents",
                "users.row",
                "row"
            ],
        )

        users = [UserRow.from_orm(user) for user in deal.users]
        participants = [
            ParticipantRow.from_orm(participant)
            for participant in deal.deal_details.participants
        ]
        documents = [
            DealDocumentRow.from_orm(document)
            for document in deal.deal_details.documents
        ]

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

    async def update(self, **kwargs):
        db = Database()

        deal_updates = {}
        deal_detail_updates = {}

        for key, value in kwargs.items():
            if hasattr(DealRowModel, key):
                deal_updates[key] = value
            if hasattr(DealModel, key):
                deal_detail_updates[key] = value

        async with db.get_session() as session:
            if deal_updates:
                await db.update_fields(DealRowModel, self.id, deal_updates, session)
            if deal_detail_updates:
                await db.update_fields(DealModel, self.id, deal_detail_updates, session)

    @classmethod
    async def delete(cls, id: int):
        db = Database()
        deal = await db.read(DealRowModel, id)

        await db.delete(deal)

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
            "participants": [
                participant.to_dict() for participant in self.participants
            ],
            "documents": [document.to_dict() for document in self.documents],
        }
