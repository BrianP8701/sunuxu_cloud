from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from core.database.abstract_sql import Base
from sqlalchemy.sql import func
from sqlalchemy import Enum


class ParticipantDetailsOrm(Base):
    __tablename__ = "participant_details"
    id = Column(Integer, ForeignKey("participants.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    person_id = Column(
        Integer, ForeignKey("people_rows.id", ondelete="CASCADE"), nullable=False
    )

    notes = Column(String)
    custom_fields = Column(JSON)

    created = Column(DateTime, default=func.now(), index=True)
    updated = Column(DateTime, default=func.now(), onupdate=func.now(), index=True)
    viewed = Column(DateTime, index=True)

    user = relationship("UserOrm", back_populates="participants")
    participant = relationship(
        "ParticipantOrm", 
        back_populates="participants"
    )
    person = relationship("PersonOrm")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "deal_id": self.deal_id,
            "person_id": self.person_id,
            "role": self.role,
        }
