from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TYPE_CHECKING
from core.models.associations import FileParticipantAssociation

if TYPE_CHECKING:
    from core.models.participant_details import ParticipantDetails

class File(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    url: Optional[str] = None
    reusable: bool = Field(default=False)

    participants: List["ParticipantDetails"] = Relationship(
        back_populates="files", link_model=FileParticipantAssociation
    )
