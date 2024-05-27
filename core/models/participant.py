from sqlmodel import SQLModel, Field, Relationship, DateTime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import Enum as SqlEnum, Column, DateTime
from sqlalchemy.sql import func
from datetime import datetime

from core.enums.participant_role import ParticipantRole

if TYPE_CHECKING:
    from core.models.deal import DealOrm
    from core.models.participant_details import ParticipantDetailsOrm
    from core.models.person import PersonOrm

class ParticipantOrm(SQLModel, table=True):
    __tablename__ = "participants"
    id: Optional[int] = Field(default=None, primary_key=True)

    role: ParticipantRole = Field(sa_column=Column(SqlEnum(ParticipantRole), index=True, nullable=False, default=ParticipantRole.UNKNOWN))
    custom_role: Optional[str] = None

    created: datetime = Field(index=True)    
    updated: Optional[datetime] = Field(sa_column=Column(DateTime, index=True, default=None, onupdate=func.now()))
    viewed: Optional[datetime] = Field(index=True)

    person: PersonOrm = Relationship(uselist=False)
    deal: Optional["DealOrm"] = Relationship(back_populates="participants")
    participant_details: Optional["ParticipantDetailsOrm"] = Relationship(
        back_populates="participant", 
        sa_relationship_kwargs={"uselist": False, "cascade": "all, delete-orphan"}
    )
