from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Column, DateTime, func, Enum as SqlEnum

from core.enums.transaction_type import DealType
from core.enums.transaction_status import DealStatus
from core.models.associations import UserDealAssociation

if TYPE_CHECKING:
    from core.models.user import UserOrm
    from core.models.deal_details import DealDetailsOrm

class DealOrm(SQLModel, table=True):
    __tablename__ = "deals"
    id: Optional[int] = Field(default=None, primary_key=True)
    address: Optional[str] = Field(max_length=255, nullable=False)
    buyer_name: Optional[str] = Field(default=None, max_length=255)

    status: DealStatus = Field(sa_column=Column(SqlEnum(DealStatus), default=DealStatus.UNKNOWN, nullable=False, index=True))
    type: DealType = Field(sa_column=Column(SqlEnum(DealType), default=DealType.UNKNOWN, nullable=False, index=True))

    created: datetime = Field(index=True)    
    updated: Optional[datetime] = Field(sa_column=Column(DateTime, index=True, default=None, onupdate=func.now()))
    viewed: Optional[datetime] = Field(index=True)

    users: List["UserOrm"] = Relationship(back_populates="transaction_rows", link_model=UserDealAssociation)
    deal_details: Optional["DealDetailsOrm"] = Relationship(back_populates="deal", sa_relationship_kwargs={"uselist": False, "cascade": "all, delete-orphan"})
