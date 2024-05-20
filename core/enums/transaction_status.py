from enum import Enum


class TransactionStatus(Enum):
    PENDING = "pending"
    CLOSED = "closed"
    EXPIRED = "expired"
    WITHDRAWN = "withdrawn"
    OFF_MARKET = "off_market"
    OTHER = "other"
