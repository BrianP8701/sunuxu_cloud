import asyncio
import os
from functools import wraps
from typing import Any, Dict, List, Optional, Type

from dotenv import load_dotenv
from sqlalchemy.exc import (DisconnectionError, OperationalError,
                            SQLAlchemyError)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import joinedload, sessionmaker
from sqlalchemy.sql import text
from sqlmodel import SQLModel, select

load_dotenv()


def retry_on_disconnection(retries=3, delay=2):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return await func(*args, **kwargs)
                except (DisconnectionError, OperationalError) as e:
                    if attempts == retries - 1:
                        print(f"Failed after {retries} attempts: {str(e)}")
                        raise
                    print(
                        f"Attempt {attempts+1} failed, retrying in {delay} seconds..."
                    )
                    attempts += 1
                    await asyncio.sleep(delay)
                except SQLAlchemyError as e:
                    raise e
                except Exception as e:
                    print(f"An unexpected error occurred: {str(e)}")
                    raise e

        return wrapper

    return decorator


class AzurePostgreSQLDatabase:
    _instance = None

    def __init__(self):
        db_url = os.getenv("AZURE_POSTGRES_CONN_STRING")
        self.connection_string = db_url
        ssl_args = {"ssl": "require"}
        self.engine = create_async_engine(
            self.connection_string,
            connect_args=ssl_args,
            pool_pre_ping=True,
            pool_size=20,
            max_overflow=30,
            pool_timeout=30,
            pool_recycle=1800,
        )
        SQLModel.metadata.bind = self.engine
        self.sessionmaker = sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AzurePostgreSQLDatabase, cls).__new__(cls)
        return cls._instance

    async def _enable_extensions(self) -> None:
        async with self.engine.begin() as conn:
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm;"))
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;"))

    @classmethod
    async def dispose_instance(cls) -> None:
        if cls._instance:
            await cls._instance.engine.dispose()
            cls._instance = None

    def get_session(self) -> AsyncSession:
        return self.sessionmaker()

    @retry_on_disconnection()
    async def create_tables(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    @retry_on_disconnection()
    async def list_tables(self) -> List[str]:
        async with self.engine.begin() as conn:
            result = await conn.execute(
                text(
                    "SELECT table_name FROM information_schema.tables WHERE table_schema='public'"
                )
            )
            tables = result.fetchall()
            return [table[0] for table in tables]

    @retry_on_disconnection()
    async def delete_tables(self):
        async with self.engine.begin() as conn:
            tables = await self.list_tables()
            for table in tables:
                print(f"Dropping table {table}")
                await conn.run_sync(
                    lambda conn: conn.execute(
                        text(f"DROP TABLE IF EXISTS {table} CASCADE")
                    )
                )
                print(f"Dropped table {table}")

    @retry_on_disconnection()
    async def clear_tables(self, session: Optional[AsyncSession] = None) -> None:
        async with (session or self.sessionmaker()) as session:
            meta = SQLModel.metadata
            for table in reversed(meta.sorted_tables):
                await session.execute(table.delete())
            await session.commit()

    @retry_on_disconnection()
    async def create(
        self, model: SQLModel, session: Optional[AsyncSession] = None
    ) -> SQLModel:
        async with (session or self.sessionmaker()) as session:
            session.add(model)
            await session.commit()
            await session.refresh(model)
            return model

    @retry_on_disconnection()
    async def update(
        self, model: SQLModel, session: Optional[AsyncSession] = None
    ) -> None:
        async with (session or self.sessionmaker()) as session:
            await session.merge(model)
            await session.commit()

    @retry_on_disconnection()
    async def update_fields(
        self,
        model_class: Type[SQLModel],
        id: int,
        updates: Dict[str, Any],
        session: Optional[AsyncSession] = None,
    ) -> None:
        """
        Update specific fields of a database entry identified by id.
        :param model_class: The SQLModel class of the database model.
        :param id: The primary key ID of the record to update.
        :param update_data: A dictionary of the fields to update.
        :param session: Optional; an existing database session.
        """
        async with (session or self.sessionmaker()) as session:
            # Create a query to select the record to update
            query = select(model_class).where(model_class.id == id)
            result = await session.execute(query)
            instance = result.scalars().first()
            if instance:
                # Update the fields with data from update_data dictionary
                for key, value in updates.items():
                    setattr(instance, key, value)
                await session.commit()
            else:
                raise ValueError(f"No record found with ID {id}")

    @retry_on_disconnection()
    async def delete(
        self,
        model_class: Type[SQLModel],
        conditions: dict,
        session: Optional[AsyncSession] = None,
    ) -> None:
        async with (session or self.sessionmaker()) as session:
            query = select(model_class)
            for key, value in conditions.items():
                query = query.filter(getattr(model_class, key) == value)
            result = await session.execute(query)
            for instance in result.scalars().all():
                await session.delete(instance)
            await session.commit()

    @retry_on_disconnection()
    async def delete_by_id(
        self,
        model_class: Type[SQLModel],
        id: int,
        session: Optional[AsyncSession] = None,
    ) -> None:
        """
        Delete a record by its ID.
        :param model_class: The SQLModel class of the database model.
        :param id: The primary key ID of the record to delete.
        :param session: Optional; an existing database session.
        """
        async with (session or self.sessionmaker()) as session:
            query = select(model_class).where(model_class.id == id)
            result = await session.execute(query)
            instance = result.scalars().first()
            if instance:
                await session.delete(instance)
                await session.commit()
            else:
                raise ValueError(f"No record found with ID {id}")

    @retry_on_disconnection()
    async def query(
        self,
        model_class: Type[SQLModel],
        conditions: dict = None,
        columns: List[str] = None,
        limit: int = None,
        offset: int = None,
        sort_by: str = None,
        ascending: bool = True,
        eager_load: List[str] = None,
        session: Optional[AsyncSession] = None,
    ) -> List[Any]:
        async with (session or self.sessionmaker()) as session:
            if columns:
                query = select([getattr(model_class, column) for column in columns])
            else:
                query = select(model_class)

            if conditions:
                for key, value in conditions.items():
                    if isinstance(value, list):
                        query = query.filter(getattr(model_class, key).in_(value))
                    else:
                        query = query.filter(getattr(model_class, key) == value)

            if eager_load:
                for relation in eager_load:
                    query = query.options(joinedload(relation))

            if sort_by:
                order_by_column = getattr(model_class, sort_by)
                if not ascending:
                    order_by_column = order_by_column.desc()
                query = query.order_by(order_by_column)

            if limit is not None:
                query = query.limit(limit)
            if offset is not None:
                query = query.offset(offset)

            result = await session.execute(query)
            return result.scalars().all()

    @retry_on_disconnection()
    async def read(
        self,
        model_class: Type[SQLModel],
        id: int,
        columns: List[str] = None,
        eager_load: List[str] = None,
        session: Optional[AsyncSession] = None,
    ) -> SQLModel:
        async with (session or self.sessionmaker()) as session:
            if columns:
                query = select([getattr(model_class, column) for column in columns])
            else:
                query = select(model_class)
            query = query.filter(model_class.id == id)

            if eager_load:
                for relation in eager_load:
                    query = query.options(joinedload(relation))

            result = await session.execute(query)
            return result.scalars().first()

    @retry_on_disconnection()
    async def add_association(
        self, association_model: SQLModel, session: Optional[AsyncSession] = None
    ) -> SQLModel:
        """
        Add a new record to an association table.

        :param association_model: The instance of the association model to add.
        :param session: Optional; an existing database session.
        :return: The added association model instance.
        """
        async with (session or self.sessionmaker()) as session:
            session.add(association_model)
            await session.commit()
            await session.refresh(association_model)
            return association_model

    @retry_on_disconnection()
    async def exists(
        self,
        model_class: Type[SQLModel],
        conditions: dict = None,
        session: Optional[AsyncSession] = None,
    ) -> bool:
        async with (session or self.sessionmaker()) as session:
            query = select(model_class)
            if conditions:
                for key, value in conditions.items():
                    query = query.filter(getattr(model_class, key) == value)
            result = await session.execute(query)
            return result.scalars().first() is not None

    @retry_on_disconnection()
    async def execute_raw_sql(
        self,
        sql: str,
        params: Optional[dict] = None,
        session: Optional[AsyncSession] = None,
    ) -> Any:
        async with (session or self.sessionmaker()) as session:
            result = await session.execute(text(sql), params)
            if result.returns_rows:
                return result.fetchall()
            else:
                await session.commit()
                return None

    @retry_on_disconnection()
    async def perform_transaction(
        self, operations: callable, session: Optional[AsyncSession] = None
    ) -> None:
        async with (session or self.sessionmaker()) as session:
            try:
                await operations(session)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e

    @retry_on_disconnection()
    async def batch_create(
        self, models: List[SQLModel], session: Optional[AsyncSession] = None
    ) -> None:
        async with (session or self.sessionmaker()) as session:
            session.add_all(models)
            await session.commit()

    @retry_on_disconnection()
    async def batch_delete(
        self,
        model_class: Type[SQLModel],
        conditions: dict,
        session: Optional[AsyncSession] = None,
    ) -> None:
        async with (session or self.sessionmaker()) as session:
            query = select(model_class)
            for attr, value in conditions.items():
                if isinstance(value, list):
                    query = query.filter(getattr(model_class, attr).in_(value))
                else:
                    query = query.filter(getattr(model_class, attr) == value)
            result = await session.execute(query)
            for instance in result.scalars().all():
                await session.delete(instance)
            await session.commit()

    @retry_on_disconnection()
    async def batch_read(
        self,
        model_class: Type[SQLModel],
        ids: List[int],
        columns: List[str] = None,
        eager_load: List[str] = None,
        session: Optional[AsyncSession] = None,
    ) -> List[SQLModel]:
        async with (session or self.sessionmaker()) as session:
            if columns:
                column_objects = [getattr(model_class, column) for column in columns]
                query = select(*column_objects)
            else:
                query = select(model_class)
            query = query.filter(model_class.id.in_(ids))

            if eager_load:
                for relation in eager_load:
                    query = query.options(joinedload(relation))

            result = await session.execute(query)
            return result.scalars().all()

    @retry_on_disconnection()
    async def batch_add_associations(
        self, associations: List[SQLModel], session: Optional[AsyncSession] = None
    ) -> None:
        """
        Add multiple records to an association table in a batch.

        :param associations: A list of association model instances to add.
        :param session: Optional; an existing database session.
        """
        async with (session or self.sessionmaker()) as session:
            session.add_all(associations)
            await session.commit()

    @retry_on_disconnection()
    async def query_with_user_and_conditions(
        self,
        model_class: Type[SQLModel],
        user_id: int,
        sort_by: str,
        ascending: bool,
        page_size: int,
        offset: int,
        include: Dict[str, Any],
        session: Optional[AsyncSession] = None,
    ) -> List[SQLModel]:
        """
        Query the database for records of a given model class, filtered by user ID and additional conditions.

        :param model_class: The SQLModel class of the database model.
        :param user_id: The user ID to filter the records by.
        :param sort_by: The column name to sort the results by.
        :param ascending: Boolean indicating whether the sorting should be in ascending order.
        :param page_size: The number of records to return per page. If -1, pagination is not applied.
        :param offset: The offset to start the pagination from.
        :param include: A dictionary of additional conditions to filter the records by.
        :param session: Optional; an existing database session.
        :return: A list of SQLModel instances that match the query conditions.
        """
        async with (session or self.sessionmaker()) as session:
            query = select(model_class)

            # Ensure the given user_id is in the user_ids column
            query = query.filter(model_class.user_ids.contains([user_id]))

            # Apply include conditions
            for column, values in include.items():
                column_attr = getattr(model_class, column)
                if isinstance(values, list):
                    query = query.filter(column_attr.in_(values))
                else:
                    query = query.filter(column_attr == values)

            # Apply sorting
            if ascending:
                query = query.order_by(getattr(model_class, sort_by))
            else:
                query = query.order_by(getattr(model_class, sort_by).desc())

            # Apply pagination if page_size is not -1
            if page_size != -1:
                query = query.limit(page_size).offset(offset)

            result = await session.execute(query)
            return result.scalars().all()
