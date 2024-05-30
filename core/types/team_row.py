from pydantic import BaseModel

from core.enums import Enums

class TeamRow(BaseModel):
    id: int
    name: str
    state: Enums.State
    office_address: str
    brokerage: Enums.Brokerage
