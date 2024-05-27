from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Enum as SqlEnum, Column, DateTime
from sqlalchemy.sql import func
from datetime import datetime

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
    unread: bool = Field(default=False, index=True, nullable=False)
    tags: Optional[List[str]] = Field(default=None, index=True)

    last_activity: Optional[datetime] = Field(default=None, index=True)
    last_messaged: Optional[datetime] = Field(default=None, index=True)
    temperature: Optional[int] = Field(default=None, index=True)

    created: datetime = Field(index=True)    
    updated: Optional[datetime] = Field(sa_column=Column(DateTime, index=True, default=None, onupdate=func.now()))
    viewed: Optional[datetime] = Field(index=True)

    users: List["UserOrm"] = Relationship(back_populates="people", link_model=UserPersonAssociation)
    person_details: Optional["PersonDetailsOrm"] = Relationship(
        back_populates="person", 
        sa_relationship_kwargs={"uselist": False, "cascade": "all, delete-orphan"}
    )
