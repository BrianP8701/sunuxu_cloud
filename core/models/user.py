from sqlalchemy import Column, Integer, String, CheckConstraint

from core.database.abstract_sql import Base

class UserOrm(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    phone = Column(String(20))
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    user_type = Column(String, CheckConstraint("user_type IN ('admin', 'agent', 'person')"))

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "email": self.email,
            "phone": self.phone,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "user_type": self.user_type
        }
