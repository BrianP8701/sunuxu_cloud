from pydantic import BaseModel
from typing import List, Optional

from core.database import Database
from core.models import UserOrm

class User(BaseModel):
    id: Optional[int]
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

    def insert(self) -> "User":
        if self.id:
            raise ValueError("User already exists")
        db = Database()
        user = UserOrm(**self.model_dump())
        db.insert(user)
        self.id = user.id
        return self

    @classmethod
    def batch_get(cls, user_ids: List[int]) -> List["User"]:
        db = Database()
        users = db.batch_query(UserOrm, {"id": user_ids})
        return [cls(**user.to_dict()) for user in users]

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "phone": self.phone,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "custom_person_types": self.custom_person_types,
            "custom_property_types": self.custom_property_types,
            "custom_transaction_types": self.custom_transaction_types,
            "custom_transaction_statuses": self.custom_transaction_statuses,
            "custom_participant_roles": self.custom_participant_roles
        }

