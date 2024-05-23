from sqlalchemy import Column, Integer, String, JSON
from core.database.abstract_sql import Base


class DocumentTemplateOrm(Base):
    __tablename__ = "document_templates"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    tags = Column(JSON)
    url = Column(String)
    form_fields = Column(JSON)
    participants_needed = Column(JSON)
