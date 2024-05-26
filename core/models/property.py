from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Enum as SqlEnum, Column, DateTime
from sqlalchemy.sql import func
from datetime import datetime

from core.enums.property_type import PropertyType
from core.models.associations import UserPropertyAssociation

if TYPE_CHECKING:
    from core.models.user import UserOrm
    from core.models.property_details import PropertyDetailsOrm

class PropertyOrm(SQLModel, table=True):
    __tablename__ = "properties"
    id: Optional[int] = Field(default=None, primary_key=True)

    street_number: str = Field(max_length=255, nullable=False)
    street_name: str = Field(max_length=255, nullable=False)
    street_suffix: str = Field(max_length=255, nullable=False)
    city: str = Field(max_length=255, nullable=False)
    unit: Optional[str] = Field(default=None, max_length=255)
    state: str = Field(max_length=255, nullable=False)
    zip_code: str = Field(max_length=255, nullable=False)
    country: str = Field(max_length=255, nullable=False)
    mls_number: Optional[str] = Field(default=None, max_length=255, index=True)
    type: PropertyType = Field(sa_column=Column(SqlEnum(PropertyType), index=True, nullable=False, default=PropertyType.UNKNOWN))
    custom_type: Optional[str] = Field(default=None, max_length=255, index=True)
    active: bool = Field(default=False, index=True, nullable=False)
    price: Optional[int] = Field(default=None)

    created: datetime = Field(index=True)    
    updated: Optional[datetime] = Field(sa_column=Column(DateTime, index=True, default=None, onupdate=func.now()))
    viewed: Optional[datetime] = Field(index=True)

    users: List["UserOrm"] = Relationship(back_populates="property_rows", link_model=UserPropertyAssociation)
    property_details: Optional["PropertyDetailsOrm"] = Relationship(back_populates="property", sa_relationship_kwargs={"uselist": False, "cascade": "all, delete-orphan"})

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
