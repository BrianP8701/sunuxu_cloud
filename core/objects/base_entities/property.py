from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel

from core.database import Database
from core.enums import PropertyType
from core.models.entities.property import PropertyModel
from core.models.rows.person import PersonRowModel
from core.models.rows.property import PropertyRowModel
from core.objects.base_entities.base_entity import BaseEntity
from core.utils.strings import assemble_address

if TYPE_CHECKING:
    from core.models.associations import UserPropertyAssociation
    from core.objects.rows.deal_row import DealRow
    from core.objects.rows.person_row import PersonRow
    from core.objects.rows.user_row import UserRow


class BaseProperty(BaseEntity):
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
    active: bool
    created: datetime
    updated: Optional[datetime]
    viewed: Optional[datetime]
    user_ids: List[int]

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

    owners: Optional[List[PersonRow]]
    occupants: Optional[List[PersonRow]]
    deals: Optional[List[DealRow]]
    users: Optional[List[UserRow]]

    property_orm: Optional[PropertyRowModel]
    property_details_orm: Optional[PropertyModel]
    deals: Optional[List[DealRow]]

    @classmethod
    async def read(cls, id: int):
        db = Database()
        property_details = await db.read(
            PropertyRowModel,
            id,
            eager_load=["property", "users", "owners", "occupants", "deals"],
        )

        deals = [DealRow.from_orm(deal) for deal in property_details.deals]
        owners = [PersonRow.from_orm(owner) for owner in property_details.owners]
        occupants = [
            PersonRow.from_orm(occupant) for occupant in property_details.occupants
        ]
        users = [UserRow.from_orm(user) for user in property_details.users]

        return cls(
            id=id,
            street_number=property_details.street_number,
            street_name=property_details.street_name,
            street_suffix=property_details.street_suffix,
            city=property_details.city,
            unit=property_details.unit,
            state=property_details.state,
            zip_code=property_details.zip_code,
            country=property_details.country,
            mls_number=property_details.property.mls_number,
            type=property_details.property.type,
            custom_type=property_details.property.custom_type,
            active=property_details.property.active,
            created=property_details.property.created,
            updated=property_details.property.updated,
            viewed=property_details.property.viewed,
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
            owners=owners,
            occupants=occupants,
            users=users,
            property_orm=property_details.property,
            property_details_orm=property_details,
            deals=deals,
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
            "list_start_date": self.list_start_date.isoformat()
            if self.list_start_date
            else None,
            "list_end_date": self.list_end_date.isoformat()
            if self.list_end_date
            else None,
            "expiration_date": self.expiration_date.isoformat()
            if self.expiration_date
            else None,
            "attached_type": self.attached_type,
            "section": self.section,
            "school_district": self.school_district,
            "property_tax": self.property_tax,
            "pictures": self.pictures,
            "notes": self.notes,
            "description": self.description,
            "deals": {
                deal.to_dict(): participant.to_dict()
                for deal, participant in self.deals.items()
            },
            "owners": [owner.to_dict() for owner in self.owners],
            "occupants": [occupant.to_dict() for occupant in self.occupants],
            "users": [user.to_dict() for user in self.users],
        }

    async def create(self):
        """
        Inserts a new property into the database
        Only makes relationships with users here
        """
        db = Database()

        property = self._assemble_property_orm()
        property_details = self._assemble_property_details_orm()

        async with db.get_session() as session:
            property = await db.create(property, session)
            property_details = await db.create(property_details, session)

        self.id = property.id
        self.property_orm = property
        self.property_details_orm = property_details

    async def update(self, **kwargs):
        db = Database()

        property_updates = {}
        property_details_updates = {}

        for key, value in kwargs.items():
            if hasattr(PropertyRowModel, key):
                property_updates[key] = value
            if hasattr(PropertyModel, key):
                property_details_updates[key] = value

        async with db.get_session() as session:
            if property_updates:
                await db.update_fields(
                    PropertyRowModel, self.id, property_updates, session
                )
            if property_details_updates:
                await db.update_fields(
                    PropertyModel, self.id, property_details_updates, session
                )

    @classmethod
    async def delete(cls, id: int):
        db = Database()
        await db.delete_by_id(PropertyRowModel, id)

    async def add_owner(self, person_id: int):
        db = Database()
        property = self.property_orm
        person = await db.read(PersonRowModel, person_id)

        async with db.get_session() as session:
            property.owners.append(person)
            await db.update(property, session)

    async def remove_owner(self, person_id: int):
        db = Database()
        property = self.property_orm
        person = await db.read(PersonRowModel, person_id)

        async with db.get_session() as session:
            property.owners.remove(person)
            await db.update(property, session)

    async def add_occupant(self, person_id: int):
        db = Database()
        property = self.property_orm
        person = await db.read(PersonRowModel, person_id)

        async with db.get_session() as session:
            property.occupants.append(person)
            await db.update(property, session)

    async def remove_occupant(self, person_id: int):
        db = Database()
        property = self.property_orm
        person = await db.read(PersonRowModel, person_id)

        async with db.get_session() as session:
            property.occupants.remove(person)
            await db.update(property, session)

    def _assemble_orm(self):
        property_data = {
            "address": assemble_address(
                self.street_number,
                self.street_name,
                self.street_suffix,
                self.city,
                self.unit,
                self.state,
                self.zip_code,
                self.country,
            ),
            "mls_number": self.mls_number,
            "type": self.type,
            "custom_type": self.custom_type,
            "active": self.active,
            "price": self.price,
            "created": self.created,
            "updated": self.updated,
            "viewed": self.viewed,
            "user_ids": self.user_ids,
        }

        property_details_data = {
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
            "list_start_date": self.list_start_date,
            "list_end_date": self.list_end_date,
            "expiration_date": self.expiration_date,
            "attached_type": self.attached_type,
            "section": self.section,
            "school_district": self.school_district,
            "property_tax": self.property_tax,
            "pictures": self.pictures,
            "notes": self.notes,
            "description": self.description,
        }

        user_associations = [
            UserPropertyAssociation(user_id=user_id, property_id=self.id)
            for user_id in self.user_ids
        ]
        property_details_data["users"] = user_associations

        return PropertyRowModel(**property_data), PropertyModel(**property_details_data)
