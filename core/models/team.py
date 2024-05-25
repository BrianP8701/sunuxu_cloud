from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Enum as SqlEnum

from core.enums.state import State
from core.enums.brokerage import Brokerage
from core.models.associations import UserTeamAssociation, TeamAdminAssociation

if TYPE_CHECKING:
    from core.models.user import User

class TeamOrm(SQLModel, table=True):
    __tablename__ = "teams"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, nullable=False)

    office: Optional[str] = Field(default=None, max_length=255)
    state: Optional[State] = Field(sa_column=SqlEnum(State))
    brokerage: Optional[Brokerage] = Field(sa_column=SqlEnum(Brokerage))

    users: List["User"] = Relationship(
        back_populates="teams", link_model=UserTeamAssociation
    )
    admins: List["User"] = Relationship(
        link_model=TeamAdminAssociation
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "users": [
                {"id": user.id, "role": association.role}
                for user, association in zip(self.users, self.user_associations)
            ],
        }
