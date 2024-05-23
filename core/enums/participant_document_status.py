from enum import Enum

class ParticipantDocumentStatus(Enum):
    PENDING = 'pending'
    SUBMITTED = 'submitted'
    APPROVED = 'approved'
    REJECTED = 'rejected'
