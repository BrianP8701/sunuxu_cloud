from .associations import (DealParticipantAssociation,
                           DocumentPersonAssociation,
                           PropertyOccupantAssociation,
                           PropertyOwnerAssociation, UserDealAssociation,
                           UserPersonAssociation, UserPropertyAssociation,
                           UserTeamAssociation)
from .deal_document import DealDocumentModel
from .document_template import DocumentTemplateModel
from .entities.deal import DealModel
from .entities.person import PersonModel
from .entities.property import PropertyModel
from .entities.team import TeamModel
from .entities.user import UserModel
from .message import MessageModel
from .rows.deal import DealRowModel
from .rows.person import PersonRowModel
from .rows.property import PropertyRowModel
from .rows.team import TeamRowModel
from .rows.user import UserRowModel


class Models:
    UserOrm = UserModel
    UserRowOrm = UserRowModel
    TeamOrm = TeamModel
    PersonOrm = PersonModel
    PersonRowOrm = PersonRowModel
    PropertyOrm = PropertyModel
    PropertyRowOrm = PropertyRowModel
    DealOrm = DealModel
    DealRowOrm = DealRowModel
    TeamRowOrm = TeamRowModel
    DealDocumentOrm = DealDocumentModel
    DocumentTemplateOrm = DocumentTemplateModel
    MessageOrm = MessageModel
    UserPersonAssociation = UserPersonAssociation
    UserPropertyAssociation = UserPropertyAssociation
    UserDealAssociation = UserDealAssociation
    UserTeamAssociation = UserTeamAssociation
    DocumentPersonAssociation = DocumentPersonAssociation
    PropertyOccupantAssociation = PropertyOccupantAssociation
    PropertyOwnerAssociation = PropertyOwnerAssociation
