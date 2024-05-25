from sqlmodel import Field, SQLModel, Relationship, DateTime
from typing import Optional, List, Dict, TYPE_CHECKING
from core.models.associations import DocumentParticipantAssociation, FileParticipantAssociation
from sqlalchemy.sql import func

if TYPE_CHECKING:
    from core.models.user import User
    from core.models.participant import Participant
    from core.models.person import Person
    from core.models.document import Document
    from core.models.file import File

class ParticipantDetails(SQLModel, table=True):
    id: Optional[int] = Field(default=None, foreign_key="participants.id", primary_key=True, sa_column_kwargs={"ondelete": "CASCADE"})
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", sa_column_kwargs={"ondelete": "CASCADE"})
    person_id: int = Field(foreign_key="people_rows.id", nullable=False, sa_column_kwargs={"ondelete": "CASCADE"})

    notes: Optional[str] = None
    custom_fields: Optional[Dict] = Field(default=None, sa_column_kwargs={"type_": "JSON"})

    created: Optional[DateTime] = Field(default=func.now(), index=True)
    updated: Optional[DateTime] = Field(default=func.now(), sa_column_kwargs={"onupdate": func.now()}, index=True)
    viewed: Optional[DateTime] = Field(default=None, index=True)

    user: Optional["User"] = Relationship(back_populates="participants")
    participant: Optional["Participant"] = Relationship(back_populates="participants")
    person: Optional["Person"] = Relationship()
    documents: List["Document"] = Relationship(
        back_populates="participants",
        link_model=DocumentParticipantAssociation
    )
    files: List["File"] = Relationship(
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
