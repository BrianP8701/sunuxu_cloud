from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from core.database.abstract_sql import Base
from core.models.associations import file_participant_association

class FileOrm(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    url = Column(String)
    reusable = Column(Boolean, default=False)

    participants = relationship(
        "ParticipantDetailsOrm", 
        secondary=file_participant_association, 
        back_populates="files"
    )
