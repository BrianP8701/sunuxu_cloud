from typing import  List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from core.types.person import PersonType
from core.models.person import PersonOrm
from core.models.person_details import PersonDetailsOrm
from core.database import Database
from core.types.message import Message
from core.types.deal_row import DealRow
from core.types.participant_row import ParticipantRow
from core.types.deal_row import DealRow
from core.types.participant_row import ParticipantRow
from core.types.property_row import PropertyRow
from core.models.property import PropertyOrm

class Person(BaseModel):
    id: int
    first_name: str
    middle_name: Optional[str]
    last_name: str
    email: Optional[str]
    phone: Optional[str]
    type: PersonType
    custom_type: Optional[str]
    active: bool
    unread_message: bool
    last_activity: Optional[datetime]
    last_messaged: Optional[datetime]
    temperature: Optional[int]
    signature: Optional[bytes]
    notes: Optional[str]
    language: Optional[str]
    source: Optional[str]
    viewed_properties: Optional[List[str]]

    messages: Optional[List[Message]]
    deals: Optional[Dict[DealRow, ParticipantRow]]
    residence: Optional[PropertyRow]
    portfolio: Optional[List[PropertyRow]]

    created: datetime
    updated: Optional[datetime]
    viewed: Optional[datetime]
    
    person_orm: Optional[PersonOrm]
    person_details_orm: Optional[PersonDetailsOrm]

    @classmethod
    async def get(cls, id: int):
        db = Database()
        person = await db.get(PersonOrm, id)
        person_details = await db.get(PersonDetailsOrm, id)

        first_page_messages = Message.get(relationship_id=person.id, page_size=25, offset=0)
        participants = person_details.participants
        deals = {DealRow.from_orm(participant.deal): ParticipantRow.from_orm(participant) for participant in participants}
        residence = PropertyRow.from_orm(person_details.residence) if person_details.residence else None
        portfolio = [PropertyRow.from_orm(property) for property in person_details.portfolio]

        return cls(
            id=person.id,
            first_name=person.first_name,
            middle_name=person.middle_name,
            last_name=person.last_name,
            email=person.email,
            phone=person.phone,
            type=person.type,
            custom_type=person.custom_type,
            active=person.active,
            unread_message=person.unread_message,
            last_activity=person.last_activity,
            last_messaged=person.last_messaged,
            temperature=person.temperature,
            created=person.created,
            updated=person.updated,
            viewed=person.viewed,
            signature=person_details.signature,
            notes=person_details.notes,
            language=person_details.language,
            source=person_details.source,
            viewed_properties=person_details.viewed_properties,
            messages=first_page_messages,
            deals=deals,
            residence=residence,
            portfolio=portfolio,
            person_orm=person,
            person_details_orm=person_details        
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
            "custom_type": self.custom_type,
            "active": self.active,
            "unread_message": self.unread_message,
            "last_activity": self.last_activity.isoformat() if self.last_activity else None,
            "last_messaged": self.last_messaged.isoformat() if self.last_messaged else None,
            "temperature": self.temperature,
            "created": self.created.isoformat() if self.created else None,
            "updated": self.updated.isoformat() if self.updated else None,
            "viewed": self.viewed.isoformat() if self.viewed else None,
            "signature": self.signature,
            "notes": self.notes,
            "language": self.language,
            "source": self.source,
            "viewed_properties": self.viewed_properties,
            "messages": [message.to_dict() for message in self.messages],
            "deals": {deal.to_dict(): participant.to_dict() for deal, participant in self.deals.items()},
            "residence": self.residence.to_dict() if self.residence else None,
            "portfolio": [property.to_dict() for property in self.portfolio]
        }

    async def insert(self):
        db = Database()

        person = self._assemble_person_orm()
        person_details = self._assemble_person_details_orm()

        async with db.get_session() as session:
            person = await db.insert(person, session)
            person_details = await db.insert(person_details, session)

        self.id = person.id
        self.person_orm = person
        self.person_details_orm = person_details

    @classmethod
    async def batch_insert(cls, people: List['Person']):
        db = Database()
        people_orm = [person._assemble_person_orm() for person in people]
        people_details_orm = [person._assemble_person_details_orm() for person in people]

        async with db.get_session() as session:
            await db.batch_insert(people_orm, session)
            await db.batch_insert(people_details_orm, session)

    async def set_residence(self, property_id: int):
        db = Database()
        person_details = self.person_details_orm
        property = await db.get(PropertyOrm, property_id)

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
        property = await db.get(PropertyOrm, property_id)

        person_details.portfolio.append(property)

        async with db.get_session() as session:
            await db.update(person_details, session)

    async def remove_from_portfolio(self, property_id: int):
        db = Database()
        person_details = self.person_details_orm
        property = await db.get(PropertyOrm, property_id)

        person_details.portfolio.remove(property)

        async with db.get_session() as session:
            await db.update(person_details, session)

    def _assemble_person_orm(self):
        person_data = {
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'type': self.type,
            'custom_type': self.custom_type,
            'active': self.active,
            'unread': self.unread,
            'last_activity': self.last_activity,
            'last_messaged': self.last_messaged,
            'temperature': self.temperature,
            'created': self.created,
            'updated': self.updated,
            'viewed': self.viewed,
            'tags': self.tags
        }
        return PersonOrm(**person_data)

    async def update(self, **kwargs):
        db = Database()
        person = self.person_orm
        person_details = self.person_details_orm

        person_changed = False
        person_details_changed = False
        for key, value in kwargs.items():
            if hasattr(person, key):
                setattr(person, key, value)
                person_changed = True
            if hasattr(person_details, key):
                setattr(person_details, key, value)
                person_details_changed = True
        
        async with db.get_session() as session:
            if person_changed:
                await db.update(person, session)
            if person_details_changed:
                await db.update(person_details, session)

    @classmethod
    async def delete(cls, id: int):
        db = Database()
        person = await db.get(PersonOrm, id)

        await db.delete(person)

    def _assemble_person_details_orm(self):
        person_details_data = {
            'notes': self.notes,
            'language': self.language,
            'source': self.source,
            'signature': self.signature,
            'viewed_properties': self.viewed_properties
        }
        return PersonDetailsOrm(**person_details_data)
