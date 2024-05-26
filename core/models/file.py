from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TYPE_CHECKING
from core.models.associations import FileParticipantAssociation

if TYPE_CHECKING:
    from core.models.participant_details import ParticipantDetailsOrm

class FileOrm(SQLModel, table=True):
    __tablename__ = "files"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    url: Optional[str] = None
    reusable: bool = Field(default=False)

    participants: List["ParticipantDetailsOrm"] = Relationship(
        back_populates="files", link_model=FileParticipantAssociation
    )
