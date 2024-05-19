from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship
from core.database.abstract_sql import Base
from sqlalchemy.sql import func
from sqlalchemy.ext.mutable import MutableList


class UserOrm(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    password = Column(String(255))
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20))
    first_name = Column(String(255), nullable=False)
    middle_name = Column(String(255))
    last_name = Column(String(255), nullable=False)
    
    custom_person_types = Column(MutableList.as_mutable(JSON), default=list)
    custom_property_types = Column(MutableList.as_mutable(JSON), default=list)
    custom_transaction_types = Column(MutableList.as_mutable(JSON), default=list)
    custom_transaction_statuses = Column(MutableList.as_mutable(JSON), default=list)
    custom_participant_roles = Column(MutableList.as_mutable(JSON), default=list)

    created = Column(DateTime, default=func.now())

    people = relationship(
        "PersonOrm", back_populates="user", cascade="all, delete, delete-orphan"
    )
    people_rows = relationship(
        "PersonRowOrm", back_populates="user", cascade="all, delete, delete-orphan"
    )
    properties = relationship(
        "PropertyOrm", back_populates="user", cascade="all, delete, delete-orphan"
    )
    property_rows = relationship(
        "PropertyRowOrm", back_populates="user", cascade="all, delete, delete-orphan"
    )
    transactions = relationship(
        "TransactionOrm", back_populates="user", cascade="all, delete, delete-orphan"
    )
    transaction_rows = relationship(
        "TransactionRowOrm", back_populates="user", cascade="all, delete, delete-orphan"
    )
    participants = relationship(
        "ParticipantOrm", back_populates="user", cascade="all, delete, delete-orphan"
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "phone": self.phone,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "custom_person_types": self.custom_person_types,
            "custom_property_types": self.custom_property_types,
            "custom_transaction_types": self.custom_transaction_types,
            "custom_transaction_statuses": self.custom_transaction_statuses,
            "custom_participant_roles": self.custom_participant_roles
        }
