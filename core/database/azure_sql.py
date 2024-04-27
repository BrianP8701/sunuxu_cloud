import os
from dotenv import load_dotenv
import time
from functools import wraps

from sqlalchemy.exc import DisconnectionError, SQLAlchemyError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from core.database.abstract_sql import AbstractSQLDatabase, Base

load_dotenv()

def retry_on_disconnection(retries=3, delay=2):
    """
    A decorator to retry a function if a DisconnectionError occurs.
    :param retries: Number of retries
    :param delay: Delay between retries in seconds
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except DisconnectionError:
                    if attempts == retries - 1:
                        raise
                    attempts += 1
                    time.sleep(delay)  # wait before retrying
                except SQLAlchemyError as e:
                    # Handle other SQLAlchemy errors if necessary
                    raise e
        return wrapper
    return decorator

class AzureSQLDatabase(AbstractSQLDatabase):
    _instance = None

    def __init__(self):
        db_url = os.getenv('AZURE_SQL_URL')
        print(f"Connecting to database: {db_url}")
        self.connection_string = db_url  
        self.engine = create_engine(db_url, pool_pre_ping=True)
        Base.metadata.bind = self.engine  
        Base.metadata.reflect(self.engine)
        self.sessionmaker = sessionmaker(bind=self.engine)

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AzureSQLDatabase, cls).__new__(cls)
        return cls._instance

    @classmethod
    def dispose_instance(cls):
        if cls._instance:
            cls._instance.engine.dispose()
            cls._instance = None

    @retry_on_disconnection()
    def create_tables(self):
        Base.metadata.create_all(self.engine)

    @retry_on_disconnection()
    def delete_tables(self):
        Base.metadata.drop_all(self.engine)

    @retry_on_disconnection()
    def insert(self, model):
        session = self.sessionmaker()
        with session as session:
            session.add(model)
            session.commit()
            session.refresh(model)
            return model

    @retry_on_disconnection()
    def update(self, model):
        session = self.sessionmaker()
        with session as session:
            session.merge(model)
            session.commit()

    @retry_on_disconnection()
    def delete(self, model_class, conditions):
        session = self.sessionmaker()
        with session as session:
            query = session.query(model_class).filter_by(**conditions)
            query.delete()
            session.commit()

    @retry_on_disconnection()
    def query(self, model_class, conditions=None):
        session = self.sessionmaker()
        with session as session:
            query = session.query(model_class)
            if conditions:
                query = query.filter_by(**conditions)
            return query.all()

    @retry_on_disconnection()
    def exists(self, model_class, conditions=None):
        session = self.sessionmaker()
        with session as session:
            query = session.query(model_class)
            if conditions:
                query = query.filter_by(**conditions)
            return query.limit(1).count() > 0

    @retry_on_disconnection()
    def execute_raw_sql(self, sql: str):
        session = self.sessionmaker()
        with session as session:
            result = session.execute(text(sql))
            if result.returns_rows:
                return result.fetchall()
            else:
                session.commit()
                return None

    @retry_on_disconnection()
    def perform_transaction(self, operations: callable):
        session = self.sessionmaker()
        try:
            operations(session)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    @retry_on_disconnection() 
    def clear_database(self, safety: str):
        """
        Clear all data in the database. This operation is irreversible.
        
        Set the safety parameter to "I understand this will delete all data" to confirm the operation.
        """
        if safety != "I understand this will delete all data":
            raise ValueError("Safety string does not match. Set the safety parameter to 'I understand this will delete all data' to confirm the operation.")
        if os.getenv('MODE') == 'production':
            raise Exception("Cannot clear database in production.")
        else:
            session = self.sessionmaker()
            with session as session:
                meta = Base.metadata
                for table in reversed(meta.sorted_tables):
                    print(f"Clearing table: {table}")
                    session.execute(table.delete())
                session.commit()
            print("Database cleared successfully")