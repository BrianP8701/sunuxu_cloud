from datetime import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar
from sqlalchemy.orm import joinedload

from core.database import Database
from core.enums import TeamRole, Brokerage, State
from core.models.associations import UserTeamAssociation
from core.models.entities.team import TeamModel
from core.models.rows.team import TeamRowModel
from core.objects.base_entities.base_entity import BaseEntity
from core.objects.rows.user_row import UserRow
from core.models.entities.user import UserModel

T = TypeVar("T", bound="BaseTeam")


class BaseTeam(BaseEntity):
    id: int
    name: str
    state: str
    office_address: str
    brokerage: str
    users: Dict[UserRow, TeamRole]

    team_row_model: Optional[TeamRowModel]
    team_model: Optional[TeamModel]

    @classmethod
    async def create(cls: Type[T], data: Dict[str, Any]) -> T:
        """
        Creates a new team entry in the database.

        :param data:
            A dictionary containing the team details:
            - 'name' (str): The name of the team. (Required)
            - 'state' (str): The state where the team is located. (Required)
            - 'office_address' (str): The office address of the team. (Required)
            - 'brokerage' (str): The brokerage of the team. (Required)
            - 'users' (Dict[int, str]): Dictionary of user IDs and their roles. TeamRole enum. (Required)
        """
        db = Database()

        team_row = TeamRowModel(
            name=data["name"],
            state=State(data["state"]),
            office_address=data["office_address"],
            brokerage=Brokerage(data["brokerage"]),
            user_ids=list(data["users"].keys()),  # Store user IDs in the team row
        )

        team = TeamModel()

        # Prepare user-team associations
        user_associations = [
            UserTeamAssociation(user_id=user_id, team_id=team.id, role=TeamRole(role))
            for user_id, role in data["users"].items()
        ]

        async with db.get_session() as session:
            try:
                await db.create(TeamRowModel, team_row, session)
                team.row = team_row
                await db.create(TeamModel, team, session)
                await db.batch_add_associations(user_associations, session)
            except Exception as e:
                await session.rollback()
                raise e
            else:
                await session.commit()

        return await cls.read(team.id)

    @classmethod
    async def read(cls: Type[T], id: int) -> T:
        db = Database()

        async with db.get_session() as session:
            try:
                team = await db.read(
                    TeamModel,
                    id,
                    eager_load=[
                        joinedload(TeamModel.row),
                        joinedload(TeamModel.users).joinedload(UserModel.row),
                        joinedload(TeamModel.users).joinedload(UserModel.teams)
                    ],
                )
            except Exception as e:
                await session.rollback()
                raise e
            else:
                await session.commit()

        users = {
            UserRow.from_model(user.row): next(
                (assoc.role for assoc in user.teams if assoc.team_id == team.id), None
            )
            for user in team.users
        }

        return cls(
            id=team.id,
            name=team.row.name,
            state=team.row.state,
            office_address=team.row.office_address,
            brokerage=team.row.brokerage,
            users=users,
            team_row_model=team.row,
            team_model=team,
        )

    @classmethod
    async def update(cls: Type[T], id: int, updates: Dict[str, Any]) -> T:
        """
        Updates row by replacing columns with values specified in updates.

        :param updates:
            A dictionary containing the team details to update:
            - 'name' (Optional[str]): The name of the team. (Optional)
            - 'state' (Optional[str]): The state where the team is located. (Optional)
            - 'office_address' (Optional[str]): The office address of the team. (Optional)
            - 'brokerage' (Optional[str]): The brokerage of the team. (Optional)
        """
        db = Database()

        team_updates = {}

        for key, value in updates.items():
            if hasattr(TeamRowModel, key):
                team_updates[key] = value

        async with db.get_session() as session:
            try:
                if team_updates:
                    await db.update_fields(TeamRowModel, id, team_updates, session)
            except Exception as e:
                await session.rollback()
                raise e
            else:
                await session.commit()

        return await cls.read(id)

    @classmethod
    async def delete(cls: Type[T], id: int) -> None:
        """Delete a team entry"""
        db = Database()
        async with db.get_session() as session:
            try:
                await db.delete_by_id(TeamRowModel, id, session)
            except Exception as e:
                await session.rollback()
                raise e
            else:
                await session.commit()

    @classmethod
    async def batch_create(cls: Type[T], teams_data: List[Dict[str, Any]]) -> List[T]:
        """
        Creates multiple new team entries in the database.

        :param teams_data: List of dictionaries, each containing the team details as required by the `create` method.
        """
        db = Database()
        team_rows = []
        team_models = []
        user_associations = []

        for data in teams_data:
            team_row = TeamRowModel(
                name=data["name"],
                state=State(data["state"]),
                office_address=data["office_address"],
                brokerage=Brokerage(data["brokerage"]),
                user_ids=list(data["users"].keys())
            )
            team = TeamModel()
            team_rows.append(team_row)
            team_models.append(team)

        async with db.get_session() as session:
            try:
                await db.batch_create(team_rows, session)
                for team, team_row in zip(team_models, team_rows):
                    team.row = team_row
                await db.batch_create(team_models, session)
                user_associations.extend([
                    UserTeamAssociation(user_id=user_id, team_id=team.id, role=TeamRole(role))
                    for user_id, role in data["users"].items()
                ])
                await db.batch_add_associations(user_associations, session)
            except Exception as e:
                await session.rollback()
                raise e
            else:
                await session.commit()

        return [await cls.read(team.id) for team in team_models]

    @classmethod
    async def batch_delete(cls: Type[T], ids: List[int]) -> None:
        """
        Deletes multiple team entries by their IDs.

        :param ids: List of team IDs to delete.
        """
        db = Database()
        async with db.get_session() as session:
            try:
                for id in ids:
                    await db.delete_by_id(TeamRowModel, id, session)
                session.commit()
            except Exception as e:
                await session.rollback()
                raise e

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "state": self.state,
            "office_address": self.office_address,
            "brokerage": self.brokerage,
            "users": [
                {"user": user.to_dict(), "role": role.value}
                for user, role in self.users.items()
            ],
        }
