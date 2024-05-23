from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship

from core.database.abstract_sql import Base
from core.models.associations import document_participant_association

class DocumentOrm(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    document_template_id = Column(Integer, ForeignKey('document_templates.id'), unique=True)
    deal_id = Column(Integer, ForeignKey('deal_details.id'))  # Foreign key to DealDetailsOrm

    url = Column(String)
    field_values = Column(JSON)

    document_template = relationship("DocumentTemplateOrm", back_populates="document")

    participants = relationship(
        "ParticipantDetailsOrm", 
        secondary=document_participant_association, 
        back_populates="documents"
    )
