from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid

from core.enums.message_type import MessageType
from core.models.message import MessageOrm
from core.database import Database

class Message(BaseModel):
    id: Optional[uuid.UUID] = None
    relationship_id: Optional[int] = None # This can be a user id for convos with developer, person id for convos with person, team id for team conversations

    type: MessageType
    content: str
    attachments: Optional[List[str]] = None

    # Text specific fields
    from_number: Optional[str] = None
    to_number: Optional[str] = None

    # Email specific fields
    from_email: Optional[str] = None
    recipient_email: Optional[str] = None
    cc_email: Optional[str] = None
    bcc_email: Optional[str] = None
    email_subject: Optional[str] = None

    # Email thread fields
    thread_size: int = 1
    thread_message_ids: Optional[List[str]] = None

    # Call specific fields
    duration: Optional[int] = None

    orm: Optional[MessageOrm]

    def insert(self) -> None:
        db = Database()
        
        message = MessageOrm(
            type=self.type,
            relationship_id=self.relationship_id,
            content=self.content,
            attachments=self.attachments,
            from_number=self.from_number,
            to_number=self.to_number,
            from_email=self.from_email,
            recipient_email=self.recipient_email,
            cc_email=self.cc_email,
            bcc_email=self.bcc_email,
            email_subject=self.email_subject,
            thread_size=self.thread_size,
            thread_message_ids=self.thread_message_ids,
            duration=self.duration
        )
        self.orm = db.insert(message)
        self.id = self.orm.id

    @classmethod
    async def get(cls, relationship_id: int, page_size: int, offset: int) -> List['Message']:
        db = Database()
        conditions = {"relationship_id": relationship_id}
        messages_orm = await db.query(MessageOrm, conditions=conditions, limit=page_size, offset=offset, order_by=MessageOrm.id.desc())

        if not messages_orm:
            return []

        messages = [
            cls.from_orm(message) for message in messages_orm
        ]

        return messages

    @classmethod
    async def get_email_thread(cls, id: int) -> List['Message']:
        db = Database()
        head_message: MessageOrm = await db.get(MessageOrm, id)
        message_ids = head_message.thread_message_ids
        
        thread: List[MessageOrm] = await db.batch_get(MessageOrm, message_ids)

        messages = [
            cls.from_orm(head_message)
        ] + [
            cls.from_orm(message) for message in thread
        ]

        return messages

    @classmethod
    def from_orm(cls, orm: MessageOrm) -> 'Message':
        return cls(
            id=orm.id,
            relationship_id=orm.relationship_id,
            type=orm.type,
            content=orm.content,
            attachments=orm.attachments,
            from_number=orm.from_number,
            to_number=orm.to_number,
            from_email=orm.from_email,
            recipient_email=orm.recipient_email,
            cc_email=orm.cc_email,
            bcc_email=orm.bcc_email,
            email_subject=orm.email_subject,
            thread_size=orm.thread_size,
            thread_message_ids=orm.thread_message_ids,
            duration=orm.duration,
            orm=orm
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "relationship_id": self.relationship_id,
            "type": self.type,
            "content": self.content,
            "attachments": self.attachments,
            "from_number": self.from_number,
            "to_number": self.to_number,
            "from_email": self.from_email,
            "recipient_email": self.recipient_email,
            "cc_email": self.cc_email,
            "bcc_email": self.bcc_email,
            "email_subject": self.email_subject,
            "thread_size": self.thread_size,
            "thread_message_ids": self.thread_message_ids,
            "duration": self.duration
        }
