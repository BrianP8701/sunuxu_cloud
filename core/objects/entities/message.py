from typing import Any, Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import Database
from core.enums import MessageType
from core.models import MessageModel
from core.objects.base_entities.base_message import BaseMessage


class Message(BaseMessage):
    @classmethod
    async def query(cls, source_id: int, limit: int, offset: int) -> List["Message"]:
        """
        Queries messages based on the source ID with pagination and sorting options.

        Args:
            source_id (int): The ID of the source of the message. For developer conversations this is the user ID, for
            person conversations this is the cantor pairing of the user ID and person ID, and for team
            conversations this is the team ID.
            limit (int): The maximum number of messages to return.
            offset (int): The number of messages to skip before starting to collect the result set.

        Returns:
            List[Message]: A list of messages matching the query parameters.
        """
        db = Database()
        conditions = {"source_id": source_id}
        messages_orm = await db.query(
            MessageModel,
            conditions=conditions,
            limit=limit,
            offset=offset,
            sort_by="id",
            ascending=False,
        )
        return [cls._from_model(message) for message in messages_orm]

    @classmethod
    async def expand_thread(cls, id: int) -> List["BaseMessage"]:
        """
        Expands the email thread for a given message ID.

        Args:
            id (int): The ID of the head message.

        Returns:
            List[BaseMessage]: A list of messages in the thread, including the head message.
        """
        db = Database()
        head_message: MessageModel = await db.read(MessageModel, id)
        message_ids = head_message.thread_message_ids

        if not message_ids:
            return [cls._from_model(head_message)]

        thread: List[MessageModel] = await db.batch_read(MessageModel, message_ids)

        messages = [cls._from_model(head_message)] + [
            cls._from_model(message) for message in thread
        ]

        return messages

    @classmethod
    async def delete_by_source_id(
        cls, source_id: int, session: Optional[AsyncSession] = None
    ) -> None:
        db = Database()
        await db.delete(
            model_class=MessageModel,
            conditions={"source_id": source_id},
            session=session,
        )
