from sqlmodel import SQLModel, Field
from typing import Optional
from sqlalchemy import Enum as SqlEnum

from core.enums.team_role import TeamRole
from core.enums.participant_document_status import ParticipantDocumentStatus
from core.enums.participant_role import ParticipantRole

class UserTeamAssociation(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="user_details.id", primary_key=True)
    team_id: Optional[int] = Field(default=None, foreign_key="team_details.id", primary_key=True)
    role: TeamRole = Field(sa_column=SqlEnum(TeamRole, nullable=False))

class UserPersonAssociation(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="user_details.id", primary_key=True)
    person_id: Optional[int] = Field(default=None, foreign_key="person_details.id", primary_key=True)

class UserPropertyAssociation(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="user_details.id", primary_key=True)
    property_id: Optional[int] = Field(default=None, foreign_key="property_details.id", primary_key=True)

class UserDealAssociation(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="user_details.id", primary_key=True)
    deal_id: Optional[int] = Field(default=None, foreign_key="deal_details.id", primary_key=True)

class PropertyOccupantAssociation(SQLModel, table=True):
    property_id: Optional[int] = Field(default=None, foreign_key="properties.id", primary_key=True)
    person_id: Optional[int] = Field(default=None, foreign_key="people.id", primary_key=True)

class PropertyOwnerAssociation(SQLModel, table=True):
    property_id: Optional[int] = Field(default=None, foreign_key="properties.id", primary_key=True)
    person_id: Optional[int] = Field(default=None, foreign_key="people.id", primary_key=True)

class PersonPortfolioAssociation(SQLModel, table=True):
    person_id: Optional[int] = Field(default=None, foreign_key="person_details.id", primary_key=True)
    property_id: Optional[int] = Field(default=None, foreign_key="properties.id", primary_key=True)

class DocumentPersonAssociation(SQLModel, table=True):
    document_id: Optional[int] = Field(default=None, foreign_key="deal_documents.id", primary_key=True)
    person_id: Optional[int] = Field(default=None, foreign_key="people.id", primary_key=True)
    status: ParticipantDocumentStatus = Field(sa_column=SqlEnum(ParticipantDocumentStatus, nullable=False), default=ParticipantDocumentStatus.PENDING)

class DealDetailsPersonAssociation(SQLModel, table=True):
    __tablename__ = "deal_details_person_association"
    deal_details_id: Optional[int] = Field(default=None, foreign_key="deal_details.id", primary_key=True)
    person_id: Optional[int] = Field(default=None, foreign_key="people.id", primary_key=True)
    role: ParticipantRole = Field(sa_column=SqlEnum(ParticipantRole, nullable=False))

class PersonDealAssociation(SQLModel, table=True):
    person_details_id: Optional[int] = Field(default=None, foreign_key="person_details.id", primary_key=True)
    deal_id: Optional[int] = Field(default=None, foreign_key="deals.id", primary_key=True)
