from datetime import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar

from core.database import Database
from core.enums.person_type import PersonType
from core.models.associations import UserPersonAssociation
from core.models.entities.person import PersonModel
from core.models.rows.person import PersonRowModel
from core.models.rows.property import PropertyRowModel
from core.models.rows.user import UserRowModel
from core.objects.base_entities.base_entity import BaseEntity
from core.objects.entities.message import Message
from core.objects.rows.deal_row import DealRow
from core.objects.rows.property_row import PropertyRow
from core.objects.rows.user_row import UserRow
from core.utils.ids import cantor_pairing
from core.utils.strings import assemble_name

T = TypeVar("T", bound="BasePerson")


class BasePerson(BaseEntity):
    id: int

    # Row Fields
    name: str
    email: Optional[str]
    phone: Optional[str]
    type: PersonType
    active: bool
    last_activity: datetime

    created: datetime
    updated: Optional[datetime]
    viewed: Optional[datetime]

    user_ids: List[int]

    # Entity Fields
    first_name: str
    middle_name: Optional[str]
    last_name: str

    notes: str
    language: str

    deals: Optional[List[DealRow]] = []
    residence_id: Optional[int] = None
    residence: Optional[PropertyRow] = None
    portfolio: Optional[List[PropertyRow]] = []
    users: List[UserRow]

    messages: Optional[List[Message]] = []

    person_row_model: Optional[PersonRowModel]
    person_model: Optional[PersonModel]

    @classmethod
    async def create(cls: Type[T], user_id: int, data: Dict[str, Any]) -> T:
        """
        Creates a new person entry in the database.

        :param user_id:
            The ID of the user creating the person.
        :param data:
            A dictionary containing the person details:
            - 'first_name' (str): The first name of the person. (Required)
            - 'last_name' (str): The last name of the person. (Required)
            - 'middle_name' (Optional[str]): The middle name of the person. (Optional)
            - 'email' (Optional[str]): The email of the person. (Optional)
            - 'phone' (Optional[str]): The phone number of the person. (Optional)
            - 'type' (PersonType): The type of the person. (Required)
            - 'notes' (Optional[str]): Additional notes regarding the person. (Optional)
            - 'language' (Optional[str]): The language of the person. (Optional)
        """
        db = Database()

        person_row = PersonRowModel(
            name=assemble_name(
                data["first_name"], data.get("middle_name"), data["last_name"]
            ),
            email=data.get("email"),
            phone=data.get("phone"),
            type=data["type"],
            active=True,
            created=datetime.utcnow(),
            user_ids=[user_id],
        )

        person = PersonModel(
            first_name=data["first_name"],
            middle_name=data.get("middle_name"),
            last_name=data["last_name"],
            notes=data.get("notes"),
            language=data.get("language", "english"),
        )

        user_association = UserPersonAssociation(user_id=user_id, person_id=person.id)

        async with db.get_session() as session:
            try:
                await db.create(PersonRowModel, person_row, session)
                person.row = person_row
                await db.create(PersonModel, person, session)
                await db.add_association(user_association, session)
            except Exception as e:
                await session.rollback()
                raise e
            else:
                await session.commit()

        return await cls.read(person.id)

    @classmethod
    async def read(cls: Type[T], id: int, user_id: int) -> T:
        db = Database()

        async with db.get_session() as session:
            try:
                person = await db.read(
                    PersonModel,
                    id,
                    eager_load=[
                        "row",
                        "residence.row",
                        "portfolio.row",
                        "deals.row",
                        "deals.deal_participant_association" "users.row",
                    ],
                )
                await db.update_fields(
                    PersonRowModel, person.id, {"viewed": datetime.utcnow()}, session
                )
            except Exception as e:
                await session.rollback()
                raise e
            else:
                await session.commit()

        source_id = cantor_pairing(user_id, id)
        first_page_messages = await Message.query(
            source_id=source_id, limit=25, offset=0
        )

        deals = [DealRow.from_model(deal.row) for deal in person.deals]
        residence = (
            PropertyRow.from_model(person.residence.row)
            if person.residence.row
            else None
        )
        portfolio = [
            PropertyRow.from_model(property.row) for property in person.portfolio
        ]
        users = [UserRow.from_model(user.row) for user in person.users]

        return cls(
            id=person.id,
            name=person.name,
            first_name=person.first_name,
            middle_name=person.middle_name,
            last_name=person.last_name,
            email=person.email,
            phone=person.phone,
            type=person.type,
            active=person.active,
            last_activity=person.last_activity,
            created=person.row.created,
            updated=person.row.updated,
            viewed=person.row.viewed,
            user_ids=person.row.user_ids,
            notes=person.notes,
            language=person.language,
            messages=first_page_messages,
            deals=deals,
            residence=residence,
            portfolio=portfolio,
            users=users,
            person_row_model=person.row,
            person_model=person,
        )

    @classmethod
    async def update(cls: Type[T], id: int, updates: Dict[str, Any]) -> T:
        """
        Updates row by replacing columns with values specified in updates.

        :param updates:
            A dictionary containing the person details to update:
            - 'first_name' (Optional[str]): The first name of the person. (Optional)
            - 'middle_name' (Optional[str]): The middle name of the person. (Optional)
            - 'last_name' (Optional[str]): The last name of the person. (Optional)
            - 'type' (Optional[PersonType]): The type of the person. (Optional)
            - 'active' (Optional[bool]): Whether the person is active. (Optional)
            - 'last_activity' (Optional[datetime]): The last activity of the person. (Optional)
            - 'notes' (Optional[str]): Additional notes regarding the person. (Optional)
        """
        db = Database()

        person_updates = {}
        person_details_updates = {}

        for key, value in updates.items():
            if hasattr(PersonRowModel, key):
                person_updates[key] = value
            if hasattr(PersonModel, key):
                person_details_updates[key] = value

        # Check if name components are being updated
        if any(key in updates for key in ["first_name", "middle_name", "last_name"]):
            # Fetch the current person details to assemble the new name
            async with db.get_session() as session:
                person = await db.read(PersonModel, id, session=session)
                first_name = updates.get("first_name", person.first_name)
                middle_name = updates.get("middle_name", person.middle_name)
                last_name = updates.get("last_name", person.last_name)
                person_updates["name"] = assemble_name(
                    first_name, middle_name, last_name
                )

        async with db.get_session() as session:
            try:
                if person_updates:
                    await db.update_fields(PersonRowModel, id, person_updates, session)
                if person_details_updates:
                    await db.update_fields(
                        PersonModel, id, person_details_updates, session
                    )
            except Exception as e:
                await session.rollback()
                raise e
            else:
                await session.commit()

        return await cls.read(id)

    @classmethod
    async def delete(cls: Type[T], id: int, user_id: int) -> None:
        """Delete a person entry and all associated messages"""
        db = Database()
        async with db.get_session() as session:
            try:
                await db.delete_by_id(PersonRowModel, id, session)
                source_id = cantor_pairing(user_id, id)
                await Message.delete_by_source_id(source_id, session)
            except Exception as e:
                await session.rollback()
                raise e
            else:
                await session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "type": self.type.value,
            "active": self.active,
            "last_activity": self.last_activity.isoformat()
            if self.last_activity
            else None,
            "created": self.created.isoformat() if self.created else None,
            "updated": self.updated.isoformat() if self.updated else None,
            "viewed": self.viewed.isoformat() if self.viewed else None,
            "user_ids": self.user_ids,
            "notes": self.notes,
            "language": self.language,
            "messages": [message.to_dict() for message in self.messages],
            "deals": {
                deal.to_dict(): participant.to_dict()
                for deal, participant in self.deals.items()
            },
            "residence": self.residence.to_dict() if self.residence else None,
            "portfolio": [property.to_dict() for property in self.portfolio],
            "users": [user.to_dict() for user in self.users],
        }
