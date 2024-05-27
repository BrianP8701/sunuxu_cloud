from pydantic import BaseModel
from typing import Optional

from core.models.user import UserOrm

class UserRow(BaseModel):
    id: int
    email: str
    phone: Optional[str]
    first_name: str
    middle_name: Optional[str]
    last_name: str
    avatar: Optional[str]

    orm: UserOrm

    @classmethod
    def from_orm(cls, user: UserOrm) -> "UserRow":
        return cls(
            id=user.id,
            email=user.email,
            phone=user.phone,
            first_name=user.first_name,
            middle_name=user.middle_name,
            last_name=user.last_name,
            avatar=user.avatar,
            orm=user
        )

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "phone": self.phone,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "avatar": self.avatar,
        }
    