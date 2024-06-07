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
        sa_column=Column(Integer, ForeignKey("user_rows.id"), primary_key=True)
    )
    password: Optional[str] = Field(default=None, max_length=255)

    people: List["PersonModel"] = Relationship(
        back_populates="users", link_model=UserPersonAssociation, sa_relationship_kwargs={"cascade": "all"}
    )
    properties: List["PropertyModel"] = Relationship(
        back_populates="users", link_model=UserPropertyAssociation, sa_relationship_kwargs={"cascade": "all"}
    )
    deals: List["DealModel"] = Relationship(
        back_populates="users", link_model=UserDealAssociation, sa_relationship_kwargs={"cascade": "all"}
    )
    teams: List["TeamModel"] = Relationship(
        back_populates="users", link_model=UserTeamAssociation, sa_relationship_kwargs={"cascade": "all"}
    )

    row: "UserRowModel" = Relationship(
        sa_relationship_kwargs={
            "uselist": False,
            "single_parent": True,
            "cascade": "all, delete-orphan",
            "back_populates": None
        }
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

    skyslope_connection_status: ServiceConnectionStatus = Field(
        sa_column=SqlEnum(ServiceConnectionStatus),
        default=ServiceConnectionStatus.not_connected,
    )
    skyslope_username: Optional[str] = Field(default=None, max_length=255)
    skyslope_password: Optional[str] = Field(default=None, max_length=255)

    idx_website_domain: Optional[str] = Field(default=None, max_length=255)

    mls_connection_status: ServiceConnectionStatus = Field(
        sa_column=SqlEnum(ServiceConnectionStatus),
        default=ServiceConnectionStatus.not_connected,
    )
    mls_api_connection_status: ServiceConnectionStatus = Field(
        sa_column=SqlEnum(ServiceConnectionStatus),
        default=ServiceConnectionStatus.not_connected,
    )

    default_mls: Optional[str] = Field(default=None, max_length=255)
    default_deal_platform: Optional[DealPlatform] = Field(
        sa_column=SqlEnum(DealPlatform)
    )

    email_connection_status: ServiceConnectionStatus = Field(
        sa_column=SqlEnum(ServiceConnectionStatus),
        default=ServiceConnectionStatus.not_connected,
    )
    email_template: Optional[str] = Field(default=None)
    shared_email: Optional[str] = Field(default=None, max_length=255)
    email_access_token: Optional[str] = Field(default=None, max_length=255)
    email_refresh_token: Optional[str] = Field(default=None, max_length=255)
    email_token_expiry: Optional[str] = Field(default=None)

    instagram_connection_status: ServiceConnectionStatus = Field(
        sa_column=SqlEnum(ServiceConnectionStatus),
        default=ServiceConnectionStatus.not_connected,
    )
    instagram_access_token: Optional[str] = Field(default=None, max_length=255)
    instagram_token_expiry: Optional[str] = Field(default=None)

    linkedin_connection_status: ServiceConnectionStatus = Field(
        sa_column=SqlEnum(ServiceConnectionStatus),
        default=ServiceConnectionStatus.not_connected,
    )
    linkedin_access_token: Optional[str] = Field(default=None, max_length=255)
    linkedin_token_expiry: Optional[str] = Field(default=None)

    facebook_connection_status: ServiceConnectionStatus = Field(
        sa_column=SqlEnum(ServiceConnectionStatus),
        default=ServiceConnectionStatus.not_connected,
    )
    facebook_access_token: Optional[str] = Field(default=None, max_length=255)
    facebook_token_expiry: Optional[str] = Field(default=None)

    x_connection_status: ServiceConnectionStatus = Field(
        sa_column=SqlEnum(ServiceConnectionStatus),
        default=ServiceConnectionStatus.not_connected,
    )
    x_access_token: Optional[str] = Field(default=None, max_length=255)
    x_token_expiry: Optional[str] = Field(default=None)

    google_business_connection_status: ServiceConnectionStatus = Field(
        sa_column=SqlEnum(ServiceConnectionStatus),
        default=ServiceConnectionStatus.not_connected,
    )
    google_business_access_token: Optional[str] = Field(default=None, max_length=255)
    google_business_token_expiry: Optional[str] = Field(default=None)

    follow_up_boss_connection_status: ServiceConnectionStatus = Field(
        sa_column=SqlEnum(ServiceConnectionStatus),
        default=ServiceConnectionStatus.not_connected,
    )
    follow_up_boss_access_token: Optional[str] = Field(default=None, max_length=255)
    follow_up_boss_token_expiry: Optional[str] = Field(default=None)

    brivity_connection_status: ServiceConnectionStatus = Field(
        sa_column=SqlEnum(ServiceConnectionStatus),
        default=ServiceConnectionStatus.not_connected,
    )
    brivity_access_token: Optional[str] = Field(default=None, max_length=255)
    brivity_token_expiry: Optional[str] = Field(default=None)

    kvcore_connection_status: ServiceConnectionStatus = Field(
        sa_column=SqlEnum(ServiceConnectionStatus),
        default=ServiceConnectionStatus.not_connected,
    )
    kvcore_access_token: Optional[str] = Field(default=None, max_length=255)
    kvcore_token_expiry: Optional[str] = Field(default=None)
