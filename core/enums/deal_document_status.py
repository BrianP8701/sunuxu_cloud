from enum import Enum

class DealDocumentStatus(str, Enum):
    REQUIRED = "required"
    IF_APPLICABLE = "if_applicable"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"
