from typing import Optional

from core.database import Database
from core.models.rows.user import UserRowModel
from core.objects.rows.base_row import BaseRow
from core.utils.strings import assemble_name


class UserRow(BaseRow):
    id: int
    email: str
    phone: Optional[str]
    name: Optional[str]
    avatar: Optional[str]

    orm: UserRowModel

    @classmethod
    async def query(cls, user_id: int):
        """Get the users row"""
        db = Database()

        user_row = await db.get(UserRowModel, user_id)
        return cls.from_model(user_row)

    @classmethod
    def from_model(cls, orm: UserRowModel) -> "UserRow":
        return cls(
            id=orm.id,
            email=orm.email,
            phone=orm.phone,
            name=assemble_name(orm.first_name, orm.middle_name, orm.last_name),
            avatar=orm.avatar,
            orm=orm,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "phone": self.phone,
            "name": self.name,
            "avatar": self.avatar,
        }
