from sqlalchemy import Column, Integer, String, CheckConstraint

from core.database.abstract_sql import Base

class UserOrm(Base):
    __tablename__ = "users"
    email = Column(String(255), primary_key=True)
    phone = Column(String(20))
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)

    def to_dict(self) -> dict:
        return {
            "email": self.email,
            "phone": self.phone,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
        }
