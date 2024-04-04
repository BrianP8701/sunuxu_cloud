from enum import Enum
import os

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Enum as SQLEnum

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
    print(os.getenv('DB_URL'))
    engine = create_engine(os.getenv('DB_URL'))

    # Delete the 'users' table
    delete_table(engine, "users")

    # Create the 'users' table using the UserOrm model
    Base = declarative_base()

    class UserTypeEnum(Enum):
        ADMIN = "admin"
        AGENT = "agent"
        PERSON = "person"

    class UserOrm(Base):
        __tablename__ = "users"
        id = Column(Integer, primary_key=True)
        username = Column(String)
        password = Column(String)
        email = Column(String)
        phone = Column(String(20))
        first_name = Column(String)
        middle_name = Column(String)
        last_name = Column(String)
        user_type = Column(SQLEnum(UserTypeEnum))

    create_table(engine, UserOrm)