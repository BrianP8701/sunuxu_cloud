import os
from dotenv import load_dotenv
import time
from functools import wraps

from sqlalchemy.exc import DisconnectionError, SQLAlchemyError, OperationalError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from core.database.abstract_sql import AbstractSQLDatabase, Base

load_dotenv()

def retry_on_disconnection(retries=3, delay=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except (DisconnectionError, OperationalError) as e:
                    if attempts == retries - 1:
                        print(f"Failed after {retries} attempts: {str(e)}")
                        raise
                    print(f"Attempt {attempts+1} failed, retrying in {delay} seconds...")
                    attempts += 1
                    time.sleep(delay)
                except SQLAlchemyError as e:
                    raise e
                except Exception as e:
                    print(f"An unexpected error occurred (take a peek in retry decorator code): {str(e)}")
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
    def batch_insert(self, models):
        session = self.sessionmaker()
        with session as session:
            session.add_all(models)
            session.commit()

    @retry_on_disconnection()
    def batch_delete(self, model_class, conditions):
        session = self.sessionmaker()
        with session as session:
            query = session.query(model_class)
            for attr, value in conditions.items():
                if isinstance(value, list):
                    query = query.filter(getattr(model_class, attr).in_(value))
                else:
                    query = query.filter(getattr(model_class, attr) == value)
            num_deleted = query.delete(synchronize_session='fetch')
            session.commit()
            return num_deleted

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

    @retry_on_disconnection()
    def paginate_query(self, model_class, page_number, page_size, sort_by, sort_direction, columns, **conditions):
        """
            Paginate and filter query results from the database.

            :param model_class: The SQLAlchemy model class that represents the database table you want to query.
            :param page_number: The zero-based index of the page of results you want to retrieve.
            :param page_size: The number of records to return per page.
            :param sort_by: The name of the attribute (column) of the model class by which to sort the results.
            :param sort_direction: The direction of the sort, either 'asc' for ascending or 'desc' for descending.
            :param columns: A list of column names to include in the results. If not specified, all columns are included.
            :param conditions: A variable number of keyword arguments that specify the filtering conditions. These should match the attributes of the model class.
            :return: A list of model instances that match the query parameters, the total number of items matching the conditions, and the total number of pages.
            
        """
        session = self.sessionmaker()
        with session as session:
            # Determine the columns to query
            query_columns = []
            if columns:
                query_columns = [getattr(model_class, column) for column in columns]
            
            # Ensure the sort_by column is included if it's not already in the columns list
            if sort_by and (not columns or sort_by not in columns):
                sort_column = getattr(model_class, sort_by)
                query_columns.append(sort_column)
            else:
                sort_column = getattr(model_class, sort_by) if sort_by else None

            # Build the query with the specified columns
            if query_columns:
                query = session.query(*query_columns)
            else:
                query = session.query(model_class)

            # Apply filters based on conditions
            if conditions:
                for key, value in conditions.items():
                    if isinstance(value, list):
                        query = query.filter(getattr(model_class, key).in_(value))
                    else:
                        query = query.filter(getattr(model_class, key) == value)

            # Count total items matching the conditions
            total_items = query.count()

            # Apply sorting
            if sort_column:
                if sort_direction == 'desc':
                    query = query.order_by(sort_column.desc())
                else:
                    query = query.order_by(sort_column)
            else:
                raise ValueError("sort_by parameter must be provided for pagination in SQL Server")

        # Execute the query with pagination
        result = query.offset(page_number * page_size).limit(page_size).all()

        # Calculate total pages
        total_pages = (total_items + page_size - 1) // page_size

        return result, total_items, total_pages