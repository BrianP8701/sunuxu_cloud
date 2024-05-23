from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, JSON, Enum as SqlEnum
from sqlalchemy.orm import relationship
from core.database.abstract_sql import Base
from sqlalchemy import Enum

from core.models.associations import property_owner_association, property_occupant_association
from core.enums.mls import MLS

class PropertyDetailsOrm(Base):
    __tablename__ = "property_details"
    id = Column(Integer, ForeignKey("properties.id"), primary_key=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    google_place_id = Column(String(255))
    mls = Column(SqlEnum(MLS))
    mls_data = Column(JSON)

    bedrooms = Column(Integer)
    bathrooms = Column(Float)
    floors = Column(Integer)
    rooms = Column(Integer)
    kitchens = Column(Integer)
    families = Column(Integer)
    lot_sqft = Column(Integer)
    building_sqft = Column(Integer)
    year_built = Column(Integer)
    list_start_date = Column(DateTime)
    list_end_date = Column(DateTime)
    expiration_date = Column(DateTime)
    attached_type = Column(
        Enum("attached", "semi_attached", "detached", name="property_attached_types")
    )
    section = Column(String)
    school_district = Column(String)
    property_tax = Column(Float)

    pictures = Column(String)  # List of picture URLs/ids

    notes = Column(String)
    description = Column(String)

    user = relationship("UserOrm", back_populates="properties")
    property = relationship("PropertyOrm", back_populates="property_details", uselist=False)
    deals = relationship("DealOrm", back_populates="property_details")
    owners = relationship("PersonOrm", secondary=property_owner_association)
    occupants = relationship("PersonOrm", secondary=property_occupant_association)

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
