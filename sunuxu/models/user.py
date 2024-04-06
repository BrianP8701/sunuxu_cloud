from enum import Enum
from sqlalchemy import Column, Integer, String, CheckConstraint

from sunuxu.database.abstract import Base


class UserOrm(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String)
    phone = Column(String(20))
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    user_type = Column(String, CheckConstraint("user_type IN ('admin', 'agent', 'person')"))

    def __repr__(self) -> str:
        return f"<UserOrm(username={self.username}, email={self.email}, phone={self.phone}, first_name={self.first_name}, middle_name={self.middle_name}, last_name={self.last_name}, user_type={self.user_type})>"

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "email": self.email,
            "phone": self.phone,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "user_type": self.user_type
        }
