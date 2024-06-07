from enum import Enum


class MessageType(Enum):
    email = "email"
    sms = "sms"
    dev = "dev"
    call = "call"
