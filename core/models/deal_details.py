from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, Dict, TYPE_CHECKING
from sqlalchemy import Enum as SqlEnum

from core.enums.transaction_platform import TransactionPlatform

if TYPE_CHECKING:
    from core.models.user import User
    from core.models.property import Property
    from core.models.participant import Participant
    from core.models.deal import Deal
    from core.models.document import Document

class DealDetails(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, foreign_key="deals.id")
    user_id: int = Field(foreign_key="users.id")
    property_id: Optional[int] = Field(default=None, foreign_key="properties.id")

    transaction_platform: Optional[TransactionPlatform] = Field(sa_column=SqlEnum(TransactionPlatform), default=None, )
    transaction_platform_data: Optional[Dict] = Field(default=None, sa_column_kwargs={"type_": "json"})

    checklist: Optional[Dict[str, Optional[int]]] = Field(default=None, sa_column_kwargs={"type_": "json"})  # Dictionary of document names to document template ids, which can be None if we don't have them in our system

    notes: Optional[str] = None
    description: Optional[str] = None

    user: Optional["User"] = Relationship(back_populates="deals")
    property: Optional["Property"] = Relationship(sa_relationship_kwargs={"uselist": False})
    participants: List["Participant"] = Relationship(
        back_populates="deal", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    deal: Optional["Deal"] = Relationship(back_populates="deal_details", sa_relationship_kwargs={"uselist": False})
    documents: List["Document"] = Relationship(back_populates="deal")

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
