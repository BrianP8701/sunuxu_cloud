from enum import Enum


class DealDocumentStatus(str, Enum):
    required = "required"
    if_applicable = "if_applicable"
    in_review = "in_review"
    approved = "approved"
    rejected = "rejected"
