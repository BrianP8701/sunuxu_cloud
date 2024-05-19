from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from core.database.abstract_sql import Base
from sqlalchemy.sql import func
from sqlalchemy import Enum

from core.models.association import property_owner_association_table


class PersonOrm(Base):
    __tablename__ = "people"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    notes = Column(String)
    language = Column(String(255), default="english")

    first_name = Column(String(255), nullable=False)
    middle_name = Column(String(255))
    last_name = Column(String(255), nullable=False)

    user = relationship("UserOrm", back_populates="people")
    summary_row = relationship("PersonRowOrm", back_populates="person", uselist=False, cascade="all, delete-orphan")
    participants = relationship("ParticipantOrm", back_populates="person")
    properties = relationship(
        "PropertyOrm",
        secondary=property_owner_association_table,
        back_populates="owners",
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "phone": self.phone,
            "email": self.email,
            "notes": self.notes,
            "language": self.language
        }

    def to_table_row(self) -> dict:
        full_name = f"{self.first_name} {self.middle_name if self.middle_name else ''} {self.last_name}".replace(
            "  ", " "
        )
        return {
            "id": self.id,
            "name": full_name,
            "phone": self.phone,
            "email": self.email,
            "type": self.type,
        }
