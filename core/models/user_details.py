from sqlmodel import Field, SQLModel, Relationship, JSON
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.sql import func
from sqlalchemy import Enum as SqlEnum

from core.enums.mls import MLS
from core.enums.transaction_platform import TransactionPlatform

if TYPE_CHECKING:
    from core.models.message import Message

class UserDetails(SQLModel, table=True):
    __tablename__ = "user_details"
    id: Optional[int] = Field(default=None, primary_key=True)
    password: Optional[str] = Field(default=None, max_length=255)
    email: str = Field(max_length=255, unique=True, index=True, nullable=False)
    phone: Optional[str] = Field(default=None, max_length=20)
    first_name: str = Field(max_length=255, nullable=False)
    middle_name: Optional[str] = Field(default=None, max_length=255)
    last_name: str = Field(max_length=255, nullable=False)

    redux_version: Optional[int] = Field(default=None)
    changelog_viewed: Optional[bool] = Field(default=None)

    messages: List["Message"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"order_by": "MessageOrm.timestamp"}
    )
    developer_conversation_viewed: Optional[bool] = Field(default=None)

    signature: Optional[bytes] = Field(default=None)

    forwarding_number: Optional[str] = Field(default=None, max_length=20)
    twilio_phone_number: Optional[str] = Field(default=None, max_length=20)
    twilio_sid: Optional[str] = Field(default=None, max_length=255)

    mls_username: Optional[str] = Field(default=None, max_length=255)
    mls_password: Optional[str] = Field(default=None, max_length=255)
    skyslope_username: Optional[str] = Field(default=None, max_length=255)
    skyslope_password: Optional[str] = Field(default=None, max_length=255)

    idx_website_domain: Optional[str] = Field(default=None, max_length=255)
    default_mls: Optional[MLS] = Field(sa_column=SqlEnum(MLS))
    default_transaction_platform: Optional[TransactionPlatform] = Field(sa_column=SqlEnum(TransactionPlatform))
    default_message_new_leads: Optional[bool] = Field(default=None)

    shared_email: Optional[str] = Field(default=None, max_length=255)
    google_access_token: Optional[str] = Field(default=None, max_length=255)
    google_refresh_token: Optional[str] = Field(default=None, max_length=255)
    google_token_expiry: Optional[str] = Field(default=None)

    instagram_access_token: Optional[str] = Field(default=None, max_length=255)
    instagram_token_expiry: Optional[str] = Field(default=None)
    linkedin_access_token: Optional[str] = Field(default=None, max_length=255)
    linkedin_token_expiry: Optional[str] = Field(default=None)
    facebook_access_token: Optional[str] = Field(default=None, max_length=255)
    facebook_token_expiry: Optional[str] = Field(default=None)
    x_access_token: Optional[str] = Field(default=None, max_length=255)
    x_token_expiry: Optional[str] = Field(default=None)

    custom_person_types: List[str] = Field(default_factory=list, sa_column=MutableList.as_mutable(JSON))
    custom_property_types: List[str] = Field(default_factory=list, sa_column=MutableList.as_mutable(JSON))
    custom_transaction_types: List[str] = Field(default_factory=list, sa_column=MutableList.as_mutable(JSON))
    custom_transaction_statuses: List[str] = Field(default_factory=list, sa_column=MutableList.as_mutable(JSON))
    custom_participant_roles: List[str] = Field(default_factory=list, sa_column=MutableList.as_mutable(JSON))

    created: Optional[str] = Field(default=func.now())

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "phone": self.phone,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name
        }
