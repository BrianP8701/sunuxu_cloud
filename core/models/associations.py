from sqlalchemy import Table, Column, Integer, ForeignKey, String, Enum as SqlEnum

from core.database.abstract_sql import Base
from core.enums.team_role import TeamRole


user_team_association = Table(
    'user_team_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('team_id', Integer, ForeignKey('teams.id'), primary_key=True),
    Column('role', SqlEnum(TeamRole), nullable=False)
)

property_owner_association_table = Table(
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

property_occupant_association_table = Table(
    'property_occupant_association', Base.metadata,
    Column('property_id', Integer, ForeignKey('properties.id')),
    Column('person_id', Integer, ForeignKey('people.id'))
)

person_portfolio_association_table = Table(
    'person_portfolio_association', Base.metadata,
    Column('person_id', Integer, ForeignKey('people.id')),
    Column('property_id', Integer, ForeignKey('properties.id'))
)