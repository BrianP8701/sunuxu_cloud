from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    Enum as SqlEnum,
    LargeBinary,
)
from sqlalchemy.orm import relationship
from core.database.abstract_sql import Base
from sqlalchemy.sql import func

from core.enums.person_type import PersonType
from core.models.associations import user_person_association

class PersonOrm(Base):
    __tablename__ = "people"
    id = Column(Integer, primary_key=True)
    
    first_name = Column(String(255), nullable=False)
    middle_name = Column(String(255))
    last_name = Column(String(255), nullable=False)    
    email = Column(String, index=True)
    phone = Column(String, index=True)
    type = Column(SqlEnum(PersonType), index=True, nullable=False, default="?")
    custom_type = Column(String, index=True)
    active = Column(Boolean, default=False, index=True, nullable=False)

    created = Column(DateTime, default=func.now(), index=True)
    updated = Column(DateTime, default=func.now(), onupdate=func.now(), index=True)
    viewed = Column(DateTime, index=True)

    signature = Column(LargeBinary, nullable=True)

    users = relationship("UserOrm", secondary=user_person_association, back_populates="people")
    person_details = relationship(
        "PersonDetailsOrm", 
        back_populates="person", 
        uselist=False, 
        cascade="all, delete-orphan"
    )


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
