from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SqlEnum
from core.database.abstract_sql import Base
from sqlalchemy.sql import func
from sqlalchemy import JSON


from core.enums.message_type import MessageType

class MessageOrm(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)

    type = Column(SqlEnum(MessageType), nullable=False)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=func.now())

    email_subject = Column(String)
    attachments = Column(JSON) # List of URLs
