import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from sunuxu.database.abstract import AbstractSQLDatabase, Base

class AzureSQLDatabase(AbstractSQLDatabase):
    _instance = None

    def __init__(self):
        db_url = os.getenv('DB_URL')
        print(f"Connecting to database: {db_url}")
        self.connection_string = db_url  
        self.engine = create_engine(db_url)
        Base.metadata.bind = self.engine  # Bind the metadata to the engine
        Base.metadata.reflect(self.engine)  # Reflect the existing tables
        self.Session = sessionmaker(bind=self.engine)

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AzureSQLDatabase, cls).__new__(cls)
        return cls._instance

    @classmethod
    def reset_instance(cls):
        if cls._instance:
            cls._instance.Session().close()
            cls._instance.engine.dispose()
            cls._instance = None

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def insert(self, model):
        with self.Session() as session:
            session.add(model)
            session.commit()
            session.refresh(model)  # Refresh the model to update the id attribute
            return model  # Return the inserted model

    def update(self, model):
        with self.Session() as session:
            session.merge(model)
            session.commit()

    def delete(self, model):
        with self.Session() as session:
            session.delete(model)
            session.commit()

    def delete_by_id(self, id, model_class):
        with self.Session() as session:
            # Directly delete the object by primary key without loading it
            session.query(model_class).filter(model_class.id == id).delete()
            session.commit()

    def query(self, model_class, conditions=None):
        with self.Session() as session:
            query = session.query(model_class)
            if conditions:
                query = query.filter_by(**conditions)
            return query.all()

    def execute_raw_sql(self, sql):
        with self.Session() as session:
            result = session.execute(text(sql))
            if result.returns_rows:
                return result.fetchall()
            else:
                session.commit()
                return None

    def perform_transaction(self, operations):
        session = self.Session()
        try:
            operations(session)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def clear_database(self, safety):
        """
        Clear all data in the database. This operation is irreversible.
        
        Set the safety parameter to "I understand this will delete all data" to confirm the operation.
        """
        if safety != "I understand this will delete all data":
            raise ValueError("Safety string does not match. Set the safety parameter to 'I understand this will delete all data' to confirm the operation.")
        else:
            with self.Session() as session:
                meta = Base.metadata
                for table in reversed(meta.sorted_tables):
                    print(f"Clearing table: {table}")
                    session.execute(table.delete())
                session.commit()
            print("Database cleared successfully")
