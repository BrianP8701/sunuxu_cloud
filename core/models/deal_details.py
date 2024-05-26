from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, Dict, TYPE_CHECKING, Any
from sqlalchemy import Enum as SqlEnum, Column, JSON

from core.enums.transaction_platform import TransactionPlatform

if TYPE_CHECKING:
    from core.models.user import UserOrm
    from core.models.property import PropertyOrm
    from core.models.participant import ParticipantOrm
    from core.models.deal import DealOrm
    from core.models.document import DocumentOrm

class DealDetailsOrm(SQLModel, table=True):
    __tablename__ = "deal_details"
    id: Optional[int] = Field(default=None, primary_key=True, foreign_key="deals.id")
    user_id: int = Field(foreign_key="users.id")
    property_id: Optional[int] = Field(default=None, foreign_key="properties.id")

    transaction_platform: Optional[TransactionPlatform] = Field(sa_column=SqlEnum(TransactionPlatform), default=None, )
    transaction_platform_data: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))

    checklist: Optional[Dict[str, Optional[int]]] = Field(default=None, sa_column=Column(JSON))  # Dictionary of document names to document template ids, which can be None if we don't have them in our system

    notes: Optional[str] = None
    description: Optional[str] = None

    user: Optional["UserOrm"] = Relationship(back_populates="deals")
    property: Optional["PropertyOrm"] = Relationship(sa_relationship_kwargs={"uselist": False})
    participants: List["ParticipantOrm"] = Relationship(
        back_populates="deal", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    deal: Optional["DealOrm"] = Relationship(back_populates="deal_details", sa_relationship_kwargs={"uselist": False})
    documents: List["DocumentOrm"] = Relationship(back_populates="deal")

    def to_dict(self) -> dict:
        return {
        "id": self.id,
        "type": self.type,
        "status": self.status,
        "notes": self.notes,
        "description": self.description,
        "created": self.created.isoformat() if self.created else None,
        "updated": self.updated.isoformat() if self.updated else None,
        "viewed": self.viewed.isoformat() if self.viewed else None,
        }

    def to_table_row(self) -> dict:
        return {
        "id": self.id,
        "type": self.type,
        }
