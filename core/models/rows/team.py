from typing import List, Optional

from sqlalchemy import Column
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel

from core.enums.brokerage import Brokerage
from core.enums.state import State


class TeamRowModel(SQLModel, table=True):
    __tablename__ = "team_rows"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, nullable=False)

    office_address: Optional[str] = Field(default=None, max_length=255)
    state: Optional[State] = Field(sa_column=SqlEnum(State))
    brokerage: Optional[Brokerage] = Field(sa_column=SqlEnum(Brokerage))

    user_ids: List[int] = Field(sa_column=Column(JSONB), default=[])

    __table_args__ = (Index("team_user_ids", "user_ids", postgresql_using="gin"),)
