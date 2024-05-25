from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from core.database.abstract_sql import Base

from core.models.associations import property_owner_association, person_portfolio_association


class PersonDetailsOrm(Base):
    __tablename__ = "people_details"
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("people.id", ondelete="CASCADE"), primary_key=True)

    notes = Column(String)
    language = Column(String(255), default="english")
    source = Column(String(255))
    
    messages = relationship(
        "MessageOrm", 
        backref="user", 
        order_by="MessageOrm.timestamp"
    )

    person = relationship(
        "PersonOrm", 
        back_populates="person_details"
    )
    participants = relationship(
        "ParticipantOrm", 
        back_populates="person", 
        cascade="all, delete-orphan"
    )
    properties = relationship(
        "PropertyOrm",
        secondary=property_owner_association,
        back_populates="owners",
    )
    residence = relationship("PropertyOrm", uselist=False)
    portfolio = relationship("PropertyOrm", secondary=person_portfolio_association)


    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "phone": self.phone,
            "email": self.email,
            "notes": self.notes,
            "language": self.language,
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
