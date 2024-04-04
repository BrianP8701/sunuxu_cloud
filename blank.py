from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from typing import Optional
from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SQLEnum
from pydantic import BaseModel, ConfigDict

# Create the connection string
connection_string = 'mssql+pyodbc://brianp8701:Bp.8701ebkebk@sunuxu.database.windows.net/test_sql?driver=ODBC+Driver+18+for+SQL+Server'

# Create the SQLAlchemy engine
engine = create_engine(connection_string)

# Create a base class for declarative models
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
    phone = Column(Integer)
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    user_type = Column(SQLEnum(UserTypeEnum))
    
# Create the table in the database
Base.metadata.create_all(engine)

print("Table created successfully.")
