from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Type, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound="BaseEntity")


class BaseEntity(BaseModel, ABC, Generic[T]):
    """
    Entities represent the logical objects used in the application. In the API
    layer we don't directly interact with the database or data models; the entities
    abstract that away.

    Entities can be sent to the client with the to_dict() method, which also
    removes any sensitive information.
    """

    @classmethod
    @abstractmethod
    async def create(cls: Type[T], user_id: int, data: Dict[str, Any]) -> T:
        """
        Create a new entity.
        """
        pass

    @classmethod
    @abstractmethod
    def read(cls: Type[T], id: int, **kwargs) -> T:
        """
        Read an entity by its ID with any additional arguments needed.

        The entity should be returned as a BaseEntity object and is suitable to be
        sent to the client.
        """
        pass

    @classmethod
    @abstractmethod
    async def update(cls: Type[T], id: int, updates: Dict[str, Any]) -> T:
        """
        Update an entity by its ID with the given updates.

        This function only handles simple primitive updates. Each concrete
        class will need to implement its own logic for updating relationships
        and associations.
        """
        pass

    @classmethod
    @abstractmethod
    async def delete(cls: Type[T], id: int, **kwargs) -> None:
        """
        Delete an entity by its ID with any additional arguments needed.

        Handle cascade logic appropriately.
        """
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the entity into a dictionary to be sent to the client, ensuring
        that any sensitive information is removed.
        """
        pass
