from enum import Enum


class DealStatus(Enum):
    pending = "pending"
    closed = "closed"
    expired = "expired"
    withdrawn = "withdrawn"
    unknown = "unknown"
