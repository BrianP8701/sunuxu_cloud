from enum import Enum


class MessageSourceType(Enum):
    dev = "dev"
    changelog = "changelog"
    team = "team"
    person = "person"
    system = "system"
    copilot = "copilot"
    action = "action"
