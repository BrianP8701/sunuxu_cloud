from datetime import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar

from core.database import Database
from core.enums import PersonType, ParticipantRole
from core.models.associations import UserPersonAssociation, PropertyOwnerAssociation
from core.models.entities.person import PersonModel
from core.models.rows.person import PersonRowModel
from core.objects.base_entities.base_entity import BaseEntity
from core.objects.entities.message import Message
from core.objects.rows.deal_row import DealRow
from core.objects.rows.property_row import PropertyRow
from core.objects.rows.user_row import UserRow
from core.utils.ids import cantor_pairing
from core.utils.strings import assemble_name

T = TypeVar("T", bound="BasePerson")


class BasePerson(BaseEntity):
    id: int = None

    # Row Fields
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    type: PersonType
    active: bool
    last_activity: Optional[datetime] = None

    created: datetime = None
    updated: Optional[datetime] = None
    viewed: Optional[datetime] = None

    user_ids: List[int]

    # Entity Fields
    first_name: str
    middle_name: Optional[str] = None
    last_name: str

    notes: Optional[str] = None
    language: Optional[str] = None

    deals: Optional[Dict[DealRow, ParticipantRole]] = {}
    residence_id: Optional[int] = None
    residence: Optional[PropertyRow] = None
    portfolio: Optional[List[PropertyRow]] = []
    users: List[UserRow]

    messages: Optional[List[Message]] = []

    person_row_model: Optional[PersonRowModel] = None
    person_model: Optional[PersonModel] = None

    @classmethod
    async def create(cls: Type[T], data: Dict[str, Any]) -> T:
        """
        Creates a new person entry in the database.

        :param data:
            A dictionary containing the person details:
            - 'user_ids' (List[int]): A list of IDs of the users associated with the person. (Required)
            - 'first_name' (str): The first name of the person. (Required)
            - 'last_name' (str): The last name of the person. (Required)
            - 'middle_name' (Optional[str]): The middle name of the person. (Optional)
            - 'email' (Optional[str]): The email of the person. (Optional)
            - 'phone' (Optional[str]): The phone number of the person. (Optional)
            - 'type' (PersonType): The type of the person. (Required)
            - 'notes' (Optional[str]): Additional notes regarding the person. (Optional)
            - 'language' (Optional[str]): The language of the person. (Optional)
            - 'residence_id' (Optional[int]): The ID of the property that the person resides in. (Optional)
            - 'portfolio_ids' (Optional[List[int]]): A list of IDs of the properties that the person owns. (Optional)
        """
        db = Database()

        person_row = PersonRowModel(
            name=assemble_name(
                data["first_name"], data.get("middle_name"), data["last_name"]
            ),
            email=data.get("email"),
            phone=data.get("phone"),
            type=PersonType(data["type"]),
            active=True,
            created=datetime.utcnow(),
            user_ids=data["user_ids"],
        )

        person = PersonModel(
            first_name=data["first_name"],
            middle_name=data.get("middle_name"),
            last_name=data["last_name"],
            notes=data.get("notes"),
            language=data.get("language", "english"),
            residence_id=data.get("residence_id")
        )

        user_associations = [
            UserPersonAssociation(user_id=user_id, person_id=person.id)
            for user_id in data["user_ids"]
        ]

        # Prepare portfolio associations if any
        portfolio_associations = [
            PropertyOwnerAssociation(property_id=property_id, person_id=person.id)
            for property_id in data.get("portfolio_ids", [])
        ]

        # Add portfolio associations to the session
        async with db.get_session() as session:
            try:
                await db.create(PersonRowModel, person_row, session)
                person.row = person_row
                await db.create(PersonModel, person, session)
                await db.batch_add_associations(user_associations, session)
                await db.batch_add_associations(portfolio_associations, session)  # Add this line
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
                        "deals.deal_participant_association", 
                        "users.row",
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

        # Transform deals to include ParticipantRole
        deals = {DealRow.from_model(deal.row): ParticipantRole(deal.deal_participant_association.role) for deal in person.deals}

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
            - 'type' (Optional[str]): The type of the person. PersonType enum. (Optional)
            - 'active' (Optional[bool]): Whether the person is active. (Optional)
            - 'last_activity' (Optional[datetime]): The last activity of the person. (Optional)
            - 'notes' (Optional[str]): Additional notes regarding the person. (Optional)
        """
        db = Database()

        person_updates = {}
        person_details_updates = {}

        for key, value in updates.items():
            if hasattr(PersonRowModel, key):
                if key == "type":
                    person_updates[key] = PersonType(value)
                else:
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


    @classmethod
    async def batch_create(cls, data: List[Dict[str, Any]]) -> List[T]:
        """
        Create multiple people.

        :param data:
            A list of dictionaries, each containing the data to be created for a person.
        """
        db = Database()
        persons = []
        person_rows = []
        user_associations = []
        portfolio_associations = []

        for person_data in data:
            person_row = PersonRowModel(
                name=assemble_name(
                    person_data["first_name"], person_data.get("middle_name"), person_data["last_name"]
                ),
                email=person_data.get("email"),
                phone=person_data.get("phone"),
                type=PersonType(person_data["type"]),
                active=True,
                created=datetime.utcnow(),
                user_ids=person_data["user_ids"],
            )  
            person_rows.append(person_row)

            person = PersonModel(
                first_name=person_data["first_name"],
                middle_name=person_data.get("middle_name"),
                last_name=person_data["last_name"],
                notes=person_data.get("notes"),
                language=person_data.get("language", "english"),
                residence_id=person_data.get("residence_id")
            )
            persons.append(person)

            for user_id in person_data["user_ids"]:
                user_associations.append(UserPersonAssociation(user_id=user_id, person_id=person.id))

            for property_id in person_data.get("portfolio_ids", []):
                portfolio_associations.append(PropertyOwnerAssociation(property_id=property_id, person_id=person.id))

        async with db.get_session() as session:
            try:
                await db.batch_create(person_rows, session)
                for person, person_row in zip(persons, person_rows):
                    person.row = person_row
                await db.batch_create(persons, session)
                await db.batch_add_associations(user_associations, session)
                await db.batch_add_associations(portfolio_associations, session)
            except Exception as e:
                await session.rollback()
                raise e
            else:
                await session.commit()

        return [await cls.read(person.id, user_id) for person in persons for user_id in person.user_ids]

    @classmethod
    async def batch_delete(cls, ids: List[int], user_id: int) -> None:
        """
        Delete multiple persons by their IDs.

        :param ids:
            A list of person IDs to delete.
        """
        db = Database()
        async with db.get_session() as session:
            try:
                await db.batch_delete(PersonModel, {"id": ids}, session)
                for id in ids:
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
                deal.to_dict(): role.value
                for deal, role in self.deals.items()
            },
            "residence": self.residence.to_dict() if self.residence else None,
            "portfolio": [property.to_dict() for property in self.portfolio],
            "users": [user.to_dict() for user in self.users],
        }
