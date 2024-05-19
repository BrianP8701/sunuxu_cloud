import os
from dotenv import load_dotenv
import asyncio
from functools import wraps

from sqlalchemy.exc import DisconnectionError, SQLAlchemyError, OperationalError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, func, text, or_
from sqlalchemy.orm import joinedload, load_only

from core.database.abstract_sql import AbstractSQLDatabase, Base
from core.models import *

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


class AzurePostgreSQLDatabase(AbstractSQLDatabase):
    _instance = None

    def __init__(self):
        db_url = os.getenv("AZURE_POSTGRES_CONN_STRING")
        self.connection_string = db_url
        ssl_args = {
            "ssl": "require"
        }
        self.engine = create_async_engine(
            self.connection_string,
            connect_args=ssl_args,
            pool_pre_ping=True,
            pool_size=20,  # Adjust based on your typical workload
            max_overflow=30,  # Allows 30 additional connections beyond the pool size
            pool_timeout=30,  # Number of seconds to wait before giving up on getting a connection from the pool
            pool_recycle=1800,  # Forces connections to be recycled every half hour
        )
        Base.metadata.bind = self.engine
        self.sessionmaker = sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AzurePostgreSQLDatabase, cls).__new__(cls)
        return cls._instance

    async def _enable_extensions(self):
        async with self.engine.begin() as conn:
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm;"))
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;"))

    @classmethod
    async def dispose_instance(cls):
        if cls._instance:
            await cls._instance.engine.dispose()
            cls._instance = None

    @retry_on_disconnection()
    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @retry_on_disconnection()
    async def delete_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    @retry_on_disconnection()
    async def clear_tables(self):
        async with self.sessionmaker() as session:
            meta = Base.metadata
            for table in reversed(meta.sorted_tables):
                await session.execute(table.delete())
            await session.commit()

    @retry_on_disconnection()
    async def insert(self, model):
        async with self.sessionmaker() as session:
            session.add(model)
            await session.commit()
            await session.refresh(model)
            return model

    @retry_on_disconnection()
    async def update(self, model):
        async with self.sessionmaker() as session:
            await session.merge(model)
            await session.commit()

    @retry_on_disconnection()
    async def delete(self, model_class, conditions):
        async with self.sessionmaker() as session:
            query = select(model_class)
            for key, value in conditions.items():
                query = query.filter(getattr(model_class, key) == value)
            result = await session.execute(query)
            for instance in result.scalars().all():
                await session.delete(instance)
            await session.commit()

    @retry_on_disconnection()
    async def query(self, model_class, conditions=None, columns=None):
        async with self.sessionmaker() as session:
            if columns:
                query = select([getattr(model_class, column) for column in columns])
            else:
                query = select(model_class)

            if conditions:
                for key, value in conditions.items():
                    query = query.filter(getattr(model_class, key) == value)

            result = await session.execute(query)
            return result.scalars().all()

    @retry_on_disconnection()
    async def get(self, model_class, id):
        async with self.sessionmaker() as session:
            query = select(model_class)
            query = query.filter(model_class.id == id)
            result = await session.execute(query)
            return result.scalars().first()

    @retry_on_disconnection()
    async def exists(self, model_class, conditions=None):
        async with self.sessionmaker() as session:
            query = select(model_class)
            if conditions:
                for key, value in conditions.items():
                    query = query.filter(getattr(model_class, key) == value)
            result = await session.execute(query)
            return result.scalars().first() is not None

    @retry_on_disconnection()
    async def execute_raw_sql(self, sql: str):
        async with self.sessionmaker() as session:
            # Explicitly declare the SQL as text
            result = await session.execute(text(sql))
            if result.returns_rows:
                return result.fetchall()
            else:
                await session.commit()
                return None

    @retry_on_disconnection()
    async def perform_transaction(self, operations: callable):
        async with self.sessionmaker() as session:
            try:
                await operations(session)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e

    @retry_on_disconnection()
    async def batch_insert(self, models):
        async with self.sessionmaker() as session:
            session.add_all(models)
            await session.commit()

    @retry_on_disconnection()
    async def batch_delete(self, model_class, conditions):
        async with self.sessionmaker() as session:
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
    async def batch_query(self, model_class, conditions=None, columns=None):
        async with self.sessionmaker() as session:
            if columns:
                column_objects = [
                    getattr(model_class, column) for column in columns
                ]  # Removed .expression for testing
                query = select(*column_objects)
            else:
                query = select(model_class)

            if conditions:
                for key, value in conditions.items():
                    if isinstance(value, list):
                        query = query.filter(getattr(model_class, key).in_(value))
                    else:
                        query = query.filter(getattr(model_class, key) == value)

            print(query)  # Debug: Print the actual query
            result = await session.execute(query)
            all_results = (
                result.fetchall()
            )  # Changed from result.scalars().all() to fetchall()
            print(all_results)  # Debug: Print the results
            return all_results
