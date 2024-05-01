from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from core.database.abstract_sql import Base
from sqlalchemy.sql import func
from sqlalchemy import Enum

class ParticipantOrm(Base):
    __tablename__ = "participants"
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('people.id'))
    transaction_id = Column(Integer, ForeignKey('transactions.id', ondelete='CASCADE'))
    role = Column(Enum('buyer', 'seller', 'buyer_agent', 'seller_agent', 'buyer_attorney', 'seller_attorney', 'buyer_agent_broker', 'seller_agent_broker', name='participant_roles'))
    notes = Column(String)

    created = Column(DateTime, default=func.now(), index=True)
    updated = Column(DateTime, onupdate=func.now(), index=True)
    viewed = Column(DateTime, index=True)

    transaction = relationship("TransactionOrm", back_populates="participants")
    person = relationship("PersonOrm", back_populates="participants")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "transaction_id": self.transaction_id,
            "person_id": self.person_id,
            "role": self.role
        }
