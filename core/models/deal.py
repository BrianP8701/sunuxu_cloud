from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from core.enums.transaction_type import DealType
from core.enums.transaction_status import DealStatus
from core.models.associations import user_deal_association

if TYPE_CHECKING:
    from core.models.user import User
    from core.models.deal_details import DealDetails

class Deal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    address: str = Field(max_length=255, nullable=False)
    buyer_name: Optional[str] = Field(default=None, max_length=255)

    status: DealStatus = Field(sa_column=Field(sa_column_kwargs={"type_": "enum"}), default=DealStatus.UNKNOWN, nullable=False, index=True)
    type: DealType = Field(sa_column=Field(sa_column_kwargs={"type_": "enum"}), default=DealType.UNKNOWN, nullable=False, index=True)

    created: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow}, index=True)
    viewed: Optional[datetime] = Field(default=None, index=True)

    users: List["User"] = Relationship(back_populates="transaction_rows", link_model=user_deal_association)
    deal_details: Optional["DealDetails"] = Relationship(back_populates="deal", sa_relationship_kwargs={"uselist": False, "cascade": "all, delete-orphan"})

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
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
