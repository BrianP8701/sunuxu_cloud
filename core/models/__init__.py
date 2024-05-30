from .user import UserOrm
from .user_details import UserDetailsOrm
from .person_details import PersonDetailsOrm
from .person import PersonOrm
from .property_details import PropertyDetailsOrm
from .property import PropertyOrm
from .deal_details import DealDetailsOrm
from .deal import DealOrm
from .participant_details import ParticipantDetailsOrm
from .participant import ParticipantOrm
from .team import TeamOrm
from .deal_document import DealDocumentOrm
from .document_template import DocumentTemplateOrm
from .file import FileOrm
from .message import MessageOrm

class Models:
    UserOrm = UserOrm
    UserDetailsOrm = UserDetailsOrm
    PersonDetailsOrm = PersonDetailsOrm
    PersonOrm = PersonOrm
    PropertyDetailsOrm = PropertyDetailsOrm
    PropertyOrm = PropertyOrm
    DealDetailsOrm = DealDetailsOrm
    DealOrm = DealOrm
    ParticipantDetailsOrm = ParticipantDetailsOrm
    ParticipantOrm = ParticipantOrm
    TeamOrm = TeamOrm
    DealDocumentOrm = DealDocumentOrm
    DocumentTemplateOrm = DocumentTemplateOrm
    FileOrm = FileOrm
    MessageOrm = MessageOrm