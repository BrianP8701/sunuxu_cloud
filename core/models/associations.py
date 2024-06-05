from typing import TYPE_CHECKING, Optional

from sqlalchemy import Enum as SqlEnum
from sqlmodel import Field, Relationship, SQLModel

from core.enums.participant_document_status import ParticipantDocumentStatus
from core.enums.participant_role import ParticipantRole
from core.enums.team_role import TeamRole

if TYPE_CHECKING:
    from core.models.entities.person import PersonModel


# User-Entity associations
class UserTeamAssociation(SQLModel, table=True):
    __tablename__ = "user_team_association"
    user_id: Optional[int] = Field(
        default=None, foreign_key="users.id", primary_key=True
    )
    team_id: Optional[int] = Field(
        default=None, foreign_key="teams.id", primary_key=True
    )
    role: TeamRole = Field(sa_column=SqlEnum(TeamRole, nullable=False))


class UserPersonAssociation(SQLModel, table=True):
    __tablename__ = "user_person_association"
    user_id: Optional[int] = Field(
        default=None, foreign_key="users.id", primary_key=True
    )
    person_id: Optional[int] = Field(
        default=None, foreign_key="people.id", primary_key=True
    )


class UserPropertyAssociation(SQLModel, table=True):
    __tablename__ = "user_property_association"
    user_id: Optional[int] = Field(
        default=None, foreign_key="users.id", primary_key=True
    )
    property_id: Optional[int] = Field(
        default=None, foreign_key="properties.id", primary_key=True
    )


class UserDealAssociation(SQLModel, table=True):
    __tablename__ = "user_deal_association"
    user_id: Optional[int] = Field(
        default=None, foreign_key="users.id", primary_key=True
    )
    deal_id: Optional[int] = Field(
        default=None, foreign_key="deals.id", primary_key=True
    )


# Entity-Entity associations
class PropertyOccupantAssociation(SQLModel, table=True):
    __tablename__ = "property_occupant_association"
    property_id: Optional[int] = Field(
        default=None, foreign_key="properties.id", primary_key=True
    )
    person_id: Optional[int] = Field(
        default=None, foreign_key="people.id", primary_key=True
    )


class PropertyOwnerAssociation(SQLModel, table=True):
    __tablename__ = "property_owner_association"
    property_id: Optional[int] = Field(
        default=None, foreign_key="properties.id", primary_key=True
    )
    person_id: Optional[int] = Field(
        default=None, foreign_key="people.id", primary_key=True
    )


class DocumentPersonAssociation(SQLModel, table=True):
    __tablename__ = "document_person_association"
    document_id: Optional[int] = Field(
        default=None, foreign_key="deal_documents.id", primary_key=True
    )
    person_id: Optional[int] = Field(
        default=None, foreign_key="people.id", primary_key=True
    )
    status: ParticipantDocumentStatus = Field(
        sa_column=SqlEnum(ParticipantDocumentStatus, nullable=False),
        default=ParticipantDocumentStatus.PENDING,
    )


class DealParticipantAssociation(SQLModel, table=True):
    __tablename__ = "deal_person_association"
    deal_id: Optional[int] = Field(
        default=None, foreign_key="deals.id", primary_key=True
    )
    person_id: Optional[int] = Field(
        default=None, foreign_key="people.id", primary_key=True
    )
    role: ParticipantRole = Field(sa_column=SqlEnum(ParticipantRole, nullable=False))


class DealDocumentAssociation(SQLModel, table=True):
    __tablename__ = "deal_document_association"
    deal_id: Optional[int] = Field(
        default=None, foreign_key="deals.id", primary_key=True
    )
    document_id: Optional[int] = Field(
        default=None, foreign_key="deal_documents.id", primary_key=True
    )
