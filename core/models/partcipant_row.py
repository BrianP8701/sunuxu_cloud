from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from core.database.abstract_sql import Base
from sqlalchemy.sql import func
from sqlalchemy import Enum


class ParticipantRowOrm(Base):
    __tablename__ = "participant_rows"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    person_id = Column(
        Integer, ForeignKey("people_rows.id", ondelete="CASCADE"), nullable=False
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

    user = relationship("UserOrm", back_populates="participants")
    person_row = relationship("PersonRowOrm", back_populates="participants")

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
