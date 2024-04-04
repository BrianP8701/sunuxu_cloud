from typing import Optional
from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SQLEnum
from pydantic import BaseModel, ConfigDict

from sunuxu.database.abstract import Base

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

class User(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: int
    username: str
    password: str
    email: str
    phone: str
    first_name: str
    middle_name: Optional[str]
    last_name: str
    user_type: UserTypeEnum
