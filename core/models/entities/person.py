from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Column, ForeignKey, Integer
from sqlmodel import Field, Relationship, SQLModel

from core.models.associations import (DealParticipantAssociation,
                                      PropertyOwnerAssociation,
                                      UserPersonAssociation)

if TYPE_CHECKING:
    from core.models.entities.deal import DealModel
    from core.models.entities.property import PropertyModel
    from core.models.entities.user import UserModel
    from core.models.rows.person import PersonRowModel


class PersonModel(SQLModel, table=True):
    __tablename__ = "people"
    id: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, ForeignKey("people.id"), primary_key=True),
    )

    first_name: str = Field(max_length=255, nullable=False, index=True)
    middle_name: Optional[str] = Field(default=None, max_length=255)
    last_name: str = Field(max_length=255, nullable=False, index=True)

    notes: Optional[str] = None
    language: str = Field(default="english", max_length=255)

    # All the deals associated with the person
    deals: List["DealModel"] = Relationship(
        back_populates="people",
        link_model=DealParticipantAssociation,
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

    # The property where the person lives. A person can only have one residence.
    residence_id: Optional[int] = Field(
        default=None, sa_column=Column(Integer, ForeignKey("properties.id"))
    )
    residence: Optional["PropertyModel"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "PersonOrm.residence_id == PropertyOrm.id",
            "uselist": False,
        }
    )

    # All the properties this person owns (portfolio)
    portfolio: List["PropertyModel"] = Relationship(
        link_model=PropertyOwnerAssociation,
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

    users: List["UserModel"] = Relationship(
        back_populates="people",
        link_model=UserPersonAssociation,
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    row: "PersonRowModel" = Relationship(
        sa_relationship_kwargs={"uselist": False, "cascade": "all, delete-orphan"}
    )
