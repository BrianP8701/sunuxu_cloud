from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum as PyEnum
from datetime import datetime

class PropertyType(PyEnum):
    residential = "residential"
    condo = "condo"
    coop = "coop"
    commercial = "commercial"
    land = "land"
    hoa = "hoa"
    industrial = "industrial"
    rental = "rental"
    other = "other"

class PropertyRow(BaseModel):
    id: int
    user_id: int
    address: str = Field(..., max_length=255)
    mls_number: Optional[str] = Field(None, max_length=255)
    type: Optional[PropertyType] = None
    active: Optional[bool] = Field(default=False)
    price: Optional[int] = None
    created: Optional[datetime] = None
    updated: Optional[datetime] = None
    viewed: Optional[datetime] = None
