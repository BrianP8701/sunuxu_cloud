from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from core.database.abstract_sql import Base
from sqlalchemy.sql import func
from sqlalchemy import Enum

from core.models.association import property_owner_association_table

class PersonOrm(Base):
    __tablename__ = "people"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    first_name = Column(String(255), nullable=False)
    middle_name = Column(String(255))
    last_name = Column(String(255), nullable=False)
    phone = Column(String(20))
    email = Column(String(255))
    
    notes = Column(String)
    type = Column(Enum('lead', 'prospect', 'client', 'past_client', 'agent', 'broker', 'attorney', 'other', name='person_types'), index=True)
    status = Column(Enum('active', 'inactive', name='person_status'), index=True)
    language = Column(String(255), default='english')

    created = Column(DateTime, default=func.now(), index=True)
    updated = Column(DateTime, default=func.now(), onupdate=func.now(), index=True)
    viewed = Column(DateTime, index=True)

    user = relationship("UserOrm", back_populates="people")
    participants = relationship("ParticipantOrm", back_populates="person")
    properties = relationship("PropertyOrm", secondary=property_owner_association_table, back_populates="owners")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "phone": self.phone,
            "email": self.email,
            "notes": self.notes,
            "type": self.type,
            "language": self.language,
            "created": self.created.isoformat() if self.created else None,
            "updated": self.updated.isoformat() if self.updated else None,
            "viewed": self.viewed.isoformat() if self.viewed else None,
        }

    def to_table_row(self) -> dict:
        full_name = f"{self.first_name} {self.middle_name if self.middle_name else ''} {self.last_name}".replace('  ', ' ')        
        return {
            "id": self.id,
            "name": full_name,
            "phone": self.phone,
            "email": self.email,
            "type": self.type,
        }