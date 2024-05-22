from sqlalchemy import Column, Integer, JSON
from sqlalchemy.orm import relationship
from core.database.abstract_sql import Base
from sqlalchemy.ext.mutable import MutableList

from core.models.associations import (
    user_person_association,
    user_property_association,
    user_deal_association,
    user_team_association  # Import the association table
)


class UserOrm(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)

    custom_person_types = Column(MutableList.as_mutable(JSON), default=list)
    custom_property_types = Column(MutableList.as_mutable(JSON), default=list)
    custom_transaction_types = Column(MutableList.as_mutable(JSON), default=list)
    custom_transaction_statuses = Column(MutableList.as_mutable(JSON), default=list)
    custom_participant_roles = Column(MutableList.as_mutable(JSON), default=list)

    people = relationship(
        "PersonOrm", secondary=user_person_association, back_populates="users"
    )
    properties = relationship(
        "PropertyOrm", secondary=user_property_association, back_populates="users"
    )
    deals = relationship(
        "DealOrm", secondary=user_deal_association, back_populates="users"
    )
    teams = relationship(
        "TeamOrm", secondary=user_team_association, back_populates="users"
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "phone": self.phone,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "custom_person_types": self.custom_person_types,
            "custom_property_types": self.custom_property_types,
            "custom_transaction_types": self.custom_transaction_types,
            "custom_transaction_statuses": self.custom_transaction_statuses,
            "custom_participant_roles": self.custom_participant_roles,
            "teams": [
                {"id": team.id, "role": association.role}
                for team, association in zip(self.teams, self.team_associations)
            ],
        }
