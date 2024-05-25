from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, Dict, TYPE_CHECKING
from core.models.associations import DocumentParticipantAssociation

if TYPE_CHECKING:
    from core.models.document_template import DocumentTemplate
    from core.models.participant_details import ParticipantDetails

class Document(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    document_template_id: Optional[int] = Field(default=None, foreign_key="document_templates.id", unique=True)
    deal_id: Optional[int] = Field(default=None, foreign_key="deal_details.id")  # Foreign key to DealDetailsOrm

    url: Optional[str] = Field(default=None)
    field_values: Optional[Dict] = Field(default=None, sa_column_kwargs={"type_": "JSON"})

    document_template: Optional["DocumentTemplate"] = Relationship(back_populates="document")

    participants: List["ParticipantDetails"] = Relationship(
        back_populates="documents",
        link_model=DocumentParticipantAssociation
    )
