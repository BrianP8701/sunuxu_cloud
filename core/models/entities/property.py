from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import JSON, Column
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, Integer
from sqlmodel import Field, Relationship, SQLModel

from core.enums.property_attached_type import PropertyAttachedType
from core.models.associations import (PropertyOccupantAssociation,
                                      PropertyOwnerAssociation,
                                      UserPropertyAssociation)

if TYPE_CHECKING:
    from core.models.entities.deal import DealModel
    from core.models.entities.person import PersonModel
    from core.models.entities.user import UserModel
    from core.models.rows.property import PropertyRowModel


class PropertyModel(SQLModel, table=True):
    __tablename__ = "properties"
    id: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, ForeignKey("property_rows.id"), primary_key=True)
    )

    # All the deals associated with the property
    deals: List["DealModel"] = Relationship(back_populates="property")

    # Many to many, one property can have many owners and occupants
    owners: List["PersonModel"] = Relationship(
        link_model=PropertyOwnerAssociation,
        sa_relationship_kwargs={"cascade": "all", "overlaps": "portfolio"}
    )
    occupants: List["PersonModel"] = Relationship(
        link_model=PropertyOccupantAssociation,
        sa_relationship_kwargs={"cascade": "all"},
    )

    users: List["UserModel"] = Relationship(
        back_populates="properties",
        link_model=UserPropertyAssociation,
        sa_relationship_kwargs={"cascade": "all"},
    )
    row: "PropertyRowModel" = Relationship(
        sa_relationship_kwargs={
            "uselist": False,
            "single_parent": True,
            "cascade": "all, delete-orphan",
            "back_populates": None
        }
    )

    street_number: str = Field(max_length=255, nullable=False)
    street_name: str = Field(max_length=255, nullable=False)
    street_suffix: str = Field(max_length=255, nullable=False)
    city: str = Field(max_length=255, nullable=False)
    unit: Optional[str] = Field(default=None, max_length=255)
    state: str = Field(max_length=255, nullable=False)
    zip_code: str = Field(max_length=255, nullable=False)
    country: str = Field(max_length=255, nullable=False)

    google_place_id: Optional[str] = Field(default=None, max_length=255)
    mls: Optional[str] = Field(default=None)

    bedrooms: Optional[int] = None
    bathrooms: Optional[float] = None
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

    attached_type: Optional[PropertyAttachedType] = Field(
        sa_column=Column(
            SqlEnum(PropertyAttachedType, name="property_attached_types"), default=None
        )
    )
    section: Optional[str] = None
    school_district: Optional[str] = None
    property_tax: Optional[float] = None

    pictures: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))

    notes: Optional[str] = None
    description: Optional[str] = None
