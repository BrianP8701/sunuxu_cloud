from sqlalchemy import Column, Integer, String
from core.database.abstract_sql import Base

class PersonOrm(Base):
    __tablename__ = "persons"
    person_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    phone_number = Column(String(20))
    ssn = Column(String(11), unique=True)
    driver_license_number = Column(String, unique=True)
    current_address = Column(String)

    def to_dict(self) -> dict:
        return {
            "person_id": self.person_id,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "ssn": self.ssn,
            "driver_license_number": self.driver_license_number,
            "current_address": self.current_address
        }
