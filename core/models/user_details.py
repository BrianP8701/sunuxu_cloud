from sqlmodel import Field, SQLModel, Relationship, JSON
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.sql import func
from sqlalchemy import Enum as SqlEnum

from core.enums.deal_platform import DealPlatform
from core.enums.service_connection_status import ServiceConnectionStatus

if TYPE_CHECKING:
    from core.models.message import MessageOrm

class UserDetailsOrm(SQLModel, table=True):
    __tablename__ = "user_details"
    id: Optional[int] = Field(default=None, foreign_key="users.id", primary_key=True)

    redux_version: Optional[int] = Field(default=None)
    changelog_viewed: Optional[bool] = Field(default=None)

    messages: List["MessageOrm"] = Relationship(
        sa_relationship_kwargs={"order_by": "MessageOrm.id"}
    )
    developer_conversation_viewed: Optional[bool] = Field(default=None)

    signature: Optional[bytes] = Field(default=None)

    forwarding_number: Optional[str] = Field(default=None, max_length=20)
    twilio_phone_number: Optional[str] = Field(default=None, max_length=20)
    twilio_sid: Optional[str] = Field(default=None, max_length=255)

    mls_connected: Optional[bool] = Field(default=False)
    mls_username: Optional[str] = Field(default=None, max_length=255)
    mls_password: Optional[str] = Field(default=None, max_length=255)
    
    skyslope_connection_status: ServiceConnectionStatus = Field(sa_column=SqlEnum(ServiceConnectionStatus), default=ServiceConnectionStatus.not_connected)
    skyslope_username: Optional[str] = Field(default=None, max_length=255)
    skyslope_password: Optional[str] = Field(default=None, max_length=255)

    idx_website_domain: Optional[str] = Field(default=None, max_length=255)

    mls_connection_status: ServiceConnectionStatus = Field(sa_column=SqlEnum(ServiceConnectionStatus), default=ServiceConnectionStatus.not_connected)
    mls_api_connection_status: ServiceConnectionStatus = Field(sa_column=SqlEnum(ServiceConnectionStatus), default=ServiceConnectionStatus.not_connected)

    default_mls: Optional[str] = Field(default=None, max_length=255)
    default_deal_platform: Optional[DealPlatform] = Field(sa_column=SqlEnum(DealPlatform))
    default_message_new_leads: Optional[bool] = Field(default=None)

    email_connection_status: ServiceConnectionStatus = Field(sa_column=SqlEnum(ServiceConnectionStatus), default=ServiceConnectionStatus.not_connected)
    email_template: Optional[str] = Field(default=None)
    shared_email: Optional[str] = Field(default=None, max_length=255)
    email_access_token: Optional[str] = Field(default=None, max_length=255)
    email_refresh_token: Optional[str] = Field(default=None, max_length=255)
    email_token_expiry: Optional[str] = Field(default=None)

    instagram_connection_status: ServiceConnectionStatus = Field(sa_column=SqlEnum(ServiceConnectionStatus), default=ServiceConnectionStatus.not_connected)
    instagram_access_token: Optional[str] = Field(default=None, max_length=255)
    instagram_token_expiry: Optional[str] = Field(default=None)
    
    linkedin_connection_status: ServiceConnectionStatus = Field(sa_column=SqlEnum(ServiceConnectionStatus), default=ServiceConnectionStatus.not_connected)
    linkedin_access_token: Optional[str] = Field(default=None, max_length=255)
    linkedin_token_expiry: Optional[str] = Field(default=None)
    
    facebook_connection_status: ServiceConnectionStatus = Field(sa_column=SqlEnum(ServiceConnectionStatus), default=ServiceConnectionStatus.not_connected)
    facebook_access_token: Optional[str] = Field(default=None, max_length=255)
    facebook_token_expiry: Optional[str] = Field(default=None)
    
    x_connection_status: ServiceConnectionStatus = Field(sa_column=SqlEnum(ServiceConnectionStatus), default=ServiceConnectionStatus.not_connected)
    x_access_token: Optional[str] = Field(default=None, max_length=255)
    x_token_expiry: Optional[str] = Field(default=None)

    google_business_connection_status: ServiceConnectionStatus = Field(sa_column=SqlEnum(ServiceConnectionStatus), default=ServiceConnectionStatus.not_connected)
    google_business_access_token: Optional[str] = Field(default=None, max_length=255)
    google_business_token_expiry: Optional[str] = Field(default=None)

    follow_up_boss_connection_status: ServiceConnectionStatus = Field(sa_column=SqlEnum(ServiceConnectionStatus), default=ServiceConnectionStatus.not_connected)
    follow_up_boss_access_token: Optional[str] = Field(default=None, max_length=255)
    follow_up_boss_token_expiry: Optional[str] = Field(default=None)

    brivity_connection_status: ServiceConnectionStatus = Field(sa_column=SqlEnum(ServiceConnectionStatus), default=ServiceConnectionStatus.not_connected)
    brivity_access_token: Optional[str] = Field(default=None, max_length=255)
    brivity_token_expiry: Optional[str] = Field(default=None)

    kvcore_connection_status: ServiceConnectionStatus = Field(sa_column=SqlEnum(ServiceConnectionStatus), default=ServiceConnectionStatus.not_connected)
    kvcore_access_token: Optional[str] = Field(default=None, max_length=255)
    kvcore_token_expiry: Optional[str] = Field(default=None)

    custom_person_types: List[str] = Field(sa_type=JSON, default=[])
    custom_property_types: List[str] = Field(sa_type=JSON, default=[])
    custom_transaction_types: List[str] = Field(sa_type=JSON, default=[])
    custom_transaction_statuses: List[str] = Field(sa_type=JSON, default=[])
    custom_participant_roles: List[str] = Field(sa_type=JSON, default=[])
    tags: List[str] = Field(sa_type=JSON, default=[])

    created: Optional[str] = Field(default=func.now())
