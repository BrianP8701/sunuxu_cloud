from sqlalchemy import Column, Integer, String, DateTime, JSON, LargeBinary, Boolean, Enum as SqlEnum
from sqlalchemy.orm import relationship
from core.database.abstract_sql import Base
from sqlalchemy.sql import func
from sqlalchemy.ext.mutable import MutableList

from core.enums.mls import MLS
from core.enums.transaction_platform import TransactionPlatform

class UserDetailsOrm(Base):
    __tablename__ = "user_details"
    id = Column(Integer, primary_key=True)
    password = Column(String(255))
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20))
    first_name = Column(String(255), nullable=False)
    middle_name = Column(String(255))
    last_name = Column(String(255), nullable=False)

    redux_version = Column(Integer)
    changelog_viewed = Column(Boolean)

    messages = relationship(
        "MessageOrm", 
        backref="user", 
        order_by="MessageOrm.timestamp"
    )
    developer_conversation_viewed = Column(Boolean)

    signature = Column(LargeBinary, nullable=True)

    forwarding_number = Column(String(20))
    twilio_phone_number = Column(String(20))
    twilio_sid = Column(String(255))

    mls_username = Column(String(255))
    mls_password = Column(String(255))
    skyslope_username = Column(String(255))
    skyslope_password = Column(String(255))

    idx_website_domain = Column(String(255))
    default_mls = Column(SqlEnum(MLS))
    default_transaction_platform = Column(SqlEnum(TransactionPlatform))
    default_message_new_leads = Column(Boolean)


    shared_email = Column(String(255), nullable=True)
    google_access_token = Column(String(255), nullable=True)
    google_refresh_token = Column(String(255), nullable=True)
    google_token_expiry = Column(DateTime, nullable=True)

    instagram_access_token = Column(String(255), nullable=True)
    instagram_token_expiry = Column(DateTime, nullable=True)
    linkedin_access_token = Column(String(255), nullable=True)
    linkedin_token_expiry = Column(DateTime, nullable=True)
    facebook_access_token = Column(String(255), nullable=True)
    facebook_token_expiry = Column(DateTime, nullable=True)
    x_access_token = Column(String(255), nullable=True)
    x_token_expiry = Column(DateTime, nullable=True)


    custom_person_types = Column(MutableList.as_mutable(JSON), default=list)
    custom_property_types = Column(MutableList.as_mutable(JSON), default=list)
    custom_transaction_types = Column(MutableList.as_mutable(JSON), default=list)
    custom_transaction_statuses = Column(MutableList.as_mutable(JSON), default=list)
    custom_participant_roles = Column(MutableList.as_mutable(JSON), default=list)

    created = Column(DateTime, default=func.now())

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "phone": self.phone,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name
        }
