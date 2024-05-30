from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, Dict, TYPE_CHECKING, Any
from core.models.associations import DocumentParticipantAssociation
from sqlalchemy import Column, JSON

if TYPE_CHECKING:
    from core.models.document_template import DocumentTemplateOrm
    from core.models.participant_details import ParticipantDetailsOrm

class DealDocumentOrm(SQLModel, table=True):
    __tablename__ = "deal_documents"
    id: Optional[int] = Field(default=None, primary_key=True)
    document_template_id: Optional[int] = Field(default=None, foreign_key="document_templates.id", unique=True)
    deal_id: Optional[int] = Field(default=None, foreign_key="deal_details.id")  # Foreign key to DealDetailsOrm

    url: str = Field()
    field_values: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))

    document_template: Optional["DocumentTemplateOrm"] = Relationship(back_populates="document")

    participants: List["ParticipantDetailsOrm"] = Relationship(
        back_populates="documents",
        link_model=DocumentParticipantAssociation
    )
