from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    Enum as SqlEnum,
)
from sqlalchemy.orm import relationship
from core.database.abstract_sql import Base
from sqlalchemy.sql import func

from core.enums.property_type import PropertyType
from core.models.associations import user_property_association


class PropertyOrm(Base):
    __tablename__ = "properties"
    id = Column(Integer, primary_key=True)

    street_number = Column(String(255), nullable=False)
    street_name = Column(String(255), nullable=False)
    street_suffix = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    unit = Column(String(255))
    state = Column(String(255), nullable=False)
    zip_code = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)    
    mls_number = Column(String(255), index=True)
    type = Column(
        SqlEnum(PropertyType), index=True, nullable=False, default=PropertyType.UNKNOWN
    )
    custom_type = Column(String(255), index=True)
    active = Column(Boolean, default=False, index=True, nullable=False)
    price = Column(Integer)

    created = Column(DateTime, default=func.now(), index=True)
    updated = Column(DateTime, default=func.now(), onupdate=func.now(), index=True)
    viewed = Column(DateTime, index=True)

    users = relationship("UserOrm", secondary=user_property_association, back_populates="property_rows")
    property_details = relationship(
        "PropertyDetailsOrm", back_populates="property", uselist=False, cascade="all, delete-orphan"
    )


    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "address": self.address,
            "active": self.active,
            "type": self.type,
            "price": self.price,
            "created": self.created.isoformat() if self.created else None,
            "updated": self.updated.isoformat() if self.updated else None,
            "viewed": self.viewed.isoformat() if self.viewed else None,
        }

    def to_table_row(self) -> dict:
        full_address = f"{self.street_number} {self.street_name} {self.street_suffix if self.street_suffix else ''} {self.unit if self.unit else ''}, {self.city}, {self.state} {self.zip_code}".replace(
            "  ", " "
        )
        return {
            "id": self.id,
            "address": full_address,
            "price": self.price,
            "status": self.status,
            "type": self.type,
        }
