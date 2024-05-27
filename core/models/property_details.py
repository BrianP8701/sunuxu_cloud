from sqlmodel import Field, SQLModel, Relationship, JSON
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Enum as SqlEnum, Column, Integer, ForeignKey
from datetime import datetime
from core.models.associations import PropertyOwnerAssociation, PropertyOccupantAssociation

if TYPE_CHECKING:
    from core.models.user import UserOrm
    from core.models.property import PropertyOrm
    from core.models.deal import DealOrm
    from core.models.person import PersonOrm

class PropertyDetailsOrm(SQLModel, table=True):
    __tablename__ = "property_details"
    id: Optional[int] = Field(default=None, foreign_key="properties.id", primary_key=True)
    user_id: int = Field(sa_column=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False))

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
    attached_type: Optional[str] = Field(sa_column=SqlEnum("attached", "semi_attached", "detached", name="property_attached_types"))
    section: Optional[str] = None
    school_district: Optional[str] = None
    property_tax: Optional[float] = None

    pictures: Optional[List[str]] = None  # List of picture URLs/ids

    notes: Optional[str] = None
    description: Optional[str] = None

    user: Optional["UserOrm"] = Relationship(back_populates="properties")
    property: Optional["PropertyOrm"] = Relationship(back_populates="property_details", sa_relationship_kwargs={"uselist": False})
    deals: List["DealOrm"] = Relationship(back_populates="property_details")
    owners: List["PersonOrm"] = Relationship(link_model=PropertyOwnerAssociation)
    occupants: List["PersonOrm"] = Relationship(link_model=PropertyOccupantAssociation)
