from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SqlEnum
from sqlalchemy.orm import relationship
from core.database.abstract_sql import Base
from sqlalchemy.sql import func

from core.enums.transaction_type import TransactionType
from core.enums.transaction_status import TransactionStatus


class TransactionRowOrm(Base):
    __tablename__ = "transaction_rows"
    id = Column(Integer, ForeignKey("transactions.id"), primary_key=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    name = Column(String, index=True)
    status = Column(
        SqlEnum(TransactionStatus),
        index=True,
        default=TransactionStatus.UNKNOWN,
        nullable=False,
    )
    type = Column(
        SqlEnum(TransactionType),
        index=True,
        default=TransactionType.UNKNOWN,
        nullable=False,
    )

    created = Column(DateTime, default=func.now(), index=True)
    updated = Column(DateTime, default=func.now(), onupdate=func.now(), index=True)
    viewed = Column(DateTime, index=True)

    user = relationship("UserOrm", back_populates="transaction_rows")
    transaction = relationship(
        "TransactionOrm", back_populates="summary_row", uselist=False
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
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
