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

    pictures: Optional[str] = None  # List of picture URLs/ids

    notes: Optional[str] = None
    description: Optional[str] = None

    user: Optional["UserOrm"] = Relationship(back_populates="properties")
    property: Optional["PropertyOrm"] = Relationship(back_populates="property_details", sa_relationship_kwargs={"uselist": False})
    deals: List["DealOrm"] = Relationship(back_populates="property_details")
    owners: List["PersonOrm"] = Relationship(link_model=PropertyOwnerAssociation)
    occupants: List["PersonOrm"] = Relationship(link_model=PropertyOccupantAssociation)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "street_number": self.street_number,
            "street_name": self.street_name,
            "street_suffix": self.street_suffix,
            "city": self.city,
            "unit": self.unit,
            "state": self.state,
            "zip_code": self.zip_code,
            "country": self.country,
            "mls_number": self.mls_number,
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
            "pictures": self.pictures,
            "notes": self.notes,
            "property_tax": self.property_tax,
            "description": self.description,
        }