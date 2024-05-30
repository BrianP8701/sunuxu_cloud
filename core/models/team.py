from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Enum as SqlEnum

from core.enums.state import State
from core.enums.brokerage import Brokerage
from core.models.associations import UserTeamAssociation, TeamAdminAssociation
from core.models.message import MessageOrm

if TYPE_CHECKING:
    from core.models.user import UserOrm

class TeamOrm(SQLModel, table=True):
    __tablename__ = "teams"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, nullable=False)

    office_address: Optional[str] = Field(default=None, max_length=255)
    state: Optional[State] = Field(sa_column=SqlEnum(State))
    brokerage: Optional[Brokerage] = Field(sa_column=SqlEnum(Brokerage))

    messages: List["MessageOrm"] = Relationship(
        sa_relationship_kwargs={"order_by": "MessageOrm.id", "cascade": "all, delete-orphan"}
    )
    users: List["UserOrm"] = Relationship(
        back_populates="teams", link_model=UserTeamAssociation
    )
    admins: List["UserOrm"] = Relationship(
        link_model=TeamAdminAssociation
    )
