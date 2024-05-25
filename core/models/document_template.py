from sqlmodel import Field, SQLModel
from typing import Optional, Dict, List


class DocumentTemplate(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    tags: Optional[Dict] = None
    url: Optional[str] = None
    form_fields: Optional[Dict] = None
    participants_needed: Optional[List] = None
