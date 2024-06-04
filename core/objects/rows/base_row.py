"""
We separate people, properties and deals into row and detail types.
Rows represent the object you see in the UI, which has little information, is frequently read and needs to support complex queries.
Details represent the full view of the object when you press on the row.
"""
from abc import ABC, abstractmethod
from pydantic import BaseModel

class BaseRow(BaseModel, ABC):
    @classmethod
    @abstractmethod
    def from_orm(cls, orm_object):
        pass

    @abstractmethod
    def to_dict(self):
        pass
