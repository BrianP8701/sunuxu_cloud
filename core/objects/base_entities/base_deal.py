from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar

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

T = TypeVar("T", bound="BaseDeal")


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

    deal_row_model: Optional[DealRowModel]
    deal_model: Optional[DealModel]

    @classmethod
    async def create(cls: Type[T], user_id: int, data: Dict[str, Any]) -> T:
        """
        Creates a new deal entry in the database.

        :param user_id:
            The ID of the user creating the deal.
        :param data:
            A dictionary containing the deal details:
            - 'category' (DealCategory): Indicates if the deal is a listing. Must be 'buy', 'sell', or 'dual'. (Required)
            - 'status' (DealStatus): The current status of the deal. (Required)
            - 'type' (DealType): The type of the deal (Buy, Sell, or Dual). (Required)
            - 'participants' (Optional[Dict[int, str]]): Person IDs to participant roles. Required if category is 'buy'. (Conditional)
            - 'property_id' (Optional[int]): ID of the property the deal is for. Required if category is 'sell' or 'dual'. (Conditional)
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

        return await cls.read(deal.id)

    @classmethod
    async def read(cls: Type[T], id: int) -> T:
        db = Database()

        async with db.get_session() as session:
            try:
                deal = await db.read(
                    DealModel,
                    id,
                    eager_load=[
                        "property.row",
                        "users.row",
                        "participants.row",
                        "participants.deal_participant_association",
                        "documents",
                        "row",
                    ],
                    session=session,
                )
                db.update_fields(DealRowModel, id, {"viewed": datetime.now()}, session)
            except Exception as e:
                await session.rollback()
                raise e
            else:
                await session.commit()

        users = [UserRow.from_model(user.row) for user in deal.users]
        participants = [
            ParticipantRow(
                id=participant.id,
                name=participant.name,
                role=participant.deal_participant_association.role,
            )
            for participant in deal.participants
        ]
        documents = [
            DealDocumentRow.from_model(document) for document in deal.documents
        ]
        property = PropertyRow.from_model(deal.property.row)

        return cls(
            id=deal.id,
            category=deal.row.category,
            status=deal.row.status,
            type=deal.row.type,
            created=deal.row.created,
            updated=deal.row.updated,
            viewed=deal.row.viewed,
            transaction_platform=deal.transaction_platform,
            notes=deal.notes,
            users=users,
            property=property,
            participants=participants,
            documents=documents,
            deal_row_model=deal.row,
            deal_model=deal,
        )

    @classmethod
    async def update(cls: Type[T], id: int, updates: Dict[str, Any]) -> T:
        """
        Updates row by replacing columns with values specified in updates.

        :param updates:
            A dictionary containing the deal details to update:
            - 'category' (Optional[DealCategory]): Indicates if the deal is a listing. Must be 'buy', 'sell', or 'dual'. (Optional)
            - 'status' (Optional[DealStatus]): The current status of the deal. (Optional)
            - 'type' (Optional[DealType]): The type of the deal (Buy, Sell, or Dual). (Optional)
            - 'transaction_platform' (Optional[str]): The platform used for the transaction. (Optional)
            - 'notes' (Optional[str]): Additional notes regarding the deal. (Optional)
        """
        db = Database()

        valid_updates = {
            "category",
            "status",
            "type",
            "transaction_platform",
            "notes",
        }

        deal_row_updates = {}
        deal_updates = {}

        for key, value in updates.items():
            if key not in valid_updates:
                raise ValueError(
                    f"{key} is not a valid deal update. Must be one of {', '.join(valid_updates)}. To update participants, property, documents, or users, use the appropriate methods."
                )
            if hasattr(DealRowModel, key):
                deal_row_updates[key] = value
            if hasattr(DealModel, key):
                deal_updates[key] = value

        async with db.get_session() as session:
            try:
                if deal_row_updates:
                    await db.update_fields(DealRowModel, id, deal_row_updates, session)
                if deal_updates:
                    await db.update_fields(DealModel, id, deal_updates, session)
            except Exception as e:
                await session.rollback()
                raise e
            else:
                await session.commit()

        return await cls.read(id)

    @classmethod
    async def delete(cls: Type[T], id: int) -> None:
        db = Database()
        await db.delete_by_id(DealModel, id)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "category": self.category.value,
            "status": self.status.value,
            "type": self.type.value,
            "transaction_platform": self.transaction_platform,
            "notes": self.notes,
            "users": [user.to_dict() for user in self.users] if self.users else [],
            "property": self.property.to_dict() if self.property else None,
            "participants": [participant.to_dict() for participant in self.participants]
            if self.participants
            else [],
            "documents": [document.to_dict() for document in self.documents]
            if self.documents
            else [],
            "created": self.created.isoformat() if self.created else None,
            "updated": self.updated.isoformat() if self.updated else None,
            "viewed": self.viewed.isoformat() if self.viewed else None,
        }
