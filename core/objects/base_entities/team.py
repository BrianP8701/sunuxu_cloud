from typing import List

from core.objects.base_entities.base_entity import BaseEntity
from core.objects.rows.person_row import PersonRow


class BaseTeam(BaseEntity):
    id: int
    name: str
    state: str
    office_address: str
    brokerage: str
    members: List[PersonRow]
