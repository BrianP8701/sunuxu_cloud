from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from core.database.abstract_sql import Base
from sqlalchemy.sql import func
from sqlalchemy import Enum


class TransactionOrm(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    property_id = Column(Integer, ForeignKey("properties.id"))

    notes = Column(String)
    description = Column(String)

    custom_fields = Column(JSON)

    user = relationship("UserOrm", back_populates="transactions")
    summary_row = relationship("TransactionRowOrm", back_populates="transaction", uselist=False, cascade="all, delete-orphan")
    property = relationship("PropertyOrm", back_populates="transactions")
    participants = relationship("ParticipantOrm", back_populates="transaction")

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
