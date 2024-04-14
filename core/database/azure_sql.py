import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from core.database.abstract_sql import AbstractSQLDatabase, Base

load_dotenv()

class AzureSQLDatabase(AbstractSQLDatabase):
    _instance = None

    def __init__(self):
        db_url = os.getenv('AZURE_SQL_URL')
        print(f"Connecting to database: {db_url}")
        self.connection_string = db_url  
        self.engine = create_engine(db_url)
        Base.metadata.bind = self.engine  # Bind the metadata to the engine
        Base.metadata.reflect(self.engine)  # Reflect the existing tables
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

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def insert(self, model):
        session = self.sessionmaker()
        with session as session:
            session.add(model)
            session.commit()
            session.refresh(model)  # Refresh the model to update the id attribute
            return model  # Return the inserted model

    def update(self, model):
        session = self.sessionmaker()
        with session as session:
            session.merge(model)
            session.commit()

    def delete(self, model_class, conditions):
        session = self.sessionmaker()
        with session as session:
            query = session.query(model_class).filter_by(**conditions)
            query.delete()
            session.commit()

    def query(self, model_class, conditions=None):
        session = self.sessionmaker()
        with session as session:
            query = session.query(model_class)
            if conditions:
                query = query.filter_by(**conditions)
            return query.all()

    def exists(self, model_class, conditions=None):
        session = self.sessionmaker()
        with session as session:
            query = session.query(model_class)
            if conditions:
                query = query.filter_by(**conditions)
            return query.limit(1).count() > 0

    def execute_raw_sql(self, sql: str):
        session = self.sessionmaker()
        with session as session:
            result = session.execute(text(sql))
            if result.returns_rows:
                return result.fetchall()
            else:
                session.commit()
                return None

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
