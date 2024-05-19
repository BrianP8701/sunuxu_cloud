from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum as PyEnum
from datetime import datetime

class TransactionStatus(PyEnum):
    pending = "pending"
    closed = "closed"
    expired = "expired"
    withdrawn = "withdrawn"
    off_market = "off_market"
    other = "other"

class TransactionType(PyEnum):
    buy = "buy"
    sell = "sell"
    dual = "dual"

class TransactionRow(BaseModel):
    id: int
    user_id: int
    property_id: Optional[int] = None
    name: Optional[str] = None
    status: Optional[TransactionStatus] = None
    type: Optional[TransactionType] = None
    created: Optional[datetime] = None
    updated: Optional[datetime] = None
    viewed: Optional[datetime] = None
