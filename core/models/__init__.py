from .associations import (
    UserPersonAssociation,
    UserPropertyAssociation,
    UserDealAssociation,
    UserTeamAssociation,
    DocumentPersonAssociation,
    PropertyOccupantAssociation,
    PropertyOwnerAssociation,
    PersonPortfolioAssociation,
    DealDetailsPersonAssociation
)
from .entities.user import UserOrm
from .entities.team import TeamOrm
from .entities.person import PersonOrm
from .rows.person import PersonRowOrm
from .entities.property import PropertyOrm
from .rows.property import PropertyRowOrm
from .entities.deal import DealOrm
from .rows.deal import DealRowOrm
from .rows.team import TeamRowOrm
from .deal_document import DealDocumentOrm
from .document_template import DocumentTemplateOrm
from .message import MessageOrm
from .rows.user import UserRowOrm


class Models:
    UserOrm = UserRowOrm
    TeamDetailsOrm = TeamOrm
    UserDetailsOrm = UserOrm
    PersonDetailsOrm = PersonOrm
    PersonOrm = PersonRowOrm
    PropertyDetailsOrm = PropertyOrm
    PropertyOrm = PropertyRowOrm
    DealDetailsOrm = DealOrm
    DealOrm = DealRowOrm
    TeamOrm = TeamRowOrm
    DealDocumentOrm = DealDocumentOrm
    DocumentTemplateOrm = DocumentTemplateOrm
    MessageOrm = MessageOrm
    UserPersonAssociation = UserPersonAssociation
    UserPropertyAssociation = UserPropertyAssociation
    UserDealAssociation = UserDealAssociation
    UserTeamAssociation = UserTeamAssociation
    DocumentPersonAssociation = DocumentPersonAssociation
    PropertyOccupantAssociation = PropertyOccupantAssociation
    PropertyOwnerAssociation = PropertyOwnerAssociation
    PersonPortfolioAssociation = PersonPortfolioAssociation
    DealDetailsPersonAssociation = DealDetailsPersonAssociation

