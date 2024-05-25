from sqlmodel import Field, SQLModel, Relationship, JSON
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy.ext.mutable import MutableList

from core.models.associations import (
    UserPersonAssociation,
    UserPropertyAssociation,
    UserDealAssociation,
    UserTeamAssociation
)

if TYPE_CHECKING:
    from core.models.person import Person
    from core.models.property import Property
    from core.models.deal import Deal
    from core.models.team import Team


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)

    custom_person_types: List[str] = Field(default_factory=list, sa_column=MutableList.as_mutable(JSON))
    custom_property_types: List[str] = Field(default_factory=list, sa_column=MutableList.as_mutable(JSON))
    custom_transaction_types: List[str] = Field(default_factory=list, sa_column=MutableList.as_mutable(JSON))
    custom_transaction_statuses: List[str] = Field(default_factory=list, sa_column=MutableList.as_mutable(JSON))
    custom_participant_roles: List[str] = Field(default_factory=list, sa_column=MutableList.as_mutable(JSON))

    people: List["Person"] = Relationship(
        back_populates="users", link_model=UserPersonAssociation
    )
    properties: List["Property"] = Relationship(
        back_populates="users", link_model=UserPropertyAssociation
    )
    deals: List["Deal"] = Relationship(
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
