from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Enum as SqlEnum, Column, DateTime, Index
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

from core.enums.person_type import PersonType

if TYPE_CHECKING:
    from core.models.entities.person import PersonOrm

class PersonRowOrm(SQLModel, table=True):
    __tablename__ = "person_rows"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    name: str = Field(max_length=255, nullable=False, index=True)
    email: Optional[str] = Field(default=None, index=True)
    phone: Optional[str] = Field(default=None, index=True)
    type: PersonType = Field(sa_column=Column(SqlEnum(PersonType, name='person_type_enum', nullable=False), default="?", index=True)) 
    active: bool = Field(default=False, index=True, nullable=False)
    last_activity: Optional[datetime] = Field(default=None, index=True)

    # With IDX site we can have these
    # last_activity: Optional[datetime] = Field(default=None, index=True)
    # temperature: Optional[int] = Field(default=None, index=True)

    created: datetime = Field(index=True)    
    updated: Optional[datetime] = Field(sa_column=Column(DateTime, index=True, default=None, onupdate=func.now()))
    viewed: Optional[datetime] = Field(index=True)

    user_ids: List[int] = Field(sa_column=Column(JSONB), default=[])

    __table_args__ = (
        Index('person_user_ids', 'user_ids', postgresql_using='gin'),
    )
