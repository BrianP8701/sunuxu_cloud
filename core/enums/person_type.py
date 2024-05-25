from enum import Enum


class PersonType(Enum):
    LEAD = "lead"
    COLD_LEAD = "cold_lead"
    PROSPECT = "prospect"
    CLIENT = "client"
    PAST_CLIENT = "past_client"
    AGENT = "agent"
    BROKER = "broker"
    ATTORNEY = "attorney"
    LENDER = "lender"
    CONTRACTOR = "contractor"
    INSPECTOR = "inspector"
    APPRAISER = "appraiser"
    TITLE_OFFICER = "title_officer"
    CUSTOM = "custom"
    UNKNOWN = "unknown"
