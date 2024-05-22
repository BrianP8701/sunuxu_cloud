from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship
from core.database.abstract_sql import Base
from sqlalchemy.sql import func
from sqlalchemy.ext.mutable import MutableList


class UserDetailsOrm(Base):
    __tablename__ = "user_details"
    id = Column(Integer, primary_key=True)
    password = Column(String(255))
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20))
    first_name = Column(String(255), nullable=False)
    middle_name = Column(String(255))
    last_name = Column(String(255), nullable=False)

    mls_username = Column(String(255))
    mls_password = Column(String(255))
    skyslope_username = Column(String(255))
    skyslope_password = Column(String(255))

    custom_person_types = Column(MutableList.as_mutable(JSON), default=list)
    custom_property_types = Column(MutableList.as_mutable(JSON), default=list)
    custom_transaction_types = Column(MutableList.as_mutable(JSON), default=list)
    custom_transaction_statuses = Column(MutableList.as_mutable(JSON), default=list)
    custom_participant_roles = Column(MutableList.as_mutable(JSON), default=list)

    created = Column(DateTime, default=func.now())

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "phone": self.phone,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name
        }
