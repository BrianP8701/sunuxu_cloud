from datetime import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar

from core.database import Database
from core.models.associations import UserTeamAssociation
from core.models.entities.team import TeamModel
from core.models.rows.team import TeamRowModel
from core.objects.base_entities.base_entity import BaseEntity
from core.objects.rows.person_row import PersonRow
from core.objects.rows.user_row import UserRow

T = TypeVar("T", bound="BaseTeam")


class BaseTeam(BaseEntity):
    id: int
    name: str
    state: str
    office_address: str
    brokerage: str
    members: List[PersonRow]

    team_row_model: Optional[TeamRowModel]
    team_model: Optional[TeamModel]

    @classmethod
    async def create(cls: Type[T], user_id: int, data: Dict[str, Any]) -> T:
        """
        Creates a new team entry in the database.

        :param user_id:
            The ID of the user creating the team.
        :param data:
            A dictionary containing the team details:
            - 'name' (str): The name of the team. (Required)
            - 'state' (str): The state where the team is located. (Required)
            - 'office_address' (str): The office address of the team. (Required)
            - 'brokerage' (str): The brokerage of the team. (Required)
        """
        db = Database()

        team_row = TeamRowModel(
            name=data["name"],
            state=data["state"],
            office_address=data["office_address"],
            brokerage=data["brokerage"],
            user_ids=[user_id],
        )

        team = TeamModel()

        user_association = UserTeamAssociation(user_id=user_id, team_id=team.id)

        async with db.get_session() as session:
            try:
                await db.create(TeamRowModel, team_row, session)
                team.row = team_row
                await db.create(TeamModel, team, session)
                await db.add_association(user_association, session)
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
                        "row",
                        "users.row",
                    ],
                )
                await db.update_fields(
                    TeamRowModel, team.id, {"viewed": datetime.utcnow()}, session
                )
            except Exception as e:
                await session.rollback()
                raise e
            else:
                await session.commit()

        users = [UserRow.from_model(user.row) for user in team.users]

        return cls(
            id=team.id,
            name=team.row.name,
            state=team.row.state,
            office_address=team.row.office_address,
            brokerage=team.row.brokerage,
            members=users,
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

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "state": self.state,
            "office_address": self.office_address,
            "brokerage": self.brokerage,
            "members": [member.to_dict() for member in self.members]
            if self.members
            else [],
        }
