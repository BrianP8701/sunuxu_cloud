from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from core.database.abstract_sql import Base
from sqlalchemy.sql import func
from sqlalchemy import Enum

from core.models.association import property_owner_association_table

class PropertyOrm(Base):
    __tablename__ = "properties"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    street_number = Column(String(255))
    street_name = Column(String(255))
    street_suffix = Column(String(255))
    city = Column(String(255))
    unit_number = Column(String(255))
    state = Column(String(255))
    zip_code = Column(String(255))
    country = Column(String(255))
    
    type = Column(Enum('residential', 'condo', 'coop', 'commercial', 'land', 'hoa', 'industrial', 'rental', 'other', name='property_types'), index=True)
    status = Column(Enum('active', 'inactive', name='property_status'), index=True)

    price = Column(Integer)
    mls_number = Column(String(255))
    bedrooms = Column(Integer)
    bathrooms = Column(Float)
    floors = Column(Integer)
    rooms = Column(Integer)
    kitchens = Column(Integer)
    families = Column(Integer)
    lot_sqft = Column(Integer)
    built_year = Column(Integer)
    list_start_date = Column(DateTime)
    list_end_date = Column(DateTime)
    expiration_date = Column(DateTime)
    attached_type = Column(Enum('attached', 'semi_attached', 'detached', name='property_attached_types'))
    section = Column(String)
    school_district = Column(String)

    pictures = Column(String) # List of picture URLs/ids

    notes = Column(String)
    description = Column(String)

    created = Column(DateTime, default=func.now(), index=True)
    updated = Column(DateTime, onupdate=func.now(), index=True)
    viewed = Column(DateTime, index=True)

    user = relationship("UserOrm", back_populates="properties")
    transactions = relationship("TransactionOrm", back_populates="property")
    owners = relationship("PersonOrm", secondary=property_owner_association_table, back_populates="properties")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "street_number": self.street_number,
            "street_name": self.street_name,
            "street_suffix": self.street_suffix,
            "city": self.city,
            "unit_number": self.unit_number,
            "state": self.state,
            "zip_code": self.zip_code,
            "country": self.country,
            "status": self.status,
            "type": self.type,
            "price": self.price,
            "mls_number": self.mls_number,
            "bedrooms": self.bedrooms,
            "bathrooms": self.bathrooms,
            "floors": self.floors,
            "rooms": self.rooms,
            "kitchens": self.kitchens,
            "families": self.families,
            "lot_sqft": self.lot_sqft,
            "built_year": self.built_year,
            "list_start_date": self.list_start_date,
            "list_end_date": self.list_end_date,
            "expiration_date": self.expiration_date,
            "attached_type": self.attached_type,
            "section": self.section,
            "school_district": self.school_district,
            "pictures": self.pictures,
            "notes": self.notes,
            "description": self.description,
            "created_at": self.created_at,
            "last_updated": self.last_updated,
            "last_viewed": self.last_viewed
        }

    def to_table_row(self) -> dict:
        full_address = f"{self.street_number} {self.street_name} {self.street_suffix if self.street_suffix else ''} {self.unit_number if self.unit_number else ''}, {self.city}, {self.state} {self.zip_code}".replace('  ', ' ')
        return {
            "id": self.id,
            "address": full_address,
            "price": self.price,
            "status": self.status,
            "type": self.type,
        }
