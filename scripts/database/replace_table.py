from enum import Enum
import os

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Enum as SQLEnum

from core.models.user import UserOrm

# Assuming you have the necessary imports and configurations for your ORM models
def delete_table(engine, table_name):
    meta = MetaData()
    meta.reflect(bind=engine)
    table = meta.tables.get(table_name)
    if table is not None:
        table.drop(bind=engine)
        print(f"Table '{table_name}' deleted successfully.")
    else:
        print(f"Table '{table_name}' does not exist.")

def create_table(engine, model_class):
    model_class.__table__.create(bind=engine)
    print(f"Table '{model_class.__tablename__}' created successfully.")

# Example usage
if __name__ == "__main__":
    # Create the database engine
    print(os.getenv('AZURE_SQL_URL'))
    engine = create_engine(os.getenv('AZURE_SQL_URL'))

    # Delete the 'users' table
    delete_table(engine, "users")

    # Create the 'users' table using the UserOrm model
    Base = declarative_base()

    create_table(engine, UserOrm)
