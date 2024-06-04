from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, Dict, TYPE_CHECKING, Any
from sqlalchemy import Column, JSON, Enum as SqlEnum

from core.models.associations import DocumentPersonAssociation
from core.enums.deal_document_status import DealDocumentStatus

if TYPE_CHECKING:
    from core.models.document_template import DocumentTemplateOrm
    from core.models.rows.person import PersonRowOrm

class DealDocumentOrm(SQLModel, table=True):
    __tablename__ = "deal_documents"
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field()

    url: str = Field()
    field_values: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    status: DealDocumentStatus = Field(sa_column=Column(SqlEnum(DealDocumentStatus)))
    
    document_template: Optional["DocumentTemplateOrm"] = Relationship(sa_relationship_kwargs={"uselist": False})

    participants: List["PersonRowOrm"] = Relationship(
        link_model=DocumentPersonAssociation
    )
