import uuid
from typing import Any, Dict, List, Optional

from core.database import Database
from core.enums.message_source_type import MessageSourceType
from core.enums.message_type import MessageType
from core.models.message import MessageModel
from core.objects.base_entities.base_entity import BaseEntity


class BaseMessage(BaseEntity):
    id: Optional[uuid.UUID] = None
    source_id: int  # The id of the source of the message, this can be a user id for convos with developer, person id for convos with person, team id for team conversations
    source_type: MessageSourceType

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

    orm: Optional[MessageModel]

    def insert(self) -> None:
        db = Database()

        message = MessageModel(
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
            duration=self.duration,
        )
        self.orm = db.create(message)
        self.id = self.orm.id

    @classmethod
    async def read(
        cls, source_id: int, source_type: MessageSourceType, page_size: int, offset: int
    ) -> List["BaseMessage"]:
        """
        Handles pagination.
        source_id: The id of the source of the message, this can be a user id for convos with developer, person id for convos with person, team id for team conversations
        source_type: The type of the source of the message, this can be DEV for convos with developer, PERSON for convos with person, TEAM for team conversations, CHANGELOG for changelog messages
        """
        db = Database()
        conditions = {"source_id": source_id, "source_type": source_type}
        messages_orm = await db.query(
            MessageModel,
            conditions=conditions,
            limit=page_size,
            offset=offset,
            order_by=MessageModel.id.desc(),
        )

        if not messages_orm:
            return []

        messages = [cls.from_orm(message) for message in messages_orm]

        return messages

    @classmethod
    async def get_email_thread(cls, id: int) -> List["BaseMessage"]:
        db = Database()
        head_message: MessageModel = await db.read(MessageModel, id)
        message_ids = head_message.thread_message_ids

        thread: List[MessageModel] = await db.batch_read(MessageModel, message_ids)

        messages = [cls.from_orm(head_message)] + [
            cls.from_orm(message) for message in thread
        ]

        return messages

    @classmethod
    def from_orm(cls, orm: MessageModel) -> "BaseMessage":
        return cls(
            id=orm.id,
            source_id=orm.source_id,
            source_type=orm.source_type,
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
            orm=orm,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "source_id": self.source_id,
            "source_type": self.source_type,
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
            "duration": self.duration,
        }
