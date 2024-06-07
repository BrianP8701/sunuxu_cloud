from enum import Enum


class ParticipantDocumentStatus(Enum):
    pending = "pending"
    submitted = "submitted"
    approved = "approved"
    rejected = "rejected"
