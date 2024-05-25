from sqlmodel import Field, SQLModel, Relationship, DateTime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.sql import func

from core.enums.person_type import PersonType
from core.models.associations import UserPersonAssociation

if TYPE_CHECKING:
    from core.models.user import User
    from core.models.person_details import PersonDetails
    from core.models.user import User

class Person(SQLModel, table=True):
    __tablename__ = "people"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    first_name: str = Field(max_length=255, nullable=False, index=True)
    middle_name: Optional[str] = Field(default=None, max_length=255)
    last_name: str = Field(max_length=255, nullable=False, index=True)    
    email: Optional[str] = Field(default=None, index=True)
    phone: Optional[str] = Field(default=None, index=True)
    type: PersonType = Field(sa_column=SqlEnum(PersonType), index=True, nullable=False, default="?")
    custom_type: Optional[str] = Field(default=None, index=True)
    active: bool = Field(default=False, index=True, nullable=False)
    unread_message: bool = Field(default=False, index=True, nullable=False)

    last_activity: Optional[DateTime] = Field(default=None, index=True)
    last_messaged: Optional[DateTime] = Field(default=None, index=True)
    temperature: Optional[int] = Field(default=None, index=True)

    created: Optional[DateTime] = Field(default=func.now(), index=True)
    updated: Optional[DateTime] = Field(default=func.now(), sa_column_kwargs={"onupdate": func.now()}, index=True)
    viewed: Optional[DateTime] = Field(default=None, index=True)

    signature: Optional[bytes] = Field(default=None)

    users: List["User"] = Relationship(back_populates="people", link_model=UserPersonAssociation)
    person_details: Optional["PersonDetails"] = Relationship(
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
