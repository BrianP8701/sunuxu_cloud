from sqlalchemy import Table, Column, Integer, ForeignKey
from core.database.abstract_sql import Base

property_owner_association_table = Table(
    "association",
    Base.metadata,
    Column("person_id", Integer, ForeignKey("people.id")),
    Column("property_id", Integer, ForeignKey("properties.id")),
)
