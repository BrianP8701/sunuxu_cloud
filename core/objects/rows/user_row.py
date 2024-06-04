from typing import Optional, Dict, Any  

from core.models.rows.user import UserRowOrm
from core.utils.strings import assemble_name
from core.objects.rows.base_row import BaseRow

class UserRow(BaseRow):
    id: int
    email: str
    phone: Optional[str]
    name: Optional[str]
    avatar: Optional[str]

    orm: UserRowOrm

    @classmethod
    def from_orm(cls, user: UserRowOrm) -> "UserRow":
        return cls(
            id=user.id,
            email=user.email,
            phone=user.phone,
            name=assemble_name(user.first_name, user.middle_name, user.last_name),
            avatar=user.avatar,
            orm=user
        )

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "phone": self.phone,
            "name": self.name,
            "avatar": self.avatar,
        }
    
    @classmethod
    def query(cls, user_id: int, sort_by: str, ascending: bool, page_size: int, offset: int, include: Dict[str, Any]):
        """ Might or might not need this """
        pass
