from typing import Any, Dict, Optional

from pydantic import BaseModel

from core.database import Database
from core.enums.participant_role import ParticipantRole
from core.models.entities.deal import DealModel
from core.models.rows.person import PersonRowModel
from core.objects.rows.base_row import BaseRow


class ParticipantRow(BaseRow):
    id: Optional[int]
    name: str
    role: ParticipantRole

    orm: Optional[PersonRowModel]

    @classmethod
    async def query(cls, deal_id: int):
        """
        Fetch all participant rows for a deal.
        """
        db = Database()
        sql = """
        SELECT pr.*
        FROM person_rows pr
        JOIN people p ON p.row_id = pr.id
        JOIN deal_person_association dpa ON dpa.person_id = p.id
        WHERE dpa.deal_id = :deal_id
        """
        params = {"deal_id": deal_id}
        result = await db.execute_raw_sql(sql, params)
        return [cls.from_model(PersonRowModel(**row)) for row in result]

    @classmethod
    def from_model(cls, orm: DealModel):
        return [
            cls(
                id=association.person.id,
                name=association.person.name,
                role=association.role,
                orm=orm,
            )
            for association in orm.participants
        ]

    def to_dict(self):
        return {"id": self.id, "name": self.name, "role": self.role.value}
