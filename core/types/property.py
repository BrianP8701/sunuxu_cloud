from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from core.models.property import PropertyOrm
from core.models.property_details import PropertyDetailsOrm
from core.database import Database
from core.types.deal_row import DealRow
from core.enums import PropertyType
from core.models.person import PersonOrm

class Property(BaseModel):
    id: int
    street_number: str
    street_name: str
    street_suffix: str
    city: str
    unit: Optional[str]
    state: str
    zip_code: str
    country: str
    mls_number: Optional[str]
    type: PropertyType
    custom_type: Optional[str]
    active: bool
    price: Optional[int]
    created: datetime
    updated: Optional[datetime]
    viewed: Optional[datetime]

    google_place_id: Optional[str]
    mls: Optional[str]
    bedrooms: Optional[int]
    bathrooms: Optional[int]
    floors: Optional[int]
    rooms: Optional[int]
    kitchens: Optional[int]
    families: Optional[int]
    lot_sqft: Optional[int]
    building_sqft: Optional[int]
    year_built: Optional[int]
    list_start_date: Optional[datetime]
    list_end_date: Optional[datetime]
    expiration_date: Optional[datetime]
    attached_type: Optional[str]
    section: Optional[str]
    school_district: Optional[str]
    property_tax: Optional[float]
    pictures: Optional[List[str]]  # List of picture URLs/ids
    notes: Optional[str]
    description: Optional[str]

    property_orm: Optional[PropertyOrm]
    property_details_orm: Optional[PropertyDetailsOrm]
    deals: Optional[List[DealRow]]

    @classmethod
    async def get(cls, id: int):
        db = Database()
        property = await db.get(PropertyOrm, id)
        property_details = await db.get(PropertyDetailsOrm, id)

        deals = [DealRow.from_orm(deal) for deal in property_details.deals]

        return cls(
            id=property.id,
            street_number=property.street_number,
            street_name=property.street_name,
            street_suffix=property.street_suffix,
            city=property.city,
            unit=property.unit,
            state=property.state,
            zip_code=property.zip_code,
            country=property.country,
            mls_number=property.mls_number,
            type=property.type,
            custom_type=property.custom_type,
            active=property.active,
            price=property.price,
            created=property.created,
            updated=property.updated,
            viewed=property.viewed,
            google_place_id=property_details.google_place_id,
            mls=property_details.mls,
            bedrooms=property_details.bedrooms,
            bathrooms=property_details.bathrooms,
            floors=property_details.floors,
            rooms=property_details.rooms,
            kitchens=property_details.kitchens,
            families=property_details.families,
            lot_sqft=property_details.lot_sqft,
            building_sqft=property_details.building_sqft,
            year_built=property_details.year_built,
            list_start_date=property_details.list_start_date,
            list_end_date=property_details.list_end_date,
            expiration_date=property_details.expiration_date,
            attached_type=property_details.attached_type,
            section=property_details.section,
            school_district=property_details.school_district,
            property_tax=property_details.property_tax,
            pictures=property_details.pictures,
            notes=property_details.notes,
            description=property_details.description,
            property_orm=property,
            property_details_orm=property_details,
            deals=deals
        )

    def to_dict(self):
        return {
            "id": self.id,
            "street_number": self.street_number,
            "street_name": self.street_name,
            "street_suffix": self.street_suffix,
            "city": self.city,
            "unit": self.unit,
            "state": self.state,
            "zip_code": self.zip_code,
            "country": self.country,
            "mls_number": self.mls_number,
            "type": self.type,
            "custom_type": self.custom_type,
            "active": self.active,
            "price": self.price,
            "created": self.created.isoformat() if self.created else None,
            "updated": self.updated.isoformat() if self.updated else None,
            "viewed": self.viewed.isoformat() if self.viewed else None,
            "google_place_id": self.google_place_id,
            "mls": self.mls,
            "bedrooms": self.bedrooms,
            "bathrooms": self.bathrooms,
            "floors": self.floors,
            "rooms": self.rooms,
            "kitchens": self.kitchens,
            "families": self.families,
            "lot_sqft": self.lot_sqft,
            "building_sqft": self.building_sqft,
            "year_built": self.year_built,
            "list_start_date": self.list_start_date.isoformat() if self.list_start_date else None,
            "list_end_date": self.list_end_date.isoformat() if self.list_end_date else None,
            "expiration_date": self.expiration_date.isoformat() if self.expiration_date else None,
            "attached_type": self.attached_type,
            "section": self.section,
            "school_district": self.school_district,
            "property_tax": self.property_tax,
            "pictures": self.pictures,
            "notes": self.notes,
            "description": self.description,
            "deals": {deal.to_dict(): participant.to_dict() for deal, participant in self.deals.items()}
        }

    async def insert(self):
        db = Database()

        property = self._assemble_property_orm()
        property_details = self._assemble_property_details_orm()

        async with db.get_session() as session:
            property = await db.insert(property, session)
            property_details = await db.insert(property_details, session)

        self.id = property.id
        self.property_orm = property
        self.property_details_orm = property_details

    async def update(self, **kwargs):
        db = Database()
        property = self.property_orm
        property_details = self.property_details_orm

        property_changed = False
        property_details_changed = False
        for key, value in kwargs.items():
            if hasattr(property, key):
                setattr(property, key, value)
                property_changed = True
            if hasattr(property_details, key):
                setattr(property_details, key, value)
                property_details_changed = True

        async with db.get_session() as session:
            if property_changed:
                await db.update(property, session)
            if property_details_changed:
                await db.update(property_details, session)

    @classmethod
    async def delete(cls, id: int):
        db = Database()
        property = await db.get(PropertyOrm, id)

        await db.delete(property)

    async def add_owner(self, person_id: int):
        db = Database()
        property = self.property_orm
        person = await db.get(PersonOrm, person_id)

        async with db.get_session() as session:
            property.owners.append(person)
            await db.update(property, session)

    async def remove_owner(self, person_id: int):
        db = Database()
        property = self.property_orm
        person = await db.get(PersonOrm, person_id)

        async with db.get_session() as session:
            property.owners.remove(person)
            await db.update(property, session)

    async def add_occupant(self, person_id: int):
        db = Database()
        property = self.property_orm
        person = await db.get(PersonOrm, person_id)

        async with db.get_session() as session:
            property.occupants.append(person)
            await db.update(property, session)

    async def remove_occupant(self, person_id: int):
        db = Database()
        property = self.property_orm
        person = await db.get(PersonOrm, person_id)

        async with db.get_session() as session:
            property.occupants.remove(person)
            await db.update(property, session)

    def _assemble_property_orm(self):
        property_data = {
            'street_number': self.street_number,
            'street_name': self.street_name,
            'street_suffix': self.street_suffix,
            'city': self.city,
            'unit': self.unit,
            'state': self.state,
            'zip_code': self.zip_code,
            'country': self.country,
            'mls_number': self.mls_number,
            'type': self.type,
            'custom_type': self.custom_type,
            'active': self.active,
            'price': self.price,
            'created': self.created,
            'updated': self.updated,
            'viewed': self.viewed
        }
        return PropertyOrm(**property_data)

    def _assemble_property_details_orm(self):
        property_details_data = {
            'google_place_id': self.google_place_id,
            'mls': self.mls,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'floors': self.floors,
            'rooms': self.rooms,
            'kitchens': self.kitchens,
            'families': self.families,
            'lot_sqft': self.lot_sqft,
            'building_sqft': self.building_sqft,
            'year_built': self.year_built,
            'list_start_date': self.list_start_date,
            'list_end_date': self.list_end_date,
            'expiration_date': self.expiration_date,
            'attached_type': self.attached_type,
            'section': self.section,
            'school_district': self.school_district,
            'property_tax': self.property_tax,
            'pictures': self.pictures,
            'notes': self.notes,
            'description': self.description
        }
        return PropertyDetailsOrm(**property_details_data)
