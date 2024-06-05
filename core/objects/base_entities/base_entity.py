from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Type, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound="BaseEntity")


class BaseEntity(BaseModel, ABC, Generic[T]):
    @classmethod
    @abstractmethod
    async def create(
        cls: Type[T], user_id: int, data: Dict[str, Any]
    ) -> T:  # Specify the expected schema in each concrete implementation of this
        pass

    @classmethod
    @abstractmethod
    def read(cls: Type[T], id: int) -> T:
        pass

    @classmethod
    @abstractmethod
    async def update(cls: Type[T], id: int, updates: Dict[str, Any]) -> T:
        pass

    @classmethod
    @abstractmethod
    async def delete(cls: Type[T], id: int) -> None:
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

    @classmethod
    @abstractmethod
    def from_orm(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        pass
