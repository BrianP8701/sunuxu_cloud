from abc import ABC, abstractmethod
from typing import Any
from sqlalchemy.orm import declarative_base

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
    async def insert(self, model: Any) -> None:
        """
        Inserts a new record into the database.
        
        :param model: The model instance to be inserted.
        """
        pass

    @abstractmethod
    async def update(self, model: Any) -> None:
        """
        Updates an existing record in the database.
        
        :param model: The model instance to be updated.
        """
        pass

    @abstractmethod
    async def delete(self, model: Any) -> None:
        """
        Deletes a record from the database.
        
        :param model_class: The class of the model to delete.
        :param conditions: A dictionary of conditions to filter the query.
        """
        pass

    @abstractmethod
    async def query(self, model_class: Any, conditions: dict = None) -> list:
        """
        Queries the database for records matching the specified conditions.
        
        :param model_class: The class of the model to query.
        :param conditions: A dictionary of conditions to filter the query.
        :return: A list of model instances that match the query.
        """
        pass

    @abstractmethod
    async def exists(self, model_class: Any, conditions: dict) -> bool:
        """
        Checks if a record exists in the database.
        
        :param model_class: The class of the model to check.
        :param conditions: A dictionary of conditions to filter the query.
        :return: True if a record exists, False otherwise.
        """
        pass

    @abstractmethod
    async def execute_raw_sql(self, sql: str) -> Any:
        """
        Executes a raw SQL query against the database.
        
        :param sql: The SQL query to execute.
        :return: The result of the query execution.
        """
        pass

    @abstractmethod
    async def perform_transaction(self, operations: callable) -> None:
        """
        Performs a series of operations within a database transaction.
        
        :param operations: A callable that contains the operations to be performed.
        """
        pass

    @abstractmethod
    async def clear_database(self, safety: str) -> None:
        """
        Clears all data from the database. This operation is irreversible.
        
        :param safety: A safety string that must match a specific value to confirm the operation.
        """
        pass
