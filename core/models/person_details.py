from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import JSON, Column
from typing import Optional, List, Dict, TYPE_CHECKING, Any

from core.models.associations import PropertyOwnerAssociation, PersonPortfolioAssociation

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

    messages: List["MessageOrm"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"order_by": "MessageOrm.timestamp"}
    )

    person: Optional["PersonOrm"] = Relationship(back_populates="person_details")
    participants: List["ParticipantOrm"] = Relationship(
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    properties: List["PropertyOrm"] = Relationship(
        link_model=PropertyOwnerAssociation
    )
    residence: Optional["PropertyOrm"] = Relationship(sa_relationship_kwargs={"uselist": False})
    portfolio: List["PropertyOrm"] = Relationship(link_model=PersonPortfolioAssociation)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "phone": self.phone,
            "email": self.email,
            "notes": self.notes,
            "language": self.language,
        }

    def to_table_row(self) -> dict:
        full_name = f"{self.first_name} {self.middle_name if self.middle_name else ''} {self.last_name}".replace(
            "  ", " "
        )
        return {
            "id": self.id,
            "name": full_name,
            "phone": self.phone,
            "email": self.email,
            "type": self.type,
        }
