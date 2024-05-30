from pydantic import BaseModel
from typing import List
from core.types.person_row import PersonRow

class Team(BaseModel):
    id: int
    name: str
    description: str
    members: List[PersonRow]