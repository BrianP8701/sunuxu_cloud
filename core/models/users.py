from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from core.database.abstract_sql import Base
from sqlalchemy.sql import func

class UserOrm(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    password = Column(String(255))
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20))
    first_name = Column(String(255))
    middle_name = Column(String(255))
    last_name = Column(String(255))

    created = Column(DateTime, default=func.now())

    people = relationship("PersonOrm", back_populates="user", cascade="all, delete, delete-orphan")
    properties = relationship("PropertyOrm", back_populates="user", cascade="all, delete, delete-orphan")
    transactions = relationship("TransactionOrm", back_populates="user", cascade="all, delete, delete-orphan")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "phone": self.phone,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name
        }
