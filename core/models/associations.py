from sqlalchemy import Table, Column, Integer, ForeignKey, Enum as SqlEnum

from core.database.abstract_sql import Base
from core.enums.team_role import TeamRole
from core.enums.participant_document_status import ParticipantDocumentStatus

team_admin_association = Table(
    'team_admin_association',
    Base.metadata,
    Column('team_id', Integer, ForeignKey('teams.id'), primary_key=True),
    Column('admin_id', Integer, ForeignKey('users.id'), primary_key=True)
)

user_team_association = Table(
    'user_team_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('team_id', Integer, ForeignKey('teams.id'), primary_key=True),
    Column('role', SqlEnum(TeamRole), nullable=False)
)

property_owner_association = Table(
    "association",
    Base.metadata,
    Column("person_id", Integer, ForeignKey("people.id")),
    Column("property_id", Integer, ForeignKey("properties.id")),
)

user_person_association = Table(
    'user_person_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('person_id', Integer, ForeignKey('people.id'), primary_key=True)
)

user_property_association = Table(
    'user_property_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('property_id', Integer, ForeignKey('properties.id'), primary_key=True)
)

user_deal_association = Table(
    'user_transaction_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('transaction_id', Integer, ForeignKey('transactions.id'), primary_key=True)
)

property_occupant_association = Table(
    'property_occupant_association', Base.metadata,
    Column('property_id', Integer, ForeignKey('properties.id')),
    Column('person_id', Integer, ForeignKey('people.id'))
)

person_portfolio_association = Table(
    'person_portfolio_association', Base.metadata,
    Column('person_id', Integer, ForeignKey('people.id')),
    Column('property_id', Integer, ForeignKey('properties.id'))
)

document_participant_association = Table(
    'document_participant_association', Base.metadata,
    Column('document_id', Integer, ForeignKey('documents.id', ondelete="CASCADE"), primary_key=True),
    Column('participant_details_id', Integer, ForeignKey('participant_details.id', ondelete="CASCADE"), primary_key=True),
    Column('status', SqlEnum(ParticipantDocumentStatus), nullable=False, default=ParticipantDocumentStatus.PENDING)
)

file_participant_association = Table(
    'file_participant_association', Base.metadata,
    Column('file_id', Integer, ForeignKey('files.id', ondelete="CASCADE"), primary_key=True),
    Column('participant_details_id', Integer, ForeignKey('participant_details.id', ondelete="CASCADE"), primary_key=True)
)
