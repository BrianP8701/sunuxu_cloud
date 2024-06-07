from enum import Enum


class DealType(Enum):
    buy = "buy"
    sell = "sell"
    dual = "dual"
    rent = "rent"
    rent_out = "rent_out"
    dual_rent = "dual_rent"
    lease = "lease"
    lease_out = "lease_out"
    dual_lease = "dual_lease"
    custom = "custom"
    unknown = "unknown"
