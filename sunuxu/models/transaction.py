from pydantic import BaseModel
from typing import List
from enum import Enum

class TransactionType(str, Enum):
    Sale = "sale"
    Rental = "rental"

class OurRole(str, Enum):
    sellers_agent = "sellers_agent"
    buyers_agent = "buyers_agent"
    dual_agent = "dual_agent"



class Transaction(BaseModel):
    transaction_id: int
    our_role: str
    transaction_type: str
    participants: List[str]
    stage: int
