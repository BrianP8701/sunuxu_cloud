from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Column, Integer, ForeignKey

from core.models.associations import UserPersonAssociation, PersonDealAssociation, PersonPortfolioAssociation

if TYPE_CHECKING:
    from core.models.rows.deal import DealRowOrm
    from core.models.rows.person import PersonRowOrm
    from core.models.rows.property import PropertyRowOrm
    from core.models.entities.user import UserOrm


class PersonOrm(SQLModel, table=True):
    __tablename__ = "persons"
    id: Optional[int] = Field(default=None, sa_column=Column(Integer, ForeignKey("people.id", ondelete="CASCADE"), primary_key=True))

    first_name: str = Field(max_length=255, nullable=False, index=True)
    middle_name: Optional[str] = Field(default=None, max_length=255)
    last_name: str = Field(max_length=255, nullable=False, index=True)  

    notes: Optional[str] = None
    language: str = Field(default="english", max_length=255)
    # source: Optional[str] = Field(default=None, max_length=255)
    # viewed_properties: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    # signature: Optional[bytes] = Field(default=None)

    users: List["UserOrm"] = Relationship(back_populates="people", link_model=UserPersonAssociation)
    deals: List["DealRowOrm"] = Relationship(link_model=PersonDealAssociation)

    residence_id: Optional[int] = Field(default=None, sa_column=Column(Integer, ForeignKey("properties.id")))
    residence: Optional["PropertyRowOrm"] = Relationship(sa_relationship_kwargs={
        "primaryjoin": "PersonDetailsOrm.residence_id == PropertyOrm.id",
        "uselist": False
    })
    portfolio: List["PropertyRowOrm"] = Relationship(link_model=PersonPortfolioAssociation)
