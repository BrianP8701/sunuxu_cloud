from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Column, Enum as SqlEnum, Integer, ForeignKey
from sqlmodel import Field, Relationship, SQLModel

from core.enums.deal_platform import DealPlatform
from core.models.associations import (DealParticipantAssociation,
                                      UserDealAssociation)

if TYPE_CHECKING:
    from core.models.deal_document import DealDocumentModel
    from core.models.entities.person import PersonModel
    from core.models.entities.property import PropertyModel
    from core.models.entities.user import UserModel
    from core.models.rows.deal import DealRowModel


class DealModel(SQLModel, table=True):
    __tablename__ = "deals"
    id: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, ForeignKey("deal_rows.id"), primary_key=True)
    )

    transaction_platform: Optional[DealPlatform] = Field(
        sa_column=SqlEnum(DealPlatform), default=None
    )
    notes: Optional[str] = None

    # Each deal is associated with one property. A property may have many deals. (Many to one)
    property_id: Optional[int] = Field(default=None, foreign_key="properties.id")
    property: Optional["PropertyModel"] = Relationship(
        back_populates="deals",
        sa_relationship_kwargs={
            "foreign_keys": "DealModel.property_id",
            "uselist": False,
            "cascade": "all",
        },
    )

    # All the participants of the deal. Many to many.
    participants: List["PersonModel"] = Relationship(
        back_populates="deals",
        link_model=DealParticipantAssociation,
        sa_relationship_kwargs={"cascade": "all"},
    )

    # Documents associated with the deal.
    documents: List["DealDocumentModel"] = Relationship(
        back_populates="deal",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

    users: List["UserModel"] = Relationship(
        back_populates="deals",
        link_model=UserDealAssociation,
        sa_relationship_kwargs={"uselist": False, "cascade": "all"},
    )
    row: "DealRowModel" = Relationship(
        sa_relationship_kwargs={
            "uselist": False,
            "single_parent": True,
            "cascade": "all, delete-orphan",
            "back_populates": None
        }
    )
