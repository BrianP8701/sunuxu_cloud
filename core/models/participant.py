from sqlmodel import SQLModel, Field, Relationship, DateTime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import Enum
from sqlalchemy.sql import func

if TYPE_CHECKING:
    from core.models.deal import Deal
    from core.models.participant_details import ParticipantDetails

class Participant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    deal_id: int = Field(foreign_key="deals.id", nullable=False, sa_column_kwargs={"ondelete": "CASCADE"})

    role: Optional[Enum] = Field(
        sa_column=Enum(
            "buyer",
            "seller",
            "buyer_agent",
            "seller_agent",
            "buyer_attorney",
            "seller_attorney",
            "buyer_agent_broker",
            "seller_agent_broker",
            "custom",
            name="participant_roles",
        )
    )
    custom_role: Optional[str] = None

    created: Optional[DateTime] = Field(default=func.now(), index=True)
    updated: Optional[DateTime] = Field(default=func.now(), sa_column_kwargs={"onupdate": func.now()}, index=True)
    viewed: Optional[DateTime] = Field(default=None, index=True)

    deal: Optional["Deal"] = Relationship(back_populates="participants")
    participant_details: Optional["ParticipantDetails"] = Relationship(
        back_populates="participant", 
        sa_relationship_kwargs={"uselist": False, "cascade": "all, delete-orphan"}
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "person_id": self.person_id,
            "role": self.role,
            "custom_role": self.custom_role,
            "created": self.created,
            "updated": self.updated,
            "viewed": self.viewed,
            "name": self.person_row.name,
            "email": self.person_row.email,
            "phone": self.person_row.phone,
        }
