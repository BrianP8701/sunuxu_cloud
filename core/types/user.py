from pydantic import BaseModel
from typing import List, Optional

from core.database import Database
from core.models import UserOrm


class User(BaseModel):
    id: int
    email: str
    phone: Optional[str]
    first_name: str
    middle_name: Optional[str]
    last_name: str
    custom_person_types: List = []
    custom_property_types: List = []
    custom_transaction_types: List = []
    custom_transaction_statuses: List = []
    custom_participant_roles: List = []

    @classmethod
    def get(cls, user_id: int) -> "User":
        db = Database()
        user = db.get(UserOrm, user_id)
        return cls(**user.to_dict())

    @classmethod
    def batch_get(cls, user_ids: List[int]) -> List["User"]:
        db = Database()
        users = db.batch_query(UserOrm, {"id": user_ids})
        return [cls(**user.to_dict()) for user in users]
