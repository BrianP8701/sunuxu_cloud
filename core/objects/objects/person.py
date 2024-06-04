from typing import  List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from core.enums.person_type import PersonType
from core.models.rows.person import PersonRowOrm
from core.models.entities.person import PersonOrm
from core.database import Database
from core.objects.objects.message import Message
from core.objects.rows.deal_row import DealRow
from core.objects.rows.deal_row import DealRow
from core.objects.rows.property_row import PropertyRow
from core.models.rows.property import PropertyRowOrm
from core.models.rows.user import UserRowOrm
from core.objects.rows.user_row import UserRow
from core.models.associations import UserPersonAssociation
from core.utils.strings import assemble_name
from core.objects.objects.base_object import BaseObject
from core.objects.rows.person_row import PersonRow

class Person(BaseObject):
    id: int
    first_name: str
    middle_name: Optional[str]
    last_name: str
    email: Optional[str]
    phone: Optional[str]
    type: PersonType
    active: bool
    last_activity: datetime

    created: datetime
    updated: Optional[datetime]
    viewed: Optional[datetime]

    user_ids: List[int]

    notes: str
    language: str
    # source: Optional[str]
    # viewed_properties: Optional[List[str]]
    # signature: Optional[bytes]

    messages: List[Message] = []
    deals: List[DealRow] = []
    residence: PropertyRow = None
    portfolio: List[PropertyRow] = []
    users: List[UserRow] = []

    created: datetime
    updated: Optional[datetime]
    viewed: Optional[datetime]

    person_orm: Optional[PersonRowOrm]
    person_details_orm: Optional[PersonOrm]

    @classmethod
    async def read(cls, id: int):
        db = Database()
        person = await db.read(PersonRowOrm, id, eager_load=[
            'person_details', 
            'person_details.residence', 
            'person_details.portfolio', 
            'person_details.deals', 
            'person_details.users'
        ])

        first_page_messages = Message.read(relationship_id=person.id, page_size=25, offset=0)
        deals = [DealRow.from_orm(deal) for deal in person.person_details.deals]
        residence = PropertyRow.from_orm(person.person_details.residence) if person.person_details.residence else None
        portfolio = [PropertyRow.from_orm(property) for property in person.person_details.portfolio]
        users = [UserRow.from_orm(user) for user in person.person_details.users]

        return cls(
            id=person.id,
            first_name=person.first_name,
            middle_name=person.middle_name,
            last_name=person.last_name,
            email=person.email,
            phone=person.phone,
            type=person.type,
            # custom_type=person.custom_type,
            active=person.active,
            last_activity=person.last_activity,
            # last_messaged=person.last_messaged,
            # temperature=person.temperature,
            created=person.created,
            updated=person.updated,
            viewed=person.viewed,
            user_ids=person.user_ids,
            # signature=person_details.signature,
            notes=person.person_details.notes,
            language=person.person_details.language,
            # source=person_details.source,
            # viewed_properties=person_details.viewed_properties,
            messages=first_page_messages,
            deals=deals,
            residence=residence,
            portfolio=portfolio,
            users=users,
            person_orm=person,
            person_details_orm=person.person_details        
        )

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "type": self.type.value,
            "active": self.active,
            "last_activity": self.last_activity.isoformat() if self.last_activity else None,
            "created": self.created.isoformat() if self.created else None,
            "updated": self.updated.isoformat() if self.updated else None,
            "viewed": self.viewed.isoformat() if self.viewed else None,
            "user_ids": self.user_ids,
            "notes": self.notes,
            "language": self.language,
            "messages": [message.to_dict() for message in self.messages],
            "deals": {deal.to_dict(): participant.to_dict() for deal, participant in self.deals.items()},
            "residence": self.residence.to_dict() if self.residence else None,
            "portfolio": [property.to_dict() for property in self.portfolio],
            "users": [user.to_dict() for user in self.users]
        }

    async def create(self):
        """ 
        Inserts a new person into the database 
        Doesen't make relationships other than users
        """
        db = Database()

        person = self._assemble_person_orm()
        person_details = self._assemble_person_details_orm()

        async with db.get_session() as session:
            person = await db.create(person, session)
            person_details = await db.create(person_details, session)

        self.id = person.id
        self.person_orm = person
        self.person_details_orm = person_details

    @classmethod
    async def batch_create(cls, objects: List['Person']):
        db = Database()
        people_orm = [person._assemble_person_orm() for person in objects]
        people_details_orm = [person._assemble_person_details_orm() for person in objects]

        async with db.get_session() as session:
            await db.batch_create(people_orm, session)
            await db.batch_create(people_details_orm, session)

    async def set_residence(self, property_id: int):
        db = Database()
        person_details = self.person_details_orm
        property = await db.read(PropertyRowOrm, property_id)

        person_details.residence = property

        async with db.get_session() as session:
            await db.update(person_details, session)

    async def clear_residence(self):
        db = Database()
        person_details = self.person_details_orm

        person_details.residence = None

        async with db.get_session() as session:
            await db.update(person_details, session)

    async def add_to_portfolio(self, property_id: int):
        db = Database()
        person_details = self.person_details_orm
        property = await db.read(PropertyRowOrm, property_id)

        person_details.portfolio.append(property)

        async with db.get_session() as session:
            await db.update(person_details, session)

    async def remove_from_portfolio(self, property_id: int):
        db = Database()
        person_details = self.person_details_orm
        property = await db.read(PropertyRowOrm, property_id)

        person_details.portfolio.remove(property)

        async with db.get_session() as session:
            await db.update(person_details, session)

    async def add_user(self, user_id: int):
        db = Database()
        person = self.person_orm
        user = await db.read(UserRowOrm, user_id)

        person.user_ids.append(user.id)
        person.users.append(user)

        await db.update_fields(PersonRowOrm, self.id, {'user_ids': person.user_ids, 'users': person.users})

    @classmethod
    async def update(cls, id: int, updates: Dict[str, Any]):
        db = Database()

        person_updates = {}
        person_details_updates = {}

        for key, value in updates.items():
            if hasattr(PersonRowOrm, key):
                person_updates[key] = value
            if hasattr(PersonOrm, key):
                person_details_updates[key] = value

        async with db.get_session() as session:
            if person_updates:
                await db.update_fields(PersonRowOrm, id, person_updates, session)
            if person_details_updates:
                await db.update_fields(PersonOrm, id, person_details_updates, session)

    @classmethod
    async def delete(cls, id: int):
        db = Database()
        await db.delete_by_id(PersonRowOrm, id)

    def _assemble_person_orm(self):
        """ Creates a new PersonOrm object from the Person object """
        person_data = {
            'name': assemble_name(self.first_name, self.middle_name, self.last_name),
            'email': self.email,
            'phone': self.phone,
            'type': self.type,
            'active': self.active,
            'last_activity': self.last_activity,
            'created': self.created,
            'updated': self.updated,
            'viewed': self.viewed,
        }
        person_details_data = {
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'notes': self.notes,
            'language': self.language,
            'source': self.source,
            'signature': self.signature,
            'viewed_properties': self.viewed_properties
        }
        
        user_associations = [UserPersonAssociation(user_id=user_id, person_id=self.id) for user_id in self.user_ids]
        person_details_data['users'] = user_associations

        return PersonRowOrm(**person_data), PersonOrm(**person_details_data)
