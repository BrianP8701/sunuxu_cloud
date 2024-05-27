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
    password: Optional[str] = Field(default=None, max_length=255)

    avatar: Optional[str] = Field(default=None, max_length=255)
    email: str = Field(max_length=255, unique=True, index=True, nullable=False)
    phone: Optional[str] = Field(default=None, max_length=20)
    first_name: str = Field(max_length=255, nullable=False)
    middle_name: Optional[str] = Field(default=None, max_length=255)
    last_name: str = Field(max_length=255, nullable=False)

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
