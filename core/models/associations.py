from sqlmodel import SQLModel, Field
from typing import Optional
from core.enums.team_role import TeamRole
from core.enums.participant_document_status import ParticipantDocumentStatus

class TeamAdminAssociation(SQLModel, table=True):
    team_id: Optional[int] = Field(default=None, foreign_key="teams.id", primary_key=True)
    admin_id: Optional[int] = Field(default=None, foreign_key="users.id", primary_key=True)

class UserTeamAssociation(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", primary_key=True)
    team_id: Optional[int] = Field(default=None, foreign_key="teams.id", primary_key=True)
    role: TeamRole = Field(nullable=False)

class PropertyOwnerAssociation(SQLModel, table=True):
    person_id: Optional[int] = Field(default=None, foreign_key="people.id")
    property_id: Optional[int] = Field(default=None, foreign_key="properties.id")

class UserPersonAssociation(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", primary_key=True)
    person_id: Optional[int] = Field(default=None, foreign_key="people.id", primary_key=True)

class UserPropertyAssociation(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", primary_key=True)
    property_id: Optional[int] = Field(default=None, foreign_key="properties.id", primary_key=True)

class UserDealAssociation(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", primary_key=True)
    transaction_id: Optional[int] = Field(default=None, foreign_key="transactions.id", primary_key=True)

class PropertyOccupantAssociation(SQLModel, table=True):
    property_id: Optional[int] = Field(default=None, foreign_key="properties.id")
    person_id: Optional[int] = Field(default=None, foreign_key="people.id")

class PersonPortfolioAssociation(SQLModel, table=True):
    person_id: Optional[int] = Field(default=None, foreign_key="people.id")
    property_id: Optional[int] = Field(default=None, foreign_key="properties.id")

class DocumentParticipantAssociation(SQLModel, table=True):
    document_id: Optional[int] = Field(default=None, foreign_key="documents.id", primary_key=True, sa_column_kwargs={"ondelete": "CASCADE"})
    participant_details_id: Optional[int] = Field(default=None, foreign_key="participant_details.id", primary_key=True, sa_column_kwargs={"ondelete": "CASCADE"})
    status: ParticipantDocumentStatus = Field(default=ParticipantDocumentStatus.PENDING, nullable=False)

class FileParticipantAssociation(SQLModel, table=True):
    file_id: Optional[int] = Field(default=None, foreign_key="files.id", primary_key=True, sa_column_kwargs={"ondelete": "CASCADE"})
    participant_details_id: Optional[int] = Field(default=None, foreign_key="participant_details.id", primary_key=True, sa_column_kwargs={"ondelete": "CASCADE"})
