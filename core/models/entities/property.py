from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Enum as SqlEnum, Column, Integer, ForeignKey, JSON
from datetime import datetime

from core.models.associations import UserPropertyAssociation
from core.models.associations import PropertyOwnerAssociation, PropertyOccupantAssociation
from core.enums.property_attached_type import PropertyAttachedType

if TYPE_CHECKING:
    from core.models.entities.user import UserOrm
    from core.models.rows.property import PropertyRowOrm
    from core.models.rows.deal import DealRowOrm
    from core.models.rows.person import PersonRowOrm

class PropertyOrm(SQLModel, table=True):
    __tablename__ = "properties"
    id: Optional[int] = Field(default=None, sa_column=Column(Integer, ForeignKey("properties.id", ondelete="CASCADE"), primary_key=True))

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

    attached_type: Optional[PropertyAttachedType] = Field(sa_column=Column(SqlEnum(PropertyAttachedType, name="property_attached_types"), default=None))
    section: Optional[str] = None
    school_district: Optional[str] = None
    property_tax: Optional[float] = None

    pictures: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))

    notes: Optional[str] = None
    description: Optional[str] = None

    users: List["UserOrm"] = Relationship(back_populates="properties", link_model=UserPropertyAssociation)
    deals: List["DealRowOrm"] = Relationship()
    owners: List["PersonRowOrm"] = Relationship(link_model=PropertyOwnerAssociation)
    occupants: List["PersonRowOrm"] = Relationship(link_model=PropertyOccupantAssociation)
