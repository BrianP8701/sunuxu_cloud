from enum import Enum


class TransactionType(Enum):
    BUY = "buy"
    SELL = "sell"
    DUAL = "dual"
    RENT = "rent"
    RENT_OUT = "rent_out"
    LEASE = "lease"
    LEASE_OUT = "lease_out"
    CUSTOM = "custom"
    UNKNOWN = "unknown"
