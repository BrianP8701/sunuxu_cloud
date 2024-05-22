from enum import Enum


class DealType(Enum):
    BUY = "buy"
    SELL = "sell"
    DUAL = "dual"
    RENT = "rent"
    RENT_OUT = "rent_out"
    LEASE = "lease"
    LEASE_OUT = "lease_out"
    CUSTOM = "custom"
    UNKNOWN = "unknown"
