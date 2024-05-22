from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database.abstract_sql import Base


class SecondaryUserOrm(Base):
    __tablename__ = "secondary_users"
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("people.id"), nullable=False)
    password = Column(String(255))

    person = relationship("PersonOrm", back_populates="secondary_user")

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
