from typing import TYPE_CHECKING, Any, Dict, List, Optional

from sqlalchemy import JSON, Column, Integer, ForeignKey, Enum as SqlEnum
from sqlmodel import Field, Relationship, SQLModel

from core.enums.deal_document_status import DealDocumentStatus
from core.models.associations import DocumentPersonAssociation

if TYPE_CHECKING:
    from core.models.document_template import DocumentTemplateModel
    from core.models.entities.deal import DealModel
    from core.models.entities.person import PersonModel


class DealDocumentModel(SQLModel, table=True):
    __tablename__ = "deal_documents"
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field()

    url: str = Field()
    field_values: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    status: DealDocumentStatus = Field(sa_column=Column(SqlEnum(DealDocumentStatus)))

    document_template_id: int = Field(sa_column=Column(Integer, ForeignKey('document_templates.id')))
    document_template: Optional["DocumentTemplateModel"] = Relationship(
        sa_relationship_kwargs={"uselist": False,  "cascade": "all"}
    )

    participants: List["PersonModel"] = Relationship(
        link_model=DocumentPersonAssociation,
        sa_relationship_kwargs={"cascade": "all"},
    )
    deal_id: Optional[int] = Field(default=None, foreign_key="deals.id")
    deal: Optional["DealModel"] = Relationship(
        back_populates="documents",
        sa_relationship_kwargs={"uselist": False, "cascade": "all"},
    )
