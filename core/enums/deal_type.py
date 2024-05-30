from enum import Enum


class DealType(Enum):
    BUY = "buy"
    SELL = "sell"
    DUAL = "dual"
    RENT = "rent"
    RENT_OUT = "rent_out"
    DUAL_RENT = "dual_rent"
    LEASE = "lease"
    LEASE_OUT = "lease_out"
    DUAL_LEASE = "dual_lease"
    CUSTOM = "custom"
    UNKNOWN = "unknown"
