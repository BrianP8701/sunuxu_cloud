from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, Dict, TYPE_CHECKING, Any
from core.models.associations import DocumentParticipantAssociation, FileParticipantAssociation
from sqlalchemy import Column, JSON

if TYPE_CHECKING:
    from core.models.user import UserOrm
    from core.models.participant import ParticipantOrm
    from core.models.person import PersonOrm
    from core.models.document import DocumentOrm
    from core.models.file import FileOrm

class ParticipantDetailsOrm(SQLModel, table=True):
    __tablename__ = "participant_details"
    id: Optional[int] = Field(default=None, foreign_key="participants.id", primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    person_id: int = Field(foreign_key="people.id", nullable=False)

    notes: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))

    user: Optional["UserOrm"] = Relationship(back_populates="participants")
    participant: Optional["ParticipantOrm"] = Relationship(back_populates="participants")
    documents: List["DocumentOrm"] = Relationship(
        back_populates="participants",
        link_model=DocumentParticipantAssociation
    )
    files: List["FileOrm"] = Relationship(
        back_populates="participants",
        link_model=FileParticipantAssociation
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "deal_id": self.deal_id,
            "person_id": self.person_id,
            "role": self.role,
        }
