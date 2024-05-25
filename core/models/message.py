from sqlmodel import Field, SQLModel, JSON
from typing import List, Optional
from datetime import datetime
from core.enums.message_type import MessageType

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: MessageType
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    attachments: Optional[List[str]] = Field(default=None, sa_column_kwargs={"type_": JSON})

    # Text specific fields
    from_number: Optional[str] = Field(default=None)
    to_number: Optional[str] = Field(default=None)

    # Email specific fields
    from_email: Optional[str] = Field(default=None)
    recipient_email: Optional[str] = Field(default=None)
    cc_email: Optional[str] = Field(default=None)
    bcc_email: Optional[str] = Field(default=None)
    email_subject: Optional[str] = Field(default=None)

    # Email thread fields
    thread_size: int = Field(default=1)
    thread_message_ids: Optional[List[int]] = Field(default=None, sa_column_kwargs={"type_": JSON})

    # Call specific fields
    duration: Optional[int] = Field(default=None)
