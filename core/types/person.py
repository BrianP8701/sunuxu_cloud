from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum as PyEnum

class PersonType(PyEnum):
    lead = "lead"
    prospect = "prospect"
    client = "client"
    past_client = "past_client"
    agent = "agent"
    broker = "broker"
    attorney = "attorney"
    other = "other"
    mystery = "?"

class Person(BaseModel):
    id: int
    user_id: int
    notes: Optional[str] = None
    language: Optional[str] = Field(default="english", max_length=255)
    first_name: str = Field(..., max_length=255)
    middle_name: Optional[str] = Field(None, max_length=255)
    last_name: str = Field(..., max_length=255)
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = Field(None, max_length=255)
    type: Optional[PersonType] = Field(default="?")
    active: Optional[bool] = Field(default=False)
    created: Optional[str] = None
    updated: Optional[str] = None
    viewed: Optional[str] = None

    class Config:
        orm_mode = True
