from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import JSON  # Import JSON directly from SQLAlchemy

from core.models.associations import (
    UserPersonAssociation,
    UserPropertyAssociation,
    UserDealAssociation,
    UserTeamAssociation
)

if TYPE_CHECKING:
    from core.models.person import PersonOrm
    from core.models.property import PropertyOrm
    from core.models.deal import DealOrm
    from core.models.team import Team

class UserOrm(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)

    people: List["PersonOrm"] = Relationship(
        back_populates="users", link_model=UserPersonAssociation
    )
    properties: List["PropertyOrm"] = Relationship(
        back_populates="users", link_model=UserPropertyAssociation
    )
    deals: List["DealOrm"] = Relationship(
        back_populates="users", link_model=UserDealAssociation
    )
    teams: List["Team"] = Relationship(
        back_populates="users", link_model=UserTeamAssociation
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
