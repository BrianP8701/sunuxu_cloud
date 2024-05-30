from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import JSON, Column
from typing import Optional, List, Dict, TYPE_CHECKING, Any

from core.models.associations import PersonPortfolioAssociation

if TYPE_CHECKING:
    from core.models.message import MessageOrm
    from core.models.participant import ParticipantOrm
    from core.models.person import PersonOrm
    from core.models.property import PropertyOrm

class PersonDetailsOrm(SQLModel, table=True):
    __tablename__ = "person_details"
    id: Optional[int] = Field(default=None, primary_key=True)
    person_id: Optional[int] = Field(default=None, foreign_key="people.id")

    notes: Optional[str] = None
    language: str = Field(default="english", max_length=255)
    source: Optional[str] = Field(default=None, max_length=255)
    viewed_properties: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    signature: Optional[bytes] = Field(default=None)

    messages: List["MessageOrm"] = Relationship(
        sa_relationship_kwargs={"order_by": "MessageOrm.id", "cascade": "all, delete-orphan"}
    )

    person: Optional["PersonOrm"] = Relationship(back_populates="person_details")
    participants: List["ParticipantOrm"] = Relationship(
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    residence: Optional["PropertyOrm"] = Relationship(sa_relationship_kwargs={"uselist": False})
    portfolio: List["PropertyOrm"] = Relationship(link_model=PersonPortfolioAssociation)
