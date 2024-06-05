from enum import Enum


class MessageType(Enum):
    EMAIL = "email"
    SMS = "sms"
    DEV = "dev"
    CALL = "call"
