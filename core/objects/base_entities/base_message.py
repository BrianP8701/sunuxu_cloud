import uuid
from typing import Any, Dict, List, Optional, Type, TypeVar

from core.database import Database
from core.enums.message_source_type import MessageSourceType
from core.enums.message_type import MessageType
from core.models.message import MessageModel
from core.objects.base_entities.base_entity import BaseEntity

T = TypeVar("T", bound="BaseMessage")


class BaseMessage(BaseEntity):
    id: Optional[uuid.UUID] = None
    user_id: int
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
    thread_size: Optional[int] = None
    thread_message_ids: Optional[List[str]] = None

    # Call specific fields
    duration: Optional[int] = None

    orm: Optional[MessageModel]

    @classmethod
    async def create(cls: Type[T], user_id: int, data: Dict[str, Any]) -> T:
        db = Database()

        # Validate message has required fields given its type
        if data["type"] == MessageType.EMAIL:
            if (
                not data.get("from_email")
                or not data.get("recipient_email")
                or not data.get("email_subject")
            ):
                raise ValueError(
                    "from_email, recipient_email, and email_subject are required for email messages"
                )
        elif data["type"] == MessageType.SMS:
            if not data.get("from_number") or not data.get("to_number"):
                raise ValueError(
                    "from_number and to_number are required for SMS messages"
                )
        elif data["type"] == MessageType.CALL:
            if not data.get("duration"):
                raise ValueError("duration is required for call messages")
        elif data["type"] != MessageType.DEV:
            raise ValueError(f"Invalid message type: {data['type']}")

        message = MessageModel(
            type=data["type"],
            user_id=data["user_id"],
            source_id=data["source_id"],
            source_type=data["source_type"],
            content=data["content"],
            attachments=data.get("attachments"),
            from_number=data.get("from_number"),
            to_number=data.get("to_number"),
            from_email=data.get("from_email"),
            recipient_email=data.get("recipient_email"),
            cc_email=data.get("cc_email"),
            bcc_email=data.get("bcc_email"),
            email_subject=data.get("email_subject"),
            thread_size=data.get("thread_size"),
            thread_message_ids=data.get("thread_message_ids"),
            duration=data.get("duration"),
        )

        await db.create(MessageModel, message)

        return cls.from_model(message)

    @classmethod
    async def read(cls: Type[T], id: int) -> T:
        db = Database()
        message = await db.read(MessageModel, id)
        return cls.from_model(message)

    @classmethod
    async def update(cls: Type[T], id: int, updates: Dict[str, Any]) -> T:
        """
        The only allowed updates are to the thread_size and thread_message_ids columns.

        :param updates:
            A dictionary containing the message details to update:
            - 'thread_size' (Optional[int]): The size of the thread. (Optional)
            - 'thread_message_ids' (Optional[List[str]]): The ids of the messages in the thread. (Optional)
        """
        # Validate updates
        valid_updates = ["thread_size", "thread_message_ids"]
        for update in updates:
            if update not in valid_updates:
                raise ValueError(
                    f"Invalid update: {update}. Only the thread_size and thread_message_ids columns are allowed to be updated in a message"
                )

        db = Database()
        await db.update_fields(MessageModel, id, updates)
        return cls.read(id)

    @classmethod
    async def delete(cls: Type[T], id: int) -> None:
        db = Database()
        await db.delete_by_id(MessageModel, id)

    @classmethod
    def from_model(cls, message_model: MessageModel) -> T:
        return cls(
            id=message_model.id,
            source_id=message_model.source_id,
            source_type=message_model.source_type,
            type=message_model.type,
            content=message_model.content,
            attachments=message_model.attachments,
            from_number=message_model.from_number,
            to_number=message_model.to_number,
            from_email=message_model.from_email,
            recipient_email=message_model.recipient_email,
            cc_email=message_model.cc_email,
            bcc_email=message_model.bcc_email,
            email_subject=message_model.email_subject,
            thread_size=message_model.thread_size,
            thread_message_ids=message_model.thread_message_ids,
            duration=message_model.duration,
            message_model=message_model,
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
