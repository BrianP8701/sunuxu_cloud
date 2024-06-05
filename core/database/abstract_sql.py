from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type

from sqlalchemy.orm import declarative_base
from sqlmodel import SQLModel

Base = declarative_base()


class AbstractSQLDatabase(ABC):
    @abstractmethod
    async def dispose_instance(self) -> None:
        """
        Disposes the database instance, effectively clearing any existing connections.
        """
        pass

    @abstractmethod
    async def create_tables(self) -> None:
        """
        Creates tables in the database based on the defined models.
        """
        pass

    @abstractmethod
    async def create(self, model: SQLModel, session: Optional[Any] = None) -> SQLModel:
        """
        Inserts a new record into the database.

        :param model: The model instance to be inserted.
        :param session: Optional; an existing database session.
        :return: The inserted model instance.
        """
        pass

    @abstractmethod
    async def update(self, model: SQLModel, session: Optional[Any] = None) -> None:
        """
        Updates an existing record in the database.

        :param model: The model instance to be updated.
        :param session: Optional; an existing database session.
        """
        pass

    @abstractmethod
    async def delete(
        self,
        model_class: Type[SQLModel],
        conditions: dict,
        session: Optional[Any] = None,
    ) -> None:
        """
        Deletes a record from the database.

        :param model_class: The class of the model to delete.
        :param conditions: A dictionary of conditions to filter the query.
        :param session: Optional; an existing database session.
        """
        pass

    @abstractmethod
    async def query(
        self,
        model_class: Type[SQLModel],
        conditions: dict = None,
        columns: List[str] = None,
        limit: int = None,
        offset: int = None,
        order_by: Any = None,
        eager_load: List[str] = None,
        session: Optional[Any] = None,
    ) -> List[SQLModel]:
        """
        Queries the database for records matching the specified conditions.

        :param model_class: The class of the model to query.
        :param conditions: A dictionary of conditions to filter the query.
        :param columns: A list of columns to select.
        :param limit: The maximum number of records to return.
        :param offset: The number of records to skip.
        :param order_by: The column to order the results by.
        :param eager_load: A list of relationships to eagerly load.
        :param session: Optional; an existing database session.
        :return: A list of model instances that match the query.
        """
        pass

    @abstractmethod
    async def exists(
        self,
        model_class: Type[SQLModel],
        conditions: dict = None,
        session: Optional[Any] = None,
    ) -> bool:
        """
        Checks if a record exists in the database.

        :param model_class: The class of the model to check.
        :param conditions: A dictionary of conditions to filter the query.
        :param session: Optional; an existing database session.
        :return: True if a record exists, False otherwise.
        """
        pass

    @abstractmethod
    async def execute_raw_sql(self, sql: str, session: Optional[Any] = None) -> Any:
        """
        Executes a raw SQL query against the database.

        :param sql: The SQL query to execute.
        :param session: Optional; an existing database session.
        :return: The result of the query execution.
        """
        pass

    @abstractmethod
    async def perform_transaction(
        self, operations: callable, session: Optional[Any] = None
    ) -> None:
        """
        Performs a series of operations within a database transaction.

        :param operations: A callable that contains the operations to be performed.
        :param session: Optional; an existing database session.
        """
        pass

    @abstractmethod
    async def clear_tables(self, session: Optional[Any] = None) -> None:
        """
        Clears all data from the database. This operation is irreversible.

        :param session: Optional; an existing database session.
        """
        pass

    @abstractmethod
    async def delete_by_id(
        self, model_class: Type[SQLModel], id: int, session: Optional[Any] = None
    ) -> None:
        """
        Deletes a record by its ID.

        :param model_class: The class of the model to delete.
        :param id: The primary key ID of the record to delete.
        :param session: Optional; an existing database session.
        """
        pass

    @abstractmethod
    async def update_fields(
        self,
        model_class: Type[SQLModel],
        id: int,
        updates: Dict[str, Any],
        session: Optional[Any] = None,
    ) -> None:
        """
        Updates specific fields of a database entry identified by id.

        :param model_class: The class of the model to update.
        :param id: The primary key ID of the record to update.
        :param updates: A dictionary of the fields to update.
        :param session: Optional; an existing database session.
        """
        pass

    @abstractmethod
    async def batch_insert(
        self, models: List[SQLModel], session: Optional[Any] = None
    ) -> None:
        """
        Inserts multiple records into the database in a batch.

        :param models: A list of model instances to be inserted.
        :param session: Optional; an existing database session.
        """
        pass

    @abstractmethod
    async def batch_delete(
        self,
        model_class: Type[SQLModel],
        conditions: dict,
        session: Optional[Any] = None,
    ) -> None:
        """
        Deletes multiple records from the database in a batch.

        :param model_class: The class of the model to delete.
        :param conditions: A dictionary of conditions to filter the query.
        :param session: Optional; an existing database session.
        """
        pass

    @abstractmethod
    async def batch_get(
        self,
        model_class: Type[SQLModel],
        ids: List[int],
        columns: List[str] = None,
        eager_load: List[str] = None,
        session: Optional[Any] = None,
    ) -> List[SQLModel]:
        """
        Retrieves multiple records by their IDs.

        :param model_class: The class of the model to retrieve.
        :param ids: A list of primary key IDs of the records to retrieve.
        :param columns: A list of columns to select.
        :param eager_load: A list of relationships to eagerly load.
        :param session: Optional; an existing database session.
        :return: A list of model instances that match the query.
        """
        pass

    @abstractmethod
    async def query_with_user_and_conditions(
        self,
        model_class: Type[SQLModel],
        user_id: int,
        sort_by: str,
        ascending: bool,
        page_size: int,
        offset: int,
        include: Dict[str, Any],
        session: Optional[Any] = None,
    ) -> List[SQLModel]:
        """
        Queries the database for records of a given model class, filtered by user ID and additional conditions.

        :param model_class: The class of the model to query.
        :param user_id: The user ID to filter the records by.
        :param sort_by: The column name to sort the results by.
        :param ascending: Boolean indicating whether the sorting should be in ascending order.
        :param page_size: The number of records to return per page. If -1, pagination is not applied.
        :param offset: The offset to start the pagination from.
        :param include: A dictionary of additional conditions to filter the records by.
        :param session: Optional; an existing database session.
        :return: A list of model instances that match the query conditions.
        """
        pass

    @abstractmethod
    async def read(
        self,
        model_class: Type[SQLModel],
        id: int,
        columns: List[str] = None,
        eager_load: List[str] = None,
        session: Optional[Any] = None,
    ) -> SQLModel:
        """
        Reads a single record by its ID.

        :param model_class: The class of the model to read.
        :param id: The primary key ID of the record to read.
        :param columns: A list of columns to select.
        :param eager_load: A list of relationships to eagerly load.
        :param session: Optional; an existing database session.
        :return: The model instance that matches the query.
        """
        pass

    async def _enable_extensions(self) -> None:
        """
        Enables necessary database extensions.
        """
        pass

    def get_session(self) -> Any:
        """
        Gets a new database session.

        :return: A new database session.
        """
        pass

    async def delete_tables(self) -> None:
        """
        Deletes all tables in the database.
        """
        pass
