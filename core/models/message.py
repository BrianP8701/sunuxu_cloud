import uuid
from sqlmodel import Field, SQLModel, JSON
from typing import List, Optional
from sqlalchemy import Column, Enum as SqlEnum

from core.enums.message_type import MessageType
from core.enums.message_source_type import MessageSourceType

class MessageOrm(SQLModel, table=True):
    __tablename__ = "messages"
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid1, primary_key=True) # Time UUID

    source_id: int = Field(index=True, nullable=False) # The id of the source of the message, this can be a user id for convos with developer, person id for convos with person, team id for team conversations
    source_type: MessageSourceType = Field(sa_column=SqlEnum(MessageSourceType), index=True, nullable=False)

    type: MessageType
    content: str
    attachments: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))

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
    thread_message_ids: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))

    # Call specific fields
    duration: Optional[int] = Field(default=None)
