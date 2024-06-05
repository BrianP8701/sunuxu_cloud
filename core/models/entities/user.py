from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Column
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.sql import func
from sqlmodel import Field, Relationship, SQLModel

from core.enums.deal_platform import DealPlatform
from core.enums.service_connection_status import ServiceConnectionStatus
from core.models.associations import (UserDealAssociation,
                                      UserPersonAssociation,
                                      UserPropertyAssociation,
                                      UserTeamAssociation)

if TYPE_CHECKING:
    from core.models.entities.deal import DealModel
    from core.models.entities.person import PersonModel
    from core.models.entities.property import PropertyModel
    from core.models.entities.team import TeamModel
    from core.models.rows.user import UserRowModel


class UserModel(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, ForeignKey("users.id"), primary_key=True),
    )
    password: Optional[str] = Field(default=None, max_length=255)

    people: List["PersonModel"] = Relationship(
        back_populates="users", link_model=UserPersonAssociation
    )
    properties: List["PropertyModel"] = Relationship(
        back_populates="users", link_model=UserPropertyAssociation
    )
    deals: List["DealModel"] = Relationship(
        back_populates="users", link_model=UserDealAssociation
    )
    teams: List["TeamModel"] = Relationship(
        back_populates="users", link_model=UserTeamAssociation
    )

    row: "UserRowModel" = Relationship(
        sa_relationship_kwargs={"uselist": False, "cascade": "all, delete-orphan"}
    )

    redux_version: Optional[int] = Field(default=None)
    changelog_viewed: Optional[bool] = Field(default=None)
    developer_conversation_viewed: Optional[bool] = Field(default=None)

    created: Optional[str] = Field(default=func.now())

    signature: Optional[bytes] = Field(default=None)

    forwarding_number: Optional[str] = Field(default=None, max_length=20)
    twilio_phone_number: Optional[str] = Field(default=None, max_length=20)
    twilio_sid: Optional[str] = Field(default=None, max_length=255)

    mls_connected: Optional[bool] = Field(default=False)
    mls_username: Optional[str] = Field(default=None, max_length=255)
    mls_password: Optional[str] = Field(default=None, max_length=255)

    skyslope_connection_status: Optional[ServiceConnectionStatus] = Field(
        sa_column=SqlEnum(ServiceConnectionStatus),
        default=ServiceConnectionStatus.NOT_CONNECTED,
    )
    skyslope_username: Optional[str] = Field(default=None, max_length=255)
    skyslope_password: Optional[str] = Field(default=None, max_length=255)

    idx_website_domain: Optional[str] = Field(default=None, max_length=255)

    mls_connection_status: Optional[ServiceConnectionStatus] = Field(
        sa_column=SqlEnum(ServiceConnectionStatus),
        default=ServiceConnectionStatus.NOT_CONNECTED,
    )
    mls_api_connection_status: Optional[ServiceConnectionStatus] = Field(
        sa_column=SqlEnum(ServiceConnectionStatus),
        default=ServiceConnectionStatus.NOT_CONNECTED,
    )

    default_mls: Optional[str] = Field(default=None, max_length=255)
    default_deal_platform: Optional[DealPlatform] = Field(
        sa_column=SqlEnum(DealPlatform)
    )

    email_connection_status: Optional[ServiceConnectionStatus] = Field(
        sa_column=SqlEnum(ServiceConnectionStatus),
        default=ServiceConnectionStatus.NOT_CONNECTED,
    )
    email_template: Optional[str] = Field(default=None)
    shared_email: Optional[str] = Field(default=None, max_length=255)
    email_access_token: Optional[str] = Field(default=None, max_length=255)
    email_refresh_token: Optional[str] = Field(default=None, max_length=255)
    email_token_expiry: Optional[str] = Field(default=None)

    instagram_connection_status: Optional[ServiceConnectionStatus] = Field(
        sa_column=SqlEnum(ServiceConnectionStatus),
        default=ServiceConnectionStatus.NOT_CONNECTED,
    )
    instagram_access_token: Optional[str] = Field(default=None, max_length=255)
    instagram_token_expiry: Optional[str] = Field(default=None)

    linkedin_connection_status: Optional[ServiceConnectionStatus] = Field(
        sa_column=SqlEnum(ServiceConnectionStatus),
        default=ServiceConnectionStatus.NOT_CONNECTED,
    )
    linkedin_access_token: Optional[str] = Field(default=None, max_length=255)
    linkedin_token_expiry: Optional[str] = Field(default=None)

    facebook_connection_status: Optional[ServiceConnectionStatus] = Field(
        sa_column=SqlEnum(ServiceConnectionStatus),
        default=ServiceConnectionStatus.NOT_CONNECTED,
    )
    facebook_access_token: Optional[str] = Field(default=None, max_length=255)
    facebook_token_expiry: Optional[str] = Field(default=None)

    x_connection_status: Optional[ServiceConnectionStatus] = Field(
        sa_column=SqlEnum(ServiceConnectionStatus),
        default=ServiceConnectionStatus.NOT_CONNECTED,
    )
    x_access_token: Optional[str] = Field(default=None, max_length=255)
    x_token_expiry: Optional[str] = Field(default=None)

    google_business_connection_status: Optional[ServiceConnectionStatus] = Field(
        sa_column=SqlEnum(ServiceConnectionStatus),
        default=ServiceConnectionStatus.NOT_CONNECTED,
    )
    google_business_access_token: Optional[str] = Field(default=None, max_length=255)
    google_business_token_expiry: Optional[str] = Field(default=None)

    follow_up_boss_connection_status: Optional[ServiceConnectionStatus] = Field(
        sa_column=SqlEnum(ServiceConnectionStatus),
        default=ServiceConnectionStatus.NOT_CONNECTED,
    )
    follow_up_boss_access_token: Optional[str] = Field(default=None, max_length=255)
    follow_up_boss_token_expiry: Optional[str] = Field(default=None)

    brivity_connection_status: Optional[ServiceConnectionStatus] = Field(
        sa_column=SqlEnum(ServiceConnectionStatus),
        default=ServiceConnectionStatus.NOT_CONNECTED,
    )
    brivity_access_token: Optional[str] = Field(default=None, max_length=255)
    brivity_token_expiry: Optional[str] = Field(default=None)

    kvcore_connection_status: Optional[ServiceConnectionStatus] = Field(
        sa_column=SqlEnum(ServiceConnectionStatus),
        default=ServiceConnectionStatus.NOT_CONNECTED,
    )
    kvcore_access_token: Optional[str] = Field(default=None, max_length=255)
    kvcore_token_expiry: Optional[str] = Field(default=None)
