from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Column, ForeignKey, Integer
from sqlmodel import Field, Relationship, SQLModel

from core.models.associations import UserTeamAssociation

if TYPE_CHECKING:
    from core.models.entities.user import UserModel
    from core.models.rows.team import TeamRowModel


class TeamModel(SQLModel, table=True):
    __tablename__ = "teams"
    id: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, ForeignKey("team_rows.id"), primary_key=True)
    )

    users: List["UserModel"] = Relationship(
        back_populates="teams",
        link_model=UserTeamAssociation,
        sa_relationship_kwargs={"cascade": "all"}
    )
    row: "TeamRowModel" = Relationship(
        sa_relationship_kwargs={
            "uselist": False,
            "single_parent": True,
            "cascade": "all, delete-orphan",
            "back_populates": None
        }
    )
