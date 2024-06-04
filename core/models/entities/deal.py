from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Enum as SqlEnum, Column, Integer, ForeignKey

from core.enums.deal_platform import DealPlatform
from core.models.associations import UserDealAssociation, DealDetailsPersonAssociation

if TYPE_CHECKING:
    from core.models.entities.user import UserOrm
    from core.models.rows.deal import DealRowOrm
    from core.models.deal_document import DealDocumentOrm
    from core.models.rows.property import PropertyRowOrm
    from core.models.rows.person import PersonRowOrm

class DealOrm(SQLModel, table=True):
    __tablename__ = "deals"
    id: Optional[int] = Field(default=None, sa_column=Column(Integer, ForeignKey("deals.id", ondelete="CASCADE"), primary_key=True))

    transaction_platform: Optional[DealPlatform] = Field(sa_column=SqlEnum(DealPlatform), default=None)
    notes: Optional[str] = None

    property: Optional["PropertyRowOrm"] = Relationship(sa_relationship_kwargs={"uselist": False})    
    participants: List["PersonRowOrm"] = Relationship(link_model=DealDetailsPersonAssociation, sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    documents: List["DealDocumentOrm"] = Relationship(sa_relationship_kwargs={"cascade": "all, delete-orphan"})

    users: List["UserOrm"] = Relationship(back_populates="deals", link_model=UserDealAssociation, sa_relationship_kwargs={"uselist": False, "cascade": "all, delete-orphan"})
