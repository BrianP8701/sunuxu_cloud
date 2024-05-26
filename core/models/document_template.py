from sqlmodel import Field, SQLModel, Column, JSON
from typing import Optional, Dict, List, Any


class DocumentTemplateOrm(SQLModel, table=True):
    __tablename__ = "document_templates"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    tags: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    url: Optional[str] = None
    form_fields: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    participants_needed: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
