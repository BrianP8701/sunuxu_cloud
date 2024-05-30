from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, Dict, TYPE_CHECKING, Any
from sqlalchemy import Enum as SqlEnum, Column, JSON

from core.enums.deal_platform import DealPlatform

if TYPE_CHECKING:
    from core.models.deal import DealOrm
    from core.models.deal_document import DealDocumentOrm

class DealDetailsOrm(SQLModel, table=True):
    __tablename__ = "deal_details"
    id: Optional[int] = Field(default=None, primary_key=True, foreign_key="deals.id")

    transaction_platform: Optional[DealPlatform] = Field(sa_column=SqlEnum(DealPlatform), default=None, )
    transaction_platform_data: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))

    checklist: Optional[Dict[str, Optional[int]]] = Field(default=None, sa_column=Column(JSON))  # Dictionary of document names to document template ids, which can be None if we don't have them in our system

    notes: Optional[str] = None
    description: Optional[str] = None

    deal: Optional["DealOrm"] = Relationship(back_populates="deal_details", sa_relationship_kwargs={"uselist": False})
    documents: List["DealDocumentOrm"] = Relationship(sa_relationship_kwargs={"cascade": "all, delete-orphan"})
