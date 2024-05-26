from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Enum as SqlEnum, Column, DateTime
from sqlalchemy.sql import func
from datetime import datetime
from pydantic import ConfigDict

from core.enums.person_type import PersonType
from core.models.associations import UserPersonAssociation

if TYPE_CHECKING:
    from core.models.user import UserOrm
    from core.models.person_details import PersonDetailsOrm

class PersonOrm(SQLModel, table=True):
    __tablename__ = "people"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    first_name: str = Field(max_length=255, nullable=False, index=True)
    middle_name: Optional[str] = Field(default=None, max_length=255)
    last_name: str = Field(max_length=255, nullable=False, index=True)    
    email: Optional[str] = Field(default=None, index=True)
    phone: Optional[str] = Field(default=None, index=True)
    type: PersonType = Field(sa_column=Column(SqlEnum(PersonType, name='person_type_enum', nullable=False), default="?", index=True)) 
    custom_type: Optional[str] = Field(default=None, index=True)
    active: bool = Field(default=False, index=True, nullable=False)
    unread_message: bool = Field(default=False, index=True, nullable=False)

    last_activity: Optional[datetime] = Field(default=None, index=True)
    last_messaged: Optional[datetime] = Field(default=None, index=True)
    temperature: Optional[int] = Field(default=None, index=True)

    created: datetime = Field(index=True)    
    updated: Optional[datetime] = Field(sa_column=Column(DateTime, index=True, default=None, onupdate=func.now()))
    viewed: Optional[datetime] = Field(index=True)

    signature: Optional[bytes] = Field(default=None)

    users: List["UserOrm"] = Relationship(back_populates="people", link_model=UserPersonAssociation)
    person_details: Optional["PersonDetailsOrm"] = Relationship(
        back_populates="person", 
        sa_relationship_kwargs={"uselist": False, "cascade": "all, delete-orphan"}
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "type": self.type,
            "active": self.active,
            "created": self.created.isoformat() if self.created else None,
            "updated": self.updated.isoformat() if self.updated else None,
            "viewed": self.viewed.isoformat() if self.viewed else None,
        }

    def to_table_row(self) -> dict:
        full_name = f"{self.first_name} {self.middle_name if self.middle_name else ''} {self.last_name}".replace(
            "  ", " "
        )
        return {
            "id": self.id,
            "name": full_name,
            "phone": self.phone,
            "email": self.email,
            "type": self.type,
        }
