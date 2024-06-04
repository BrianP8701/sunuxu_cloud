from sqlmodel import Field, SQLModel
from typing import Optional, List
from datetime import datetime
from sqlalchemy import Column, DateTime, func, Enum as SqlEnum
from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import JSONB

from core.enums.deal_type import DealType
from core.enums.deal_status import DealStatus

class DealRowOrm(SQLModel, table=True):
    __tablename__ = "deal_rows"
    id: Optional[int] = Field(default=None, primary_key=True)

    is_listing: bool = Field(index=True) # True if listing or dual, False if transaction
    address: Optional[str] = Field(max_length=255, index=True) # Address of listing being bought or sold
    name: Optional[str] = Field(max_length=255, index=True) # Name of buyer if transaction, seller if listing or dual

    status: DealStatus = Field(sa_column=Column(SqlEnum(DealStatus), default=DealStatus.UNKNOWN, nullable=False, index=True))
    type: DealType = Field(sa_column=Column(SqlEnum(DealType), default=DealType.UNKNOWN, nullable=False, index=True))

    created: datetime = Field(index=True)    
    updated: Optional[datetime] = Field(sa_column=Column(DateTime, index=True, default=None, onupdate=func.now()))
    viewed: Optional[datetime] = Field(index=True)

    user_ids: List[int] = Field(sa_column=Column(JSONB), default=[])

    __table_args__ = (
        Index('deal_user_ids', 'user_ids', postgresql_using='gin'),
    )
