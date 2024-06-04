from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Enum as SqlEnum, Column, DateTime, Index
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB

from core.enums.property_type import PropertyType

class PropertyRowOrm(SQLModel, table=True):
    __tablename__ = "property_rows"
    id: Optional[int] = Field(default=None, primary_key=True)

    address: str = Field(max_length=255, nullable=False, index=True)
    mls_number: Optional[str] = Field(default=None, max_length=255, index=True)
    type: PropertyType = Field(sa_column=Column(SqlEnum(PropertyType), index=True, nullable=False, default=PropertyType.UNKNOWN))
    active: bool = Field(default=False, index=True, nullable=False)

    created: datetime = Field(index=True)    
    updated: Optional[datetime] = Field(sa_column=Column(DateTime, index=True, default=None, onupdate=func.now()))
    viewed: Optional[datetime] = Field(index=True)

    user_ids: List[int] = Field(sa_column=Column(JSONB), default=[])

    __table_args__ = (
        Index('property_user_ids', 'user_ids', postgresql_using='gin'),
    )
