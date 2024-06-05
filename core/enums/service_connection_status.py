from enum import Enum


class ServiceConnectionStatus(str, Enum):
    CONNECTED = "connected"
    PENDING = "pending"
    FAILED = "failed"
    NOT_CONNECTED = "not_connected"
