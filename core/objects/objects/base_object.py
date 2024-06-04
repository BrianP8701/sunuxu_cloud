from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Any, Dict

class BaseObject(BaseModel, ABC):
    @classmethod
    @abstractmethod
    def read(cls, id: int):
        pass

    @abstractmethod
    def to_dict(self):
        pass

    @abstractmethod
    async def create(self):
        pass

    @classmethod
    @abstractmethod
    async def update(cls, id: int, updates: Dict[str, Any]):
        pass

    @classmethod
    @abstractmethod
    async def delete(cls, id: int):
        pass

    @abstractmethod
    def _assemble_orm(self):
        pass
