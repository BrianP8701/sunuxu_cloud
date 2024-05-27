from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from core.models.property import PropertyOrm
from core.enums.property_type import PropertyType
from core.models.property import Property
from core.utils.strings import assemble_address


class PropertyRow(BaseModel):
    id: Optional[int]
    address: str
    mls_number: Optional[str]
    type: PropertyType
    custom_type: Optional[str]
    active: bool
    price: Optional[int]

    orm: Optional[Property]

    @classmethod
    def from_orm(cls, property: PropertyOrm):
        return cls(
            id=property,
            address=assemble_address(
                property.street_number, property.street_name, 
                property.street_suffix, property.city, property.unit, 
                property.state, property.zip_code
            ),
            mls_number=property.mls_number,
            type=property.type,
            custom_type=property.custom_type,
            active=property.active,
            price=property.price,
            orm=property
        )

    def to_dict(self):
        return {
            "id": self.id,
            "address": self.address,
            "mls_number": self.mls_number,
            "type": self.type.value,
            "custom_type": self.custom_type,
            "active": self.active,
            "price": self.price
        }
