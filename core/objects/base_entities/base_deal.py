from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar

from core.database import Database
from core.enums import DealStatus, DealType, DealCategory, ParticipantRole
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
    async def create(cls: Type[T], data: Dict[str, Any]) -> T:
        """
        Creates a new deal entry in the database.

        :param data:
            A dictionary containing the deal details:
            - 'user_ids' (List[int]): A list of IDs of the users associated with the deal. (Required)
            - 'category' (str): Indicates if the deal is a listing. DealCategory enum. (Required)
            - 'status' (str): The current status of the deal. DealStatus enum. (Required)
            - 'type' (str): The type of the deal (Buy, Sell, or Dual). DealType enum. (Required)
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
            category=DealCategory(data["category"]),
            status=DealStatus(data["status"]),
            type=DealType(data["type"]),
            user_ids=data["user_ids"],
        )

        deal = DealModel(
            transaction_platform=data.get("transaction_platform"),
            notes=data.get("notes"),
            property_id=data["property_id"],
        )

        # Prepare associations for participants
        participant_associations = [
            DealParticipantAssociation(deal_id=deal.id, person_id=person_id, role=ParticipantRole(role))
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
        user_associations = [
            UserDealAssociation(user_id=user_id, deal_id=deal.id)
            for user_id in data["user_ids"]
        ]

        async with db.get_session() as session:
            try:
                await db.create(DealRowModel, deal_row, session)
                deal.row = deal_row
                await db.create(DealModel, deal, session)
                await db.batch_add_associations(
                    participant_associations
                    + document_associations
                    + user_associations,
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
            - 'category' (Optional[str]): Indicates if the deal is a listing. DealCategory enum. (Optional)
            - 'status' (Optional[str]): The current status of the deal. DealStatus enum. (Optional)
            - 'type' (Optional[str]): The type of the deal (Buy, Sell, or Dual). DealType enum. (Optional)
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
                if key == "category":
                    deal_row_updates[key] = DealCategory(value)
                elif key == "status":
                    deal_row_updates[key] = DealStatus(value)
                elif key == "type":
                    deal_row_updates[key] = DealType(value)
                else:
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

    @classmethod
    async def batch_create(cls, data: List[Dict[str, Any]]) -> List[T]:
        """
        Create multiple deals for multiple users.

        :param data:
            A list of dictionaries, each containing the data to be created for the deal.
        """
        db = Database()
        deals = []
        deal_rows = []
        participant_associations = []
        document_associations = []
        user_associations = []

        for deal_data in data:
            # Validate category
            if deal_data["category"] not in ["buy", "sell", "dual"]:
                raise ValueError(
                    f'{deal_data["category"]} is not a valid deal category. Must be sell, buy or dual.'
                )

            # Setting row name depending on if it is a Buy, Sell or Dual deal
            if deal_data["category"] in ["dual", "sell"]:
                property_id = deal_data["property_id"]
                address_result = await db.query(
                    PropertyRowModel, conditions={"id": property_id}, columns=["address"]
                )
                name = address_result[0].address
            elif deal_data["category"] == "buy":
                participants = deal_data["participants"]
                participant_name_results = await db.query(
                    PersonRowModel,
                    conditions={"id": list(participants.keys())},
                    columns=["name"],
                )
                name = " ".join([f"{p.name}" for p in participant_name_results])

            deal_row = DealRowModel(
                name=name,
                category=DealCategory(deal_data["category"]),
                status=DealStatus(deal_data["status"]),
                type=DealType(deal_data["type"]),
                user_ids=deal_data["user_ids"],
            )
            deal_rows.append(deal_row)

            deal = DealModel(
                transaction_platform=deal_data.get("transaction_platform"),
                notes=deal_data.get("notes"),
                property_id=deal_data["property_id"],
            )
            deals.append(deal)

            # Prepare associations for participants
            participant_associations.extend([
                DealParticipantAssociation(deal_id=deal.id, person_id=person_id, role=ParticipantRole(role))
                for person_id, role in deal_data["participants"].items()
            ])

            # Prepare associations for documents if any
            if "documents" in deal_data:
                document_associations.extend([
                    DealDocumentAssociation(deal_id=deal.id, document_id=document_id)
                    for document_id in deal_data["documents"]
                ])

            # Prepare association for the users
            for user_id in deal_data["user_ids"]:
                user_associations.append(UserDealAssociation(user_id=user_id, deal_id=deal.id))

        async with db.get_session() as session:
            try:
                await db.batch_create(deal_rows, session)
                for deal, deal_row in zip(deals, deal_rows):
                    deal.row = deal_row
                await db.batch_create(deals, session)
                await db.batch_add_associations(
                    participant_associations + document_associations + user_associations,
                    session,
                )
            except Exception as e:
                await session.rollback()
                raise e
            else:
                await session.commit()

        return [await cls.read(deal.id) for deal in deals]

    @classmethod
    async def batch_delete(cls, ids: List[int]) -> None:
        """
        Delete multiple deals by their IDs.

        :param ids:
            A list of deal IDs to delete.
        """
        db = Database()
        async with db.get_session() as session:
            try:
                await db.batch_delete(DealModel, {"id": ids}, session)
            except Exception as e:
                await session.rollback()
                raise e
            else:
                await session.commit()


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
