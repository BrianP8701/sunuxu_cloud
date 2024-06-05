from typing import Optional

from sqlmodel import Field, SQLModel


class UserRowModel(SQLModel, table=True):
    __tablename__ = "user_rows"
    id: Optional[int] = Field(default=None, primary_key=True)

    avatar: Optional[str] = Field(default=None, max_length=255)  # Url to image
    email: str = Field(max_length=255, unique=True, index=True, nullable=False)
    phone: Optional[str] = Field(default=None, max_length=20)
    first_name: str = Field(max_length=255, nullable=False)
    middle_name: Optional[str] = Field(default=None, max_length=255)
    last_name: str = Field(max_length=255, nullable=False)
