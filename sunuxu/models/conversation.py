from pydantic import BaseModel
from typing import List

class Conversation(BaseModel):
    person_id: int
    active_transactions: List[int]