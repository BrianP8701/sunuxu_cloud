from typing import Any, Dict, List, Optional

from sqlmodel import JSON, Column, Field, SQLModel


class DocumentTemplateModel(SQLModel, table=True):
    __tablename__ = "document_templates"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    tags: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    url: Optional[str] = None
    form_fields: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    roles_needed: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
