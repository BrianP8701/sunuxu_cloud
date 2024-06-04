from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Column, Integer, ForeignKey

from core.models.associations import UserTeamAssociation

if TYPE_CHECKING:
    from core.models.rows.user import UserRowOrm
    from core.models.entities.user import UserOrm

class TeamOrm(SQLModel, table=True):
    __tablename__ = "teams"
    id: Optional[int] = Field(default=None, sa_column=Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), primary_key=True))

    users: List["UserOrm"] = Relationship(
        back_populates="teams", link_model=UserTeamAssociation
    )
