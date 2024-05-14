from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
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

    status = Column(
        Enum(
            "pending",
            "closed",
            "expired",
            "withdrawn",
            "off_market",
            "other",
            name="transaction_status",
        ),
        index=True,
    )
    type = Column(
        Enum("sale", "rent", "lease", "buy", "other", name="transaction_types"),
        index=True,
    )  # From the perspective of our user
    notes = Column(String)
    description = Column(String)

    created = Column(DateTime, default=func.now(), index=True)
    updated = Column(DateTime, default=func.now(), onupdate=func.now(), index=True)
    viewed = Column(DateTime, index=True)

    user = relationship("UserOrm", back_populates="transactions")
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
