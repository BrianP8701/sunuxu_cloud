from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Enum as SqlEnum, Column, Index
from sqlalchemy.dialects.postgresql import JSONB

from core.enums.state import State
from core.enums.brokerage import Brokerage

class TeamRowOrm(SQLModel, table=True):
    __tablename__ = "team_rows"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, nullable=False)

    office_address: Optional[str] = Field(default=None, max_length=255)
    state: Optional[State] = Field(sa_column=SqlEnum(State))
    brokerage: Optional[Brokerage] = Field(sa_column=SqlEnum(Brokerage))
    
    user_ids: List[int] = Field(sa_column=Column(JSONB), default=[])

    __table_args__ = (
        Index('team_user_ids', 'user_ids', postgresql_using='gin'),
    )