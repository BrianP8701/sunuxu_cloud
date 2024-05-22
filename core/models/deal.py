from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SqlEnum
from sqlalchemy.orm import relationship
from core.database.abstract_sql import Base
from sqlalchemy.sql import func

from core.enums.transaction_type import DealType
from core.enums.transaction_status import DealStatus
from core.models.associations import user_deal_association

class DealOrm(Base):
    __tablename__ = "deals"
    id = Column(Integer, primary_key=True)

    address = Column(String(255), nullable=False)
    buyer_name = Column(String(255))

    status = Column(
        SqlEnum(DealStatus),
        index=True,
        default=DealStatus.UNKNOWN,
        nullable=False,
    )
    type = Column(
        SqlEnum(DealType),
        index=True,
        default=DealType.UNKNOWN,
        nullable=False,
    )

    created = Column(DateTime, default=func.now(), index=True)
    updated = Column(DateTime, default=func.now(), onupdate=func.now(), index=True)
    viewed = Column(DateTime, index=True)

    users = relationship("UserOrm", secondary=user_deal_association, back_populates="transaction_rows")
    deal_details = relationship("DealDetailsOrm", back_populates="deal", uselist=False, cascade="all, delete-orphan")

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
