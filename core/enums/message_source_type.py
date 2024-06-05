from enum import Enum


class MessageSourceType(Enum):
    DEV = "dev"
    CHANGELOG = "changelog"
    TEAM = "team"
    PERSON = "person"
    SYSTEM = "system"
    COPILOT = "copilot"
    ACTION = "action"
