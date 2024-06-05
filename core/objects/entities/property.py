from core.database import Database
from core.models.rows.person import PersonRowModel
from core.objects.base_entities.base_property import BaseProperty
from core.objects.entities.person import Person


class Property(BaseProperty):
    async def add_owner(self, person_id: int):
        db = Database()
        property = self.property_orm
        person = await db.read(PersonRowModel, person_id)

        async with db.get_session() as session:
            property.owners.append(person)
            await db.update(property, session)

    async def remove_owner(self, person_id: int):
        db = Database()
        property = self.property_orm
        person = await db.read(PersonRowModel, person_id)

        async with db.get_session() as session:
            property.owners.remove(person)
            await db.update(property, session)

    async def add_occupant(self, person_id: int):
        db = Database()
        property = self.property_orm
        person = await db.read(PersonRowModel, person_id)

        async with db.get_session() as session:
            property.occupants.append(person)
            await db.update(property, session)

    async def remove_occupant(self, person_id: int):
        db = Database()
        property = self.property_orm
        person = await db.read(PersonRowModel, person_id)

        async with db.get_session() as session:
            property.occupants.remove(person)
            await db.update(property, session)
