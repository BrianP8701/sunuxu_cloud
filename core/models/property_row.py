from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from core.database.abstract_sql import Base
from sqlalchemy.sql import func
from sqlalchemy import Enum

class PropertyRowOrm(Base):
    __tablename__ = "property_rows"
    id = Column(Integer, ForeignKey('properties.id'), primary_key=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    address = Column(String(255), nullable=False, index=True)
    mls_number = Column(String(255), index=True)
    type = Column(
        Enum(
            "residential",
            "condo",
            "coop",
            "commercial",
            "land",
            "hoa",
            "industrial",
            "rental",
            "other",
            "?",
            name="property_types",
        ),
        index=True,
        nullable=False,
        default="?"
    )
    active = Column(Boolean, default=False, index=True)
    price = Column(Integer)

    created = Column(DateTime, default=func.now(), index=True)
    updated = Column(DateTime, default=func.now(), onupdate=func.now(), index=True)
    viewed = Column(DateTime, index=True)

    user = relationship("UserOrm", back_populates="property_rows")
    property = relationship("PropertyOrm", back_populates="summary_row", uselist=False)

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
