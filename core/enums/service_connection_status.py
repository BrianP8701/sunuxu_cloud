from enum import Enum

class ServiceConnectionStatus(str, Enum):
    connected = "connected"
    disconnected = "disconnected"
    pending = "pending"
    failed = "failed"
    not_connected = "not_connected"
