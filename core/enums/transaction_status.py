from enum import Enum


class DealStatus(Enum):
    PENDING = "pending"
    CLOSED = "closed"
    EXPIRED = "expired"
    WITHDRAWN = "withdrawn"
    OFF_MARKET = "off_market"
    CUSTOM = "custom"
    UNKNOWN = "unknown"
    
