from typing import TYPE_CHECKING, Any, Dict, List, Optional

from sqlalchemy import JSON, Column
from sqlalchemy import Enum as SqlEnum
from sqlmodel import Field, Relationship, SQLModel

from core.enums.deal_document_status import DealDocumentStatus
from core.models.associations import (DealDocumentAssociation,
                                      DocumentPersonAssociation)

if TYPE_CHECKING:
    from core.models.document_template import DocumentTemplateModel
    from core.models.entities.deal import DealModel
    from core.models.rows.person import PersonRowModel

if TYPE_CHECKING:
    from core.models.document_template import DocumentTemplateModel
    from core.models.rows.person import PersonRowModel


class DealDocumentModel(SQLModel, table=True):
    __tablename__ = "deal_documents"
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field()

    url: str = Field()
    field_values: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    status: DealDocumentStatus = Field(sa_column=Column(SqlEnum(DealDocumentStatus)))

    document_template: Optional["DocumentTemplateModel"] = Relationship(
        sa_relationship_kwargs={"uselist": False}
    )

    participants: List["PersonRowModel"] = Relationship(
        link_model=DocumentPersonAssociation
    )
    deal: Optional["DealModel"] = Relationship(
        link_model=DealDocumentAssociation, sa_relationship_kwargs={"uselist": False}
    )
