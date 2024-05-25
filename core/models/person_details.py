from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, Dict, TYPE_CHECKING
from core.models.associations import property_owner_association, person_portfolio_association

if TYPE_CHECKING:
    from core.models.message import MessageOrm
    from core.models.participant import ParticipantOrm
    from core.models.person import PersonOrm
    from core.models.property import PropertyOrm

class PersonDetails(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    person_id: Optional[int] = Field(default=None, foreign_key="people.id", primary_key=True, sa_column_kwargs={"ondelete": "CASCADE"})

    notes: Optional[str] = None
    language: str = Field(default="english", max_length=255)
    source: Optional[str] = Field(default=None, max_length=255)
    viewed_properties: Optional[Dict] = Field(default=None, sa_column_kwargs={"type_": "JSON"})
    
    messages: List["MessageOrm"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"order_by": "MessageOrm.timestamp"}
    )

    person: Optional["PersonOrm"] = Relationship(back_populates="person_details")
    participants: List["ParticipantOrm"] = Relationship(
        back_populates="person",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    properties: List["PropertyOrm"] = Relationship(
        back_populates="owners",
        link_model=property_owner_association
    )
    residence: Optional["PropertyOrm"] = Relationship(sa_relationship_kwargs={"uselist": False})
    portfolio: List["PropertyOrm"] = Relationship(link_model=person_portfolio_association)

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
