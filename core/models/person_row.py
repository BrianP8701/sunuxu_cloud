from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from core.database.abstract_sql import Base
from sqlalchemy.sql import func
from sqlalchemy import Enum

class PersonRowOrm(Base):
    __tablename__ = "people_rows"
    id = Column(Integer, ForeignKey('people.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    name = Column(String, index=True)
    email = Column(String, index=True)
    phone = Column(String, index=True)
    type = Column(
        Enum(
            "lead", "prospect", "client", "past_client", "agent", "broker", "attorney", "custom", "?",
            name="person_types",
        ),
        index=True,
        nullable=False,
        default="?"
    )
    custom_type = Column(String, index=True)
    active = Column(Boolean, default=False, index=True)

    created = Column(DateTime, default=func.now(), index=True)
    updated = Column(DateTime, default=func.now(), onupdate=func.now(), index=True)
    viewed = Column(DateTime, index=True)

    user = relationship("UserOrm", back_populates="people_rows")
    person = relationship("PersonOrm", back_populates="summary_row", uselist=False)
    participants = relationship("ParticipantRowOrm", back_populates="person_row")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "type": self.type,
            "active": self.active,
            "created": self.created.isoformat() if self.created else None,
            "updated": self.updated.isoformat() if self.updated else None,
            "viewed": self.viewed.isoformat() if self.viewed else None,
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
