from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum as PyEnum

from core.types.property_row import PropertyRow


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
    id: Optional[int] = None
    user_id: int

    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = Field(None, max_length=255)
    type: PersonType = Field(default="?")
    custom_type: Optional[str] = None
    active: bool = Field(default=False)
    created: str
    updated: str
    viewed: str
    
    first_name: str = Field(..., max_length=255)
    middle_name: Optional[str] = Field(None, max_length=255)
    last_name: str = Field(..., max_length=255)
    notes: Optional[str] = None
    language: Optional[str] = Field(default="english", max_length=255)

    address: Optional[str] = Field(None, max_length=255)

    street_number: Optional[str] = Field(None, max_length=255)
    street_name: Optional[str] = Field(None, max_length=255)
    street_suffix: Optional[str] = Field(None, max_length=255)
    unit: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=255)
    state: Optional[str] = Field(None, max_length=255)
    zip: Optional[str] = Field(None, max_length=255)
    country: Optional[str] = Field(None, max_length=255)

    custom_fields: Optional[dict] = None

    property_rows: List[PropertyRow] = []
