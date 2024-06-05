from core.database.azure_postgresql import AzurePostgreSQLDatabase
from core.enums import Brokerage, State
from core.models.rows.team import TeamRowModel
from core.objects.rows.base_row import BaseRow


class TeamRow(BaseRow):
    id: int
    name: str
    state: State
    brokerage: Brokerage

    @classmethod
    async def query(cls, user_id: int):
        """
        Fetch all team rows for a user.
        """
        db = AzurePostgreSQLDatabase()
        sql = """
        SELECT tr.*
        FROM team_rows tr
        JOIN teams t ON t.row_id = tr.id
        JOIN user_team_association uta ON uta.team_id = t.id
        WHERE uta.user_id = :user_id
        """
        params = {"user_id": user_id}
        result = await db.execute_raw_sql(sql, params)
        return [cls.from_model(TeamRowModel(**row)) for row in result]

    @classmethod
    def from_model(cls, orm):
        return cls(id=orm.id, name=orm.name, state=orm.state, brokerage=orm.brokerage)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "state": self.state,
            "brokerage": self.brokerage,
        }
