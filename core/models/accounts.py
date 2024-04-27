from sqlalchemy import Column, String

from core.database.abstract_sql import Base

class AccountOrm(Base):
    __tablename__ = "accounts"
    email = Column(String(255), primary_key=True)
    password = Column(String(255))

    def to_dict(self) -> dict:
        return {
            "email": self.email,
            "password": self.password
        }
