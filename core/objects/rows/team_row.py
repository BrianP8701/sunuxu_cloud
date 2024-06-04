from core.database.azure_postgresql import AzurePostgreSQLDatabase
from core.models.rows.team import TeamRowOrm
from core.objects.rows.base_row import BaseRow
from core.enums import State, Brokerage

class TeamRow(BaseRow):
    id: int
    name: str
    state: State
    brokerage: Brokerage

    @classmethod
    def from_orm(cls, team):
        return cls(
            id=team.id,
            name=team.name,
            state=team.state,
            brokerage=team.brokerage
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "state": self.state,
            "brokerage": self.brokerage
        }

    @classmethod
    async def query(cls, user_id: int):
        """
        Fetch all team rows for a user.
        """
        db = AzurePostgreSQLDatabase()
        teams = await db.query_with_user_and_conditions(
            model_class=TeamRowOrm,
            user_id=user_id,
            sort_by="id",
            ascending=True,
            page_size=-1,
            offset=0,
            include={}
        )
        return [cls.from_orm(team) for team in teams]
