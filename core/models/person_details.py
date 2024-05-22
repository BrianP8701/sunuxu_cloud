from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from core.database.abstract_sql import Base

from core.models.associations import property_owner_association_table, person_portfolio_association_table


class PersonDetailsOrm(Base):
    __tablename__ = "people_details"
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("people.id", ondelete="CASCADE"), primary_key=True)

    notes = Column(String)
    language = Column(String(255), default="english")
    address = Column(String(255))  # Person's current address of residence
    google_place_id = Column(String(255))
    street_number = Column(String(255))
    street_name = Column(String(255))
    street_suffix = Column(String(255))
    unit = Column(String(255))
    city = Column(String(255))
    state = Column(String(255))
    zip = Column(String(255))
    country = Column(String(255))

    custom_fields = Column(JSON)

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
        secondary=property_owner_association_table,
        back_populates="owners",
    )
    residence = relationship("PropertyOrm", uselist=False)
    portfolio = relationship("PropertyOrm", secondary=person_portfolio_association_table)

    secondary_user = relationship("SecondaryUserOrm", back_populates="person", uselist=False)


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
