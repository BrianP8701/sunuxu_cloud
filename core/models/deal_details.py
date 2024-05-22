from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Enum as SqlEnum
from sqlalchemy.orm import relationship

from core.database.abstract_sql import Base
from core.enums.transaction_platform import TransactionPlatform

class DealDetailsOrm(Base):
    __tablename__ = "deal_details"
    id = Column(Integer, ForeignKey("deals.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    property_id = Column(Integer, ForeignKey("properties.id"))

    transaction_platform = Column(SqlEnum(TransactionPlatform))
    transaction_platform_data = Column(JSON)
    
    checklist = Column(JSON) # Dictionary of document names to document template ids, which can be None if we don't have them in our system
    documents = Column(JSON) # Dictionary of document names to URLs of the pdf files attached to the deal

    notes = Column(String)
    description = Column(String)

    custom_fields = Column(JSON)

    user = relationship("UserOrm", back_populates="deals")
    property = relationship("PropertyOrm", uselist=False)
    participants = relationship("ParticipantOrm")
    deal = relationship("DealOrm", back_populates="deal_details", uselist=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.type,
            "status": self.status,
            "notes": self.notes,
            "description": self.description,
            "created": self.created.isoformat() if self.created else None,
            "updated": self.updated.isoformat() if self.updated else None,
            "viewed": self.viewed.isoformat() if self.viewed else None,
        }

    def to_table_row(self) -> dict:
        return {
            "id": self.id,
            "type": self.type,
        }
