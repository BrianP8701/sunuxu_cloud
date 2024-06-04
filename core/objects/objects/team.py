from pydantic import BaseModel
from typing import List
from core.objects.rows.person_row import PersonRow
from core.objects.objects.base_object import BaseObject

class Team(BaseObject):
    id: int
    name: str
    state: str
    office_address: str
    brokerage: str
    members: List[PersonRow]

