from pydantic import BaseModel, Field
from typing import Optional, List

from core.database import Database
from core.models import PropertyOrm
from core.enums.property_type import PropertyType


class PropertyRow(BaseModel):
    id: int
    user_id: int
    address: str = Field(..., max_length=255)
    mls_number: Optional[str] = Field(None, max_length=255)
    type: PropertyType = Field(default=PropertyType.UNKNOWN)
    custom_type: Optional[str] = None
    active: bool = Field(default=False)
    price: Optional[int] = None

    @classmethod
    def get(cls, property_id: int) -> "PropertyRow":
        db = Database()
        property = db.get(
            PropertyOrm,
            property_id,
            columns=[
                "id",
                "user_id",
                "address",
                "mls_number",
                "type",
                "custom_type",
                "active",
                "price",
            ],
        )
        return cls(**property.to_dict())

    @classmethod
    def batch_get(cls, property_ids: List[int]) -> List["PropertyRow"]:
        db = Database()
        properties = db.batch_query(
            PropertyOrm,
            property_ids,
            columns=[
                "id",
                "user_id",
                "address",
                "mls_number",
                "type",
                "custom_type",
                "active",
                "price",
            ],
        )
        return [cls(**property.to_dict()) for property in properties]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "address": self.address,
            "mls_number": self.mls_number,
            "type": self.type,
            "active": self.active,
            "price": self.price,
        }
