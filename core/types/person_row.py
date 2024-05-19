from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum as PyEnum
from datetime import datetime

class PersonType(PyEnum):
    lead = "lead"
    prospect = "prospect"
    client = "client"
    past_client = "past_client"
    agent = "agent"
    broker = "broker"
    attorney = "attorney"
    custom = "custom"
    mystery = "?"

class PersonRow(BaseModel):
    id: int
    user_id: int
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    type: Optional[PersonType] = None
    active: Optional[bool] = Field(default=False)
    created: Optional[datetime] = None
    updated: Optional[datetime] = None
    viewed: Optional[datetime] = None
