from core.database import Database
from core.models.rows.person import PersonRowModel
from core.models.rows.property import PropertyRowModel
from core.models.rows.user import UserRowModel
from core.objects.base_entities.base_person import BasePerson


class Person(BasePerson):
    async def set_residence(self, property_id: int):
        db = Database()
        person = self.person_orm
        property = await db.read(PropertyRowModel, property_id)

        person.residence = property

        async with db.get_session() as session:
            await db.update(person, session)

    async def clear_residence(self):
        db = Database()
        person = self.person_orm

        person.residence = None

        async with db.get_session() as session:
            await db.update(person, session)

    async def add_to_portfolio(self, property_id: int):
        db = Database()
        person = self.person_orm
        property = await db.read(PropertyRowModel, property_id)

        person.portfolio.append(property)

        async with db.get_session() as session:
            await db.update(person, session)

    async def remove_from_portfolio(self, property_id: int):
        db = Database()
        person = self.person_orm
        property = await db.read(PropertyRowModel, property_id)

        person.portfolio.remove(property)

        async with db.get_session() as session:
            await db.update(person, session)

    async def add_user(self, user_id: int):
        db = Database()
        person = self.person_orm
        user = await db.read(UserRowModel, user_id)

        person.user_ids.append(user.id)
        person.users.append(user)

        await db.update_fields(
            PersonRowModel,
            self.id,
            {"user_ids": person.user_ids, "users": person.users},
        )
