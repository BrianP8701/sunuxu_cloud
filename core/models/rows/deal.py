from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Index, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel

from core.enums.deal_category import DealCategory
from core.enums.deal_status import DealStatus
from core.enums.deal_type import DealType


class DealRowModel(SQLModel, table=True):
    __tablename__ = "deal_rows"
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str  # Address if category is dual or sell, names of buyers if category is buy

    category: DealCategory = Field(
        sa_column=Column(SqlEnum(DealCategory), nullable=False, index=True)
    )
    status: DealStatus = Field(
        sa_column=Column(
            SqlEnum(DealStatus), default=DealStatus.UNKNOWN, nullable=False, index=True
        )
    )
    type: DealType = Field(
        sa_column=Column(
            SqlEnum(DealType), default=DealType.UNKNOWN, nullable=False, index=True
        )
    )

    created: datetime = Field(index=True)
    updated: Optional[datetime] = Field(
        sa_column=Column(DateTime, index=True, default=None, onupdate=func.now())
    )
    viewed: Optional[datetime] = Field(index=True)

    user_ids: List[int] = Field(sa_column=Column(JSONB), default=[])

    __table_args__ = (Index("deal_user_ids", "user_ids", postgresql_using="gin"),)
