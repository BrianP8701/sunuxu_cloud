from abc import ABC, abstractmethod
from typing import Any
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class AbstractSQLDatabase(ABC):
    @abstractmethod
    def reset_instance(self) -> None:
        pass

    @abstractmethod
    def create_tables(self) -> None:
        pass

    @abstractmethod
    def insert(self, model: Any) -> None:
        pass

    @abstractmethod
    def update(self, model: Any) -> None:
        pass

    @abstractmethod
    def delete(self, model: Any) -> None:
        pass

    @abstractmethod
    def delete_by_id(self, model_class: Any, id: int) -> None:
        pass

    @abstractmethod
    def query(self, model_class: Any, conditions: dict = None) -> list:
        pass

    @abstractmethod
    def execute_raw_sql(self, sql: str) -> Any:
        pass

    @abstractmethod
    def perform_transaction(self, operations: callable) -> None:
        pass

    @abstractmethod
    def clear_database(self, safety: str) -> None:
        pass
