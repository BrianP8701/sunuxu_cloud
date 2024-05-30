from enum import Enum


class DealStatus(Enum):
    PENDING = "pending"
    CLOSED = "closed"
    EXPIRED = "expired"
    WITHDRAWN = "withdrawn"
    UNKNOWN = "unknown"
