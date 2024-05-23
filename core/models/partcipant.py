from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from core.database.abstract_sql import Base
from sqlalchemy.sql import func
from sqlalchemy import Enum


class ParticipantOrm(Base):
    __tablename__ = "participants"
    id = Column(Integer, primary_key=True)
    deal_id = Column(
        Integer, ForeignKey("deals.id", ondelete="CASCADE"), nullable=False
    )

    role = Column(
        Enum(
            "buyer",
            "seller",
            "buyer_agent",
            "seller_agent",
            "buyer_attorney",
            "seller_attorney",
            "buyer_agent_broker",
            "seller_agent_broker",
            "custom",
            name="participant_roles",
        )
    )
    custom_role = Column(String)

    created = Column(DateTime, default=func.now(), index=True)
    updated = Column(DateTime, default=func.now(), onupdate=func.now(), index=True)
    viewed = Column(DateTime, index=True)

    deal = relationship("DealOrm")
    participant_details = relationship(
        "ParticipantDetailsOrm", 
        back_populates="participant", 
        uselist=False, 
        cascade="all, delete-orphan"
    )    

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "person_id": self.person_id,
            "role": self.role,
            "custom_role": self.custom_role,
            "created": self.created,
            "updated": self.updated,
            "viewed": self.viewed,
            "name": self.person_row.name,
            "email": self.person_row.email,
            "phone": self.person_row.phone,
        }
