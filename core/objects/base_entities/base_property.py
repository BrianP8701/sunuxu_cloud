from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar

from core.database import Database
from core.enums import PropertyAttachedType, PropertyType
from core.models.entities.property import PropertyModel
from core.models.rows.property import PropertyRowModel
from core.objects.base_entities.base_entity import BaseEntity
from core.utils.strings import assemble_address

if TYPE_CHECKING:
    from core.models.associations import UserPropertyAssociation, PropertyOwnerAssociation, PropertyOccupantAssociation
    from core.objects.rows.deal_row import DealRow
    from core.objects.rows.person_row import PersonRow
    from core.objects.rows.user_row import UserRow

T = TypeVar("T", bound="BaseProperty")


class BaseProperty(BaseEntity):
    id: int

    # Row Fields
    address: str
    mls_number: Optional[str] = None
    type: PropertyType
    active: bool
    created: datetime
    updated: Optional[datetime]
    viewed: Optional[datetime]
    user_ids: List[int]

    # Entity Fields
    street_number: str
    street_name: str
    street_suffix: str
    city: str
    unit: Optional[str] = None
    state: str
    zip_code: str
    country: str

    google_place_id: Optional[str] = None
    mls: Optional[str] = None

    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    floors: Optional[int] = None
    rooms: Optional[int] = None
    kitchens: Optional[int] = None
    families: Optional[int] = None
    lot_sqft: Optional[int] = None
    building_sqft: Optional[int] = None
    year_built: Optional[int] = None
    list_start_date: Optional[datetime] = None
    list_end_date: Optional[datetime] = None
    expiration_date: Optional[datetime] = None
    attached_type: PropertyAttachedType = None
    section: Optional[str] = None
    school_district: Optional[str] = None
    property_tax: Optional[float] = None
    pictures: Optional[List[str]] = None  # List of picture URLs/ids
    notes: Optional[str] = None
    description: Optional[str] = None

    deals: Optional[List["DealRow"]] = []
    owners: Optional[List["PersonRow"]] = []
    occupants: Optional[List["PersonRow"]] = []
    users: Optional[List["UserRow"]] = []

    property_row_model: Optional[PropertyRowModel]
    property_model: Optional[PropertyModel]

    @classmethod
    async def create(cls: Type[T], data: Dict[str, Any]) -> T:
        """
        Creates a new property entry in the database.

        :param data:
            A dictionary containing the property details:
            - 'user_ids' (List[int]): A list of IDs of the users associated with the property. (Required)
            - 'street_number' (str): The street number of the property. (Required)
            - 'street_name' (str): The street name of the property. (Required)
            - 'street_suffix' (str): The street suffix of the property. (Required)
            - 'city' (str): The city where the property is located. (Required)
            - 'state' (str): The state where the property is located. (Required)
            - 'zip_code' (str): The zip code of the property. (Required)
            - 'country' (str): The country where the property is located. (Required)
            - 'unit' (Optional[str]): The unit number of the property. (Optional)
            - 'type' (str): The type of the property. PropertyType enum. (Required)
            - 'owner_ids' (Optional[List[int]]): A list of IDs of the people who own the property. (Optional)
            - 'occupant_ids' (Optional[List[int]]): A list of IDs of the people who occupy the property. (Optional)
            ...
        """
        db = Database()

        address = assemble_address(
            data["street_number"],
            data["street_name"],
            data["street_suffix"],
            data["city"],
            data["state"],
            data["zip_code"],
            data["country"],
            data.get("unit"),
        )

        property_row = PropertyRowModel(
            address=address,
            mls_number=data.get("mls_number"),
            type=PropertyType(data["type"]),
            active=True,
            created=datetime.utcnow(),
            user_ids=data["user_ids"],
        )

        property = PropertyModel(
            street_number=data["street_number"],
            street_name=data["street_name"],
            street_suffix=data["street_suffix"],
            city=data["city"],
            unit=data.get("unit"),
            state=data["state"],
            zip_code=data["zip_code"],
            country=data["country"],
            google_place_id=data.get("google_place_id"),
            mls=data.get("mls"),
            bedrooms=data.get("bedrooms"),
            bathrooms=data.get("bathrooms"),
            floors=data.get("floors"),
            rooms=data.get("rooms"),
            kitchens=data.get("kitchens"),
            families=data.get("families"),
            lot_sqft=data.get("lot_sqft"),
            building_sqft=data.get("building_sqft"),
            year_built=data.get("year_built"),
            list_start_date=data.get("list_start_date"),
            list_end_date=data.get("list_end_date"),
            expiration_date=data.get("expiration_date"),
            attached_type=PropertyAttachedType(data.get("attached_type")) if data.get("attached_type") else None,
            section=data.get("section"),
            school_district=data.get("school_district"),
            property_tax=data.get("property_tax"),
            pictures=data.get("pictures"),
            notes=data.get("notes"),
            description=data.get("description"),
        )

        user_associations = [
            UserPropertyAssociation(user_id=user_id, property_id=property.id)
            for user_id in data["user_ids"]
        ]
        
        # Prepare owner associations if any
        owner_associations = [
            PropertyOwnerAssociation(property_id=property.id, person_id=owner_id)
            for owner_id in data.get("owner_ids", [])
        ]

        # Prepare occupant associations if any
        occupant_associations = [
            PropertyOccupantAssociation(property_id=property.id, person_id=occupant_id)
            for occupant_id in data.get("occupant_ids", [])
        ]

        async with db.get_session() as session:
            try:
                await db.create(PropertyRowModel, property_row, session)
                property.row = property_row
                await db.create(PropertyModel, property, session)
                await db.batch_add_associations(user_associations, session)
                await db.batch_add_associations(owner_associations + occupant_associations, session)  # Add this line
            except Exception as e:
                await session.rollback()
                raise e
            else:
                await session.commit()

        return await cls.read(property.id)

    @classmethod
    async def read(cls: Type[T], id: int) -> T:
        db = Database()

        async with db.get_session() as session:
            try:
                property = await db.read(
                    PropertyModel,
                    id,
                    eager_load=[
                        "row",
                        "deals.row",
                        "owners.row",
                        "occupants.row",
                        "users.row",
                    ],
                )
                await db.update_fields(
                    PropertyRowModel,
                    property.id,
                    {"viewed": datetime.utcnow()},
                    session,
                )
            except Exception as e:
                await session.rollback()
                raise e
            else:
                await session.commit()

        deals = [DealRow.from_model(deal.row) for deal in property.deals]
        owners = [PersonRow.from_model(owner.row) for owner in property.owners]
        occupants = [
            PersonRow.from_model(occupant.row) for occupant in property.occupants
        ]
        users = [UserRow.from_model(user.row) for user in property.users]

        return cls(
            id=property.id,
            address=property.row.address,
            mls_number=property.row.mls_number,
            type=property.row.type,
            active=property.row.active,
            created=property.row.created,
            updated=property.row.updated,
            viewed=property.row.viewed,
            user_ids=property.row.user_ids,
            street_number=property.street_number,
            street_name=property.street_name,
            street_suffix=property.street_suffix,
            city=property.city,
            unit=property.unit,
            state=property.state,
            zip_code=property.zip_code,
            country=property.country,
            google_place_id=property.google_place_id,
            mls=property.mls,
            bedrooms=property.bedrooms,
            bathrooms=property.bathrooms,
            floors=property.floors,
            rooms=property.rooms,
            kitchens=property.kitchens,
            families=property.families,
            lot_sqft=property.lot_sqft,
            building_sqft=property.building_sqft,
            year_built=property.year_built,
            list_start_date=property.list_start_date,
            list_end_date=property.list_end_date,
            expiration_date=property.expiration_date,
            attached_type=property.attached_type,
            section=property.section,
            school_district=property.school_district,
            property_tax=property.property_tax,
            pictures=property.pictures,
            notes=property.notes,
            description=property.description,
            deals=deals,
            owners=owners,
            occupants=occupants,
            users=users,
            property_row_model=property.row,
            property_model=property,
        )

    @classmethod
    async def update(cls: Type[T], id: int, updates: Dict[str, Any]) -> T:
        """
        Updates row by replacing columns with values specified in updates.

        :param updates:
            A dictionary containing the property details to update:
            - 'street_number' (Optional[str]): The street number of the property. (Optional)
            - 'street_name' (Optional[str]): The street name of the property. (Optional)
            - 'street_suffix' (Optional[str]): The street suffix of the property. (Optional)
            - 'city' (Optional[str]): The city where the property is located. (Optional)
            - 'state' (Optional[str]): The state where the property is located. (Optional)
            - 'zip_code' (Optional[str]): The zip code of the property. (Optional)
            - 'country' (Optional[str]): The country where the property is located. (Optional)
            - 'unit' (Optional[str]): The unit number of the property. (Optional)
            - 'mls_number' (Optional[str]): The MLS number of the property. (Optional)
            - 'type' (Optional[str]): The type of the property. PropertyType enum. (Optional)
            - 'google_place_id' (Optional[str]): The Google Place ID of the property. (Optional)
            - 'mls' (Optional[str]): The MLS of the property. (Optional)
            - 'bedrooms' (Optional[int]): The number of bedrooms in the property. (Optional)
            - 'bathrooms' (Optional[int]): The number of bathrooms in the property. (Optional)
            - 'floors' (Optional[int]): The number of floors in the property. (Optional)
            - 'rooms' (Optional[int]): The number of rooms in the property. (Optional)
            - 'kitchens' (Optional[int]): The number of kitchens in the property. (Optional)
            - 'families' (Optional[int]): The number of families the property can accommodate. (Optional)
            - 'lot_sqft' (Optional[int]): The lot size in square feet. (Optional)
            - 'building_sqft' (Optional[int]): The building size in square feet. (Optional)
            - 'year_built' (Optional[int]): The year the property was built. (Optional)
            - 'list_start_date' (Optional[datetime]): The start date of the listing. (Optional)
            - 'list_end_date' (Optional[datetime]): The end date of the listing. (Optional)
            - 'expiration_date' (Optional[datetime]): The expiration date of the listing. (Optional)
            - 'attached_type' (Optional[str]): The attached type of the property. PropertyAttachedType enum. (Optional)
            - 'section' (Optional[str]): The section of the property. (Optional)
            - 'school_district' (Optional[str]): The school district of the property. (Optional)
            - 'property_tax' (Optional[float]): The property tax amount. (Optional)
            - 'pictures' (Optional[List[str]]): A list of picture URLs/ids. (Optional)
            - 'notes' (Optional[str]): Additional notes regarding the property. (Optional)
            - 'description' (Optional[str]): A description of the property. (Optional)
        """
        db = Database()

        property_updates = {}
        property_details_updates = {}

        for key, value in updates.items():
            if hasattr(PropertyRowModel, key):
                if key == "type":
                    property_updates[key] = PropertyType(value)
                else:
                    property_updates[key] = value
            if hasattr(PropertyModel, key):
                if key == "attached_type":
                    property_details_updates[key] = PropertyAttachedType(value)
                else:
                    property_details_updates[key] = value

        # Check if address components are being updated
        if any(
            key in updates
            for key in [
                "street_number",
                "street_name",
                "street_suffix",
                "city",
                "state",
                "zip_code",
                "country",
                "unit",
            ]
        ):
            # Fetch the current property details to assemble the new address
            async with db.get_session() as session:
                property = await db.read(PropertyModel, id, session=session)
                street_number = updates.get("street_number", property.street_number)
                street_name = updates.get("street_name", property.street_name)
                street_suffix = updates.get("street_suffix", property.street_suffix)
                city = updates.get("city", property.city)
                state = updates.get("state", property.state)
                zip_code = updates.get("zip_code", property.zip_code)
                country = updates.get("country", property.country)
                unit = updates.get("unit", property.unit)
                property_updates["address"] = assemble_address(
                    street_number,
                    street_name,
                    street_suffix,
                    city,
                    state,
                    zip_code,
                    country,
                    unit,
                )

        async with db.get_session() as session:
            try:
                if property_updates:
                    await db.update_fields(
                        PropertyRowModel, id, property_updates, session
                    )
                if property_details_updates:
                    await db.update_fields(
                        PropertyModel, id, property_details_updates, session
                    )
            except Exception as e:
                await session.rollback()
                raise e
            else:
                await session.commit()

        return await cls.read(id)

    @classmethod
    async def delete(cls: Type[T], id: int) -> None:
        """Delete a property entry"""
        db = Database()
        async with db.get_session() as session:
            try:
                await db.delete_by_id(PropertyRowModel, id, session)
            except Exception as e:
                await session.rollback()
                raise e
            else:
                await session.commit()

    @classmethod
    async def batch_create(cls, data: List[Dict[str, Any]]) -> List[T]:
        """
        Create multiple properties for multiple users.

        :param data:
            A list of dictionaries, each containing the data to be created for the property.
        """
        db = Database()
        properties = []
        property_rows = []
        user_associations = []
        owner_associations = []
        occupant_associations = []

        for property_data in data:
            address = assemble_address(
                property_data["street_number"],
                property_data["street_name"],
                property_data["street_suffix"],
                property_data["city"],
                property_data["state"],
                property_data["zip_code"],
                property_data["country"],
                property_data.get("unit"),
            )

            property_row = PropertyRowModel(
                address=address,
                mls_number=property_data.get("mls_number"),
                type=PropertyType(property_data["type"]),
                active=True,
                created=datetime.utcnow(),
                user_ids=property_data["user_ids"],
            )
            property_rows.append(property_row)

            property = PropertyModel(
                street_number=property_data["street_number"],
                street_name=property_data["street_name"],
                street_suffix=property_data["street_suffix"],
                city=property_data["city"],
                unit=property_data.get("unit"),
                state=property_data["state"],
                zip_code=property_data["zip_code"],
                country=property_data["country"],
                google_place_id=property_data.get("google_place_id"),
                mls=property_data.get("mls"),
                bedrooms=property_data.get("bedrooms"),
                bathrooms=property_data.get("bathrooms"),
                floors=property_data.get("floors"),
                rooms=property_data.get("rooms"),
                kitchens=property_data.get("kitchens"),
                families=property_data.get("families"),
                lot_sqft=property_data.get("lot_sqft"),
                building_sqft=property_data.get("building_sqft"),
                year_built=property_data.get("year_built"),
                list_start_date=property_data.get("list_start_date"),
                list_end_date=property_data.get("list_end_date"),
                expiration_date=property_data.get("expiration_date"),
                attached_type=PropertyAttachedType(property_data.get("attached_type")) if property_data.get("attached_type") else None,
                section=property_data.get("section"),
                school_district=property_data.get("school_district"),
                property_tax=property_data.get("property_tax"),
                pictures=property_data.get("pictures"),
                notes=property_data.get("notes"),
                description=property_data.get("description"),
            )
            properties.append(property)

            for user_id in property_data["user_ids"]:
                user_associations.append(UserPropertyAssociation(user_id=user_id, property_id=property.id))

            for owner_id in property_data.get("owner_ids", []):
                owner_associations.append(PropertyOwnerAssociation(property_id=property.id, person_id=owner_id))

            for occupant_id in property_data.get("occupant_ids", []):
                occupant_associations.append(PropertyOccupantAssociation(property_id=property.id, person_id=occupant_id))

        async with db.get_session() as session:
            try:
                await db.batch_create(property_rows, session)
                for property, property_row in zip(properties, property_rows):
                    property.row = property_row
                await db.batch_create(properties, session)
                await db.batch_add_associations(user_associations + owner_associations + occupant_associations, session)
            except Exception as e:
                await session.rollback()
                raise e
            else:
                await session.commit()

        return [await cls.read(property.id) for property in properties]

    @classmethod
    async def batch_delete(cls, ids: List[int]) -> None:
        """
        Delete multiple properties by their IDs.

        :param ids:
            A list of property IDs to delete.
        """
        db = Database()
        async with db.get_session() as session:
            try:
                await db.batch_delete(PropertyModel, {"id": ids}, session)
            except Exception as e:
                await session.rollback()
                raise e
            else:
                await session.commit()


    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "address": self.address,
            "mls_number": self.mls_number,
            "type": self.type.value,
            "active": self.active,
            "created": self.created.isoformat() if self.created else None,
            "updated": self.updated.isoformat() if self.updated else None,
            "viewed": self.viewed.isoformat() if self.viewed else None,
            "user_ids": self.user_ids,
            "street_number": self.street_number,
            "street_name": self.street_name,
            "street_suffix": self.street_suffix,
            "city": self.city,
            "unit": self.unit,
            "state": self.state,
            "zip_code": self.zip_code,
            "country": self.country,
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
            "attached_type": self.attached_type.value if self.attached_type else None,
            "section": self.section,
            "school_district": self.school_district,
            "property_tax": self.property_tax,
            "pictures": self.pictures,
            "notes": self.notes,
            "description": self.description,
            "deals": [deal.to_dict() for deal in self.deals] if self.deals else [],
            "owners": [owner.to_dict() for owner in self.owners] if self.owners else [],
            "occupants": [occupant.to_dict() for occupant in self.occupants]
            if self.occupants
            else [],
            "users": [user.to_dict() for user in self.users] if self.users else [],
        }
